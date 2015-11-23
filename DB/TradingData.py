__author__ = 'zmiller'

from Parameters import Company, Stock
from Common import Logger
import Connection
import datetime

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


def insert(oDB, strTableType, aRows):
    """
    Inserts data into the tables of type strTableType. Will create tables if needed. Each row must contain a
    Stock.DATE and Company.SYMBOL key.

    :param oDB: MySQLdb object
    :param strTableType: Type of table that will recieve inserts
    :param aRows: An array of objects where the object keys are Parameters
    :return: boolean indicating the success of the inserts
    """

    bSuccess = True
    strColumns = '(' + ",".join(['date', 'dim_name', 'value']) + ')'
    while aRows:
        oRow = aRows.pop()

        #each row must have a date and a ticker symbol
        if not oRow[Stock.DATE] or oRow[Stock.DATE] == 'N/A' or not oRow[Company.SYMBOL] or oRow[Company.SYMBOL] == 'N/A':
            Logger.log('Each row provided to insertData must have a Stock.DATE and Stock.SYMBOL value. ')
            return False

        date = oRow[Stock.DATE].replace('"', '');
        strDate = "'" + datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d') + "'"
        strSymbol = oRow[Company.SYMBOL]
        strTable = strTableType.replace(TABLE_WILDCARD, strSymbol).replace('"', '')

        #create a table for this stock if it doesnt exist. Return false if there's a MySQL error
        if not createTable(oDB, strTable):
            return False

        #create an insert statement for eah row and add it to aInsertStatements
        for oDim, mVal in oRow.iteritems():

            #never insert the stocks date since its a column
            if oDim == Stock.DATE:
                continue

            #if the value cannot be parsed as an int, then quote it
            try:
                float(mVal)
            except ValueError:
                mVal = "'" + mVal + "'"

            #construct and execute INSERT statement
            oDim = '"' + oDim + '"'
            strRow = '(' + ",".join([strDate, oDim, mVal]) + ')'
            strInsert = """
                INSERT IGNORE INTO {0}
                {1}
                VALUES
                {2};
                """.format(strTable, strColumns, strRow)


            if not Connection.insert(oDB, strInsert):
                Logger.log("Failed to execute: " + strInsert)
                bSuccess = False

    return bSuccess
