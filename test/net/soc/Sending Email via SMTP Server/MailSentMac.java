import java.io.*;
import java.time.LocalDateTime;
import javax.net.ssl.*;
import java.util.*;
import java.net.*;

class MailSentMac {

  private static DataOutputStream dos;
  public static BufferedReader br;

  public static void main(String argv[]) throws Exception {
    String user = "s2111176131@ru.ac.bd"; 
    String pass = "sxbh egyq ospn mati";   

    String username = Base64.getEncoder().encodeToString(user.getBytes());
    String password = Base64.getEncoder().encodeToString(pass.getBytes());
    
    SSLSocket s = (SSLSocket) SSLSocketFactory.getDefault().createSocket("smtp.gmail.com", 465);
    dos = new DataOutputStream(s.getOutputStream());
    br = new BufferedReader(new InputStreamReader(s.getInputStream()));

    send("EHLO smtp.gmail.com\r\n");
    for (int i = 0; i < 9; i++) {
      System.out.println("SERVER: " + br.readLine());
    }

    send("AUTH LOGIN\r\n");
    System.out.println("SERVER: " + br.readLine());

    send(username + "\r\n");
    System.out.println("SERVER: " + br.readLine());

    send(password + "\r\n");
    System.out.println("SERVER: " + br.readLine());

    send("MAIL FROM:<s2111176131@ru.ac.bd>\r\n");
    System.out.println("SERVER: " + br.readLine());

    send("RCPT TO:<nazmul7762@gmail.com>\r\n");
    System.out.println("SERVER: " + br.readLine());

    send("DATA\r\n");
    System.out.println("SERVER: " + br.readLine());

    // Get system info
    InetAddress ip = InetAddress.getLocalHost();
    String ipAddress = ip.getHostAddress();
    String timeNow = LocalDateTime.now().toString();
    String macAddress = getMacAddress(ip);

    // Send email
    send("FROM: s2111176131@ru.ac.bd\r\n");
    send("TO: nazmul7762@gmail.com\r\n");
    send("Subject: Email test " + timeNow + "\r\n");
    send("\r\n");
    send("Hello Nazmul. What's up?\r\n");
    send("Your machine's IP address: " + ipAddress + "\r\n");
    send("Your MAC address: " + macAddress + "\r\n");
    send("Your system time: " + timeNow + "\r\n");
    send(".\r\n");
    System.out.println("SERVER: " + br.readLine());

    send("QUIT\r\n");
    System.out.println("SERVER: " + br.readLine());
  }

  private static void send(String s) throws Exception {
    dos.writeBytes(s);
    Thread.sleep(1000);
    System.out.println("CLIENT: " + s);
  }

  private static String getMacAddress(InetAddress ip) throws Exception {
    NetworkInterface network = NetworkInterface.getByInetAddress(ip);
    byte[] mac = network.getHardwareAddress();

    if (mac == null) return "MAC not found";

    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < mac.length; i++) {
      sb.append(String.format("%02X%s", mac[i], (i < mac.length - 1) ? "-" : ""));
    }
    return sb.toString();
  }
}
