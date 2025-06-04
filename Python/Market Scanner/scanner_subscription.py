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
        # Building a ScannerSubscription object
        scanner_sub = ScannerSubscription()
        scanner_sub.instrument = "STK"
        scanner_sub.locationCode = "STK.US"
        scanner_sub.scanCode = "MOST_ACTIVE"
        scanner_sub.numberOfRows = 10
        filter_options = [
            # TagValue("priceAbove", "50"),
            # TagValue("marketCapAbove1e6", "1000")
        ]

        # Requesting scanner using ScannerSubscription object
        self.reqScannerSubscription(self.nextId(), scanner_sub, [], filter_options)

    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, projection, legsStr):
        print(rank, contractDetails.contract.symbol)

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