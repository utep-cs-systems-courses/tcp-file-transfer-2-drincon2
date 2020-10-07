#! /usr/bin/env python3

# server
import sys, re, socket
import threading
# for params
sys.path.append("../lib")       
import params
# For proxy
sys.path.append("../framed-echo")
from framedSock import framedSend, framedReceive


# Handle client connection and file transfer
def handle_client(conn, addr):
   print(f">>New connection: {addr} connected.")
   fi = 0
   fi += 1
   with conn:
      while True:
         data = conn.recv(1024)
         udata = data.decode()
         if udata:
            with open("fileTest" + str(fi) + ".txt", "w") as fp:
               for line in udata:
                  fp.write(line)
            fp.close()
            print(f">>File received from client {addr}!")
         elif not data:
            break
   print(f">>Closing connection to client {addr}")
   conn.close()
   
   
# Start client connection 
def start(s):
   s.listen()
   print(f">>Server is listening on 127.0.0.1")
   while True:
      conn, addr = s.accept()
      thread = threading.Thread(target=handle_client, args=(conn, addr))
      thread.start()
      print(f">>Active connections: {threading.activeCount() -1}")

# Server framework    
def server():
   switchesVarDefaults = (
       (('-l', '--listenPort') ,'listenPort', 50001),
       (('-d', '--debug'), "debug", False), # boolean (set if present)
       (('-?', '--usage'), "usage", False), # boolean (set if present)
       )

   progname = "fileServer"
   paramMap = params.parseParams(switchesVarDefaults)

   debug, listenPort = paramMap['debug'], paramMap['listenPort']

   if paramMap['usage']:
      params.usage()
    
   # Server connection to client
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      try:
         s.bind(("127.0.0.1", listenPort))
      except socket.error as msg:
         print(">>Bind failed. Error code : " + str(msg[0]) + " Message " + msg[1])
         s.close()
      # Start client connection to server  
      start(s)

server()
