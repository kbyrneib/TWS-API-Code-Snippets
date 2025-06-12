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
        # Build Contract
        contract = Contract()
        contract.conId = 265598 # AAPL
        contract.exchange = "SMART"
        
        # Order Type: Trailing Stop Limit Order
        # Explanation: A trailing stop but with an added limit price, calculated based on an offset from the trailing stop
        # General Link: 
        # API Link: 
        # Building the Order with required attributes
        order = Order()
        order.action = "BUY" # Identifies the side, BUY in this case
        order.orderType = "TRAIL LIMIT" # The order type (obviously)
        order.totalQuantity = 1 # The number of positions being bought/sold (Qty in TWS GUI)
        order.trailStopPrice = 200.5 # Required - Trigger price beyond which trailing behavior will begin.

        # Specify one of:
        order.trailingPercent = 1.0 # Specifies the trailing amount as a percentage of the market price e.g. 0.50 = 0.50%
        # order.auxPrice = 1.0 # Specifies the trailing amount as an absolute value in units of the instruments currency e.g. 1.0 USD
        
        # Specify one of:
        order.lmtPriceOffset = 0.1 # Set by default in the TWS/IBG settings. This setting either needs to be changed in the Order Presets, the default value accepted, or the limit price offset sent from the API as in the example below.
        # order.lmtPrice = 201.0

        # Place Order
        self.placeOrder(self.nextId(), contract, order)

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print(f"OrderStatus:, orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}\n")

    def openOrder(self, orderId, contract, order, orderState):
        print(f"OpenOrder, orderId: {orderId}, contract: {contract}, order: {order}, orderState: {orderState}")

    def execDetails(self, reqId, contract, execution):
        print(f"ExecDetails:, reqId: {reqId}, contract: {contract}, execution: {execution}\n")

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