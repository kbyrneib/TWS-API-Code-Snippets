from ibapi.client import *
from ibapi.wrapper import *

class TestApp(EClient, EWrapper):
    def __init__(self, account):
        self.account = account
        EClient.__init__(self, wrapper=self)

    def nextValidId(self, orderId):
        print(f"Next valid order ID is {orderId}")
        self.orderId = orderId
        self.start()

    def nextId(self):
        self.orderId += 1
        return self.orderId

    def start(self):
        # Request Account Updates - Set to False to cancel updates
        self.reqAccountUpdates(True, self.account)

    def updateAccountValue(self, key, val, currency, accountName):
        print(key, val, currency, accountName)

    def updatePortfolio(self, contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName):
        print(contract, position, marketPrice, marketValue, averageCost, unrealizedPNL, realizedPNL, accountName)

    def updateAccountTime(self, timeStamp):
        print(timeStamp)

    def accountDownloadEnd(self, accountName):
        print(f"Account download for {accountName} has finished.")
        print("Will update again either when change in position or every 3 minutes.")

    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        print(errorCode, errorString)

# Required args for connectivity
host = "localhost"
port = 7497
clientId = 0

# Creating, connecting and running app
app = TestApp(account="{your account ID here}")
app.connect(host, port, clientId)
app.run()