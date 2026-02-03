import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 import v
 text=v.vertaal_tekst(text,"dutch")
 speatch.output(text)

class buffer():
 def __init__(self,name):
  self.name=name
  self.muted=False
  self.items=[]
  self.pos=0
 def move(self,dir=1):
  if dir==0 and self.pos>0:
   self.pos-=1
   speak(self.items[self.pos])
  if dir==1 and self.pos<len(self.items)-1:
   self.pos+=1
   speak(self.items[self.pos])
 def edge(self,dir=0):
  try:
   if dir==0:
    self.pos=0
    speak(self.items[self.pos])
   else:
    self.pos=len(self.items)-1
    speak(self.items[self.pos])
  except:
    speak("There are no items in this buffer")
 def add(self,what):
  self.items.append(what)
  if self.muted==False and self.name!="all":
   speak(what)
