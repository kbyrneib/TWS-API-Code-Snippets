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
        
        # Order Type: Market If Touched Order
        # Explanation: Buy (sell) an instrument below (above) the market.
        # Held in the system until the trigger price is touched, and is then submitted as a market order. 
        # An MIT order is similar to a stop order, except that an MIT sell order is placed above the current 
        # market price, and a stop sell order is placed below.
        # General Link: https://www.interactivebrokers.com/en/trading/ordertypes.php?m=marketTouchModal
        # API Link: https://www.interactivebrokers.com/campus/ibkr-api-page/order-types/#market-if-touched-order
        # Building the Order with required attributes
        order = Order()
        order.action = "SELL" # Identifies the side
        order.orderType = "MIT" # The order type (obviously)
        order.totalQuantity = 1 # The number of positions being bought/sold (Qty in TWS GUI)
        order.auxPrice = 197.3 # The trigger price - if touched, a market order is submitted
        
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