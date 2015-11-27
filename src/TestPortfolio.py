__author__ = 'zmiller'

from unittest import TestCase
from Portfolio import Portfolio as P
from Dimensions import Company, RealTime
from datetime import datetime

class TestPortfolio(TestCase):


    def test_basic_functionality(self):

        aDataDimensions = [
            Company.SYMBOL,
            RealTime.RT_LAST_TRADE,
            RealTime.RT_ASK,
            RealTime.RT_BID
        ]

        oAlgorithmConf = {
            "name": "Test Algorithm",
            "start_bal": 10000.0,
            "add_balance": 0.0,
            "comission": 2.50
        }

        # construct
        Portfolio = P(oAlgorithmConf, aDataDimensions)
        self.assertEqual(Portfolio.fCashValue, 10000.00)
        self.assertEqual(Portfolio.fLiveValue, 0)
        self.assertEqual(Portfolio.fTradeComission, 2.50)
        self.assertEqual(Portfolio.oAlgoConf, oAlgorithmConf)

        oNewData = {"GE": {Company.SYMBOL: "GE", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 22.50, RealTime.RT_BID: 22.25},
                    "AAPL": {Company.SYMBOL: "AAPL", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 101.00, RealTime.RT_BID: 100.25}}

        # update
        Portfolio.update(oNewData)
        self.assertEqual(Portfolio.oNewValues, oNewData)

        # buy aapl
        iShares = 49
        self.assertTrue(Portfolio.buy('AAPL', iShares))
        self.assertEqual(Portfolio.fLiveValue, 4949.00)
        self.assertEqual(Portfolio.fCashValue, 5048.50)
        self.assertEqual(Portfolio.oOpenPositions['AAPL']["quantity"], 49)
        self.assertEqual(Portfolio.oOpenPositions['AAPL']["market_value"], 4949.00)
        self.assertEqual(Portfolio.oOpenPositions['AAPL']["cost_basis"], 4949.00)

        oNewData = {"GE": {Company.SYMBOL: "GE", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 23.00, RealTime.RT_BID: 22.75},
                    "AAPL": {Company.SYMBOL: "AAPL", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 102.00, RealTime.RT_BID: 101.25}}

        # update
        Portfolio.update(oNewData)
        self.assertEqual(Portfolio.fCashValue, 5048.50)
        self.assertEqual(Portfolio.fLiveValue, 4961.25)
        self.assertEqual(Portfolio.oOpenPositions["AAPL"]["market_value"], 4961.25)
        self.assertEqual(Portfolio.oOpenPositions["AAPL"]["cost_basis"], 4949.00)

        # buy GE
        iShares = 50
        self.assertTrue(Portfolio.buy("GE", iShares))
        self.assertEqual(Portfolio.fCashValue, 3896)
        self.assertEqual(Portfolio.fLiveValue, 6111.25)
        self.assertEqual(Portfolio.oOpenPositions['GE']["quantity"], 50)
        self.assertEqual(Portfolio.oOpenPositions['GE']["market_value"], 1150)
        self.assertEqual(Portfolio.oOpenPositions['GE']["cost_basis"], 1150)

        oNewData = {"GE": {Company.SYMBOL: "GE", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 23.50, RealTime.RT_BID: 23.25},
                    "AAPL": {Company.SYMBOL: "AAPL", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 103.00, RealTime.RT_BID: 102.25}}

        # update
        Portfolio.update(oNewData)
        self.assertEqual(Portfolio.fCashValue, 3896)
        self.assertEqual(Portfolio.fLiveValue, 6172.75)
        self.assertEqual(Portfolio.oOpenPositions["AAPL"]["market_value"], 5010.25)
        self.assertEqual(Portfolio.oOpenPositions["AAPL"]["cost_basis"], 4949.00)
        self.assertEqual(Portfolio.oOpenPositions["GE"]["market_value"], 1162.5)
        self.assertEqual(Portfolio.oOpenPositions["GE"]["cost_basis"], 1150)

        # sell AAPL
        self.assertTrue(Portfolio.sell("AAPL", 49))
        self.assertEqual(Portfolio.fCashValue, 8940.5)
        self.assertEqual(Portfolio.fLiveValue, 1162.5)
        self.assertTrue("AAPL" not in Portfolio.oOpenPositions)

        # sell GE
        self.assertTrue(Portfolio.sell("GE", 50))
        self.assertEqual(Portfolio.fCashValue, 10113)
        self.assertEqual(Portfolio.fLiveValue, 0)
        self.assertTrue("GE" not in Portfolio.oOpenPositions)

    def test_invalid_data(self):

        aDataDimensions = [
            Company.SYMBOL,
            RealTime.RT_LAST_TRADE,
            RealTime.RT_ASK,
            RealTime.RT_BID
        ]

        oAlgorithmConf = {
            "name": "Test Algorithm",
            "start_bal": 10000.0,
            "add_balance": 0.0,
            "comission": 2.50
        }

        # construct
        Portfolio = P(oAlgorithmConf, aDataDimensions)

        oNewData = {"GE": {Company.SYMBOL: "GE", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 22.50},
                    "AAPL": {Company.SYMBOL: "AAPL", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 101.00, RealTime.RT_BID: 100.25}}

        Portfolio.update(oNewData)
        self.assertTrue("GE" not in Portfolio.oNewValues)
        self.assertTrue("AAPL" in Portfolio.oNewValues)

        oNewData = {"GE": {Company.SYMBOL: "GE", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 22.50, RealTime.RT_BID: 22.25},
                    "AAPL": {Company.SYMBOL: "AAPL", RealTime.RT_LAST_TRADE: str(datetime.now()), RealTime.RT_ASK: 101.00, RealTime.RT_BID: 100.25}}

        Portfolio.update(oNewData)
        self.assertTrue("GE" in Portfolio.oNewValues)
        self.assertTrue("AAPL" in Portfolio.oNewValues)

        self.assertFalse(Portfolio.buy("GE", "asdf")) # must be an numeric type
        self.assertFalse(Portfolio.buy("GE", -100)) # must be > 0
        self.assertFalse(Portfolio.buy("ASDF", 100)) # must exist in oNewData
        self.assertTrue(Portfolio.buy("GE", 100)) # all good

        self.assertFalse(Portfolio.sell("GE", "GE")) # must be numeric type
        self.assertFalse(Portfolio.sell("GE", -100)) # cannot be negative
        self.assertFalse(Portfolio.sell("AAPL", 100)) # must be purchased
        self.assertFalse(Portfolio.sell("ASDF", 100)) # must be in oNewData
        self.assertTrue(Portfolio.sell("GE", 100)) # all good
