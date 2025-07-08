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
        
        # Order Type: Stop Limit Order
        # Explanation: Submit a limit order if stop price is attained/penetrated.
        # General Link: https://www.interactivebrokers.co.uk/en/trading/ordertypes.php?m=stopLimitModal
        # API Link: https://www.interactivebrokers.com/campus/ibkr-api-page/order-types/#stop-limit-order
        # Building the Order with required attributes
        order = Order()
        order.action = "BUY"  # Specifies whether the order is to buy or sell (e.g., 'BUY', 'SELL')
        order.orderType = "STP LMT"  # Type of order such as Market, Limit, Stop, etc.
        order.totalQuantity = 1  # Total number of units (shares, contracts) to be bought or sold
        order.auxPrice = 198.0  # Auxiliary price for stop orders, trailing stop orders, etc.
        order.lmtPrice = 197.0  # Limit price for limit orders or stop-limit orders
        
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