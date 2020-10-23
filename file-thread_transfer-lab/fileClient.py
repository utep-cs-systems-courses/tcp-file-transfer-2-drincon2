#! /usr/bin/env python3
# Client
import socket, sys, re
import os
# For params
sys.path.append("../lib")
import params
# For framed socket 
from framedSocket import FramedSock


# client framework

# Client switches
switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)
server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]
   
if usage:
   params.usage()
      
# Client connection to server
# Split server into local host and port
try:
   host, serverPort = re.split(":", server)
   port = int(serverPort)
except:
   print(">>Unable to parse port from '%s'" % server)
   sys.exit(1)
# Make socket to connect and send files to server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   # Check socket can be opened
   if s is None:
      print(">>Socket could not be opened")
      sys.exit(1)
   # Connect to server
   s.connect((host, port))
   
   # Make new client framed socket
   encap_s = FramedSock((s, (host, port)))
   
   # Send files 
   while True:
      usr_in = input(">>Please type the file you want to upload to server.\n" +
                     ">>Alternatively, if you wish to close connection to server, type 'exit'.\n>>")
      # Close connection to server
      if usr_in == "exit":
         sys.exit(0)
      # Send file to server
      else:
         # Check file exists in current directory
         filename = usr_in
         if os.path.exists(filename):   
            # Send file data. Errors might happen here
            file = open(filename, "rb")
            file_data = file.read()
            encap_s.framedSend(filename, file_data, debug)
            
            print(">>File sent")
            
            # Receive prompt from server if file is received or already exists
            prompt_file, server_prompt = encap_s.framedReceive(debug)
            state = server_prompt.decode()
            
            # Continue file transfer or overwrite file
            if state == "cnt":
               continue
            else:
               usr_response = input(">>" + state)
               encap_s.framedSend(filename, usr_response.encode(), debug)
               state = "cnt"
            
         else:
            print("File %s not found" % filename) 

