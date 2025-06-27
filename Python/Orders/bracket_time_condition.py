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
        parent.action = "BUY" # Identifies the side
        parent.orderType = "LMT" # The order type 
        parent.totalQuantity = 1 # The number of positions being bought/sold (Qty in TWS GUI)
        parent.lmtPrice = 198.41 # The limit price that you will accept (or better)
        parent.transmit = False # Specifies whether the order will be transmitted by TWS

        # Adding the Time Condition to the parent order of the bracket
        parent.conditions = [timeCondition] # Adding the time condition to the parent order
        parent.conditionsCancelOrder = True # The bracket will cancel if the time condition is met

        # The take profit order
        take_profit = Order()
        take_profit.orderId = parent.orderId + 1
        take_profit.parentId = parent.orderId # ID of parent order
        take_profit.action = "SELL" # Identifies the side
        take_profit.orderType = "LMT" # The order type 
        take_profit.totalQuantity = 1 # The number of positions being bought/sold (Qty in TWS GUI)
        take_profit.lmtPrice = parent.lmtPrice + 0.5 # The limit price that you will accept (or better)
        take_profit.transmit = False # Specifies whether the order will be transmitted by TWS
        
        # The stop loss order
        stop_loss = Order()
        stop_loss.orderId = parent.orderId + 2
        stop_loss.parentId = parent.orderId # ID of parent order
        stop_loss.action = "SELL" # Identifies the side
        stop_loss.orderType = "STP" # The order type
        stop_loss.totalQuantity = 1 # The number of positions being bought/sold (Qty in TWS GUI)
        stop_loss.auxPrice = parent.lmtPrice - 0.5 # The stop price - if attained/penetrated, a market order is submitted
        stop_loss.transmit = True # Specifies whether the order will be transmitted by TWS

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