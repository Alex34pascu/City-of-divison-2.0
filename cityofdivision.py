from concurrent.futures import ProcessPoolExecutor
import webbrowser
import translator
import sd
import v
v.get()
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 text=v.vertaal_tekst(text,v.language)
 speatch.output(text)

speak("Loading game. Please wait")
import traceback
import os
import dlg
import pygame, pygame.locals as pl
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("loading City of division, (The fading of trust.")
import simon
import key_constants as kc
import pyperclip as pc
import cProfile
import pstats
import io
profiler = cProfile.Profile()
profiler.enable()
import audio_player
import math
import instance_checker as ins
import slider
import updater
import time
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
import radar
from threading import Thread
import weapons
import weaponmenu
import player
import menus
import time
import net
import threading
from _thread import *
import socket
import virtual_input
from pathlib import Path
import map
import rotation
import timer
import random
import sound_pool
pygame.display.set_caption("City of division, (The fading of trust. Version "+str(v.version))

import menu

m=menu.Menu()
scopetimer=timer.timer()
zoomtimer=timer.timer()
walktimer=timer.timer()
jumps=3
can_jumptimer=timer.timer()

appdata_path = os.getenv('APPDATA')
subfolder_path = os.path.join(appdata_path, 'firegaming', 'city of division')
settings_file = os.path.join(subfolder_path, 'temp_settings.dat')
settings_file2 = os.path.join(subfolder_path, 'settings.dat')
if not os.path.exists(subfolder_path):
 os.makedirs(subfolder_path)
from Cryptodome.Cipher import AES
key = b"1001001001001001"

def decrypt_file(input_file, output_file, key):
    chunk_size = 64 * 1024  
    cipher = AES.new(key, AES.MODE_ECB)
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        while True:
            chunk = infile.read(chunk_size)
            if len(chunk) == 0:
                break
            outfile.write(cipher.decrypt(chunk))

def encrypt_file(input_file, output_file, key):
    chunk_size = 64 * 1024  
    cipher = AES.new(key, AES.MODE_ECB)
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        while True:
            chunk = infile.read(chunk_size)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += b' ' * (16 - len(chunk) % 16)  
            outfile.write(cipher.encrypt(chunk))



def save_data():
  sd.save("name",v.name,settings_file)
  sd.save("pass",v.password,settings_file)
  sd.save("language",v.language,settings_file)
  sd.save("musicvolume",v.musicvolume,settings_file)
  sd.save("speak_cap",v.speak_cap,settings_file)
  sd.save("typing_sounds",v.typing_sounds,settings_file)
  sd.save("speak_chars",v.speak_chars,settings_file)
  sd.save("right_ctrl",v.right_ctrl,settings_file)
  sd.save("allow_wait",v.allow_wait,settings_file)
  sd.save("allow_log_buffers",v.allow_log_buffers,settings_file)
  sd.save("precize_turning",v.precize_turning,settings_file)
  sd.save("askexit",v.askexit,settings_file)
  sd.save("rules",v.rules,settings_file)
  sd.save("shiftexit",v.shiftexit,settings_file)
  sd.save("radartime",v.radartime,settings_file)
  sd.save("volume",v.get_master_volume(),settings_file)
  for b in v.buffers:
   sd.save(b.name+"muted",b.muted,settings_file)
  encrypt_file(settings_file,settings_file2,key)
  if os.path.exists(settings_file):
   os.remove(settings_file)

def read_data():
 try:
  decrypt_file(settings_file2,settings_file,key)
 except:
  pass
 v.name=sd.get("name",settings_file,"")
 v.password=sd.get("pass",settings_file,"")
 v.allow_wait=sd.get("allow_wait",settings_file,"")
 v.language=sd.get("language",settings_file,"")
 v.t=translator.translator(v.language,r"languages\\"+v.language+".txt")
 v.musicvolume=sd.get("musicvolume",settings_file,-15)
 v.speak_cap=sd.get("speak_cap",settings_file,1)
 v.speak_chars=sd.get("speak_chars",settings_file,1)
 v.right_ctrl=sd.get("right_ctrl",settings_file,1)
 v.typing_sounds=sd.get("typing_sounds",settings_file,1)
 v.askexit=sd.get("askexit",settings_file,1)
 v.rules=sd.get("rules",settings_file,0)
 v.precize_turning=sd.get("precize_turning",settings_file,True)
 v.allow_log_buffers=sd.get("allow_log_buffers",settings_file,1)
 v.shiftexit=sd.get("shiftexit",settings_file,0)
 v.radartime=sd.get("radartime",settings_file,190)
 v.set_master_volume(sd.get("volume",settings_file,1.0))
 for b in v.buffers:
  b.muted=sd.get(b.name+"muted",settings_file,False)
 if os.path.exists(settings_file):
  os.remove(settings_file)



locationtimer=timer.timer()
volumetimer=timer.timer()
radartimer=timer.timer()
radardir=0
turntimer=timer.timer()
turn_soundtimer=timer.timer()
def notify_direction(facing):
  if facing in rotation.directions:
    speak(rotation.directions[facing])
    v.sp.play_stationary(r"sounds\\turn_indicator.ogg")
          
def play_turn_sound():
  if turn_soundtimer.elapsed()>320:
    turn_soundtimer.restart()
    net.send(r"player_sound "+v.name+" sounds\\turn"+str(random.randint(1,5))+".ogg 0")

def update_turn(facing):
  play_turn_sound()
  notify_direction(facing)

