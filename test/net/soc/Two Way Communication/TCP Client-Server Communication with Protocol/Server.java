import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.time.LocalDate;
import java.time.LocalTime;

public class Server {
    public static void main(String[] args) throws Exception {
        ServerSocket ss = new ServerSocket(7777);
        System.out.println("Server is waiting ... ");
        Socket s1 = ss.accept();
        System.out.println("Client connected successfully. ");
        DataInputStream dsIn = new DataInputStream(s1.getInputStream());
        DataOutputStream dsOut = new DataOutputStream(s1.getOutputStream());

        while (true) {
            String msg = dsIn.readUTF();

            System.out.println("Client: " +msg);

            if(msg.equalsIgnoreCase("quit")) {
                dsOut.writeUTF("Connection terminated successfully.");
                break;
            }
            else if(msg.equalsIgnoreCase("Hi")) {
                dsOut.writeUTF("Hello");
            }
            else if (msg.equalsIgnoreCase("ok")) {
                int i = 0;
                while (i < 9) {
                    dsOut.writeUTF("Ok");
                    i++;
                }
            }        
            else if(msg.equalsIgnoreCase("time")) {
                dsOut.writeUTF("Time is " + LocalTime.now());
            }
            else if(msg.equalsIgnoreCase("date")) {
                dsOut.writeUTF("Date is " + LocalDate.now());
            }
            else {
                dsOut.writeUTF("Unknown Command");
            }
        }
        ss.close();
    }
}
