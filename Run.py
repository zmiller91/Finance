__author__ = 'zmiller'

from Parameters import Company, Stock, IncomeStatement, BalanceSheet
from Api import Api, ApiParameters
from Common import Error, Logger
from DB import TradingData, Connection

def getData(aTickers, aParams):
    Logger.log("STARTED DATA RETREVIAL" )
    oData = Api.getData(aTickers, aParams)
    if not oData:
        Logger.log('There was an error retrieving data.')
    else:
        oDB = Connection.getDB()
        TradingData.insert(oDB, TradingData.S_DAILY_DATA, oData)
        oDB.commit()
    Logger.log("Finished DATA RETREVIAL")

#dimensions to retrieve
aParams = [Stock.DATE,
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

#retrieve daily data for all our tickers
Logger.log('QUANDL_DJIA:');
getData(Api.getQuandlTickers(ApiParameters.QUANDL_DJIA), aParams)
Logger.log('QUANDL_FTSE100:');
getData(Api.getQuandlTickers(ApiParameters.QUANDL_FTSE100), aParams)
Logger.log('QUANDL_NASDAQ:');
getData(Api.getQuandlTickers(ApiParameters.QUANDL_NASDAQ), aParams)
Logger.log('QUANDL_NASDAQ100:');
getData(Api.getQuandlTickers(ApiParameters.QUANDL_NASDAQ100), aParams)
Logger.log('QUANDL_NYSE:');
getData(Api.getQuandlTickers(ApiParameters.QUANDL_NYSE), aParams)
Logger.log('QUANDL_SP500:');
getData(Api.getQuandlTickers(ApiParameters.QUANDL_SP500), aParams)