def game():
 v.start_game=False
 v.lobby=False
 exittimer=timer.timer()
 net.send("set_name "+v.name)
 net.send("object_mapdata")
 lobbytimer=timer.timer()
 v.players={}
 player.shooting_players=[]
 v.sp.pan_step=8.5
 v.sp.volume_step=0.85
 global radardir
 global jumps
 flag=True
 v.can_fire=True
 while flag:
  net.mainloop()
  if v.c4_use==True and v.stunned==False:
   v.c4_use=False
   s=slider.slider(20,120,"Set the time for the C4 detonation. Press f1 for help")
   s.player_sound=True
   s.name="c4timer"
   r=s.run(True,-1,6,"time")
   if r==-1:
    speak("canceled")
    net.send(r"player_sound "+v.name+" sounds\\c4remove.ogg 0")
   else:
    speak("c4 detonation time set to "+str(r)+" seconds")
    net.send("spawn_c4 "+str(r))
  if v.infrared_scanner_timer.elapsed()>=v.infrared_scanner_time and v.infraredscanner==False:
   v.infraredscanner=True
   net.send(r"player_sound "+v.name+" sounds\\infrared_scannerinterferencestop.ogg 0")

  if v.exiting==True and exittimer.elapsed()>2000:
   v.mainmenu=True
  if v.mainmenu==True:
   v.mainmenu=False
   flag=False
  if radardir!=0 and radartimer.elapsed()>v.radartime:
   radartimer.restart()
   if radardir==1:
    radar.spawn_radar(v.x,v.y,v.z,v.facing,0)
   if radardir==2:
    radar.spawn_radar(v.x,v.y,v.z,v.facing+90,0)
   if radardir==3:
    radar.spawn_radar(v.x,v.y,v.z,v.facing+180,0)
   if radardir==4:
    radar.spawn_radar(v.x,v.y,v.z,v.facing+270,0)
   if radardir==5:
    radar.spawn_radar(v.x,v.y,v.z,v.facing+270,1)
   if radardir==6:
    radar.spawn_radar(v.x,v.y,v.z,v.facing+270,-1)
  if v.reconnecting==True:
   reconnect()
  if v.dieing==True:
   net.send("stop_shooting")
   death()
  if locationtimer.elapsed()>1027:
   locationtimer.restart()
   if v.track_thing=="location":
    index=map.get_locations_index(v.tracked)
   elif v.track_thing=="corpse":
    index=map.get_objects_index(v.tracked)
   else:
    index=-1
   if index>-1:
    if v.track_thing=="location":
     v.msp.play_3d("sounds\location.ogg",v.x,v.y,v.z,map.locations[index].x,map.locations[index].y,map.locations[index].z)
    if v.track_thing=="corpse":
     v.msp.play_3d("sounds\location.ogg",v.x,v.y,v.z,math.floor((map.objects[index].minx+map.objects[index].maxx)/2),math.floor((map.objects[index].miny+map.objects[index].maxy)/2),math.floor((map.objects[index].minz+map.objects[index].maxz)/2))

  if v.track_thing=="location":
   index=map.get_locations_index(v.tracked)
   if index>-1:
    if round(v.x)==map.locations[index].x and round(v.y)==map.locations[index].y and round(v.z)==map.locations[index].z:
     v.tracked=-1
     speak("location found!")
     v.msp.play_stationary("sounds\locationfind.ogg")
  if v.track_thing=="corpse":
   index=map.get_objects_index(v.tracked)
   if index>-1:
    if round(v.x)==math.floor((map.objects[index].minx+map.objects[index].maxx)/2) and round(v.y)==math.floor((map.objects[index].miny+map.objects[index].maxy)/2) and round(v.z)==math.floor((map.objects[index].minz+map.objects[index].maxz)/2):
     v.tracked=-1
     speak("corpse found!")
     v.msp.play_stationary("sounds\locationfind.ogg")
  max_jumps=3
  try:
   if v.skill_data["jump endurance"]["active"]==True:
    max_jumps+=v.skill_data["jump endurance"]["level"]
  except:
   pass
  if jumps<=max_jumps and can_jumptimer.elapsed()>=3000:
   can_jumptimer.restart()
   jumps+=1
  keys = pygame.key.get_pressed()
  if keys[pygame.K_e] and turntimer.elapsed()>5 and v.shift == v.precize_turning and v.scopedistance==0 and v.stunned==False:
    turntimer.restart()
    v.facing+=1
    if v.facing>=360:
      v.facing=0
    update_turn(v.facing)
  if keys[pygame.K_q] and turntimer.elapsed()>5 and v.shift == v.precize_turning and v.scopedistance==0 and v.stunned==False:
    turntimer.restart()
    v.facing-=1
    if v.facing <0:
      v.facing=359
    update_turn(v.facing)
      

  if v.server_menu_responce==True:
   walktimer.restart()
   v.firetimer.restart()
  else:
   if v.scoping==True and v.scope_viewing==True:
    if keys[pygame.K_UP] and v.scopedistance<v.max_scopedistance and walktimer.elapsed()>=20:
     walktimer.restart()
     if v.updown>=-1 and v.updown<=1:
      nx,ny=rotation.move(v.lx,v.ly,v.facing)
     else:
      nx,ny=v.lx,v.ly
     if v.updown>0:
      nz=v.lz+1
     elif v.updown<0:
      nz=v.lz-1
     elif v.updown==0:
      nz=v.z
     w=1
     wall=map.get_platform(nx,ny,nz)
     if wall=="wall":
      w=0
     if map.get_wall(nx,ny,nz)=="wallglass":
      w=1
     if w==1:
      if zoomtimer.elapsed()>700:
       zoomtimer.restart()
       net.send(r"player_sound "+v.name+" sounds\\scopezoom"+str(random.randint(1,3))+ ".ogg 0")
      v.scopedistance+=1
    if keys[pygame.K_DOWN] and v.scopedistance>0 and walktimer.elapsed()>=20:
     walktimer.restart()
     if v.updown>=-1 and v.updown<=1:
      nx,ny=rotation.move(v.lx,v.ly,v.facing+180)
     else:
      nx,ny=v.lx,v.ly
     if v.updown>0:
      nz=v.lz-1
     elif v.updown<0:
      nz=v.lz+1
     elif v.updown==0:
      nz=v.lz
     w=1
     wall=map.get_platform(nx,ny,nz)
     if wall=="wall":
      w=0
     if map.get_wall(nx,ny,nz)=="wallglass":
      w=1
     if w==1:
      if zoomtimer.elapsed()>700:
       zoomtimer.restart()
       net.send(r"player_sound "+v.name+" sounds\\scopezoom"+str(random.randint(1,3))+ ".ogg 0")
      v.scopedistance-=1
   climb_time=120
   try:
    if v.skill_data["Learn how to climb"]["active"]==True:
     min=v.skill_data["Learn how to climb"]["level"]*20
     climb_time-=min
   except:
    pass
   if keys[pygame.K_PAGEUP] and walktimer.elapsed()>=v.walktime+climb_time and map.get_platform(v.x,v.y,v.z+1)!="blank" and map.get_platform(v.x,v.y,v.z+1)!="" and v.jumping==False and v.shift==False and v.alt==False and v.stunned==False and v.heavy_weapon==False and v.scoping==False:
    walktimer.restart()
    w=map.get_wall(v.x,v.y,v.z+1)
    if w!="":
     net.send(r"player_sound "+v.name+" sounds\\"+w+".ogg 0")
    else:
     v.z+=1
     net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\"+map.get_platform(v.x,v.y,v.z)+"step"+str(random.randint(1,5))+".ogg 0|n|player_sound "+v.name+" sounds\\sub"+map.get_sub_tile(v.x,v.y,v.z)+"step"+str(random.randint(1,8))+".ogg 0")
   if keys[pygame.K_PAGEDOWN] and walktimer.elapsed()>=v.walktime+climb_time-20 and map.get_platform(v.x,v.y,v.z-1)!="" and map.get_platform(v.x,v.y,v.z-1)!="blank" and v.jumping==False and v.shift==False and v.alt==False and v.stunned==False and v.heavy_weapon==False and v.scoping==False:
    walktimer.restart()
    w=map.get_wall(v.x,v.y,v.z-1)
    if w!="":
     net.send(r"player_sound "+v.name+" sounds\\"+w+".ogg 0")
    else:
     v.z-=1
     net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\"+map.get_platform(v.x,v.y,v.z)+"step"+str(random.randint(1,5))+".ogg 0|n|player_sound "+v.name+" sounds\\sub"+map.get_sub_tile(v.x,v.y,v.z)+"step"+str(random.randint(1,8))+".ogg 0")
   if keys[pygame.K_UP] and walktimer.elapsed()>=v.walktime and v.shift==False  and v.alt==False and v.stunned==False and v.heavy_weapon==False and v.scoping==False:
    walktimer.restart()
    cx,cy=rotation.move(v.x,v.y,v.facing)
    cz=v.z
    c=map.get_staircase(v.x,v.y,v.z)
    if c!=-1:
     v.steptimer.restart()
     if map.get_platform(cx,cy,v.z)=="blank" and map.get_staircase(cx,cy,v.z)!=-1 or map.get_platform(cx,cy,v.z)=="" and map.get_staircase(cx,cy,v.z)!=-1 and v.jumping==False and v.falling==False:
      if v.jumping==False and v.falling==False:
       net.send(r"player_sound "+v.name+" sounds\\stairmove"+str(random.randint(1,5))+".ogg 0")
       v.step=True
       v.steptime=75
       cz-=1
     if map.get_platform(cx,cy,v.z)=="wall" and map.get_staircase(cx,cy,v.z)!=-1 and map.get_platform(v.x,v.y,v.z+1)!="wall" and map.get_platform(cx,cy,v.z+1)!="wall" and v.jumping==False and v.falling==False:
      if v.jumping==False and v.falling==False:
       net.send(r"player_sound "+v.name+" sounds\\stairmove"+str(random.randint(1,5))+".ogg 0")
       v.step=True
       v.steptime=100
       cz+=1
    w=map.get_wall(cx,cy,cz)
    if w!="":
     v.step=False
     net.send(r"player_sound "+v.name+" sounds\\"+w+".ogg 0")
    else:
     v.x,v.y=rotation.move(v.x,v.y,v.facing)
     v.z=cz
     if v.step==False:
      net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\"+map.get_platform(v.x,v.y,v.z)+"step"+str(random.randint(1,5))+".ogg 0|n|player_sound "+v.name+" sounds\\sub"+map.get_sub_tile(v.x,v.y,v.z)+"step"+str(random.randint(1,8))+".ogg 0")
     else:
      net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z))

   if keys[pygame.K_RIGHT] and walktimer.elapsed()>=v.walktime and v.shift==False  and v.alt==False and v.stunned==False and v.heavy_weapon==False and v.scoping==False:
    walktimer.restart()
    cx,cy=rotation.move(v.x,v.y,v.facing+90)
    cz=v.z
    c=map.get_staircase(v.x,v.y,v.z)
    if c!=-1:
     v.steptimer.restart()
     if map.get_platform(cx,cy,v.z)=="wall" and map.get_staircase(cx,cy,v.z)!=-1 and map.get_platform(v.x,v.y,v.z+1)!="wall" and map.get_platform(cx,cy,v.z+1)!="wall" and v.jumping==False and v.falling==False:
      if v.jumping==False and v.falling==False:
       net.send(r"player_sound "+v.name+" sounds\\stairmove"+str(random.randint(1,5))+".ogg 0")
       v.step=True
       v.steptime=100
       cz+=1
     if map.get_platform(cx,cy,v.z)=="blank" and map.get_staircase(cx,cy,v.z)!=-1 or map.get_platform(cx,cy,v.z)=="" and map.get_staircase(cx,cy,v.z)!=-1 and v.jumping==False and v.falling==False:
      if v.jumping==False and v.falling==False:
       net.send(r"player_sound "+v.name+" sounds\\stairmove"+str(random.randint(1,5))+".ogg 0")
       v.step=True
       v.steptime=75
       cz-=1

    w=map.get_wall(cx,cy,cz)
    if w!="":
     v.step=False
     net.send(r"player_sound "+v.name+" sounds\\"+w+".ogg 0")
    else:
     v.x,v.y=rotation.move(v.x,v.y,v.facing+90)
     v.z=cz
     if v.step==False:
      net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\"+map.get_platform(v.x,v.y,v.z)+"step"+str(random.randint(1,5))+".ogg 0|n|player_sound "+v.name+" sounds\\sub"+map.get_sub_tile(v.x,v.y,v.z)+"step"+str(random.randint(1,8))+".ogg 0")
     else:
      net.send("move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z))
   if keys[pygame.K_DOWN] and walktimer.elapsed()>=v.walktime and v.shift==False  and v.alt==False and v.stunned==False and v.heavy_weapon==False and v.scoping==False:
    walktimer.restart()
    cx,cy=rotation.move(v.x,v.y,v.facing+180)
    cz=v.z
    c=map.get_staircase(v.x,v.y,v.z)
    if c!=-1:
     v.steptimer.restart()
     if map.get_platform(cx,cy,v.z)=="wall" and map.get_staircase(cx,cy,v.z)!=-1 and map.get_platform(v.x,v.y,v.z+1)!="wall" and map.get_platform(cx,cy,v.z+1)!="wall" and v.jumping==False and v.falling==False:
      if v.jumping==False and v.falling==False:
       net.send(r"player_sound "+v.name+" sounds\\stairmove"+str(random.randint(1,5))+".ogg 0")
       v.step=True
       v.steptime=100
       cz+=1
     if map.get_platform(cx,cy,v.z)=="blank" and map.get_staircase(cx,cy,v.z)!=-1 or map.get_platform(cx,cy,v.z)=="" and map.get_staircase(cx,cy,v.z)!=-1 and v.jumping==False and v.falling==False:
      if v.jumping==False and v.falling==False:
       net.send(r"player_sound "+v.name+" sounds\\stairmove"+str(random.randint(1,5))+".ogg 0")
       v.step=True
       v.steptime=75
       cz-=1
    w=map.get_wall(cx,cy,cz)
    if w!="":
     v.step=False
     net.send(r"player_sound "+v.name+" sounds\\"+w+".ogg 0")
    else:
     v.x,v.y=rotation.move(v.x,v.y,v.facing+180)
     v.z=cz
     if v.step==False:
      net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\"+map.get_platform(v.x,v.y,v.z)+"step"+str(random.randint(1,5))+".ogg 0|n|player_sound "+v.name+" sounds\\sub"+map.get_sub_tile(v.x,v.y,v.z)+"step"+str(random.randint(1,8))+".ogg 0")
     else:
      net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z))
   w=weapons.weapon(v.current_weapon)
   if v.ctrl==False:
    v.can_fire=True
    if v.firing==True:
     net.send("stop_shooting")
     v.firing=False
   if v.ctrl==True and v.alt==False and v.current_weapon!="" and v.current_weapon!="nothing":
    if v.right_ctrl==1 or v.right_ctrl==0 and not keys[pygame.K_RCTRL] and keys[pygame.K_LCTRL]:
     w=weapons.weapon(v.current_weapon)
     if v.rapid_fire==True and v.skill_data["rapid fire"]["active"]==True and v.current_weapon in v.sorts[1]:
      w.firetime=(w.firetime*0.75)
     if v.stunned==False and v.can_fire==True and v.firetimer.elapsed()>w.firetime:
       v.firetimer.restart()
       net.send("facing "+str(v.facing)+"|n|start_shooting|n|shoot")
       v.firing=True
       v.can_fire=w.automatic
   if keys[pygame.K_LEFT] and walktimer.elapsed()>=v.walktime and v.shift==False  and v.alt==False and v.stunned==False and v.heavy_weapon==False and v.scoping==False:
    walktimer.restart()
    cx,cy=rotation.move(v.x,v.y,v.facing+270)
    cz=v.z
    c=map.get_staircase(v.x,v.y,v.z)
    if c!=-1:
     v.steptimer.restart()
     if map.get_platform(cx,cy,v.z)=="wall" and map.get_staircase(cx,cy,v.z)!=-1 and map.get_platform(v.x,v.y,v.z+1)!="wall" and map.get_platform(cx,cy,v.z+1)!="wall" and v.jumping==False and v.falling==False:
      if v.jumping==False and v.falling==False:
       net.send(r"player_sound "+v.name+" sounds\\stairmove"+str(random.randint(1,5))+".ogg 0")
       v.step=True
       v.steptime=100
       cz+=1
     if map.get_platform(cx,cy,v.z)=="blank" and map.get_staircase(cx,cy,v.z)!=-1 or map.get_platform(cx,cy,v.z)=="" and map.get_staircase(cx,cy,v.z)!=-1 and v.jumping==False and v.falling==False:
      if v.jumping==False and v.falling==False:
       net.send(r"player_sound "+v.name+" sounds\\stairmove"+str(random.randint(1,5))+".ogg 0")
       v.step=True
       v.steptime=75
       cz-=1

    w=map.get_wall(cx,cy,cz)
    if w!="":
     v.step=False
     net.send(r"player_sound "+v.name+" sounds\\"+w+".ogg 0")
    else:
     v.x,v.y=rotation.move(v.x,v.y,v.facing+270)
     v.z=cz
     if v.step==False:
      net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\"+map.get_platform(v.x,v.y,v.z)+"step"+str(random.randint(1,5))+".ogg 0|n|player_sound "+v.name+" sounds\\sub"+map.get_sub_tile(v.x,v.y,v.z)+"step"+str(random.randint(1,8))+".ogg 0")
     else:
      net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z))

  for event in pygame.event.get():
   if v.server_menu_responce==True:
    pygame.event.clear()
   if event.type==pygame.KEYDOWN and v.server_menu_responce==False:
    if event.unicode == '\b' and v.shift==False:
     if v.buffers[v.bufferpos].name=="chats":
      if len(v.buffers[v.bufferpos].items)>0:
       words=v.buffers[v.bufferpos].items[v.buffers[1].pos].split(" ")
       f=words[1]
       if f=="answered":
         f=words[0]
       v.new_sm=1
       v.first_sm=""
       net.send("player_info "+f)
      else:
       speak("there are no chats in this buffer")
     else:
      speak("navigate to the chats buffer to use this function")
    if(event.unicode == '\b') and v.shift==True:
     if v.buffers[v.bufferpos].name=="chats":
      if len(v.buffers[v.bufferpos].items)>0:
       words=v.buffers[v.bufferpos].items[v.buffers[1].pos].split(" ")
       f=words[1]
       if f=="answered":
         speak("can't reply to a reply")
         continue
       reply=virtual_input.input("type your responce to "+f,True)
       if reply!="":
        message=v.name+" answered to "+f+": "+reply+". Quoted message: "+v.buffers[1].items[v.buffers[1].pos].replace(words[0]+" says:","")
        net.send("chat_reply "+message)
      else:
       speak("there are no chats in this buffer")
     else:
      speak("navigate to the chats buffer to use this function")
    elif event.scancode==kc.K_END: 
     v.change_master_volume(0)
     v.msp.play_stationary(r"sounds\\mastervolume.ogg")
    if event.scancode==kc.K_HOME:
     v.change_master_volume(1)
     v.msp.play_stationary(r"sounds\\mastervolume.ogg")
    if v.scoping==True:
     if event.scancode==kc.K_LEFT and v.scope_viewing==False and v.alt==False and v.shift==False:
      net.send(r"player_sound "+v.name+" sounds\\lookscope.ogg 0")
      speak("looking through the scope.")
      map.demper_zoneloop(v.x,v.y,v.z)
      v.scope_viewing=True
     if event.scancode==kc.K_RIGHT and v.scope_viewing==True and v.alt==False and v.shift==False:
      net.send(r"player_sound "+v.name+" sounds\\lookenvironment.ogg 0")
      speak("looking by your self.")
      map.demper_zoneloop(v.x,v.y,v.z)
      v.scope_viewing=False

     if event.scancode==kc.K_d and v.shift==True:
      percent=v.scopedistance/v.max_scopedistance
      percent=percent*100
      speak(str(round(percent))+"% zoomed in with your scope. your scope is focussed on "+str(round(v.lx))+", "+str(round(v.ly))+", "+str(round(v.lz)))
    if event.scancode==kc.K_i and v.alt==True:
     net.send("belt_information")
    if event.scancode==kc.K_s and v.alt==True:
     v.new_sm=1
     v.first_sm=""
     net.send("belt_store")
    if event.scancode==kc.K_1 and v.alt==True:
     net.send("belt_category_move 0")
    if event.scancode==kc.K_2 and v.alt==True:
     net.send("belt_category_move 1")
    if event.scancode==kc.K_3 and v.alt==True:
     net.send("belt_category_move 2")
    if event.scancode==kc.K_4 and v.alt==True:
     net.send("belt_category_move 3")
    if event.scancode==kc.K_5 and v.alt==True:
     net.send("belt_category_move 4")

    if event.scancode==kc.K_g and v.alt==True:
     v.new_sm=1
     v.first_sm=""
     net.send("belt_give")

    if event.scancode==kc.K_LEFT and v.alt==True:
     net.send("belt_move 0")
    if event.scancode==kc.K_RIGHT and v.alt==True:
     net.send("belt_move 1")
    if event.scancode==kc.K_RETURN and v.shift==True and v.stunned==False:
     v.new_sm=1
     v.first_sm=""
     net.send("push_object")
    if event.scancode==kc.K_RETURN and v.shift==False and v.stunned==False and v.ctrl==False:
     v.new_sm=1
     v.first_sm=""
     net.send("use_item")
    if event.scancode==kc.K_UP and v.shift==True:
     if radardir==1:
      radardir=0
      speak("radar disabled")
     else:
      radardir=1
      speak("radar forward")
    if event.scancode==kc.K_RIGHT and v.shift==True:
     if radardir==2:
      radardir=0
      speak("radar disabled")
     else:
      radardir=2
      speak("radar right")
    if event.scancode==kc.K_DOWN and v.shift==True:
     if radardir==3:
      radardir=0
      speak("radar disabled")
     else:
      radardir=3
      speak("radar backward")
    if event.scancode==kc.K_LEFT and v.shift==True:
     if radardir==4:
      radardir=0
      speak("radar disabled")
     else:
      radardir=4
      speak("radar left")
    if event.scancode==kc.K_PAGEUP and v.shift==True:
     if radardir==5:
      radardir=0
      speak("radar disabled")
     else:
      radardir=5
      speak("radar upward")
    if event.scancode==kc.K_PAGEDOWN and v.shift==True:
     if radardir==6:
      radardir=0
      speak("radar disabled")
     else:
      radardir=6
      speak("radar downward")
    if event.scancode==kc.K_SPACE and v.jumping==False and v.falling==False and v.stunned==False and v.heavy_weapon==False and v.scoping==False and map.get_platform(v.x,v.y,v.z+1)!="wall" and v.current_weapon!="SVD_Dragunov" and v.current_weapon!="hk_mg4" and v.current_weapon!="AR10":
     if jumps>1:
      can_jumptimer.restart()
      jumps-=1
      if v.get_tile_type(map.get_platform(v.x,v.y,v.z),["water"])!="water":
       net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\jump"+str(random.randint(1,3))+".ogg 0|n|player_sound "+v.name+" sounds\\"+v.get_tile_type(map.get_platform(v.x,v.y,v.z),["water","grass","gravel","dirt"])+"jump.ogg 0")
      else:
       net.send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\"+v.get_tile_type(map.get_platform(v.x,v.y,v.z),["water","grass","gravel","dirt"])+"jump.ogg 0")
        
      v.jumping=True
     else:
      speak("you can't jump right now. Wait "+str(round((3000-can_jumptimer.elapsed())/1000))+" seconds.")
    if event.scancode==kc.K_ESCAPE and v.shiftexit==False or event.scancode==kc.K_ESCAPE and v.shift==True and v.shiftexit==1:
     if lobbytimer.elapsed()<15000:
      speak("you can't go back to the lobby immediately")
      continue
     if v.askexit==1:
      q=menus.yesno("Do you really want to leave the map and return to the lobby?")
      if q==1:
       net.send("disconnect_check")
       v.which_menu="lobby"
       exittimer.restart()
       v.exiting=True
     else:
      net.send("disconnect_check")
      v.which_menu="lobby"
      exittimer.restart()
      v.exiting=True

    elif event.scancode==kc.K_BACKQUOTE:
     if v.alt==True:
      v.firetimer.restart()
      net.send("holster_put "+v.current_weapon)
     elif v.shift==True:
      net.send("holster_information")
     else:
      net.send("holster_take")
    elif event.scancode==kc.K_F1 and v.pinging==False:
     v.msp.play_stationary("sounds\ping.ogg")
     v.pingtimer.restart()
     v.pinging=True
     net.send("ping")
    elif event.scancode==kc.K_F2:
     if v.shift==False:
      v.new_sm=1
      v.first_sm="player_menu"
      net.send("player_menu")
     else:
      net.send("who_on_my_map")
    elif event.scancode==kc.K_F4:
     v.new_sm=1
     v.first_sm="server_menu"
     v.new_sm=1
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
    elif event.scancode==kc.K_SLASH and v.shift==True:
     v.new_sm=1
     v.first_sm=""
     net.send("staff_chat")
    elif event.scancode==kc.K_y:
     v.new_sm=1
     v.first_sm=""
     net.send("team_chat")

    elif event.scancode==kc.K_SLASH and v.shift==False:
     message=virtual_input.input("type your message here. Press enter when you're done.")
     if message!="":
      if v.messages>0:
       v.messages-=1
       net.send("chat "+message)
      else:
       speak("you can't send a chat at the moment. Please wait a bit.")
    elif event.scancode==kc.K_l:
     if len(map.locations)>0:
      menus.locationsmenu()
     else:
      speak("there are no locations to track")
    elif event.scancode==kc.K_n and v.shift==False:
     if v.tracked==-1:
      speak("you haven't tracked anything")
     else:
      if v.track_thing=="location":
       index=map.get_locations_index(v.tracked)
       if index>-1:
        speak(map.locations[index].get_instructions(v.x,v.y,v.z))
       else:
        speak("location can't be found.")
      if v.track_thing=="corpse":
       index=map.get_objects_index(v.tracked)
       if index>-1:
        speak(map.objects[index].get_instructions(v.x,v.y,v.z))
       else:
        speak("corpse can't be found.")
    elif event.scancode==kc.K_n and v.shift==True:
     if v.track_thing=="location":
      index=map.get_locations_index(v.tracked)
      if index>-1:
       speak("stopt tracking "+map.locations[index].name)
       v.tracked=-1
       v.track_thing=""
      else:
       speak(v.track_thing+" can't be found.")
     elif v.track_thing=="corpse":
      index=map.get_objects_index(v.tracked)
      if index>-1:
       speak("stopt tracking "+map.objects[index].name)
       v.tracked=-1
       v.track_thing=""
      else:
       speak(v.track_thing+" can't be found.")
     else:
      speak("you haven't tracked anything")
    elif event.scancode==kc.K_c and v.shift==False:
     speak(str(round(v.x))+",  "+str(round(v.y))+",  "+str(round(v.z)))
    elif event.scancode==kc.K_c and v.shift==True:
     corpse_list=[]
     for c in map.objects:
      if c.name[0:6]=="corpse" and map.get_3d_distance(v.x,v.y,v.z,(c.minx+c.maxx)/2,(c.miny+c.maxy)/2,(c.minz+c.maxz)/2)<=30:
       corpse_list.append(c.id)
     if len(corpse_list)==0:
      speak("there are no corpses around you")
     else:
      menus.corpses_menu(corpse_list)
    elif event.scancode==kc.K_a:
     net.send("check_ammo")
    elif event.scancode==kc.K_r and v.stunned==False and v.ctrl==False:
     if v.shift==False:
      net.send("reload")
     else:
      net.send("unload")

    elif event.scancode==kc.K_d and v.shift==False and scopetimer.elapsed()>1000:
     if v.scoping==False:
      net.send("start_scoping")
     else:
      scopetimer.restart()
      v.scoping=False
      v.scope_viewing=False
      v.scopedistance=0
      v.max_scopedistance=0
      speak("you stop looking through the scope of your "+v.current_weapon)
      map.demper_zoneloop(v.x,v.y,v.z)
      net.send(r"player_sound "+v.name+" sounds\\scopelookstop.ogg 0")
    elif event.scancode==kc.K_b:
     speak("current location: "+map.get_zone(v.x,v.y,v.z))
    elif event.scancode==kc.K_p:
     """
     profiler.disable()
     result_buffer = io.StringIO()
     stats = pstats.Stats(profiler, stream=result_buffer)
     stats.sort_stats(pstats.SortKey.TIME)
     stats.print_stats()
     profile_results = result_buffer.getvalue()
     if profile_results.strip():
      pc.copy(profile_results)
     else:
         print("No profiling data collected.")
     """

     v.objlist=[]
     net.send("builder_menu")
    elif event.scancode==kc.K_TAB and v.ctrl==False:
     weaponmenu.weapon_menu()
    elif event.scancode==kc.K_h:
     net.send("health")
    elif event.scancode==kc.K_w:
     if v.shift==True:
      net.send("scanner_mode")
     else:
      net.send("facing "+str(v.facing)+"|n|scanner "+str(v.scopedistance))
    elif event.scancode==kc.K_BACKSLASH:
     message=virtual_input.input("type your reply to your last private message")
     if message!="":
      net.send("reply "+message)
    elif event.scancode==kc.K_z:
     v.new_sm=1
     v.first_sm="locker_menu"
     net.send("interact")
    elif event.scancode==kc.K_v and v.shift==True:
     speak("your last scan with the infra red scanner found "+str(len(v.infrascanninglist))+" players: "+v.get_list_in_text(v.infrascanninglist))

    elif event.scancode==kc.K_v and v.shift==False:
     if v.infraredscanner==True:
      if v.infrascannerusetimer.elapsed()>4000:
       v.infrascannerusetimer.restart()
       v.msp.play_stationary("sounds\infrared_scannerclick.ogg")
       v.infrascanning=True
       v.infrascannertimer.restart()
       v.infrascanninglist=[]
      else:
       speak("you still need to wait "+str(round((5000-v.infrascannerusetimer.elapsed())/1000))+" seconds to use the infra red scanner")
     else:
      speak("you cannot use your infrared scanner due to some interference.")
    elif event.scancode==kc.K_i and v.alt==False:
     v.new_sm=1
     v.first_sm=""
     net.send("player_info "+v.name)
    elif event.scancode==kc.K_g and v.stunned==False and v.alt==False:
     if v.shift==True:
      net.send("use_skill 2")
     else:
      net.send("use_skill 1")

    elif event.scancode==kc.K_f:
      if v.shift:
        v.precize_turning=  not v.precize_turning
        if v.precize_turning==True:
          speak("snapping without shift keys")
        else:
          speak("snapping with shift keys")
      else:
       l=""
       if v.updown==-2:
        l="straight down"
       if v.updown==-1:
        l="half down"
       if v.updown==0:
        l="straight forward"
       if v.updown==2:
        l="straight up"
       if v.updown==1:
        l="half up"
       speak("facing "+str(rotation.get_dir(v.facing))+" at "+str(v.facing)+" degrees. You are facing "+l)
    if event.scancode==kc.K_s and v.updown<2 and v.scopedistance==0 and v.alt==False and v.shift==False:
     v.updown+=1
     l=""
     if v.updown==-2:
      l="straight down"
     if v.updown==-1:
      l="half down"
     if v.updown==0:
      l="straight forward"
     if v.updown==2:
      l="straight up"
     if v.updown==1:
      l="half up"
     net.send(r"player_sound "+v.name+" sounds\\aim"+str(v.updown)+".ogg 0")
     speak("facing "+l)
     net.send("updown "+str(v.updown))
    if event.scancode==kc.K_x and v.updown>-2 and v.scopedistance==0:
     v.updown-=1
     l=""
     if v.updown==-2:
      l="straight down"
     if v.updown==-1:
      l="half down"
     if v.updown==0:
      l="straight forward"
     if v.updown==2:
      l="straight up"
     if v.updown==1:
      l="half up"
     net.send(r"player_sound "+v.name+" sounds\\aim"+str(v.updown)+".ogg 0")
     speak("facing "+l)
     net.send("updown "+str(v.updown))
    if event.scancode==kc.K_e and v.scopedistance==0 and v.stunned==False and v.shift!=v.precize_turning:
     old_facing=v.facing
     v.facing=rotation.snap_to_closest_angle(v.facing,"right")
     if v.facing == old_facing:
      v.facing+=45
      if v.facing >=360:
       v.facing=0
     net.send("facing "+str(v.facing))
     play_turn_sound()
     speak(rotation.get_dir(v.facing))

    if event.scancode==kc.K_s and v.shift==True and v.scoping==False and v.stunned==False:
     v.facing+=180
     if v.facing>=360:
      v.facing-=360
     net.send("facing "+str(v.facing))
     net.send(r"player_sound "+v.name+" sounds\\turnhalf"+str(random.randint(1,3))+".ogg 0")
     speak(rotation.get_dir(v.facing))
    if event.scancode==kc.K_q and v.scopedistance==0 and v.stunned==False and v.shift!=v.precize_turning:
     old_facing=v.facing
     v.facing=rotation.snap_to_closest_angle(v.facing,"left")
     if v.facing == old_facing:
      v.facing-=45
      if v.facing<0:
       v.facing=315
     net.send("facing "+str(v.facing))
     play_turn_sound()
     speak(rotation.get_dir(v.facing))

 v.sp.destroy_all()
 v.msp.destroy_all()
 v.exiting=False
 if v.which_menu=="mainmenu":
  mainmenu()
 elif v.which_menu=="lobby":
  lobby_loop()
 else:
  mainmenu()

