import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;
import java.util.Scanner;

public class Client {
    public static void main(String[] args) throws Exception {
        Scanner scanner = new Scanner((System.in));
        String message, receivedMSG;

        Socket s2 = new Socket("localhost", 7777);
        DataInputStream dsIn = new DataInputStream(s2.getInputStream());
        DataOutputStream dsOut = new DataOutputStream(s2.getOutputStream());

        while (true) {
            System.out.print("CLIENT: ");
            message = scanner.nextLine();
            dsOut.writeUTF(message);

            if(message.equalsIgnoreCase("quit")) {
                receivedMSG = dsIn.readUTF();
                System.out.println("SERVER: "+receivedMSG);
                break;
            }

            else if(message.equalsIgnoreCase("ok")) {
                for(int i=0 ; i<9 ;i++){
                receivedMSG = dsIn.readUTF();
                System.out.println("SERVER: "+receivedMSG);
                }
            }
            else{
            receivedMSG = dsIn.readUTF();
            System.out.println("SERVER: "+receivedMSG);
            }
        }

        s2.close();
        scanner.close();
    }
}
