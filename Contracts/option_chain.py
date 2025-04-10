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
        # Request security definition option parameters for viewing a contract's option chain
        self.reqSecDefOptParams(self.nextId(), "MSFT", "", "STK", 272093)

    def securityDefinitionOptionParameter(self, reqId, exchange, underlyingConId, tradingClass, multiplier, expirations, strikes):
        # Printing received option chain nicely so it is clear
        print(f"Exchange:\n{exchange}")
        print(f"Multiplier:\n{multiplier}")
        print("Expirations:")
        for i, exp in enumerate(expirations, 1):
            if i % 10 != 0:
                print(exp, end=", ")
            else:
                print(exp)

        print("\nStrikes:")
        for i, strike in enumerate(strikes, 1):
            if i % 10 != 0:
                print(strike, end=", ")
            else:
                print(strike)

        print("\n")

    def securityDefinitionOptionParameterEnd(self, reqId):
        print(f"{reqId} : Finished returning option chain.")

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