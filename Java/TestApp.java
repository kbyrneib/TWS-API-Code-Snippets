import com.ib.client.*;

public class TestApp extends MyEWrapper {

    public TestApp(int port, int clientId) {
        // Client sends messages
        EClientSocket mClient = this.getClient();

        // A signal/notification is triggered upon messages received from the socket
        EReaderSignal mSignal = this.getSignal();

        // Establish connection
        mClient.eConnect("127.0.0.1", 7497, 0);

        // Reader processes the messages from the socket, and triggers the Wrapper callbacks
        EReader reader = new EReader(mClient, mSignal); 

        // Start reader thread
        reader.start();

        // An additional thread is created in this program design to empty the messaging queue
        new Thread(() -> {
            while (mClient.isConnected()) {
                mSignal.waitForSignal();
                try {
                    reader.processMsgs(); // decode msgs and invoke approporiate functions in MyEWrapper
                } catch (Exception e) {
                    System.out.println("Exception: " + e.getMessage());
                }
            }
        }).start();
    }

    public static void main(String[] args) {
        // Creating new instance of TestApp, specifying port and clientId
        System.out.println("Starting app...");
        TestApp app = new TestApp(7497, 0);
    }
}