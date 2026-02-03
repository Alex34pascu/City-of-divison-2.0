import key_constants as kc
import music
import virtual_input
import sound_pool
import timer
import net
import pygame, pygame.locals as pl
from pygame.locals import *
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 if text=="":
  return
 text=v.vertaal_tekst(text,v.language)
 speatch.output(text)
pygame.init()
import v
v.get()
import menu

class square_menu(menu.Menu):
 def __init__(self):
  super().__init__()
  self.stoptimer=timer.timer()
  self.stoptime=0
  self.stopping=False
  self.cowndown=False
  self.set_cords(5,5)

  self.x_pos=0
  self.y_pos=0

 def play_sound(self,name):
  v.msp.play_stationary(name.replace("%name",self.items[self.x_pos][self.y_pos]))

 def set_cords(self,maxx,maxy):
  self.items=[]
  self.subitems=[]
  for _ in range(maxx):
   row = ["" for _ in range(maxy)]
   self.items.append(row)
   self.subitems.append(row)

 def get_item(self):
  return self.items[self.x_pos][self.y_pos]

 def add_item(self,x,y,what,sub=""):
  self.items[x][y]=what
  if sub!="":
   self.subitems[x][y]=sub
  else:
   self.subitems[x][y]=what

 def loop(self,message="",online=False):
  v.firing=False
  net.send("stop_shooting")
  self.search=""
  if self.pos==-1:
   speak(message)
   self.play_sound(self.open_sound)
   if self.music!="":
    music.pause_all_musics()

   if self.music!="":
    self.mus=music.music(self.music)
   else:
    self.mus=None
  flag=True
  while flag:
   if self.stopping==True:
    if self.stoptimer.elapsed()>self.stoptime-5000 and self.cowndown==False:
     self.cowndown=True
     v.msp.play_stationary("sounds\countdown.ogg")
    if self.stoptimer.elapsed()>self.stoptime:
     return self.items[0][0]

   keys = pygame.key.get_pressed()
   v.shift= keys[K_LSHIFT] or keys[K_RSHIFT]
   v.alt= keys[K_LALT] or keys[K_RALT]
   v.ctrl= keys[K_LCTRL] or keys[K_RCTRL]
   v.msp.reverb=-1
   v.msp.mix=-100
   if online==True:
    m=net.mainloop()
    if m==1:
     return
   keys = pygame.key.get_pressed()
   try:
    if keys[pygame.K_PAGEUP] and self.musictimer.elapsed()>=10 and self.mus.handle.volume<0:
     self.musictimer.restart()
     self.mus.handle.volume+=1
     v.musicvolume+=1
    if keys[pygame.K_PAGEDOWN] and self.musictimer.elapsed()>=10 and self.mus.handle.volume>-100:
     self.musictimer.restart()
     self.mus.handle.volume-=1
     v.musicvolume-=1
   except:
    pass
   for event in pygame.event.get():
    if event.type==pygame.KEYDOWN:
     if event.scancode==kc.K_LEFT:
      if self.x_pos>=1:
       self.x_pos-=1
       speak(self.items[self.x_pos][self.y_pos])
       self.play_sound(self.click_sound)
      else:
       self.play_sound(self.edge_sound)
     if event.scancode==kc.K_RIGHT:
      if self.x_pos<=len(self.items)-2:
       self.x_pos+=1
       speak(self.items[self.x_pos][self.y_pos])
       self.play_sound(self.click_sound)
      else:
       self.play_sound(self.edge_sound)

     if event.scancode==kc.K_UP:
      if self.y_pos>=1:
       self.y_pos-=1
       speak(self.items[self.x_pos][self.y_pos])
       self.play_sound(self.click_sound)
      else:
       self.play_sound(self.edge_sound)
     if event.scancode==kc.K_DOWN:
      if self.y_pos<=len(self.items[self.x_pos])-2:
       self.y_pos+=1
       speak(self.items[self.x_pos][self.y_pos])
       self.play_sound(self.click_sound)
      else:
       self.play_sound(self.edge_sound)

     elif event.scancode==kc.K_RETURN and self.subitems[self.x_pos][self.y_pos]!="":
      self.play_sound(self.enter_sound)
      return self.subitems[self.x_pos][self.y_pos]
     elif event.scancode==kc.K_ESCAPE: 
      self.play_sound(self.close_sound)
      return ""

class online_square_menu(square_menu):
 def play_sound(self,name):
  net.send(r"player_sound "+v.name+" "+name.replace("%name",self.items[self.x_pos][self.y_pos])+" 0")