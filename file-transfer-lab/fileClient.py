#! /usr/bin/env python3

# Client
import socket
import sys

# localhost and port
host = '127.0.0.1'
port = 8080

# Client socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   # Connect to server
   s.connect((host, port))
   # Open file
   with open("fileTest.txt", "rb") as cf:
      # Transfer file
      tf = cf.read(1024)
      for line in tf:
         # Send file
         data = s.send(bytes(str(line), 'utf-8')) 
   
print('Received', repr(data))
s.close()

