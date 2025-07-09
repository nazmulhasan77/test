import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
    public static void main(String[] args) {
        System.out.println("Waiting for client connection...");

        try (ServerSocket serverSocket = new ServerSocket(9000);
             Socket socket = serverSocket.accept();
             BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter output = new PrintWriter(socket.getOutputStream(), true);
             BufferedReader consoleInput = new BufferedReader(new InputStreamReader(System.in))) {

            System.out.println("Client connected!");

            Thread receiveThread = new Thread(() -> {
                try {
                    String clientMessage;
                    while ((clientMessage = input.readLine()) != null) {
                        System.out.println("Client: " + clientMessage);
                        if (clientMessage.equalsIgnoreCase("bye")) {
                            System.out.println("Client disconnected. Closing connection...");
                            break;
                        }
                    }
                } catch (Exception e) {
                    System.err.println("Error receiving message: " + e.getMessage());
                }
            });

            receiveThread.start();

            String serverMessage;
            while (true) {
                System.out.print("Server: ");
                serverMessage = consoleInput.readLine();
                output.println(serverMessage);
                if (serverMessage.equalsIgnoreCase("bye")) {
                    System.out.println("Closing connection...");
                    break;
                }
            }

            receiveThread.join();  // Wait for the receive thread to finish
        } catch (Exception e) {
            System.err.println("Server error: " + e.getMessage());
        }

        System.out.println("Server shutting down.");
    }
}
