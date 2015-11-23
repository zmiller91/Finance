__author__ = 'zmiller'

from Dimensions import Company, Stock, IncomeStatement, BalanceSheet
from Api import Api, ApiParameters
from Common import Error, Logger
from DB import TradingData, Connection
import time

class Runable:
    def __init__(self):
        #dimensions to retrieve
        self.aParams = [Stock.DATE,
                   Company.SYMBOL,
                   Company.STOCK_EXCHANGE,
                   Stock.PRICE,
                   Stock.OPEN,
                   Stock.CLOSE,
                   Stock.VOLUME,
                   Stock.EPS,
                   Stock.HIGH_52WK,
                   Stock.LOW_52WK,
                   Stock.MA_200_DAY,
                   Stock.MA_50_DAY,
                   Stock.RATIO_SHORT,
                   Stock.HIGH,
                   Stock.LOW,
                   IncomeStatement.EBITDA,
                   IncomeStatement.PE_RATIO,
                   IncomeStatement.PRICE_TO_BOOK,
                   IncomeStatement.PRICE_TO_SALES]
        self.oDB = Connection.getDB()

    def insertDailyData(self):
        aQuandlTickers = [ApiParameters.QUANDL_DJIA, ApiParameters.QUANDL_FTSE100, ApiParameters.QUANDL_NASDAQ,
                          ApiParameters.QUANDL_NASDAQ100, ApiParameters.QUANDL_NYSE, ApiParameters.QUANDL_SP500]

        for strQuandl in aQuandlTickers:

            Logger.logError("STARTED DATA RETREVIAL" )
            aTickers = Api.getQuandlTickers(strQuandl)
            print aTickers
            oData = Api.getData(aTickers, self.aParams)
            print oData
            if not oData:
                Logger.logError('There was an error retrieving data.')
            else:
                TradingData.insert(self.oDB, TradingData.S_DAILY_DATA, oData)
                self.oDB.commit()
            Logger.logError("Finished DATA RETREVIAL")

    def getRTData(self):
        # retrieve daily data for all our tickers
        TradingData.get(self.oDB, TradingData.S_DAILY_DATA, Api.getQuandlTickers(ApiParameters.QUANDL_SP500), '2015-11-20')

    def test(self):
        bHaveDaily = False
        while True:
            if not bHaveDaily:
                self.insertDailyData()
                bHaveDaily = True