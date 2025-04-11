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
        # Building a contract
        contract = Contract()
        contract.symbol = "IBM"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        # Request historical ticks
        self.reqHistoricalTicks(self.nextId(), contract, "", "20250410 21:30:00", 10, "TRADES", 1, True, [])

    # Change function to historicalTicks for whatToShow = MIDPOINT
    # Change function to historicalTicksBidAsk for whatToShow = BID_ASK
    def historicalTicksLast(self, reqId, ticks, done):
        print(reqId, ticks, done)

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