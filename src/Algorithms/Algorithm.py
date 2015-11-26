__author__ = 'zmiller'

# These imports are essential for accessing critical components of this application
from src.Portfolio import Portfolio
from src.Dimensions import RealTime, Company

class Algorithm(Portfolio):

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
        # any of these fields.  Adding fields will do nothing.
        oAlgorithmConf = {
            "name": "Algorithm Name",
            "start_bal": 0.0,
            "add_balance": 0.0,
            "max_positions": 0.0,
            "comission": 0.0
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