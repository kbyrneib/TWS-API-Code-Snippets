from ibapi.client import *
from ibapi.wrapper import *
import datetime

class TestApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, wrapper=self)

    def nextValidId(self, orderId):
        print(f"Next valid order ID is {orderId}")
        self.orderId = orderId
        self.start()

    def nextId(self):
        self.orderId += 1
        return self.orderId

    def start(self):
        # Making the historical request
        contract = Contract()
        contract.symbol = "TSLA"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        self.reqHistoricalData(self.nextId(), contract, "", "1 D", "1 day", "TRADES", 1, 1, False, [])

    def historicalData(self, reqId, bar):
        print(reqId, bar)

    def historicalDataEnd(self, reqId, start, end):
        print(reqId, "All historical data returned from", start, "to", end)

    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        print(errorCode, errorString)

# Required args for connectivity
host = "localhost"
port = 7497
clientId = 0

# Creating, connecting and running app
app = TestApp()
app.connect(host, port, clientId)
app.run()