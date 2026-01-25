import java.net.*;
import java.io.*;

public class HttpServer {
    public static void main(String[] args) throws Exception {
        int port = 4000;
        ServerSocket server = new ServerSocket(port);
        System.out.println("Server listening on port " + port);
        while (true) {
            Socket socket = server.accept();
            System.out.println("Client connected: " + socket.getRemoteSocketAddress());
            new Thread(new Handler(socket)).start();
        }
    }

    static class Handler implements Runnable {
        private Socket socket;

        Handler(Socket s) { this.socket = s; }

        public void run() {
            try (Socket s = socket;
                 DataInputStream dis = new DataInputStream(s.getInputStream());
                 DataOutputStream dos = new DataOutputStream(s.getOutputStream())) {

                String urlStr = dis.readUTF();
                System.out.println("Requested URL: " + urlStr);

                URL url = new URL(urlStr);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(10000);
                conn.setReadTimeout(10000);

                int status = conn.getResponseCode();
                InputStream in = (status >= 400) ? conn.getErrorStream() : conn.getInputStream();
                if (in == null) {
                    in = new ByteArrayInputStream(("No content, status: " + status).getBytes("UTF-8"));
                }

                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                byte[] buf = new byte[8192];
                int r;
                while ((r = in.read(buf)) != -1) baos.write(buf, 0, r);
                byte[] data = baos.toByteArray();

                dos.writeInt(status);
                dos.writeInt(data.length);
                dos.write(data);
                dos.flush();

                System.out.println("Sent " + data.length + " bytes (status " + status + ") to client.");

            } catch (Exception e) {
                System.err.println("Handler error: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }
}
