from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue
from ibapi.ticktype import TickTypeEnum

import threading
import time
import datetime

port = 7497

total_cash = 0
positions = {}
symbol_lookup = {}
cutoff = 750000

class ATS(EClient, EWrapper):
    """
    Simple Automated Trading System example
    Based on example from tutorial https://www.interactivebrokers.com/campus/trading-lessons/tws-python-api-concurrency-example/
    """

    def __init__(self):
        EClient.__init__(self, wrapper=self)
        
    def nextValidId(self, orderId):
        self.orderId = orderId

        # Request account updates
        self.reqAccountUpdates(True, "")

        # Request position updates
        self.reqPositions()

        # Build scanner
        sub = ScannerSubscription()
        sub.instrument = "STK"
        sub.locationCode = "STK.US.MAJOR"
        sub.scanCode = "TOP_PERC_GAIN"
        scan_options = []
        filter_options = [
            TagValue("avgVolumeAbove","1000000"),
            TagValue("priceAbove", '50')
        ]

        # Request scanner subscription
        self.reqScannerSubscription(orderId, sub, scan_options, filter_options)

    def nextId(self):
        # NextValidId above provides first next valid identifier, and this function, nextId, locally increments the value for each request
        self.orderId += 1
        return self.orderId
    
    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderReject):
        print(f"reqId: {reqId}, errorCode: {errorCode}, errorString: {errorString}, orderReject: {advancedOrderReject}")

    def updateAccountValue(self, key, val, currency, accountName):
        # Check if current key:val pair is total cash balance in base currency
        if key == "TotalCashBalance" and currency == "BASE":
            # Assign total cash balance in base currency to total_cash
            total_cash = float(val)

            # Disconnect if cash balance drops below cutoff
            if total_cash < cutoff:
                print(f"Total Cash Balance has dropped below cutoff of {cutoff} in base currency!")
                print("Disconnecting...")
                self.disconnect()

    def position(self, account, contract, position, avgCost):
        # If position in a particular stk changes, update value in positions dictionary
        positions[contract.symbol] = {"ReqId": -1, "Contract": contract, "Position": position, "LAST": False}

    def positionEnd(self):
        # Only need to request positions on startup in order to add them to the positions dictionary
        # After this, can just cancel requesting positions as they are now being tracked by positions dictionary
        # If I dont do this, ReqId key reset to -1 for every position each time a trade is made i.e. when all positions are returned again
        self.cancelPositions()

    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        # Filter for top x results from scanner
        if rank < 1:
            # Create unique ID 
            rankId = rank+reqId

            # Create position entry or update ReqId if position already exists
            # This accounts for contracts returned by scanner that I do not have existing positions in
            if contractDetails.contract.symbol not in positions.keys():
                positions[contractDetails.contract.symbol] = {"ReqId": rankId, "Contract": contractDetails.contract, "Position": 0, "LAST": False}
            else:
                positions[contractDetails.contract.symbol]["ReqId"] = rankId

            # Assign rankIds to each symbol in positions to create ability to lookup symbol of contract
            symbol_lookup[rankId] = contractDetails.contract.symbol

            # Print out info on contract
            print(f"Rank {rank} Contract: {contractDetails.contract.symbol} @ {contractDetails.contract.exchange}")

            # Set data type of returned market data to be of type 3, which is live unless user does not have subscription, then would be delayed
            self.reqMarketDataType(3)

            # Begin the request for market data - will be returned by tickPrice callback below
            # Generic tick requested is blank, which will allow access to Last Price, corresponding to tick Id of 4
            self.reqMktData(rankId, contractDetails.contract, "", False, False, [])

    def scannerDataEnd(self, reqId):
        # We have our desired contracts - cancel scanner subscription
        self.cancelScannerSubscription(reqId)

    def tickPrice(self, reqId, tickType, price, attrib):
        # Filter price data for just LAST price
        if TickTypeEnum.toStr(tickType) == "LAST":
            # Grab symbol required based on reqId
            symbol = symbol_lookup[reqId]
            
            # Check if a LAST price has been recorded, will be False if not
            if not positions[symbol]["LAST"]:
                positions[symbol]["LAST"] = price

            # Build out order object to use for trades
            # Will just do a day market order of quantity 5
            order = Order()
            order.tif = "DAY"
            order.totalQuantity = 5
            order.orderType = "MKT"

            # If the new price is more than 5% higher than our previous price point.
            if (positions[symbol]["LAST"] * 1.05) < price:
                order.action = "BUY"
                self.placeOrder(self.nextId(), positions[symbol]["Contract"], order)
            # If the new price is less than 6% of our previous price point
            elif (positions[symbol]["LAST"] * 0.94) > price and positions[symbol]["Position"] >= 5:
                order.action = "SELL"
                self.placeOrder(self.nextId(), positions[symbol]["Contract"], order)

            # Assign new LAST price to contract
            positions[symbol]["LAST"] = price

    def openOrder(self, orderId, contract, order, orderState):
        print(f"{datetime.datetime.now()} {orderState.status}: ID:{orderId} || {order.action} {order.totalQuantity} {contract.symbol}")

    def execDetails(self, reqId, contract, execution):
        print(f"Execution Details: ID:{execution.orderId} || {execution.side} {execution.shares} {contract.symbol} @ {execution.time}")

# Defining host, port and clientId for connection
host = "localhost"
port = 7497
clientId = 0

# Instantiate app
app = ATS()

# Create connection to localhost via port, with client ID of 1001
app.connect(host, port, clientId)

# Call run to begin processing message queue
app.run()