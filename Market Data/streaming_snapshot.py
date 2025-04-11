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
        # Build a contract
        contract = Contract()
        contract.conId = 8314
        contract.exchange = "SMART"

        # Requesting streaming snapshot data
        self.reqMktData(self.nextId(), contract, "", False, False, [])

    def tickPrice(self, reqId, tickType, price, attrib):
        # Lets just fiter for LAST price
        if tickType == 4:
            print(reqId, tickType, price, attrib)

    def tickSnapshotEnd(self, reqId):
        print(reqId, "Snapshot has ended")

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