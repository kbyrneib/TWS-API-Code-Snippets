from ibapi.client import *
from ibapi.wrapper import *
import time

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
        # Build Contracts
        parent_contract = Contract()
        parent_contract.conId = 29831612 # DPZ (Domino's Pizza)
        parent_contract.exchange = "SMART"

        hedge_child_contract = Contract()
        hedge_child_contract.conId = 273538 # PZZA (Papa John's)
        hedge_child_contract.exchange = "SMART"
        
        # Order Type: Pair Trade
        # Explanation: The attached Pair Trade can be used to hedge one contract against another, generally in the same industry. Offset a price discrepancy between the two contracts with a ratio.
        # General Link: https://www.interactivebrokers.com/en/trading/ordertypes.php?m=pairTradeModal
        # API Link: https://www.interactivebrokers.com/campus/ibkr-api-page/order-types/#hedging
        # Building the Order with required attributes

        # The parent order
        parent = Order()
        parent.orderId = self.nextId()
        parent.action = "BUY"  # Specifies whether the order is to buy or sell (e.g., 'BUY', 'SELL')
        parent.orderType = "MKT"  # Type of order such as Market, Limit, Stop, etc.
        parent.totalQuantity = 1  # Total number of units (shares, contracts) to be bought or sold
        parent.transmit = False  # If false, the order is created but not transmitted to market

        # Hedged child order
        hedge_child = Order()
        hedge_child.orderId = parent.orderId + 1 
        hedge_child.parentId = parent.orderId  # ID of the parent order for bracket, trailing stop, or other attached orders
        hedge_child.action = "SELL"  # Specifies whether the order is to buy or sell (e.g., 'BUY', 'SELL')
        hedge_child.orderType = "MKT"  # Type of order such as Market, Limit, Stop, etc.
        hedge_child.totalQuantity = 0  # Total number of units (shares, contracts) to be bought or sold
        hedge_child.hedgeType = "P"  # Type of hedge for the order (delta, beta, FX, or pair)
        hedge_child.hedgeParam = "5"  # Parameter for the hedge order (e.g., beta value or hedge ratio)
        hedge_child.transmit = True  # If false, the order is created but not transmitted to market
        
        self.placeOrder(parent.orderId, parent_contract, parent)
        time.sleep(.2) # Error "10006: Missing parent order" may be triggered if dont include small delay
        self.placeOrder(hedge_child.orderId, hedge_child_contract, hedge_child)

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