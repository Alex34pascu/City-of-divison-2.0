import random
import v
v.get()
import net
import key_constants as kc
import timer
import pygame, pygame.locals as pl
from pygame.locals import *
pygame.init()
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 speatch.output(text)

def simon(amount):
 endtimer=timer.timer()
 new_timer=timer.timer()
 new_timer.set(800)
 new=True
 comands=[]
 progress=0
 while 1:
  net.mainloop()
  if endtimer.elapsed()>2000:
   return False

  if new==True and new_timer.elapsed()>800:
   new=False
   i=random.randint(1,4)
   v.msp.play_stationary(r"sounds\\simon"+str(i)+".ogg")
   comands.append(i)

  if progress>=amount:
   return True

  if progress>=len(comands) and new==False:
   new_timer.restart()
   new=True
   progress=0

  for event in pygame.event.get():
   if event.type==pygame.KEYDOWN:
    if event.scancode==kc.K_ESCAPE: 
     return False
    if new==False:
     if event.scancode==kc.K_LEFT: 
      endtimer.restart()
      i=2
      if comands[progress]==i:
       v.msp.play_stationary(r"sounds\\simon"+str(i)+".ogg")
       progress+=1
      else:
       return False
     elif event.scancode==kc.K_DOWN: 
      endtimer.restart()
      i=1
      if comands[progress]==i:
       v.msp.play_stationary(r"sounds\\simon"+str(i)+".ogg")
       progress+=1
      else:
       return False
     elif event.scancode==kc.K_UP: 
      endtimer.restart()
      i=3
      if comands[progress]==i:
       v.msp.play_stationary(r"sounds\\simon"+str(i)+".ogg")
       progress+=1
      else:
       return False
     elif event.scancode==kc.K_RIGHT: 
      endtimer.restart()
      i=4
      if comands[progress]==i:
       v.msp.play_stationary(r"sounds\\simon"+str(i)+".ogg")
       progress+=1
      else:
       return False
