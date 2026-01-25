import java.net.*;
import java.io.*;

public class HttpClient {
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Usage: java HttpClient <url> [output-file]");
            return;
        }
        String url = args[0];
        String outFile = args.length >= 2 ? args[1] : "output.html";

        try (Socket socket = new Socket("localhost", 4000);
             DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
             DataInputStream dis = new DataInputStream(socket.getInputStream())) {

            dos.writeUTF(url);
            dos.flush();

            int status = dis.readInt();
            int len = dis.readInt();
            System.out.println("Received status: " + status + ", length: " + len);

            byte[] data = new byte[len];
            dis.readFully(data);

            try (FileOutputStream fos = new FileOutputStream(outFile)) {
                fos.write(data);
            }

            System.out.println("Saved to " + outFile);

        } catch (Exception e) {
            System.err.println("Client error: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
