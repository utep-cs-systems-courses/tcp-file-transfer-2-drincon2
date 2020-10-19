#! /usr/bin/env python3

import sys, re, socket, os
import threading
# For params
sys.path.append("../lib")       
import params
# For framed socket
from framedSocket import EncapFramedSock

# Client files
files = set()
# Lock
lock = Lock()


# File transfer start
def file_transfer_start(filename):
   global files, lock
   lock.acquire()
   if filename in files:
      print("File is currently in use")
      lock.release()
      sys.exit(1)
   else:
      files.add(filename)
      lock.release()

# File transfer end
def file_transfer_end(filename):
   global files, lock
   lock.acquire()
   files.remove(filename)
   lock.release()
   
   
# Handle client connection and file transfer
def handle_client(conn, addr, socket, debug):
   # File size
   payload = ""
   # Get name of file and data
   try:
      filename, file_data = socket.receive(debug)
   except:
      print(">>File transfer failed. Closing connection...")
      sys.exit(1)
      
   if debug:
      print("rec'd: ", payload)
   
   if payload is None:
       print("File is empty. Closing connection...")
       sys.exit(1)
   
   filename = filename.decode()
   
   # Save client file
   with conn:
      try:
         if not os.path.exists("./Server_Files/" + filename):
            # Attempt to lock thread transfering file
            file_transfer_start(filename)
            with open("./Server_Files/" + filename, "w") as fp:
               for line in udata:
                  fp.write(line)
            fp.close()
            print(f">>File {filename} received from client {addr}!")
            # Release lock on thread      
            file_transfer_end(filename)
         else:
            print("File already exists on server. Closing connection...")
            sys.exit(1)
      except:
         print("File" + filename + "failed to upload. Closing connection...")
         sys.exit(1)
   print(f">>Closing connection to client {addr}")   
   conn.close()


# Server
class Server(Thread):
   def __init__(self, s_addr, debug):
      Thread.__init__(self)
      self.conn, self.addr = s_addr
      self.file_s = EncapFramedSock(s_addr)
      self.debug = debug
      
   def run(self):
       print(f">>New connection: {self.addr} connected.")
       while True:
          # Handle client
          handle_client(self.conn, self.addr, self.file_s, self.debug)
   

# Listening socket 
def listening_socket():
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
      # Allow as many connections as needed
      s.listen()
      print(f">>Server is listening on 127.0.0.1")
      # Start client connection 
      while True:
         # Accept client connection
         conn, addr = s.accept()
         # Start client connection 
         server = Server((conn, addr))
         server.start()
         print(f">>Active connections: {threading.activeCount() -1}")

listening_socket()
