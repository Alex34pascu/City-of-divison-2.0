import key_constants as kc
import timer
import net
import pygame, pygame.locals as pl

from pygame.locals import *
pygame.init()

import sound_pool
sp=sound_pool.sound_pool
import v
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 text=v.vertaal_tekst(text,v.language)
 speatch.output(text)
v.get()
rshift=False
lshift=False
shift=False
class mega_menu():
 def __init__(self):
  self.pos=0
  self.items=[]
 def reset(self):
  self.pos=0
  self.items=[]
 def change_check_box(self,name,value):
  for i in self.items:
   if i.name=="check_box":
    if i.text==name:
     i.onoff=value
     if i.onoff==0:
      on="unchecked"
     else:
      on="checked"
     i.sort="check_box: "+on
 def get_check_box(self,name):
  for i in self.items:
   if i.name=="check_box":
    if i.text==name:
     return i.onoff
  return -1
 def add_item(self,what,text=""):
  if what=="check_box":
   self.items.append(check_box(text))
  if what=="dlg":
   self.items.append(dlg(text))
  if what=="button":
   self.items.append(button(text))
 def loop(self,message="",online=True):
  global rshift
  global lshift
  global shift
  speak(message)
  flag=True
  while flag:
   if online==True:
    m=net.mainloop()
    if m==1:
     return
   if rshift==False and lshift==False:
    shift=False
   else:
    shift=True
   keys = pygame.key.get_pressed()
   if keys[pygame.K_LSHIFT]:
    lshift=True
   if keys[pygame.K_RSHIFT]:
    rshift=True
   for event in pygame.event.get():
    if event.type==pygame.KEYDOWN:
     if event.scancode==kc.K_TAB:
      if shift==True:
       self.pos-=1
      else:      
       self.pos+=1
      if self.pos>=len(self.items):
       self.pos=0
      if self.pos<0:
       self.pos=len(self.items)-1
      speak(self.items[self.pos].text+", "+self.items[self.pos].sort)
    if event.type==pygame.KEYUP:
     if event.scancode==kc.K_LSHIFT:
      lshift=False
     if event.scancode==kc.K_RSHIFT:
      rshift=False
     if event.scancode==kc.K_ESCAPE:
      return ""
     if event.scancode==kc.K_RETURN:
      if self.items[self.pos].sort=="button":
       return self.items[self.pos].text

     if event.scancode==kc.K_SPACE:
      if self.items[self.pos].sort=="button":
       return self.items[self.pos].text
      self.items[self.pos].update("space")
     if event.scancode==kc.K_RIGHT:
      self.items[self.pos].update("right")
     if event.scancode==kc.K_LEFT:
      self.items[self.pos].update("left")
     if event.scancode==kc.K_UP:
      self.items[self.pos].update("up")
     if event.scancode==kc.K_DOWN:
      self.items[self.pos].update("down")
class check_box():
 def __init__(self,text,onoff=0):
  self.text=text
  self.onoff=onoff
  if self.onoff==0:
   on="unchecked"
  else:
   on="checked"
  self.sort="check_box: "+on
  self.name="check_box"
 def update(self,key):
  if key=="space":
   if self.onoff==0:
    sp.play_stationary("sounds\checkboxcheck.ogg")
    speak("checked")
    self.onoff=1
   else:
    sp.play_stationary("sounds\checkboxuncheck.ogg")
    speak("unchecked")
    self.onoff=0
  if self.onoff==0:
   on="unchecked"
  else:
   on="checked"
  self.sort="check_box: "+on

class dlg():
 def __init__(self,text):
  self.sort="dialog"
  self.text=text
  self.name=self.sort
 def update(self,key):
  if key=="left" or key=="right" or key=="up" or key=="down":
   speak(self.text)
class button():
 def __init__(self,text):
  self.sort="button"
  self.text=text
  self.name=self.sort
 def update(self,key):
  pass
