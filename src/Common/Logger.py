__author__ = 'zmiller'

import time

from Conf import Conf


def log(strFile, strMessage, bPrint):
    strDate = time.strftime("%x")
    strTime = time.strftime("%X")
    strMessage = strDate + " " + strTime + "\t" + strMessage + "\n"
    with open(strFile, "a+") as myfile:
        myfile.write(strMessage)
        myfile.close()

    if(bPrint):
        print strMessage


def logError(strMessage):
    log(Conf.LOG_ERROR, strMessage, Conf.LOG_ERR_PRINT)

def logApp(strMessage):
    log(Conf.LOG_APP, strMessage, Conf.LOG_APP_PRINT)