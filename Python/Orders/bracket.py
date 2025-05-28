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
        mycontract = Contract()
        mycontract.conId = 265598
        mycontract.exchange = "SMART"

        parent = Order()
        parent.orderId = self.nextId()
        parent.action = "BUY"
        parent.orderType = "MKT"
        parent.totalQuantity = 1
        parent.transmit = False

        profit_taker = Order()
        profit_taker.orderId = parent.orderId + 1
        profit_taker.parentId = parent.orderId
        profit_taker.action = "SELL"
        profit_taker.orderType = "LMT"
        profit_taker.totalQuantity = 1
        profit_taker.lmtPrice = 202.0
        profit_taker.transmit = False

        stop_loss = Order()
        stop_loss.orderId = parent.orderId + 2
        stop_loss.parentId = parent.orderId
        stop_loss.action = "SELL"
        stop_loss.orderType = "STP"
        stop_loss.totalQuantity = 1
        stop_loss.auxPrice = 198.0
        stop_loss.transmit = True

        self.placeOrder(parent.orderId, mycontract, parent)
        self.placeOrder(profit_taker.orderId, mycontract, profit_taker)
        self.placeOrder(stop_loss.orderId, mycontract, stop_loss)
        
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