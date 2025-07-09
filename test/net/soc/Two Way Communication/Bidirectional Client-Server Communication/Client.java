import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {
    public static void main(String[] args) {
        System.out.println("Client started");

        try (Socket socket = new Socket("localhost", 9000);
             BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter output = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader consoleInput = new BufferedReader(new InputStreamReader(System.in))) {

            System.out.println("Connected to server!");

            Thread receiveThread = new Thread(() -> {
                try {
                    String serverMessage;
                    while ((serverMessage = input.readLine()) != null) {
                        System.out.println(serverMessage);
                        if (serverMessage.equalsIgnoreCase("Server: bye")) {
                            System.out.println("Server ended the chat. Closing connection...");
                            break;
                        }
                    }
                } catch (Exception e) {
                    System.err.println("Error receiving message: " + e.getMessage());
                }
            });

            receiveThread.start();

            String clientMessage;
            while (true) {
                System.out.print("Client: ");
                clientMessage = consoleInput.readLine();
                output.println(clientMessage);
                if (clientMessage.equalsIgnoreCase("bye")) {
                    System.out.println("Closing connection...");
                    break;
                }
            }

            receiveThread.join();  // Wait for the receive thread to finish
        } catch (Exception e) {
            System.err.println("Client error: " + e.getMessage());
        }

        System.out.println("Client terminated.");
    }
}
