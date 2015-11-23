__author__ = 'zmiller'

from Conf import Conf
from Common import Logger
import MySQLdb
from warnings import filterwarnings

filterwarnings('ignore', category = MySQLdb.Warning)

"""
Returns a database object

Returns:
MySQLdb object
"""
def getDB():
    """
    Returns a database object

    :return: MySQLdb object
    """

    oDB = MySQLdb.connect(
        host = Conf.DB_HOST,
        user = Conf.DB_USER,
        passwd = Conf.DB_PASS,
        db = Conf.DB)
    return oDB

def execute(oDB, strQuery):
    """
    Executes a MySQL statement

    :param oDB: MySQLdb object
    :param strQuery: The statement to execute
    :return: the resultset on success and False on failure
    """

    try:
        oDB.cursor().execute(strQuery)
        oDB.cursor().close()
    except MySQLdb.Error, e:
        oDB.rollback()
        if e.message:
            Logger.log(e.message)
        if len(e.args) > 1:
            Logger.log(e.args[1])
        Logger.log(strQuery)
        return False

def insert(oDB, strQuery):
    """
    Performs an INSERT

    :param oDB: MySQLdb object
    :param strQuery: The insert statement to execute
    :return: boolean indicating success or failure
    """
    return execute(oDB, strQuery) != False