__author__ = 'zmiller'

from Conf import Conf
import time

def log(strFile, strMessage):
    strDate = time.strftime("%x")
    strTime = time.strftime("%X")
    strMessage = strDate + " " + strTime + "\t" + strMessage + "\n"
    with open(strFile, "a+") as myfile:
        myfile.write(strMessage)
        myfile.close()

    if(Conf.LOG_PRINT):
        print strMessage


def logError(strMessage):
    log(Conf.LOG_ERROR, strMessage)

def logApp(strMessage):
    log(Conf.LOG_APP, strMessage)