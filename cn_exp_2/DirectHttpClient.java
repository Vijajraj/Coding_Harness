import javax.net.ssl.SSLSocketFactory;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class DirectHttpClient {
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.out.println("Usage: java DirectHttpClient <url> [output-file]");
            return;
        }
        String urlStr = args[0];
        String outFile = args.length >= 2 ? args[1] : "direct_output.html";

        URL url = new URL(urlStr);
        FetchResult res = fetch(url);
        if (res == null) {
            System.err.println("Fetch failed");
            return;
        }

        System.out.println("Status: " + res.status);
        System.out.println("Content-Type: " + res.headers.getOrDefault("Content-Type", "(unknown)"));

        try (FileOutputStream fos = new FileOutputStream(outFile)) {
            fos.write(res.body);
        }
        System.out.println("Saved body to " + outFile + " (" + res.body.length + " bytes)");
    }

    static class FetchResult {
        int status;
        Map<String,String> headers;
        byte[] body;
    }

    static FetchResult fetch(URL url) {
        String proto = url.getProtocol();
        String host = url.getHost();
        int port = url.getPort() == -1 ? (proto.equalsIgnoreCase("https") ? 443 : 80) : url.getPort();
        String path = url.getFile().isEmpty() ? "/" : url.getFile();

        try (Socket socket = openSocket(proto, host, port)) {
            socket.setSoTimeout(15000);
            OutputStream out = socket.getOutputStream();
            InputStream in = socket.getInputStream();

            String req = "GET " + path + " HTTP/1.1\r\n" +
                    "Host: " + host + "\r\n" +
                    "User-Agent: DirectHttpClient/1.0\r\n" +
                    "Connection: close\r\n" +
                    "\r\n";
            out.write(req.getBytes(StandardCharsets.US_ASCII));
            out.flush();

            BufferedInputStream bis = new BufferedInputStream(in);

            // Read headers (until CRLF CRLF)
            ByteArrayOutputStream headerBuf = new ByteArrayOutputStream();
            int cur;
            int state = 0; // track CRLFCRLF
            while ((cur = bis.read()) != -1) {
                headerBuf.write(cur);
                if (cur == '\r') state = (state == 1) ? 1 : 1;
                else if (cur == '\n' && state == 1) state = 2;
                else if (cur == '\r' && state == 2) state = 3;
                else if (cur == '\n' && state == 3) break;
                else if (cur == '\n') state = 0;
                else state = 0;
            }

            byte[] headerBytes = headerBuf.toByteArray();
            String headerStr = new String(headerBytes, StandardCharsets.ISO_8859_1);
            String[] lines = headerStr.split("\r\n");
            if (lines.length == 0) return null;

            String statusLine = lines[0];
            String[] statusParts = statusLine.split(" ", 3);
            int status = statusParts.length >= 2 ? Integer.parseInt(statusParts[1]) : -1;

            Map<String,String> headers = new LinkedHashMap<>();
            for (int i = 1; i < lines.length; i++) {
                String line = lines[i];
                int idx = line.indexOf(":");
                if (idx > 0) {
                    String k = line.substring(0, idx).trim();
                    String v = line.substring(idx + 1).trim();
                    headers.put(k, v);
                }
            }

            byte[] body;
            String te = headers.getOrDefault("Transfer-Encoding", "").toLowerCase();
            if (te.contains("chunked")) {
                body = readChunked(bis);
            } else if (headers.containsKey("Content-Length")) {
                int len = Integer.parseInt(headers.get("Content-Length"));
                body = readFixed(bis, len);
            } else {
                body = readUntilEOF(bis);
            }

            FetchResult res = new FetchResult();
            res.status = status;
            res.headers = headers;
            res.body = body;
            return res;

        } catch (Exception e) {
            System.err.println("Fetch error: " + e.getMessage());
            e.printStackTrace();
            return null;
        }
    }

    static Socket openSocket(String proto, String host, int port) throws IOException {
        if (proto.equalsIgnoreCase("https")) {
            return SSLSocketFactory.getDefault().createSocket(host, port);
        } else {
            return new Socket(host, port);
        }
    }

    static byte[] readFixed(InputStream in, int len) throws IOException {
        byte[] buf = new byte[len];
        int off = 0;
        while (off < len) {
            int r = in.read(buf, off, len - off);
            if (r == -1) break;
            off += r;
        }
        if (off < len) return Arrays.copyOf(buf, off);
        return buf;
    }

    static byte[] readUntilEOF(InputStream in) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        byte[] buf = new byte[8192];
        int r;
        while ((r = in.read(buf)) != -1) baos.write(buf, 0, r);
        return baos.toByteArray();
    }

    static byte[] readChunked(InputStream in) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        BufferedReader br = new BufferedReader(new InputStreamReader(in, StandardCharsets.ISO_8859_1));
        while (true) {
            String line = br.readLine();
            if (line == null) break;
            line = line.trim();
            int semi = line.indexOf(';');
            String lenStr = (semi > 0) ? line.substring(0, semi) : line;
            int chunkSize = Integer.parseInt(lenStr.trim(), 16);
            if (chunkSize == 0) {
                while (true) {
                    String l = br.readLine();
                    if (l == null || l.length() == 0) break;
                }
                break;
            }
            int toRead = chunkSize;
            byte[] buf = new byte[8192];
            while (toRead > 0) {
                int r = in.read(buf, 0, Math.min(buf.length, toRead));
                if (r == -1) throw new EOFException("Unexpected EOF in chunked body");
                baos.write(buf, 0, r);
                toRead -= r;
            }
            in.read(); in.read();
        }
        return baos.toByteArray();
    }
}
