#! /usr/bin/env python3

# Client
import socket

# localhost and port
host = '127.0.0.1'
port = 8080

# Server socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   # Connect to client 
   s.bind((host, port))
   # Allow 1 client connection
   s.listen()
   
   # File receive loop
   while True:
      # Wait for incoming client connection
      conn, addr = s.accept()
      # File instance
      fi = 1
      with open("fileTest" + str(fi) + ".txt", "wb") as sf:
         # Client transfer file
         ctf = conn.recv(1024)
         for line in ctf:
            sf.write(bytes(str(line), 'utf-8'))
         
      print("File received!")
      sf.close()
      
   print("Closing connection to client")
   conn.close()


      
            
      
