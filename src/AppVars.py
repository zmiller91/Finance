__author__ = 'zmiller'
"""

This is the where application defined variables are.  These are not located in Conf because this is not configuration.
This file has the ability to use the entire application to create custom application variables.  They can be used in
any part of the application and exist as a central repository that's easy to view and update.

"""
from Dimensions import Company, IncomeStatement, RealTime
from Dimensions import Stock
from Api import ApiParameters

"""
This variable defines the dimensions to use when making a GET request to the YahooApi for daily data.
"""
DATA_DAILY_DIMENSIONS = [
    Stock.DATE,
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
    IncomeStatement.PRICE_TO_SALES
]

"""
This variable defines the dimensions to use when making a GET request to the YahooApi for real time data.
"""
DATA_RT_DIMENSIONS = [
    RealTime.RT_ASK,
    RealTime.RT_BID,
    RealTime.RT_LAST_TRADE,
    Company.SYMBOL
]

"""
This variable defines the Quandl GET requests, used to return a set of tickers for daily data
"""
DATA_DAILY_TICKERS = [
    ApiParameters.QUANDL_DJIA,
    ApiParameters.QUANDL_FTSE100,
    ApiParameters.QUANDL_NASDAQ,
    ApiParameters.QUANDL_NASDAQ100,
    ApiParameters.QUANDL_NYSE,
    ApiParameters.QUANDL_SP500
]


"""
This variable defines the Quandl GET requests, used to return a set of tickers for real time data
"""
DATA_RT_TICKERS = [
    ApiParameters.QUANDL_SP500
]

"""
This variable defines the max number of entries each ticker chunk contains. It's used to limit the length of URIs when
we make a GET request to the YahooApi for stock data.
"""
CHUNK_TICKERS = 100