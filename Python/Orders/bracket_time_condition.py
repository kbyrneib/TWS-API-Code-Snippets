from ibapi.client import *
from ibapi.wrapper import *
from ibapi.order_condition import *

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

        # Build Time Condition
        timeCondition = TimeCondition()
        timeCondition.isMore = True
        timeCondition.time = "20250627 10:30:00 US/Eastern"   
        
        # Order Type: Bracket Order
        # Explanation: Bracket an order with two opposite side orders to prevent losses and lock in gains
        # General Link: https://www.interactivebrokers.co.uk/en/trading/ordertypes.php?m=bracketModal
        # API Link: https://www.interactivebrokers.com/campus/ibkr-api-page/order-types/#bracket-orders
        # Building the Order with required attributes

        # The parent order
        parent = Order()
        parent.orderId = self.nextId()
        parent.action = "BUY"  # Specifies whether the order is to buy or sell (e.g., 'BUY', 'SELL')
        parent.orderType = "LMT"  # Type of order such as Market, Limit, Stop, etc.
        parent.totalQuantity = 1  # Total number of units (shares, contracts) to be bought or sold
        parent.lmtPrice = 198.41  # Limit price for limit orders or stop-limit orders
        parent.transmit = False  # If false, the order is created but not transmitted to market

        # Adding the Time Condition to the parent order of the bracket
        parent.conditions = [timeCondition]  # List of conditions that must be met before the order becomes active
        parent.conditionsCancelOrder = True  # If true, order is canceled when conditions become invalid after being active

        # The take profit order
        take_profit = Order()
        take_profit.orderId = parent.orderId + 1
        take_profit.parentId = parent.orderId  # ID of the parent order for bracket, trailing stop, or other attached orders
        take_profit.action = "SELL"  # Specifies whether the order is to buy or sell (e.g., 'BUY', 'SELL')
        take_profit.orderType = "LMT"  # Type of order such as Market, Limit, Stop, etc.
        take_profit.totalQuantity = 1  # Total number of units (shares, contracts) to be bought or sold
        take_profit.lmtPrice = parent.lmtPrice + 0.5  # Limit price for limit orders or stop-limit orders
        take_profit.transmit = False  # If false, the order is created but not transmitted to market

        # The stop loss order
        stop_loss = Order()
        stop_loss.orderId = parent.orderId + 2
        stop_loss.parentId = parent.orderId  # ID of the parent order for bracket, trailing stop, or other attached orders
        stop_loss.action = "SELL"  # Specifies whether the order is to buy or sell (e.g., 'BUY', 'SELL')
        stop_loss.orderType = "STP"  # Type of order such as Market, Limit, Stop, etc.
        stop_loss.totalQuantity = 1  # Total number of units (shares, contracts) to be bought or sold
        stop_loss.auxPrice = parent.lmtPrice - 0.5  # Auxiliary price for stop orders, trailing stop orders, etc.
        stop_loss.transmit = True  # If false, the order is created but not transmitted to market

        # Bundling the parent, take profit and stop loss orders together
        bracket_order = [parent, take_profit, stop_loss]
        
        # Place Orders
        for order in bracket_order:
            self.placeOrder(order.orderId, contract, order)

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