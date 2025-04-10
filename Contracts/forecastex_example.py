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
        # Defining contract
        fex_contract = Contract()
        fex_contract.symbol = "USCE"
        fex_contract.secType = "OPT" # All ForecastEx contracts use the OPT security type
        fex_contract.exchange = "FORECASTX" # Will always be the same for ForecastEx contracts
        fex_contract.currency = "USD" # All currently offered Event Contracts are hosted in USA so always USD
        fex_contract.right = "C" # Call (C) = Yes, Put (P) = No
        fex_contract.strike = 4650

        # Code written on 10th April 2025, so Day 100 of year
        # Market closes in 265 days
        # 100 + 265 = Day 365 of the year i.e. 31st December 2025 or 20251231
        fex_contract.lastTradeDateOrContractMonth = "20251231"

        # Creating Order object
        fex_order = Order()
        fex_order.action = "BUY"
        fex_order.orderType = "LMT"
        fex_order.totalQuantity = 1000
        fex_order.lmtPrice = 0.50

        # Placing order
        self.placeOrder(self.nextId(), fex_contract, fex_order)

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