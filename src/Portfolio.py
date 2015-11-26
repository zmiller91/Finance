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
        """
        Buy a stock
        :return:
        """

    def sell(self):
        """
        Sell a stock
        :return:
        """

    def update(self, oNewVals):
        """
        Updates a portfolio's position
        :param oNewVals: an object of new real time values
        :return:
        """

    def insert(self):
        """
        Insert portfolio information into the DB.
        :return:
        """