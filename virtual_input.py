import key_constants as kc
import timer
import pyperclip as pc
import map
import v as va
va.get()
import net
import pygame
from pygame.locals import *
pygame.init()

import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 text=va.vertaal_tekst(text,"nl")
 speatch.output(text,True)

class virtual_input():
 def __init__(self,label):
  self.actiontimer=timer.timer()
  self.actiontime=300
  self.typing_sounds=va.typing_sounds
  self.speak_chars=va.speak_chars
  self.numeric=False
  self.closing=False
  self.hidden=False
  self.closing=False
  self.cursor=0
  self.lselect=0
  self.rselect=0
  self.text=""
  self.submited=False
  self.submitedtext=""
  self.label=label
  speak(label)
 def translate(self,char):
  if self.cursor<=-1:
   return ""
  if char.isupper() and va.speak_cap==1:
   return "capital "+char
  elif char=="%":
   return "percent"
  elif char==",":
   return "comma"
  elif char==" ":
   return "space"

  elif char==".":
   return "dot"
  elif char=="!":
   return "exclamation mark"
  elif char=="@":
   return "at"
  elif char=="#":
   return "hashtag"
  elif char=="$":
   return "dollar"
  elif char=="^":
   return "caret"
  elif char=="&":
   return "and"
  elif char==r"'":
   return "appostrophe"
  elif char==r'"':
   return "quotation mark"
  elif char==")":
   return "right paren"
  elif char=="(":
   return "left paren"
  elif char=="]":
   return "right bracket"
  elif char=="[":
   return "left bracket"
  elif char=="{":
   return "left brace"
  elif char=="}":
   return "right brace"
  elif char=="+":
   return "plus"
  elif char=="-":
   return "minus"
  elif char=="=":
   return "equals"
  elif char=="/":
   return "slash"
  elif char=="<":
   return "less"
  elif char==">":
   return "greater"
  elif char=="?":
   return "question mark"
  elif char=="`":
   return "accent graf"
  elif char=="_":
   return "underscore"
  elif char=="\\":
   return "backslash"
  elif char=="|":
   return "bar"
  elif char=="":
   return "empty"
  elif char==":":
   return "colon"
  elif char==";":
   return "semi"
  else:
   return char
 def cursormove(self,direction):
  if(direction=="l") and len(self.text)>0:
   self.cursor=self.cursor-1
  if(direction=="r"):
   self.cursor=self.cursor+1
  if self.cursor>len(self.text)-1:
   self.cursor=len(self.text)
   if self.speak_chars==1:
    speak(" ")
  elif(self.cursor<0):
   self.cursor=0
   if self.speak_chars==1:
    speak(self.translate(self.text[self.cursor]))
  else:
   if self.hidden==False:
    if self.speak_chars==1:
     speak(self.translate(self.text[self.cursor]))
   else:
    if self.speak_chars==1:
     speak("*")

 def loop(self):
   if self.actiontime!=300 and self.actiontimer.elapsed()>300:
    self.actiontime=300
   keys = pygame.key.get_pressed()
   if keys[pygame.K_BACKSPACE] and self.actiontimer.elapsed()>self.actiontime:
    self.actiontimer.restart()
    self.actiontime=120
    if(self.cursor>len(self.text)):
     self.cursor=len(self.text)
    if((self.cursor-1>=0) and (len(self.text)>0)):
     self.cursor=self.cursor-1
     ungluded=list(self.text)
     if self.typing_sounds==1:
      va.msp.play_stationary(r"sounds\\typebackspace.ogg")
     if self.hidden==False:
      speak(self.translate(ungluded[self.cursor]))
     else:
      speak("*")
     ungluded[self.cursor]=""
     self.text="".join(ungluded)


 def update(self,keyrec,say=True):
   keys = pygame.key.get_pressed()
   if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
    if(keyrec.scancode==kc.K_RIGHT) and self.cursor<len(self.text):
     i=0
     while i!=1:
      if self.cursor>=len(self.text)-1:
       self.cursor=len(self.text)-1
       self.cursormove("r")
       break
       speak("")
      self.cursor+=1

      if self.text[self.cursor]==" ":
       while self.cursor<len(self.text)-1 and self.text[self.cursor]==" ":
        self.cursor+=1
       cursor=self.cursor
       j=0
       while j!=1:
        if cursor>=len(self.text)-1 or self.text[cursor]==" " and self.text[self.cursor:cursor].replace(" ","")!="":
         j=1
        cursor+=1
       speak(self.text[self.cursor:cursor])
       i=1
    if(keyrec.scancode==kc.K_LEFT) and self.cursor>0:
     i=0
     cursor=self.cursor
     while i!=1:
      cursor-=1
      if self.text[cursor]==" " and self.text[cursor:self.cursor].replace(" ","")!="":
       cursor+=1
       speak(self.text[cursor:self.cursor])
       self.cursor=cursor
       break
      if cursor<=0:
       speak(self.text[cursor:self.cursor])
       self.cursor=0
       break

    if(keyrec.scancode==kc.K_v):
     ungluded=list(self.text)
     text=pc.paste()
     chars=list(text)
     for t in chars:
      self.cursor=self.cursor+1
      ungluded.insert(self.cursor,t)
     self.text="".join(ungluded)
     speak("text pasted")
     if self.typing_sounds==1:
      va.msp.play_stationary(r"sounds\\typepaste.ogg")
     return
    elif(keyrec.scancode==kc.K_c):
     pc.copy(self.text)
     speak(self.text+" copied to clipboard.")
     return
    elif(keyrec.scancode==kc.K_x):
      pc.copy(self.text)
      speak(self.text+" cut to clipboard.")
      self.text=""
      self.cursor=self.lselect
      return
    else:
     return
   if(keyrec.scancode==kc.K_ESCAPE):
    self.closing=True
    self.submitedtext=""
    self.closing=True
    speak("canceled")
   elif(keyrec.scancode==kc.K_HOME) and len(self.text)>0:
    self.cursor=0
    if self.hidden==False:
     if self.speak_chars==1:
      speak(self.translate(self.text[self.cursor]))
    else:
     if self.speak_chars==1:
      speak("*")
   elif(keyrec.scancode==kc.K_END) and len(self.text)>0:
    self.cursor=len(self.text)-1
    self.cursormove("r")
