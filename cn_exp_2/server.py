#!/usr/bin/env python3
import socket
import struct
import threading
from urllib.request import urlopen, Request

HOST = '127.0.0.1'
PORT = 4000

def handle_client(conn, addr):
    try:
        with conn:
            # read url (terminated by newline)
            buf = bytearray()
            while True:
                b = conn.recv(1)
                if not b:
                    return
                if b == b'\n':
                    break
                buf += b
            url = buf.decode('utf-8').strip()
            print('Requested URL from', addr, url)

            try:
                req = Request(url, headers={'User-Agent': 'PythonServer/1.0'})
                with urlopen(req, timeout=10) as resp:
                    status = getattr(resp, 'status', 200)
                    body = resp.read()
            except Exception as e:
                status = 0
                body = ('ERROR: ' + str(e)).encode('utf-8')

            # send status (4 bytes) and length (4 bytes) then body
            conn.sendall(struct.pack('!I', int(status)))
            conn.sendall(struct.pack('!I', len(body)))
            conn.sendall(body)
            print('Sent', len(body), 'bytes to', addr)
    except Exception as e:
        print('handler error:', e)

def serve():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print('Server listening on', HOST, PORT)
        while True:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == '__main__':
    serve()
