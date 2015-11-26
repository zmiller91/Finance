__author__ = 'zmiller'

import datetime

from Dimensions import Company, RealTime
from Dimensions import Stock
from Common import Logger
import Connection

TABLE_WILDCARD = ':x:'
S_DAILY_DATA = 's_' + TABLE_WILDCARD + '_daily_data'
S_RT_DATA = 's_' + TABLE_WILDCARD + '_rt_data'
A_DAILY_DATA = 's_' + TABLE_WILDCARD + '_daily_data'
A_RT_DATA = 'a_' + TABLE_WILDCARD + '_rt_data'
A_DAILY_DATA = 'a_' + TABLE_WILDCARD + '_daily_data'
P_RT_DATA = 'p_' + TABLE_WILDCARD + '_rt_data'
P_DAILY_DATA = 'p_' + TABLE_WILDCARD + '_daily_data'

def createTable(oDB, strTable):
    """
    Creates a table if it doesn't exist

    :param oDB: a MySQLdb object
    :param strTable: The table to be created
    :return: boolean indicating the CREATE TABLE
    """

    return Connection.execute(oDB,
        """
        CREATE TABLE IF NOT EXISTS {0}(
            date date not null,
            dim_name varchar(256) not null,
            value varchar(256) not null,
            primary key (dim_name, date),
            key (date)
        );
        """.format(strTable)
    ) != False


def insert(oDB, strTableTemplate, aRows):
    """
    Inserts data into the tables of type strTableTemplate. Will create tables if needed. Each row must contain a
    Stock.DATE and Company.SYMBOL key. Each row represents a unique
        INSERT IGNORE INTO strTableTemplate
        (date, dim_name, value)
        VALUES (aRows[Stock.DATE], aRows[Dimension], aRows[DimensionValue])


    :param oDB: MySQLdb object
    :param strTableTemplate: Type of table that will recieve inserts
    :param aRows: An array of objects where the object keys are Dimensions
    :return: boolean indicating the success of the inserts
    """

    bSuccess = True
    strColumns = '(' + ",".join(['date', 'dim_name', 'value']) + ')'
    while aRows:
        oRow = aRows.pop()
        strDateDim = ''
        strDateDimVal = ''

        if Stock.DATE in oRow and oRow[Stock.DATE] != 'N/A':
            strDateDim = Stock.DATE
            strDateDimVal = oRow[Stock.DATE]

        elif RealTime.RT_LAST_TRADE in oRow and oRow[RealTime.RT_LAST_TRADE] != 'N/A':
            strDateDim = RealTime.RT_LAST_TRADE
            strDateDimVal = oRow[RealTime.RT_LAST_TRADE]

        else:
            continue

        if not Company.SYMBOL in oRow and oRow[Company.SYMBOL] != 'N/A':
            continue

        strDate = datetime.datetime.strptime(strDateDimVal.replace('"', ''), '%m/%d/%Y').strftime('%Y-%m-%d')
        strSymbol = oRow[Company.SYMBOL]
        strTable = strTableTemplate.replace(TABLE_WILDCARD, strSymbol).replace('"', '')

        #create a table for this stock if it doesnt exist. Skip insert if there's a MySQL error
        if not createTable(oDB, strTable):
            bSuccess = False
            continue

        #insert
        for oDim, mVal in oRow.iteritems():

            #never insert the date dimension or any dimension with a 'N/A' value
            if oDim == strDateDim or mVal == 'N/A':
                continue

            #construct and execute INSERT statement
            strRow = '(' + ",".join([quoteString(strDate), quoteString(oDim), quoteString(mVal)]) + ')'
            strInsert = """
                INSERT IGNORE INTO {0}
                {1}
                VALUES
                {2};
                """.format(strTable, strColumns, strRow)


            if not Connection.insert(oDB, strInsert):
                Logger.logError("Failed to execute: " + strInsert)
                bSuccess = False

    return bSuccess

def get(oDB, strTableTemplate, aTickers, strDate):

    aRetval = {}
    for strTicker in aTickers:

        #dont do the same work twice
        if strTicker in aRetval:
            continue

        strTable = strTableTemplate.replace(TABLE_WILDCARD, strTicker)
        strQuery = """
            SELECT *
            FROM {0}
            WHERE date >= {1}
            ORDER BY date DESC;
        """.format(strTable, quoteString(strDate))

        #go to next ticker if error selecting data
        aData = Connection.execute(oDB, strQuery)
        if not aData:
            Logger.logError("Error trying to select data")
            continue

        #add data to retval
        aRetval[strTicker] = mapSelect(aData)

    return aRetval

def mapSelect(aData):
    """
    Takes the result set of a SELECT and maps it to be an array of objects where the keys are dimensions

    :param aData: the result set of a SELECT
    :return: an array of objects
    """
    aRetVal = []
    oCurRow = {}
    strCurDate = ""

    #perform the map
    for aRow in aData:

        if not strCurDate:
            strCurDate = aRow['date']

        if aRow['date'] != strCurDate:
            aRetVal.append(oCurRow)
            oCurRow = {}
            strCurDate = aRow['date']

        oCurRow[Stock.DATE] = strCurDate
        oCurRow[aRow['dim_name']] = aRow['value']

    #clean up stragglers
    if len(oCurRow) > 0:
        aRetVal.append(oCurRow)

    return aRetVal

def quoteString(string):
    """
    Takes a string and encapsulates it in double quotes.  Will trim leading and trailing double quotes and escape any
    interior double quotes.

    :param string: the string to quote
    :return: the encapsulated in double quotes
    """

    if(string):
        if(len(string) > 1):

            #trim leading double quotes
            if string[0] == '"':
                string = string[1:len(string)]

            #trim trailing double quotes
            if string[len(string) - 1] == '"':
                string = string[0:len(string) - 1]

        #escape all inner quotes
        string.replace('"', '\"')
        string = '"' + string + '"'
    return string