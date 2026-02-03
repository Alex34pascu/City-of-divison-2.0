import socket

class InstanceChecker():
 def __init__(self):
  self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 def is_running(self):
  try:
   self.s.bind(("87.248.157.107", 3030))
   self.s.listen(1)
   return False
  except socket.error:
   return True