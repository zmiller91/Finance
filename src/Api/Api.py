__author__ = 'zmiller'

import urllib
import urllib2

import ApiParameters
from src.Common import Logger, Error


def get(strRequest):
    """
    Performs a GET request provided by the given request

    :param strRequest: the URL of the request
    :return: response if OK, False if not
    """
    try:
        return urllib2.urlopen(strRequest);
    except urllib2.HTTPError as e:
        strError = "The server couldn't fulfill the request. Error code: " + str(e.code)
        Logger.logError(strError)
        return None
    except urllib2.URLError as e:
        strError = "We failed to reach the server. Reason: " + e.reason
        Logger.logError(strError)
        return None

def getQuandlTickers(strQuandl):
    """
    Performs a GET on quandl to retrieve a list of tickers

    :param strQuandl: the quandle URL to use -- located in ApiParameters.py
    :return: a list of tickers provided by quandl
    """
    oRetVal = get(strQuandl)
    if not oRetVal:
        return False

    return parseQuandl(oRetVal.read())

def parseQuandl(strResponse):
    """
    Parse a quandl GET request to collect all the tickers returned in the response

    :param strResponse: a response from quandl
    :return: array containing tickers
    """
    aTickers = []
    aRows = strResponse.split('\n')

    #the first row will be a header
    #find the 'ticker' column so we can figure out what column contains the ticker

    i = 0
    iTickerCol = -1
    aHeader = aRows.pop(0).split(',')
    while i < len(aHeader):
        if aHeader[i] == 'ticker':
            iTickerCol = i
            break
        i += 1

    if iTickerCol == -1:
        Logger.logError('There were no tickers returned from quandl')

    #loop through the remaining rows and collect all the tickers
    for strRow in aRows:
        aRow = strRow.split(',')
        aTickers.append(aRow[iTickerCol])

    return aTickers

def getData(aTickers, aParams):
    """
    Performs a GET on yahoo finance to retrieve ticker data.
    :param aTickers: list of tickers to retrieve data
    :param aParams: the columns to be returned
    :return: array of objects where each object represents a row in the CSV
    """

    oQuery = {
        ApiParameters.YAHOO_TICKERS: ApiParameters.YAHOO_TICKER_SEPARATOR.join(aTickers),
        ApiParameters.YAHOO_PARAMS: ApiParameters.YAHOO_PARAM_SEPARATOR.join(aParams)
    }
    strQuery = urllib.urlencode(oQuery)
    strRequest = ApiParameters.YAHOO_BASE_URL + '?' + strQuery
    oResponse = get(strRequest)

    if not oResponse:
        return False

    return parseYahoo(oResponse.read(), aParams)

def parseYahoo(strResponse, aColMap):
    """
    Transforms the response of get() into an
    array of objects where each object represents
    a row in the returned CSV and each key in the
    object represents a column.

    :param strResponse: returned value from get()
    :param aColMap: array of columns that maps the returned value from get()
    :return: Array of objects representing the CSV returned from get()
    """
    aResponse = []
    for aRow in strResponse.split('\n'):
        if not aRow:
            continue

        oCols = {}
        aCols = aRow.split(",")
        iCol = 0

        if len(aCols) != len(aColMap):
            Error.throw("Column map must have the same number " +
                        "of columns as columns in the api response. " +
                        "len(aCols) = " + str(len(aCols)) + " and " +
                        "len(aColMap) = " + str(len(aColMap)))

        while iCol < len(aCols):
            oCols[aColMap[iCol]] = aCols[iCol]
            iCol += 1

        aResponse.append(oCols)

    return aResponse