def reconnect():
 wait_time=12
 speak("reconnecting in "+str(wait_time)+" seconds...")
 time.sleep(wait_time)
 net.disconnect()
 c=net.connect()
 if c==True:
  v.reconnecting=False
  lobby_loop()
 else:
  read_data()
  v.reconnecting=False
  mainmenu()




def death():
 for mu in map.musics:
  mu.stop()
 global jumps
 jumps=3
 v.standart_filter=15000
 v.heavy_weapon=False
 v.scopedistance=0
 v.c4_use=False
 v.scoping=False
 v.walktime=180
 v.scope_viewing=False
 v.death=True
 map.pause_all_sources()
 map.pause_all_bounded_sources()
 map.pause_all_ambiences()
 v.dieing=False
 respawntimer=timer.timer()
 respawning=False
 menutimer=timer.timer()
 v.msp.play_stationary("sounds\death.ogg")
 flag=True
 while flag:
  net.mainloop()
  for event in pygame.event.get():
   pass
  if respawntimer.elapsed()>=3300 and respawning==False:
   respawntimer.restart()
  if respawntimer.elapsed()>3100 and respawning==True:
   net.send("start_game|n|respawn")
   v.sorts=[["melee"],["pistols"],["revolvers"],["shotguns"],["sub_machine_guns"],["assault_rifles"],["machine_guns"],["marksman_rifles"],["sniper_rifles"]]
   v.facing=0
   v.updown=0
   map.resume_all_sources()
