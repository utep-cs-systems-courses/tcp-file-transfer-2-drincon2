#! /usr/bin/env python3

# server
import sys, re, socket, os
# for params
sys.path.append("../lib")       
import params
# For proxy
sys.path.append("../framed-echo")
from framedSocket import FramedSock

# Server transfer file process    
class Server():
   def __init__(self, s):
      self.sock, self.addr = s
      self.file_s = FramedSock(s)  
   
   # Save client file
   def save_file(self, file_name, file_data):
      file_name = file_name.decode()
      if not os.path.exists("./Server_Files/" + file_name):
         with open("./Server_Files/" + file_name, "w+b") as save_file:
            save_file.write(file_data)
         save_file.close()
         print(f">>File received from client {self.addr}!")
         self.file_s.framedSend(file_name, b"cnt", debug)
      else:
         self.file_s.framedSend(file_name, b"File is already in server. Overwrite? (Y/n)", debug)
         client_file, client_response = self.file_s.framedReceive(debug)
         client_response = client_response.decode()
         if client_response == "Y":
            # Overwrite file
            with open("./Server_Files/" + file_name, "w+b") as save_file:
               save_file.write(file_data)
            save_file.close()
            print(f">>File {file_name} overwritten by client {self.addr}!")
         else:
            # Close connection to user
            print("Closing connection...")
            sys.exit(1)
            
   # Handle client with fork  
   def handle_client(self):
      # Display client host and port
      print(f">>New connection: {self.addr} connected")
      # Get name of file
      file_name, file_data = self.file_s.framedReceive(debug)
      # Check file is not empty
      if file_data is None:
         print(">>File is empty. Closing connection...")
         sys.exit(1)
      # Save file client to server
      self.save_file(file_name, file_data) 
      

# Server framework
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
   bindAddr = ("127.0.0.1", listenPort)
   try:
      s.bind(bindAddr)
   except socket.error as msg:
      print(">>Bind failed. Error code : " + str(msg[0]) + " Message " + msg[1])
      s.close()
   # Allow as many connections as needed
   s.listen()
   print(f">>Server is listening on: {bindAddr}")
   # Start client connection
   while True:
      sock = s.accept()
      if not sock:
         sys.exit(1)
         # Use fork to handle multiple clients
      elif not os.fork():
         server = Server(sock)
         server.handle_client()

