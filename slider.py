import key_constants as kc
import timer
import net
import pygame, pygame.locals as pl
from pygame.locals import *
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 text=v.vertaal_tekst(text,"nl")
 speatch.output(text)
pygame.init()
import v
v.get()

class slider():
 def __init__(self,min,max,text):
  self.min=min
  self.max=max
  self.text=text
  self.movetimer=timer.timer()
  self.movetimer.set(80)
  self.player_sound=False
  self.name=""
 def play_sound(self,name):
  if self.player_sound==False:
   v.msp.play_stationary(r"sounds\\"+self.name+name+".ogg")
  else:
   net.send(r"player_sound "+v.name+" sounds\\"+self.name+name+".ogg 0")
 def run(self,online=False,cursorpos=-1,jumps=10,value="value"):
  if cursorpos>-1:
   cursor=cursorpos
  else:
   cursor=self.min
  speak(self.text)
  flag=True
  self.play_sound("open")
  while flag:
   if online==True:
    m=net.mainloop()
    if m==1:
     return

   for event in pygame.event.get():
    if event.type==pygame.KEYDOWN:
     if event.scancode==kc.K_ESCAPE: 
      return -1
     if event.scancode==kc.K_F1: 
      speak("Use the arrow keys to adjust the "+value+" by 1. Shift + arrow keys to adjust the "+value+" by 10. Control + shift + arrow keys to adjust the "+value+" by "+str(jumps*10)+".")
     if event.scancode==kc.K_RETURN: 
      self.play_sound("enter")
      return cursor

     if event.scancode==kc.K_UP: 
      if v.shift==True:
       if v.ctrl==True:
        cursor+=jumps*10
       else:
        cursor+=10

      else:
       cursor+=1
      if cursor>self.max:
       cursor=self.max
      speak(str(cursor))
      self.play_sound("click")
     if event.scancode==kc.K_DOWN: 
      if v.shift==True:
       if v.ctrl==True:
        cursor-=10*jumps
       else:
        cursor-=10
      else:
       cursor-=1
      if cursor<self.min:
       cursor=self.min
      speak(str(cursor))
      self.play_sound("click")