#   map.resume_all_bounded_sources()
#   map.resume_all_ambiences()
   v.death=False
   flag=False
  if menutimer.elapsed()>4000 and respawning==False:
   m.reset()
   m.edge_sound=".ogg"
   m.click_sound=".ogg"
   m.enter_sound=".ogg"
   m.close_sound=".ogg"
   m.music=""
   m.open_sound=""
   m.add_item("yes")
   m.add_item("no")
   q=m.loop("would you like to respawn?",True)
   if q=="yes":
    respawntimer.restart()
    respawning=True
    v.msp.play_stationary("sounds\spawning.ogg")
   else:
    v.sp.destroy_all()
    v.msp.destroy_all()
    net.send("lobby|n|respawn")
    v.death=False
    lobby_loop()

def mainmenu():
 m.reset()
 if v.name!="":
  m.add_item("log in")
 m.add_item("create an account")
 m.add_item("send a password reset key.")
 m.add_item("enter your password reset key.")
 m.add_item("settings")
 m.add_item("download translations (opens in your web browser)","download translations")
 m.add_item("learn sounds")
 m.add_item("view rules")
 m.add_item("exit")
 m.music="menumusic"
 m.edge_sound="sounds\menuedge.ogg"
 m.click_sound="sounds\menuclick.ogg"
 m.enter_sound="sounds\menuenter.ogg"
 m.close_sound="sounds\menuclose.ogg"
 m.open_sound="sounds\menuopen.ogg"
 item=m.loop("main menu. Select an option with the arrow keys and press enter to select. You could also press escape to exit the game.",False)
 if item=="download translations":
  webbrowser.open("http://fire-gaming.eu/city_of_division/translations.php", new=2)
  mainmenu()
 if item=="learn sounds":
  menus.learn_sounds_menu()
  mainmenu()
 if item=="view rules":
  m.reset()
  for l in v.rules_data:
   m.add_item(l)
  m.loop("view the rules here")
  mainmenu()

 if item=="settings":
  m.mus.stop()
  menus.settings_menu(False)
  save_data()
  mainmenu()
 if item=="create an account":
  read_data()
  new_name=virtual_input.input("type your name here.",False)
  if new_name=="":
   mainmenu()
  else:
   new_password=virtual_input.input("type your password here.",False,"",True)
   if new_password=="":
    mainmenu()
   check_password=virtual_input.input("type your password again.",False,"",True)
   if check_password!=new_password:
    dlg.dlg("error: the second password is not the same as the first password")
    mainmenu()
   if new_name==" " or new_password==" ":
    dlg.dlg("error: the name or password input isn't legal")
    mainmenu()
   dlg.dlg("press enter to connect")
   m.mus.stop()
   new_name=new_name.replace(" ","_")
   new_password=new_password.replace(" ","_")
   v.name=new_name
   v.password=new_password
   save_data()
   c=net.connect("create")
   if c==True:
    net.disconnect()
    dlg.dlg("Your account has been created successfully. You can now press log in in the main menu to start playing.")
   read_data()
   mainmenu()

 if item=="enter your password reset key.":
  m.mus.stop()
  c=net.connect("password reset")
  if c==False:
   read_data()
  mainmenu()

 if item=="send a password reset key.":
  m.mus.stop()
  c=net.connect("password reset key")
  if c==False:
   read_data()
  mainmenu()

 elif item=="log in":
  m.mus.stop()
  c=net.connect()
  if c==True:
   lobby_loop()
  else:
   read_data()
   mainmenu()
 if item=="exit" or item=="":
  time.sleep(1)
  m.mus.stop()
  v.log_buffers()
  save_data()
  exit()

