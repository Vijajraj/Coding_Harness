#!/usr/bin/env python3
import socket
import struct
import sys

HOST = '127.0.0.1'
PORT = 4000

def read_n(sock, n):
    data = bytearray()
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise EOFError('socket closed')
        data.extend(chunk)
    return bytes(data)

def main():
    if len(sys.argv) < 2:
        print('Usage: python client.py <url> [output-file]')
        return
    url = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) >= 3 else 'output.html'

    with socket.create_connection((HOST, PORT), timeout=10) as s:
        # send url terminated by newline
        s.sendall((url + '\n').encode('utf-8'))

        status_b = read_n(s, 4)
        length_b = read_n(s, 4)
        status = struct.unpack('!I', status_b)[0]
        length = struct.unpack('!I', length_b)[0]
        print('Status:', status, 'Length:', length)

        body = read_n(s, length) if length > 0 else b''
        with open(out, 'wb') as f:
            f.write(body)
        print('Saved', len(body), 'bytes to', out)

if __name__ == '__main__':
    main()
