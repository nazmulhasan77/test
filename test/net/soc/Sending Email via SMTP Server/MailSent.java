import java.io.*;
import java.net.InetAddress;
import java.time.LocalDateTime;
import java.util.Base64;

import javax.net.ssl.*;


class MailSent {

  private static DataOutputStream dos;
  public static BufferedReader br;

  public static void main(String argv[]) throws Exception {
    String user = "s2111176131@ru.ac.bd";  
    String pass = "sxbh egyq ospn mati"; 
    
    String username =new String(Base64.getEncoder().encode(user.getBytes()));
    String password = new String(Base64.getEncoder().encode(pass.getBytes()));
    SSLSocket s = (SSLSocket) SSLSocketFactory.getDefault().createSocket("smtp.gmail.com", 465);
    dos = new DataOutputStream(s.getOutputStream());
    br = new BufferedReader(new InputStreamReader(s.getInputStream()));

    //String ipAddress = InetAddress.getLocalHost().getHostAddress();
    String timeNow = LocalDateTime.now().toString();
    InetAddress ip = InetAddress.getLocalHost();
    String ipAddress = ip.getHostAddress();

    send("EHLO smtp.gmail.com\r\n");
              for(int i=0 ; i<9 ;i++){
                System.out.println("SERVER: "+ br.readLine());
                }

    
    send("AUTH LOGIN\r\n");
              System.out.println("SERVER: "+ br.readLine());


    send(username + "\r\n");
              System.out.println("SERVER: "+ br.readLine());



    send(password + "\r\n");
              System.out.println("SERVER: "+ br.readLine());


    send("MAIL FROM:<s2111176131@ru.ac.bd>\r\n");//change
              System.out.println("SERVER: "+ br.readLine());


    send("RCPT TO:<nazmul7762@gmail.com>\r\n");//change
              System.out.println("SERVER: "+ br.readLine());



    send("DATA\r\n");
            System.out.println("SERVER: "+ br.readLine());


    send("FROM: 2111176131@ru.ac.bd\r\n");//change
    send("TO: nazmul7762@gmail.com\r\n");//change
    send("Subject: Email test" + LocalDateTime.now() + "\r\n");
    send("Hello Nazmul.What's up? \r\n");
    send("Your machine's IP address: " + ipAddress + "\r\n");
    send("Your system time: " + timeNow + "\r\n");
    send(".\r\n");
          System.out.println("SERVER: "+ br.readLine());


          
    send("QUIT\r\n");
    System.out.println("SERVER: "+ br.readLine());
  }


  private static void send(String s) throws Exception {
    dos.writeBytes(s);
    Thread.sleep(1000);
    System.out.println("CLIENT: " + s);
     }
}