def open_chest():
 current_item=""
 status="opening"
 waittimer=timer.timer()
 layer="chest_layer_normal.ogg"
 if v.chest=="platinum":
  layer="chest_layer_platinum.ogg"
 if v.chest=="diamond":
  layer="chest_layer_diamond.ogg"
 v.msp.play_stationary(r"sounds\\"+layer)
 v.msp.play_stationary(r"sounds\\chestopen.ogg")
 while 1:
  time.sleep(0.001)
  net.mainloop()
  if waittimer.elapsed()>3500 and status=="opening":
   v.msp.play_stationary(r"sounds\\chestopenwoosh.ogg")
   status="reviling"
   break
 for f in v.chest_data:
    waittimer.restart()
    intervaltimer=timer.timer()
    if f!="team_token":
     amount=v.chest_data[f]/5
     if amount>20:
      amount=20
     if amount<1:
      amount=1
     interval=1000/amount
     if interval<49:
      interval=50
     intervaltimer.set(interval)
    else:
     amount=1
     v.msp.play_stationary(r"sounds\\tokenget.ogg")

    i=0
    while i<amount:
     for event in pygame.event.get():
      pass
     if intervaltimer.elapsed()>interval:
      intervaltimer.restart()
      if f!="team_token": 
       v.msp.play_stationary(r"sounds\\skillpointget.ogg")
      i+=1

    m.reset()
    m.pos=0
    m.enter_sound="sounds\chestclick.ogg"
    m.close_sound="sounds\chestclick.ogg"
    m.add_item(f)
    if f!="team_token":
     m.add_item(str(v.chest_data[f])+" skill points.")
    else:
     m.add_item(str(v.chest_data[f])+" tokens.")
    speak(f+"!")
    m.loop(f+"!",True)

 v.chest=""


