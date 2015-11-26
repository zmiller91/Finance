__author__ = 'zmiller'

#Yahoo params
YAHOO_BASE_URL = 'http://finance.yahoo.com/d/quotes.csv'
YAHOO_TICKERS = 's'
YAHOO_TICKER_SEPARATOR = '+'
YAHOO_PARAMS = 'f'
YAHOO_PARAM_SEPARATOR = ''

#Quandl params
QUANDL_BASE_URL = "https://s3.amazonaws.com/static.quandl.com/tickers/"
QUANDL_SP500 = QUANDL_BASE_URL + "SP500.csv"
QUANDL_DJIA = QUANDL_BASE_URL + "dowjonesA.csv"
QUANDL_NASDAQ = QUANDL_BASE_URL + "NASDAQComposite.csv"
QUANDL_NASDAQ100 = QUANDL_BASE_URL + "nasdaq100.csv"
QUANDL_NYSE = QUANDL_BASE_URL + "NYSEComposite.csv"
QUANDL_FTSE100 = QUANDL_BASE_URL + "FTSE100.csv"