import key_constants as kc
import virtual_input
import timer
import sound_pool
import pygame, pygame.locals as pl
from pygame.locals import *
pygame.init()

import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 speatch.output(text)


def audio_player(sound_name,online=True,audio_description=True):
 import menus
 import v
# v.get()
 import music
 music.pause_all_musics()
 set_audio_description=audio_description
 speak("audio player. Press F1 for help")
 volumetimer=timer.timer()
 positiontimer=timer.timer()
 import net
 import v
 paused=False
 s=sound_pool.sound.sound()
 s.load(sound_name,True)
 ads=sound_pool.sound.sound()
 ads.load(sound_name.replace(r"sounds\\",r"sounds\\AD_"),True)
 s.handle.set_link(ads.handle)
 s.play()

 flag=True
 while flag:
  if online==True:
   net.mainloop()
  if s.handle.get_length()==s.handle.get_position():
   paused=True
   s.handle.set_position(s.handle.seconds_to_bytes(0))
   if audio_description==True:
    ads.handle.set_position(s.handle.get_position())

  for event in pygame.event.get():
   if event.type==pygame.KEYDOWN:
    if event.scancode==kc.K_END: 
     v.change_master_volume(0)
     v.msp.play_stationary(r"sounds\\mastervolume.ogg")
    if event.scancode==kc.K_HOME:
     v.change_master_volume(1)
     v.msp.play_stationary(r"sounds\\mastervolume.ogg")
    if online==True:
     if event.scancode==kc.K_SLASH and v.shift==True:
      v.new_sm=1
      v.first_sm=""
      net.send("staff_chat")
     elif event.scancode==kc.K_SLASH and v.shift==False:
      message=virtual_input.input("type your message here. Press enter when you're done.")
      if message!="":
       if v.messages>0:
        v.messages-=1
        net.send("chat "+message)
       else:
        speak("you can't send a chat at the moment. Please wait a bit.")
     elif event.scancode==kc.K_LEFTBRACKET and v.bufferpos>0 and v.shift==False:
      v.bufferpos-=1
      if v.buffers[v.bufferpos].muted==False:
       speak(v.buffers[v.bufferpos].name+": "+str(len(v.buffers[v.bufferpos].items))+" items")
      else:
       speak(v.buffers[v.bufferpos].name+": muted. "+str(len(v.buffers[v.bufferpos].items))+" items")

     elif event.scancode==kc.K_LEFTBRACKET and v.shift==True:
      v.bufferpos=0
      if v.buffers[v.bufferpos].muted==False:
       speak(v.buffers[v.bufferpos].name+": "+str(len(v.buffers[v.bufferpos].items))+" items")
      else:
       speak(v.buffers[v.bufferpos].name+": muted. "+str(len(v.buffers[v.bufferpos].items))+" items")

     elif event.scancode==kc.K_RIGHTBRACKET and v.bufferpos<len(v.buffers)-1 and v.shift==False:
      v.bufferpos+=1
      if v.buffers[v.bufferpos].muted==False:
       speak(v.buffers[v.bufferpos].name+": "+str(len(v.buffers[v.bufferpos].items))+" items")
      else:
       speak(v.buffers[v.bufferpos].name+": muted. "+str(len(v.buffers[v.bufferpos].items))+" items")
     elif event.scancode==kc.K_RIGHTBRACKET and v.shift==True:
      v.bufferpos=len(v.buffers)-1
      if v.buffers[v.bufferpos].muted==False:
       speak(v.buffers[v.bufferpos].name+": "+str(len(v.buffers[v.bufferpos].items))+" items")
      else:
       speak(v.buffers[v.bufferpos].name+": muted. "+str(len(v.buffers[v.bufferpos].items))+" items")
     elif event.scancode==kc.K_COMMA:
      if v.shift==True:
       v.buffers[v.bufferpos].edge(0)
      else:
       v.buffers[v.bufferpos].move(0)
     elif event.scancode==kc.K_PERIOD:
      if v.shift==True:
       v.buffers[v.bufferpos].edge(1)
      else:
       v.buffers[v.bufferpos].move(1)
     elif event.scancode==kc.K_F2:
      v.new_sm=1
      v.first_sm="player_menu"
      net.send("player_menu")
     elif  event.scancode==kc.K_F4:
      v.new_sm=1
      v.first_sm="server_menu"
      net.send("server_menu")
     elif event.scancode==kc.K_F5:
      if v.buffers[v.bufferpos].name=="all" or v.buffers[v.bufferpos].name=="important":
       speak("this buffer can't be muted")
      elif v.buffers[v.bufferpos].muted==False:
       v.buffers[v.bufferpos].muted=True
       speak(v.buffers[v.bufferpos].name+" muted")
      elif v.buffers[v.bufferpos].muted==True:
       v.buffers[v.bufferpos].muted=False
       speak(v.buffers[v.bufferpos].name+" unmuted")

     elif event.scancode==kc.K_F3:
      menus.settings_menu(True)
     elif event.scancode==kc.K_BACKSLASH:
      message=virtual_input.input("type your reply to your last private message")
      if message!="":
       net.send("reply "+message)

    if event.scancode==kc.K_F1:
     comands=["press space to pause or unpause the audio","press the left and right arrow keys to move through the audio file","press the up and down arrow keys to adjust the volume of the audio","press T to see the current position","press V to see the volume"]
     if set_audio_description==True:
      comands.append("Press shift + up and down arrow keys to change the volume of the audio description")
      comands.append("Press tab to enable or disable audio description")
     speak(v.get_list_in_text(comands))
    elif event.scancode==kc.K_ESCAPE:
     flag=False
    elif event.scancode==kc.K_TAB and set_audio_description==True:
     if audio_description==True:
      audio_description=False
      s.handle.remove_link(ads.handle)
      ads.handle.pause()
      speak("audio description off")
     else:
      audio_description=True
      s.handle.set_link(ads.handle)
      ads.handle.set_position(s.handle.get_position())
      if paused==False:
       ads.handle.play()
      speak("audio description on")

    elif event.scancode==kc.K_SPACE:
     if paused==False:
      s.handle.pause()
      paused=True
      speak("paused")
     else:
      try:
       s.handle.play()
      except:
       s.handle.play(True)

      paused=False
      speak("playing")
    elif event.scancode==kc.K_t:
     speak(v.get_time_in_mm(round(s.handle.bytes_to_seconds(s.handle.get_position()))*1000)+" of "+v.get_time_in_mm(round(s.handle.length_in_seconds())*1000))
    elif event.scancode==kc.K_v:
     speak("volume: "+str(s.volume))
  keys = pygame.key.get_pressed()
  try:
   if v.shift==False:
    if keys[pygame.K_UP] and volumetimer.elapsed()>=10 and s.volume<0:
     volumetimer.restart()
     s.volume+=1
    if keys[pygame.K_DOWN] and volumetimer.elapsed()>=10 and s.volume>-100:
     volumetimer.restart()
     s.volume-=1
   else:
    if set_audio_description==True:
     if keys[pygame.K_UP] and volumetimer.elapsed()>=10 and ads.volume<0:
      volumetimer.restart()
      ads.volume+=1
     if keys[pygame.K_DOWN] and volumetimer.elapsed()>=10 and ads.volume>-100:
      volumetimer.restart()
      ads.volume-=1

   if keys[pygame.K_RIGHT] and positiontimer.elapsed()>=50:
    positiontimer.restart()
    try:
     s.handle.set_position(s.handle.seconds_to_bytes(s.handle.bytes_to_seconds(s.handle.get_position())+1))
    except:
     s.handle.set_position(s.handle.seconds_to_bytes(s.handle.length_in_seconds()))
    if audio_description==True:
     ads.handle.set_position(s.handle.get_position())

   if keys[pygame.K_LEFT] and positiontimer.elapsed()>=50:
    positiontimer.restart()
    try:
     s.handle.set_position(s.handle.seconds_to_bytes(s.handle.bytes_to_seconds(s.handle.get_position())-1))
    except:
     s.handle.set_position(s.handle.seconds_to_bytes(0))
    if audio_description==True:
     ads.handle.set_position(s.handle.get_position())
  except:
   pass
 speak("audio player closed")
 music.resume_all_musics()