def match_findingloop():
 endtimer=timer.timer()
 s=sound_pool.sound.sound()
 s.load("sounds\matchsearch.ogg",True)
 s.play_looped()
 speak("finding a match. Press enter to cancel")
 while(1):
  net.mainloop()
  if v.start_game==True:
   return
  if endtimer.elapsed()>60000:
   speak("didn't find any match")
   v.sp.play_stationary("sounds\matchnotfound.ogg")
   net.send("stop_finding_match")
   return
  for event in pygame.event.get():
   if event.type==pygame.KEYDOWN and v.server_menu_responce==False:
    if event.scancode==kc.K_RETURN:
     speak("match_finding_stopped")
     net.send("stop_finding_match")
     return
def lobby_loop():
 musictimer=timer.timer()
 v.players={}
 for mu in map.musics:
  mu.stop()

 mus=menu.music.music("lobbymusic",v.musicvolume)
 net.send("lobby")
 v.lobby=True
 speak("welcome "+v.name+" to the lobby. Press enter to open the lobby menu.")
 flag=True
 while flag:
  net.mainloop()
  if v.dieing==True:
   net.send("stop_shooting")
   death()
  if v.mainmenu==True:
   v.mainmenu=False
   flag=False
  if v.start_match==True:
   v.start_match=False
   match_findingloop()

  if v.chest!="":
   open_chest()
  if v.reconnecting==True:
   mus.stop()
   reconnect()

  if v.start_game==True:
   v.start_game=False
   mus.stop()
   flag=False
   game()
  keys = pygame.key.get_pressed()
  try:
   if keys[pygame.K_PAGEUP] and musictimer.elapsed()>=10 and mus.handle.volume<0:
    musictimer.restart()
    mus.handle.volume+=1
    v.musicvolume+=1
   if keys[pygame.K_PAGEDOWN] and musictimer.elapsed()>=10 and mus.handle.volume>-100:
    musictimer.restart()
    mus.handle.volume-=1
    v.musicvolume-=1
  except:
   pass
  for event in pygame.event.get():
   if v.server_menu_responce==True:
    pass
   if event.type==pygame.KEYDOWN and v.server_menu_responce==False:
    if event.unicode == '\b' and v.shift==False:
     if v.buffers[v.bufferpos].name=="chats":
      if len(v.buffers[v.bufferpos].items)>0:
       words=v.buffers[v.bufferpos].items[v.buffers[1].pos].split(" ")
       f=words[1]
       if f=="answered":
         f=words[0]
       v.new_sm=1
       v.first_sm=""
       net.send("player_info "+f)
      else:
       speak("there are no chats in this buffer")
     else:
      speak("navigate to the chats buffer to use this function")
    if(event.unicode == '\b') and v.shift==True:
     if v.buffers[v.bufferpos].name=="chats":
      if len(v.buffers[v.bufferpos].items)>0:
       words=v.buffers[v.bufferpos].items[v.buffers[1].pos].split(" ")
       f=words[1]
       if f=="answered":
         speak("can't reply to a reply")
         continue
       reply=virtual_input.input("type your responce to "+f,True)
       if reply!="":
        message=v.name+" answered to "+f+": "+reply+". Quoted message: "+v.buffers[1].items[v.buffers[1].pos].replace(words[0]+" says:","")
        net.send("chat_reply "+message)
      else:
       speak("there are no chats in this buffer")
     else:
      speak("navigate to the chats buffer to use this function")
    if event.scancode==kc.K_i and v.alt==False:
     v.new_sm=1
     v.first_sm=""
     net.send("player_info "+v.name)
    if event.scancode==kc.K_ESCAPE and v.shiftexit==False or event.scancode==kc.K_ESCAPE and v.shift==True and v.shiftexit==1:
     if v.askexit==1:
      q=menus.yesno("Do you really want to leave the lobby and return to the main menu?")
      if q==1:
       net.send("disconnect")
       net.disconnect()
       mus.stop()
       mainmenu()
     else:
      net.send("disconnect")
      net.disconnect()
      mus.stop()
      mainmenu()
    elif event.scancode==kc.K_RETURN:
     v.new_sm=1
     v.first_sm="lobby_menu"
     net.send("lobby_menu")

    elif event.scancode==kc.K_END: 
     v.change_master_volume(0)
     v.msp.play_stationary(r"sounds\\mastervolume.ogg")
    if event.scancode==kc.K_HOME:
     v.change_master_volume(1)
     v.msp.play_stationary(r"sounds\\mastervolume.ogg")
    elif event.scancode==kc.K_y:
     v.new_sm=1
     v.first_sm=""
     net.send("team_chat")
    elif event.scancode==kc.K_SLASH and v.shift==True:
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
    elif event.scancode==kc.K_F1 and v.pinging==False:
     v.msp.play_stationary("sounds\ping.ogg")
     v.pingtimer.restart()
     v.pinging=True
     net.send("ping")
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


 mus.stop()
 if v.which_menu=="mainmenu":
  mainmenu()
 elif v.which_menu=="lobby":
  lobby_loop()
 else:
  mainmenu()

#i=ins.InstanceChecker()
#if i.is_running():
# dlg.dlg("error: You are not allowed to run the game twice.")
# exit()



def main():
 speak(" checking for updates..." )
 try:
  updater.check_for_updates("https://fire-gaming.eu/city_of_division/version.txt")
 except Exception as e:
   error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
   dlg.dlg("error: "+error_message)
 read_data()
 if v.language=="":
  menus.language_menu()
 if v.rules==0:
  menus.rules_menu()
 save_data()
 try:
  mainmenu()
 except Exception as e:
   error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
   dlg.dlg("error: "+error_message)



if __name__ == "__main__":
 main()
