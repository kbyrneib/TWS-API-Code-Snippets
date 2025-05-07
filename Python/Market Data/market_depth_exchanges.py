from ibapi.client import *
from ibapi.wrapper import *

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
        # Requesting a list of exchanges that offer deep book data
        self.reqMktDepthExchanges()

    def mktDepthExchanges(self, depthMktDataDescriptions):
        for desc in depthMktDataDescriptions:
            print(desc)

        # Building contract
        contract = Contract()
        contract.conId = 265598
        contract.exchange = "IEX"

        # Making request for market depth
        self.reqMktDepth(self.nextId(), contract, 5, True, [])

    def updateMktDepth(self, reqId, position, operation, side, price, size):
        print(reqId, position, operation, side, price, size)

    def updateMktDepthL2(self, reqId, position, marketMaker, operation, side, price, size, isSmartDepth):
        print(reqId, position, marketMaker, operation, side, price, size, isSmartDepth)

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