__author__ = 'zmiller'

# These imports are essential for accessing critical components of this application
from Portfolio import Portfolio
from Dimensions import RealTime, Company
from datetime import datetime

class TestAlgo(Portfolio):

    def __init__(self):
        """
        All the fields in the constructor are required.  They are inputs into our real time trading environment.
        :return:
        """

        # This information is required and defines the data dimensions you will receive our real time
        # data provider. An example is provided, feel free to add or remove dimensions.  You can find more
        # dimensions in the RealTime and Company modules
        aDataDimensions = [
            Company.SYMBOL,
            RealTime.RT_LAST_TRADE,
            RealTime.RT_ASK,
            RealTime.RT_BID
        ]

        # This information is required. It defines how we configure a trading environment.  Please do not remove
        # any of these fields.  Adding fields will be accessible through self.oAlgoConf.
        oAlgorithmConf = {
            "name": "Test Algorithm",
            "start_bal": 10000.0,
            "add_balance": 0.0,
            "comission": 2.50
        }

        # Construct the parent
        Portfolio.__init__(self, oAlgorithmConf, aDataDimensions)
        del aDataDimensions, oAlgorithmConf

    def run(self, oNewData):
        """
        Our trading environment will call this method when new data arrives. There's some setup we need to do
        before you start trading
        :param oNewData: objects where keys are tickers and values are market data
        :return:
        """

        Portfolio.update(self, oNewData)
        self.trade(oNewData)

    def trade(self, oNewData):
        """
        This is the main method of your algorithm.  When we receive new data from the trading environment
        we will call this function with the new data.  All trade logic should be defined in this method.
        :return: None
        """

        # buy signal for AAPL
        if 'AAPL' not in self.oOpenPositions and oNewData['AAPL'][RealTime.RT_ASK] >= 101:
            iShares = int ((self.fCashValue * 0.5) / 101)
            Portfolio.buy(self, 'AAPL', iShares)

        # sell signal for AAPL
        if 'AAPL' in self.oOpenPositions and oNewData['AAPL'][RealTime.RT_ASK] >= 103:
            iShares = self.oOpenPositions['AAPL']['quantity']
            Portfolio.sell(self, 'AAPL', iShares)

        # buy signal for GE
        if 'GE' not in self.oOpenPositions and oNewData['GE'][RealTime.RT_ASK] >= 23:
            iShares = int ((self.fCashValue * 0.5) / 23)
            Portfolio.buy(self, 'GE', iShares)

        # sell signal for GE
        if 'GE' in self.oOpenPositions and oNewData['GE'][RealTime.RT_ASK] > 23.49:
            iShares = self.oOpenPositions['GE']['quantity']
            Portfolio.sell(self, 'GE', iShares)


# represents new data
oNewDataArray = [
    {"GE": {Company.SYMBOL: "GE", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 22.50, RealTime.RT_BID: 22.25},
    "AAPL": {Company.SYMBOL: "AAPL", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 101.00, RealTime.RT_BID: 100.25},
    },
    {"GE": {Company.SYMBOL: "GE", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 23.00, RealTime.RT_BID: 22.75},
    "AAPL": {Company.SYMBOL: "AAPL", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 102.00, RealTime.RT_BID: 101.25},
    },
    {"GE": {Company.SYMBOL: "GE", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 23.50, RealTime.RT_BID: 23.25},
    "AAPL": {Company.SYMBOL: "AAPL", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 103.00, RealTime.RT_BID: 102.25},
    }
]

oAlgo = TestAlgo()
for oNewData in oNewDataArray:
    oAlgo.run(oNewData)
    continue