__author__ = 'zmiller'

from DB import Connection
from Dimensions import RealTime
from datetime import datetime

class Portfolio:

    def __init__(self, aAlgoConf, aDataDims):
        """
        Construct
        :return: None
        """

        #instantiate class variables

        self.oDB = Connection.getDB()
        self.oAlgoConf = aAlgoConf
        self.aDataDims = aDataDims

        self.fLiveValue = 0
        self.fCashValue = self.oAlgoConf["start_bal"]
        self.fTradeComission= self.oAlgoConf["comission"]

        self.oOpenPositions = {}
        self.aTradeLog = []
        self.oNewValues = {}

    def log(self, strTicker, strType, iShares, fTradeValue, fTradeCost):
        """
        Insert an entry into the trade log
        :param strTicker: stock's ticker
        :param strType: trade type, BUY or SELL
        :param iShares: number of shares
        :param fTradeValue: value of shares
        :param fTradeCost: cost of trade
        :return: None
        """
        self.aTradeLog.append({
            "trade_date": str(datetime.now()) ,
            "trade_type": strType,
            "ticker": strTicker,
            "shares": iShares,
            "value": fTradeValue,
            "cost": fTradeCost
        })

    def buy(self, strTicker, iShares):
        """
        Buy a stock.  If your trade costs more than your cash value then your trade will be adjusted to purchase
        as many shares as possible.
        :param strTicker: stock to buy
        :param iShares: number of shares to buy
        :return: boolean indicating success or failure
        """

        # shares must be an int, long, or float
        if not isinstance(iShares, (int, long, float)) or iShares < 0:
            return False

        iShares = int(iShares)

        # ticker must be in new data object and it must have a RT_ASK value
        if not strTicker in self.oNewValues or not RealTime.RT_ASK in self.oNewValues[strTicker]:
            return False

        # get trade details, adjust assumptions if we do not have enough cash
        fCurAsk = self.oNewValues[strTicker][RealTime.RT_ASK]
        fTradeValue = fCurAsk * iShares
        fTradeCost = fTradeValue + self.fTradeComission
        if  fTradeCost > self.fCashValue:
            fTradePower = self.fCashValue - self.fTradeComission
            iShares = int(fTradePower / fCurAsk)
            fTradeValue = fCurAsk * iShares
            fTradeCost = fTradeValue + self.fTradeComission
            del fTradePower

        if iShares > 0:

            # create an open position if it doesn't already exist
            if strTicker not in self.oOpenPositions:
                self.oOpenPositions[strTicker] = {
                    "quantity": 0,
                    "market_value": 0.0,
                    "cost_basis": 0.0,
                    "last_modified": str(datetime.now())
                }

            # spend down cash
            self.fCashValue -= fTradeCost
            self.fLiveValue += fTradeValue

            # update open position
            self.oOpenPositions[strTicker]["quantity"] += iShares
            self.oOpenPositions[strTicker]["market_value"] += fTradeValue
            self.oOpenPositions[strTicker]["cost_basis"] += fTradeValue

            # update trade log
            self.log(strTicker, "BUY", iShares, fTradeValue, fTradeCost)

        del fCurAsk, iShares, fTradeValue, fTradeCost
        return True

    def sell(self, strTicker, iShares):
        """
        Sell a stock. If you're trying to sell more shares than are currently open, then we will wil sell all open
        positions.  If your trade results in a quantity of 0 stocks held then we will close the position.
        :param strTicker: stock to sell
        :param iShares: number of shares to sell
        :return: boolean indicating success or failure
        """

        # shares must be an int, long, or float
        if not isinstance(iShares, (int, long, float)) or iShares < 0:
            return False

        # ticker must be in new data object and it must have a RT_ASK value
        if strTicker not in self.oNewValues or RealTime.RT_ASK not in self.oNewValues[strTicker]:
            return False

        # position must be open
        if not strTicker in self.oOpenPositions:
            return False

        if iShares > 0:

            # get trade details
            fCurAsk = self.oNewValues[strTicker][RealTime.RT_ASK]
            iShares = min(int(iShares), self.oOpenPositions[strTicker]["quantity"])
            fTradeValue = iShares * fCurAsk
            fPctSellOff = (float(iShares) / float(self.oOpenPositions[strTicker]["quantity"]))
            fCostBasisReduction =  self.oOpenPositions[strTicker]["cost_basis"] * fPctSellOff

            # add to cash
            self.fCashValue += fTradeValue - self.fTradeComission

            # use RT_BID because update() uses RT_BID and we essentially want to negate
            # the effect of the update on these shares
            self.fLiveValue -= iShares * self.oNewValues[strTicker][RealTime.RT_BID]

            # update open positions
            self.oOpenPositions[strTicker]["quantity"] -= iShares
            self.oOpenPositions[strTicker]["market_value"] -= fTradeValue
            self.oOpenPositions[strTicker]["cost_basis"] -= fCostBasisReduction
            self.oOpenPositions[strTicker]["last_modified"] = str(datetime.now())

            # close trade if needed
            if self.oOpenPositions[strTicker]["quantity"] == 0:
                del self.oOpenPositions[strTicker]

            # update trade log
            self.log(strTicker, "SELL", iShares, fTradeValue, self.fTradeComission)
            del fCurAsk, iShares, fTradeValue, fPctSellOff, fCostBasisReduction

        return True

    def update(self, oNewVals):
        """
        Updates a portfolio's position and sets new realtime values used for buying and selling
        :param oNewVals: an object of new real time values
        :return: None
        """

        # validate data coming in. i hate to do it in this method, since it gets run for every algorithm
        # right before every trade, but...this data can be manipulated by the user, so we should probably
        # validate it
        for strTicker, oData in oNewVals.iteritems():
            if RealTime.RT_BID not in oData:
                continue
            self.oNewValues[strTicker] = oData

        self.fLiveValue = 0
        for strTicker, oPosition in self.oOpenPositions.iteritems():

            # ticker must be in new data object and it must have a RT_ASK value
            if not strTicker in self.oNewValues:
                continue

            oPosition["market_value"] = oPosition["quantity"] * self.oNewValues[strTicker][RealTime.RT_BID]
            oPosition["last_modified"] = str(datetime.now())

            self.fLiveValue += oPosition["market_value"]


    def insert(self):
        """
        Insert portfolio information into the DB.
        :return:
        """