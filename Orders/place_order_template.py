from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import TagValue

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
        # Fill in details of contract
        
        # Build order type here
        order = Order()
        # Fill in details of order
        
        # Place Order
        self.placeOrder(self.nextId(), contract, order)
        
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        print("OrderStatus:", orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)

    def openOrder(self, orderId, contract, order, orderState):
        print("OpenOrders:", orderId, contract, order, orderState)

    def execDetails(self, reqId, contract, execution):
        print("ExecDetails:", reqId, contract, execution)

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