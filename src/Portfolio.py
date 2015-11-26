__author__ = 'zmiller'

from src.DB import Connection

class Portfolio:

    def __init__(self, aAlgoConf, aDataDims):
        """
        Construct
        :return: None
        """

        #instantiate class variables
        self.fPortfolioValue = 0.0
        self.fCashValue = 0.0
        self.fTradeComission= 0.0
        self.oOpenPositions = {}

        self.oDB = Connection.getDB()
        self.oAlgoConf = aAlgoConf
        self.aDataDims = aDataDims
        self.aTradeLog = []

    def buy(self):
        return

    def sell(self):
        return

    def udatePositions(self, oNewVals):
        """
        Updates a portfolio's position
        :param oNewVals: an object of new real time values
        :return:
        """

    def insertData(self):
        """
        inserts portfolio performance values
        :return:
        """

    def feedData(self):
        """
        Method informs the algorithm new data has been received. This method executes the algorithm's run method.
        :retur
        """
        print "Feeding Data!"