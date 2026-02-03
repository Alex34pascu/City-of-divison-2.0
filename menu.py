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
 text=v.vertaal_tekst(text,v.language)
 speatch.output(text)
pygame.init()
import v
v.get()
class Menu:
 def __init__(self):
  self.preview=""
  self.frash=True
  self.searched=""
  self.previewpos=-1
  self.previewsound=None
  self.search=""
  self.cleansearchtimer=timer.timer()
  self.musictimer=timer.timer()
  self.close_sound=""
  self.edge_sound=""
  self.items=[]
  self.subitems=[]
  self.pos=-1
  self.music=""
  self.click_sound=""
  self.open_sound=""
  self.enter_sound=""
 def play_sound(self,name):
  v.msp.play_stationary(name)
 def get_item(self):
  return self.subitems[self.pos]

 def reset(self,reset_pos=True):
  self.__init__()
 def add_item(self,what,sub=""):
  if sub!="":
   self.subitems.append(sub)
  else:
   self.subitems.append(what)
  self.items.append(v.vertaal_tekst(what,v.language))

 def loop(self,message="",online=False):
  if(online==True):
   v.firing=False
   net.send("stop_shooting")
  self.search=""
  if self.pos==-1:
   speak(message)
   self.play_sound(self.open_sound)
   if self.music!="":
    music.pause_all_musics()

   if self.music!="":
    self.mus=music.music(self.music,v.musicvolume)
   else:
    self.mus=None
  flag=True
  while flag:
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
   if self.cleansearchtimer.elapsed()>300:
    self.cleansearchtimer.restart()
    self.frash=True
    self.search=""
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
     if event.scancode==kc.K_f and self.search=="" and v.ctrl==True:
      search=virtual_input.input("search for "+self.searched,online,self.searched)
      if search!="":
       self.searched=search
       c=self.pos
       f=0
       for i in self.items:
        if search.lower() in i.lower() and self.items.index(i)>c:
         f=1
         c=self.items.index(i)
         break
       if f==0:
        for i in self.items:
         if search.lower() in i.lower():
          f=1
          c=self.items.index(i)
          break

       if f==1:
        self.pos=c
        speak(self.items[self.pos])
       else:
        speak("no results.")
     if event.scancode==kc.K_SPACE and self.search=="" and self.pos>-1 and self.preview!="":
      f=self.preview.replace("%name",self.items[self.pos])
      v.msp.destroy_all()
      self.play_sound(r"sounds\\"+f)
     if event.scancode==kc.K_DOWN or event.scancode==kc.K_RIGHT:
      if self.pos<=len(self.items)-2:
       self.pos+=1
       speak(self.items[self.pos])
       self.play_sound(self.click_sound)
      else:
       self.play_sound(self.edge_sound)
     elif event.scancode==kc.K_HOME:
      self.pos=0
      speak(self.items[self.pos])
      self.play_sound(self.click_sound)
     elif event.scancode==kc.K_END:
      self.pos=len(self.items)-1
      speak(self.items[self.pos])
      self.play_sound(self.click_sound)
     elif event.scancode==kc.K_UP or event.scancode==kc.K_LEFT:
      if self.pos>=1:
       self.pos-=1
       speak(self.items[self.pos])
       self.play_sound(self.click_sound)
      else:
       self.play_sound(self.edge_sound)
     elif event.scancode==kc.K_RETURN and self.pos>-1:
      self.play_sound(self.enter_sound)
      return self.subitems[self.pos]
     elif event.scancode==kc.K_ESCAPE: 
      self.play_sound(self.close_sound)
      return ""
     else:
      if v.ctrl==True:
       break
      if event.unicode=="":
       break
      if event.unicode==" " and len(self.search)==0:
       break
      self.cleansearchtimer.restart()
      self.search=self.search+event.unicode
      c=self.pos
      f=0
      for i in self.items:
       if i[0:len(self.search)].lower()==self.search.lower() and self.items.index(i)>=self.pos and self.frash==False or i[0:len(self.search)].lower()==self.search.lower() and self.items.index(i)>self.pos:
        f=1
        c=self.items.index(i)
        break
      if f==0:
       for i in self.items:
        if i[0:len(self.search)].lower()==self.search.lower() and i!=self.items[self.pos]:
         f=1
         c=self.items.index(i)
         break

      if f==1 and c!=self.pos:
       self.pos=c
       self.play_sound(self.click_sound)
       self.frash=False
       speak(self.items[self.pos])

class online_menu(Menu):
 def play_sound(self,name):
  net.send(r"player_sound "+v.name+" "+name+" 0")