#! /usr/bin/env python3

import sys, re, socket, os
import threading
# For params
sys.path.append("../lib")       
import params


# Handle client connection and file transfer
def handle_client(conn, addr):
   # Display client host and port
   print(f">>New connection: {addr} connected.")
   fi = 0
   fi += 1
   # Get name of file
   filename = conn.recv(1024).decode()
   print(filename)

   # Save client file
   with conn:
      while True:
         data = conn.recv(1024)
         udata = data.decode()
         if udata:
            with open(str(fi) + filename, "w") as fp:
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
   # Allow as many connections as needed
   s.listen()
   print(f">>Server is listening on 127.0.0.1")
   # Start a new thread for each new client connection
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
      # Start client connection   
      start(s)

server()
