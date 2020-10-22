#! /usr/bin/env python3

import sys, re, socket, os
import threading
# For params
sys.path.append("../lib")
import params
# For framed socket
from framedSocket import FramedSock

# Lock
lock = threading.Lock()
# Server files
files = list()

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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
try:
   s.bind(bindAddr)
except socket.error as msg:
   print(">>Bind failed. Error code : " + str(msg[0]) + " Message " + msg[1])
   s.close()
s.listen()
print(f">>Server listening on: {bindAddr}")

# Server file transfer
class Server(threading.Thread):
   def __init__(self, s):
      threading.Thread.__init__(self)
      self.sock, self.addr = s
      self.file_s = FramedSock(s)

   # Check file availability
   # Apply lock to ensure only one thread checks file availability at a time
   def file_transfer_start(self, file_name):
      global lock, files
      lock.acquire()
      if file_name in files:
         lock.release()
         print("File currently in use. Try again later. Closing connection...")
         sys.exit(1)
      else:
         files.append(file_name)
         lock.release()

   # Close file
   # Apply lock to ensure only one thread removes the file it was using
   def file_transfer_end(self, file_name):
      global lock, files
      lock.acquire()
      files.remove(file_name)
      lock.release()

   # Save client file to server
   def save_file(self, file_name, file_data):
      file_name = file_name.decode()
      if not os.path.exists("./Server_Files/" + file_name):
         # Check file availability and apply lock
         self.file_transfer_start(file_name)
         # Save client file in server
         with open("./Server_Files/" + file_name, "w+b") as save_file:
            save_file.write(file_data)
         save_file.close()
         print(f">>File received from client {self.addr}!")
         self.file_transfer_end(file_name)
      else:
         print(f">>Filename {file_name} already exists in server. Closing connection...")
         sys.exit(1)
      
   # Handle client
   def run(self):
      # Display client host and port
      print(f">>New connection: {self.addr} connected.")
      # Get name of file
      file_name, file_data = self.file_s.framedReceive(debug)
      # Get file size
      if debug: print("rec'd: ", payload)
      # Check file is not empty
      if file_data is None:
         print(">>File is empty. Closing connection...")
         sys.exit(1)
      # Save client file to server
      self.save_file(file_name, file_data)
      
   

while True:
   sock = s.accept()
   server = Server(sock)
   server.start()
