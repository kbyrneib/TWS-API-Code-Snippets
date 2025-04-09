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
        # Subscribes to position updates for all accessible accounts. 
        # All positions sent initially, and then only updates as positions change.
        self.reqPositionsMulti(self.nextId(), "", "")

    def positionMulti(self, reqId, account, modelCode, contract, pos, avgCost):
        print(reqId, account, modelCode, contract, pos, avgCost)

    def positionMultiEnd(self, reqId):
        print("All positions have been transmitted.")

        # Cancel previous position subscription request made with EClient.reqPositions
        self.cancelPositionsMulti(reqId)

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