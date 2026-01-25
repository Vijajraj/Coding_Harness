# TCP HTTP downloader (Java)

This project implements a simple TCP-based HTTP downloader: a server accepts a URL from a client, fetches the web page using HTTP(S), and returns the bytes to the client which saves them to a file.

Files:

- File: [cn_exp_2/HttpServer.java](cn_exp_2/HttpServer.java)
- File: [cn_exp_2/HttpClient.java](cn_exp_2/HttpClient.java)

Compile:

```bash
# Java (optional)
javac HttpServer.java HttpClient.java
```

Run server (keep running):

```bash
java HttpServer
```

Run client (from another terminal):

```bash
java HttpClient https://example.com output.html
```

Python (no JDK required):

Run the Python server (requires Python 3):

```bash
python server.py
```

Run the Python client (in another terminal):

```bash
python client.py https://example.com output.html
```

The Python server listens on `127.0.0.1:4000`, accepts a URL terminated by a newline, fetches it using Python's `urllib`, and sends a 4-byte status code, a 4-byte body length, then the body bytes.


Notes:
- The server listens on `localhost:4000`.
- The client sends a UTF-8 encoded URL string to the server; the server responds with a 4-byte status code, a 4-byte length, and then the raw bytes of the response body.
- If Java is not available on your system, install the JDK and ensure `javac` and `java` are on your PATH.
