import pygame, pygame.locals as pl
pygame.init()
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
import sound_pool
import v
v.get()

def speak(text):
 text=v.vertaal_tekst(text,v.language)
 speatch.output(text)


def dlg(message,playsounds=True):
 import v
 v.get()
 speak(message)
 if playsounds==True:
  v.msp.play_stationary("sounds\popup_open.ogg",False)
 flag=True
 while flag:
  for event in pygame.event.get():
   if event.type==pygame.KEYDOWN:
    if event.key==pl.K_UP or event.key==pl.K_DOWN or event.key==pl.K_LEFT or event.key==pl.K_RIGHT:
      speak(message)
    elif event.key==pl.K_RETURN:
      flag=False
      if playsounds==True:
       v.msp.play_stationary("sounds\popup_close.ogg",False)
