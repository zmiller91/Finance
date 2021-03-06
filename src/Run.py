__author__ = 'zmiller'

import datetime
import time

from pytz import timezone

import AppVars
from PortfolioCollection import PortfolioCollection
from Dimensions import Company
from Api import Api, ApiParameters
from Common import Logger, Utils
from Conf import Conf
from DB import TradingData, Connection


class Runable:

    def __init__(self):
        """
        Construct
        :return: None
        """
        self.oDB = Connection.getDB()

    def getQuandlTickers(self, aQuandlUrls):
        """
        get a unique set of tickers by adding everything in "aSet not in aTickers" to aTickers
        link: http://stackoverflow.com/questions/7961363/python-removing-duplicates-in-lists
        :param aQuandlUrls: Quandl URLs
        :return: a list of unique tickers from the provided quandl urls
        """

        aTickers = []
        for strQuandl in aQuandlUrls:
            aSet = Api.getQuandlTickers(strQuandl)
            aTickers += list(set(aSet) - set(aTickers))
            del aSet

        return aTickers

    def insertDailyData(self):
        """
        Routine for collecting and inserting daily data from the YahooApi. All data is for the previously closed
        trading day.
        :return: None
        """

        Logger.logApp("Collecting and inserting daily data...")

        # chunk the tickers into a managable size, retrieve data for each chunk, and then insert each chunk
        # chunking allows us to insert periodicly through the data collection process and ensures our YahooApi request
        # doesnt return a 414 response code (URI too long)
        iCurChunk = 0
        aTickers = self.getQuandlTickers(AppVars.DATA_DAILY_TICKERS)
        aTickerChunks = Utils.chunk(aTickers, AppVars.CHUNK_TICKERS)
        for iCurChunk in range(0, len(aTickerChunks)):
            oData = Api.getData(aTickerChunks[iCurChunk], AppVars.DATA_DAILY_DIMENSIONS)
            if  oData:
                TradingData.insert(self.oDB, TradingData.S_DAILY_DATA, oData)
                self.oDB.commit()
                Logger.logApp("Inserting data for chunk " + str(iCurChunk + 1) + " of " + str(len(aTickerChunks)))
            else:
                Logger.logError('There was an error retrieving data for chunk ' +  str(iCurChunk + 1))
            del oData

    def selectDailyData(self):
        """
        Retrieve daily data for all our tickers
        :return:
        """
        TradingData.get(self.oDB, TradingData.S_DAILY_DATA, Api.getQuandlTickers(ApiParameters.QUANDL_SP500), '2015-11-20')

    def run(self):
        """
        Main daemon process invoked by DataDaemon. This method is a infinite loop that has logic in it's body to
        execute commands at specific times of day.  More specifically, this process is responsible for creating,
        running, and closing each trading day. This process will get killed when the daemon stops.
        :return:
        """

        # service variables
        bTrading = False

        while True:

            # Get the current EST time and date
            oNow = datetime.datetime.now(timezone(Conf.MARKET_TIMEZONE))
            oNowDate = datetime.datetime(oNow.year, oNow.month, oNow.day)

            # Market is only open on week days from 9:30AM EST to 4:00PM EST
            bIsWeekDay = not(oNow.strftime('%A') == 'sunday' or oNow.strftime('%A') == 'saturday')
            bIsMarketHours = datetime.time(Conf.MARKET_OPEN_HOUR, Conf.MARKET_OPEN_MINUTE) <= datetime.time(oNow.hour, oNow.minute) \
                             and datetime.time(oNow.hour, oNow.minute) < datetime.time(Conf.MARKET_CLOSE_HOUR, Conf.MARKET_CLOSE_MINUTE)
            bIsOpen = bIsWeekDay and bIsMarketHours

            # it's after 5:00AM EST on a week day, let's collect the previous days data and get everything set up
            if (bIsWeekDay and not bTrading and oNow.hour >= 5) or Conf.DAEMON_IS_DEBUG:

                # insert daily data from yesterday
                if Conf.DAEMON_INSERT_DAILY:
                    self.insertDailyData()

                # market vars, must be deleted at EOD
                aTickers = self.getQuandlTickers(AppVars.DATA_RT_TICKERS)
                aTickerChunks = Utils.chunk(aTickers, AppVars.CHUNK_TICKERS)
                del aTickers

                oPortfolioCollection = PortfolioCollection()

                # OK to stop trading
                bTrading = True

            # the market is open! start collecting data and trading
            if (bTrading and bIsOpen and aTickerChunks) or Conf.DAEMON_IS_DEBUG:

                Logger.logApp("Starting a trading cycle...")

                # get current pricing data for all tickers and create a data map where keys are tickers and values are
                # the location of the ticker's value in the data list
                aDataList = []
                oDataMap = {}
                for iCurChunk in range(0, len(aTickerChunks)):
                    aChunkData = Api.getData(aTickerChunks[iCurChunk], AppVars.DATA_RT_DIMENSIONS)
                    for iDataIndex in range(len(aDataList), len(aDataList) + len(aChunkData)):
                        oDataMap[aChunkData[iDataIndex - len(aDataList)][Company.SYMBOL]] = iDataIndex
                    aDataList += aChunkData

                    del aChunkData
                    del iCurChunk
                    del iDataIndex

                # broadcast new data to all portfolios
                for oPortfolio in oPortfolioCollection.iteritems():
                    oAlgorithm = oPortfolio['algorithm']
                    oAlgorithm.run(oDataMap)

                # insert new data
                if aDataList:
                    TradingData.insert(self.oDB, TradingData.S_RT_DATA, aDataList)
                    self.oDB.commit()
                else:
                    Logger.logError('There was an error inserting real time data')
                del oDataMap

                Logger.logApp("Finished a trading cycle")

            # it's after 4:30PM EST on a week day let's close the trading day and go to sleep
            if (bIsWeekDay and bTrading and oNow.hour >= 16 and oNow.minute > 30) or Conf.DAEMON_IS_DEBUG:

                # insert portfolio data
                for oPortfolio in oPortfolioCollection.iteritems():
                    oAlgorithm = oPortfolio['algorithm']
                    oAlgorithm.insert()

                # clean up market vars
                del aTickerChunks
                del oPortfolioCollection

                # OK to start trading
                bTrading = False

            time.sleep(Conf.DAEMON_SLEEP)