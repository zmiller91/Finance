__author__ = 'zmiller'

from Conf import Conf
import time

def log(strMessage):
    strDate = time.strftime("%x")
    strTime = time.strftime("%X")
    strMessage = strDate + " " + strTime + "\t" + strMessage + "\n"
    with open(Conf.LOG_FILE, "a") as myfile:
        myfile.write(strMessage)
        myfile.close()

    if(Conf.LOG_PRINT):
        print strMessage