#    if self.hidden==False:
#     speak(self.translate(self.text[self.cursor]))
#    else:
#     speak("*")
   elif(keyrec.scancode==kc.K_UP):
    if self.hidden==False:
     speak(self.text)
    else:
      speak(str(len(self.text))+"*")
   elif(keyrec.scancode==kc.K_DOWN):
    if self.hidden==False:
     speak(self.text)
    else:
      speak(str(len(self.text))+"*")
   elif(keyrec.scancode==kc.K_RETURN):
    self.submitedtext=self.text
    self.text=""
    self.cursor=0
    if self.typing_sounds==1:
     va.msp.play_stationary(r"sounds\\typeenter.ogg")
   elif(keyrec.scancode==kc.K_LEFT):
    self.cursormove("l")
   elif(keyrec.scancode==kc.K_RIGHT):
    self.cursormove("r")
   elif(keyrec.scancode==kc.K_TAB):
    speak(self.label)
#    for event in pygame.event.get():
#     if event.type==pygame.KEYDOWN:
#      v.update(event)

#    return
 def add_text(self,keyrec,say=True):
   old_length=len(self.text)
   if self.cursor>=0 and keyrec.text!="":
    if not keyrec.text.isnumeric() and self.numeric==True:
     return
    ungluded=list(self.text)
    if self.cursor<len(ungluded)-1 and self.cursor>=1:
     ungluded.insert(self.cursor,keyrec.text)
    else:
     ungluded.insert(self.cursor,keyrec.text)
    self.text="".join(ungluded)
    key=keyrec.text
    if key!="":
     if key!=" ":
           if self.typing_sounds==1:
            va.msp.play_stationary(r"sounds\\typechar.ogg")
           if self.hidden==False:
            if say==True:
             if self.speak_chars==1:
              speak(self.translate(key))
           else:
            if self.speak_chars==1:
             speak("*")
     else:
           if self.typing_sounds==1:
            va.msp.play_stationary(r"sounds\\typespace.ogg")
           if say==True:
            if self.speak_chars==1:
             speak("space")
    self.cursor+=len(self.text)-old_length

def calculation(message=""):
 pygame.key.start_text_input()
 endtimer=timer.timer()
 message=message.replace("+","plus")
 message=message.replace("-","minus")
 message=message.replace("*","times")
 message=message.replace("/","divided by")
 if va.firing==True:
  va.firing=False
  net.send("stop_shooting")
 v=virtual_input(message)
 v.numeric=True
 flag=True
 while flag:
  m=net.mainloop()
  if m==1:
   va.dieing=True
   return ""
  if endtimer.elapsed()>4000:
   speak("time is over")
   return ""
  if v.submitedtext!="" or v.closing==True:
   flag=False
  v.loop()
  for event in pygame.event.get():
   if event.type == pygame.TEXTINPUT:
    v.add_text(event)
   if event.type==pygame.KEYDOWN:
    v.update(event)


 if v.closing==False:
  pygame.key.stop_text_input()
  if "|n|" in v.submitedtext or "|end|" in v.submitedtext:
   speak("There are 1 or more forbidden charactars in your tekst.")
   return ""
  else:
   return v.submitedtext
 else:
  return ""


  return ""

def input(message="",online=True,text="",hidden=False,numeric=False):
 pygame.key.start_text_input()
 if va.firing==True:
  va.firing=False
  net.send("stop_shooting")
 v=virtual_input(message)
 if text!="":
  v.text=text
  v.cursor=len(v.text)
 v.hidden=hidden
 v.numeric=numeric
 flag=True
 while flag:
  if online==True:
   m=net.mainloop()
   if m==1:
    va.dieing=True
    return ""
  v.loop()
  if v.submitedtext!="" or v.closing==True:
   flag=False
  for event in pygame.event.get():
   if event.type == pygame.TEXTINPUT:
    v.add_text(event)
   if event.type==pygame.KEYDOWN:
    v.update(event)

 if v.closing==False:
  pygame.key.stop_text_input()
  if len(v.submitedtext)>10000:
   speak("input is to long")
   return ""
  if "|n|" in v.submitedtext or "|end|" in v.submitedtext:
   speak("There are 1 or more forbidden charactars in your tekst.")
   return ""
  else:
   return v.submitedtext
 else:
  return ""

