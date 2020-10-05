#! /usr/bin/env python3

# server
import sys, re, socket
# for params
sys.path.append("../lib")       
import params
# For proxy
sys.path.append("../framed-echo")
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "dummy_server"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()
    
# Server connection to client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
   # Check server can bind to client
   try:
      s.bind(("127.0.0.1", listenPort))
   except socket.error as msg:
      print("Bind failed. Error code : " + str(msg[0]) + " Message " + msg[1])
      s.close()
   # Accept to 1 connection   
   s.listen()
   # Wait for client connection to server
   conn, addr = s.accept()
   
   # Save client file in server
   with conn:
      while True:
         data = conn.recv(1024)
         udata = data.decode()
         if udata:
            fi = 1
            with open("fileTest" + str(fi) + ".txt", "w") as fp:
               for line in udata:
                  fp.write(line)
            fp.close()
            print("File received!")
         elif not data:
            break
   print("Closing connection to client")
   conn.close()

