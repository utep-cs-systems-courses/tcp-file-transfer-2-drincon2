import re

class FramedSock:
   def __init__(self, s):
      self.sock, self.addr = s
      # receive buffer
      self.rbuf = b"" 

   def close(self):
      return self.sock.close()

   def framedSend(self, filename, payload, debug=0):
      if debug: print("framedSend: sending %d byte message" % len(payload))
      msg = str(len(payload)).encode() + b':' + filename.encode() + b':' + payload
      while len(msg):
         nsent = self.sock.send(msg)
         msg = msg[nsent:]
     
   def framedReceive(self, debug=0):
      state = "getLength"
      msgLength = -1
      while True:
         if (state == "getLength"):
            match = re.match(b'([^:]+):(.*):(.*)', self.rbuf, re.DOTALL | re.MULTILINE) # look for colon
            if match:
               #print(match.groups())
               lengthStr, filename, self.rbuf = match.groups()
               try: 
                  msgLength = int(lengthStr)
               except:
                  if len(self.rbuf):
                     print("badly formed message length:", lengthStr)
                     return None
               state = "getPayload"
         if state == "getPayload":
            if len(self.rbuf) >= msgLength:
               payload = self.rbuf[0:msgLength]
               self.rbuf = self.rbuf[msgLength:]
               return filename, payload
         r = self.sock.recv(100)
         self.rbuf += r
         if len(r) == 0:
            if len(self.rbuf) != 0:
               print("FramedReceive: incomplete message. \n  state=%s, length=%d, self.rbuf=%s" % (state, msgLength, self.rbuf))
            return None
         if debug: print("FramedReceive: state=%s, length=%d, self.rbuf=%s" % (state, msgLength, self.rbuf))
