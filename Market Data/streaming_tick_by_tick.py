from ibapi.client import *
from ibapi.wrapper import *
from ibapi.ticktype import TickTypeEnum

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
        # Build a contract
        contract = Contract()
        contract.conId = 8314
        contract.exchange = "SMART"

        # Requesting tick by tick data
        # First requesting historical tick data via numberOfTicks = 10
        # Then, requeting the streaming tick tick data
        self.reqTickByTickData(self.nextId(), contract, "Last", 10, True)

    def tickByTickAllLast(self, reqId, tickType, time, price, size, tickAttribLast, exchange, specialConditions):
        print(reqId, tickType, time, price, size, tickAttribLast, exchange, specialConditions)

    def historicalTicksLast(self, reqId, ticks, done):
        for tick in ticks:
            print(reqId, tick)

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