#! /usr/bin/env python3

# Client
import socket, sys, re, os
# For params
sys.path.append("../lib")
import params
# For framed socket
from framedSocket import EncapFramedSock

# client framework
def client():
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
      
      # TODO Send client file to frame socket
      # Send files. Try breaking loop if errors occur here or in thread_framework
      while True:
         usr_in = input(">>Please type the file you want to upload to server.\n" +
                        ">>Alternatively, if you wish to close connection to server, type 'exit'.\n>>")
         # Close connection to server
         if usr_in == "exit":
            sys.exit(0)
         # Send file to server
         else:
            # File name
            filename = usr_in
            # Check file exists in current directory
            if os.path.exists(filename):          
               # Make new encapsulated socket 
               encap_s = EncapFramedSock((s, (host, port)))
               # Send file data
               with open(filename, "r") as cf:
                  while True:
                     # Transfer file
                     tf = cf.read(1024)
                     # Check file is not empty
                     if len(tf) == 0:
                        print("File empty, closing connection...")
                        sys.exit(1)
                     # Send file to encapsulated socket
                     encap_s.send(filename, tf, debug)
               cf.close()
            else:
               print("File %s not found" % filename) 
   
   print('>>Received', repr(data))
   s.close() 
   
   
client()

