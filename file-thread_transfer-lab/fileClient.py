#! /usr/bin/env python3
# Client
import socket, sys, re
import os
# For params
sys.path.append("../lib")
import params

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
               # Send name of file
               s.send(filename.encode())

               # Send file data
               with open(filename, "r") as cf:
                  while True:
                     # Transfer file
                     tf = cf.read(1024)
                     # Send all file data to server
                     s.send(tf.encode())
                     if not tf:
                        break
               cf.close()
            else:
               print("File %s not found" % filename) 

   print('>>Received', repr(data))
   s.close() 

client()
