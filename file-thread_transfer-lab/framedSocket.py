import re

class EncapFramedSock:

   def __init__(self, s_addr):
      self.sock, self.addr = s_addr
      # receive buffer
      self.rbuf = b""

   def send(self, filename, payload, debug=0):
      if debug: print("framedSend: sending %d byte message" % len(payload))
      msg = str(len(payload)).encode() + b':' + filename.encode() + b':' + payload
      while len(msg):
         nsent = self.sock.send(msg)
         msg = msg[nsent:]

   def receive(self, debug=0):
      state = "getLength"
      msgLength = -1
      while True:
         if (state == "getLength"):
             # Look for colon
             match = re.match(b'([^:]+):(.*)', self.rbuf, re.DOTALL | re.MULTILINE)
             if match:
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
               return payload
            r = self.sock.recv(100)
            self.rbuf += r
            if len(r) == 0:
               if len(self.rbuf) != 0:
                  print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, self.rbuf))
                  return None
            if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, self.rbuf))

