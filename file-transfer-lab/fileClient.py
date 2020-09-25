#! /usr/bin/env python3

# Client
import socket

# localhost and port
host = '127.0.0.1'
port = 8080

# Client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   s.connect((host, port))
   s.sendall(b'Hello World!')
   data = s.recv(1024)
   
print('Received', repr(data))
