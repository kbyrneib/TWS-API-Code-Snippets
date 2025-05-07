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
        # Creates subscription for real time daily PnL and unrealized PnL updates.
        self.reqPnL(self.nextId(), account, "")

    def pnl(self, reqId, dailyPnL, unrealizedPnL, realizedPnL):
        print(reqId, dailyPnL, unrealizedPnL, realizedPnL)

        # Cancels subscription for real time updated daily PnL
        self.cancelPnL(reqId)

    def error(self, reqId, errorTime, errorCode, errorString, advancedOrderRejectJson=""):
        print(errorCode, errorString)

# Required args for connectivity
host = "localhost"
port = 7497
clientId = 0

with open("nums.txt") as f:
    account = f.read()

# Creating, connecting and running app
app = TestApp(account=account)
app.connect(host, port, clientId)
app.run()