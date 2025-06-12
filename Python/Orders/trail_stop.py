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
        
        # Order Type: Trailing Stop Order
        # Explanation: A sell (buy) trailing stop order sets the stop price at a fixed amount below (above) the market price with an attached "trailing" amount.
        # General Link: https://www.interactivebrokers.co.uk/en/trading/ordertypes.php?m=trailingModal
        # API Link: https://www.interactivebrokers.com/campus/ibkr-api-page/order-types/#trailing-stop-order
        # Building the Order with required attributes
        order = Order()
        order.action = "BUY" # Identifies the side, BUY in this case
        order.orderType = "TRAIL" # The order type (obviously)
        order.totalQuantity = 1 # The number of positions being bought/sold (Qty in TWS GUI)
        order.trailingPercent = 1.0 # Specifies the trailing amount as a percentage of the market price e.g. 0.50 = 0.50% OR
        # order.auxPrice = 1.0 # Specifies the trailing amount as an absolute value in units of the instruments currency e.g. 1.0 USD
        # order.trailStopPrice = 201.0 # Not required - Trigger price beyond which trailing behavior will begin. If no stop price value is supplied, this is set to UNSET_DOUBLE

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