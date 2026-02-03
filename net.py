import re
import select
import simon
import traceback
import audio_player
import ast
import slider
import time
import win32gui
script_window = win32gui.GetForegroundWindow()
script_window_title = win32gui.GetWindowText(script_window)
import keyboard
import math
def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)
import rotation
import random
import weapons
import pygame
from pygame.locals import *
pygame.init()

import radar
import pyperclip as pc
import menus
import player
import sound_pool
import map
import v
v.get()
import timer
speedhacktimer=timer.timer()

import virtual_input
import socket
from threading import Thread
import dlg
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 text=v.vertaal_tekst(text,v.language)
 speatch.output(text)

connected=False
import zlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

def compress_data(data):
    """Comprimeert de data met zlib."""
    return zlib.compress(data.encode())

def decompress_data(data):
        decompressed_data = zlib.decompress(data)
        return decompressed_data.decode()  

def aes_cipher(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(text.encode(), AES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return encrypted_text

def aes_decipher(encrypted_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = cipher.decrypt(encrypted_text)
    unpadded_text = unpad(decrypted_text, AES.block_size)
    return unpadded_text.decode()


has_connected=False
def connect_to_server(ip, port):
 global has_connected
 v.name=v.name.replace(" ","")
 v.password=v.password.replace(" ","")
 try:
  v.s.connect((ip, port))
  has_connected=True
 except:
  disconnect()

def connect(thing=""):
 global has_connected
 has_connected=False
 try:
  disconnect()
  v.s.setblocking(1)
  global connected
  connected=False
  if v.name=="" and thing=="" or v.password=="" and thing=="":
   dlg.dlg("you haven't set a name or password for your account. Go to the settings menu to set this up.")
   return
  connected=True
  speak("connecting. Please wait")
  v.s.setblocking(1)
  host="91.232.103.194"
#  host="localhost"

  if v.beta==False:
   thread = Thread(target=connect_to_server, args=(host, 3030))
   thread.start()
  else:
   thread = Thread(target=connect_to_server, args=(host, 3031))
   thread.start()

#95.111.226.105
#26.191.173.221
  flag=True
  connecttimer=timer.timer()
 except Exception as e:
  error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
  dlg.dlg("error: "+error_message)
  connected=False
  return

 while flag:
  try:
#   v.s.getpeername()
   if has_connected==True:
    flag=False
  except Exception as e:
   error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
   dlg.dlg("error: "+error_message)


  if connecttimer.elapsed()>5000:
   dlg.dlg("the server is down")
   disconnect()
   connected=False
   return False
  for event in pygame.event.get():
   if event.type==pygame.KEYDOWN:
    if event.key==pygame.K_ESCAPE:
     disconnect()
     return False
 speak("logging in...")
 try:
  v.s.setblocking(0)
  if thing=="create":
   send("create_account "+v.name+" "+v.password+" "+v.comp_id+" "+v.version)
  elif thing=="password reset":
   key=virtual_input.input("type the key that you've got",False)
   if key=="":
    return
   password=virtual_input.input("type the new password.",False)
   password=password.replace(" ","_")
   if password=="":
    return
   send("password_reset2 "+key+" "+password)

  elif thing=="password reset key":
   name=virtual_input.input("type the name of the account that needs the password reset.",False)
   if name=="":
    return
   send("password_reset "+name)
  else:
   send("connect "+v.name+" "+v.password+" "+v.comp_id+" "+v.version)

  while 1 :
   for event in pygame.event.get():
    if event.type==pygame.KEYDOWN:
     if event.key==pygame.K_ESCAPE:
      disconnect()
      return False
   maindata=""
   maindata=get_pakket()
   if maindata!="":
    if maindata!="":
     maindata=maindata.replace("|end|","")
     bytes_packet = bytes.fromhex(maindata)
     maindata = aes_decipher(bytes_packet, v.packet_key)+"|n|"
#     maindata=decompress_data(bytes.fromhex(maindata))+"|n|"

     lines=maindata.split("|n|")
     for data in lines:
      if data=="":
       continue
      parsed=data.split()
      if len(parsed)<=0:
       continue
      if parsed[0]=="already_exsist":
       dlg.dlg("error: This account already exsists")
       disconnect()
       return False
      elif parsed[0]=="version":
       dlg.dlg("error: your client is out of date")
       disconnect()
       return False
      elif parsed[0]=="beta":
       dlg.dlg("error: only beta_members of the game can loggin to the server at this moment")
       disconnect()
       return False
      elif parsed[0]=="dlg" and len(parsed)>1:
       dlg.dlg(data.replace("dlg ",""))
       disconnect()
       return False

      elif parsed[0]=="developer":
       dlg.dlg("error: only developers of the game can loggin to the server at this moment")
       disconnect()
       return False
      elif parsed[0]=="loggedin":
       return True
      elif parsed[0]=="not_exsist":
       dlg.dlg("this account doesn't exsist")
       disconnect()
       return False
      elif parsed[0]=="banned":
       dlg.dlg("error: you have been banned")
       disconnect()
       return False
      elif parsed[0]=="samename":
       dlg.dlg("error: this name is already logged in.")
       disconnect()
       return False
      elif parsed[0]=="wrong_password":
       disconnect()
       dlg.dlg("error: the password of this player is not correct.")
       return False
 except Exception as e:
  error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
  dlg.dlg("error: "+error_message)

total_data=""
def get_pakket():
 t=""
 global total_data
 maindata=""
 try:
  maindata=""
  maindata=v.s.recv(4)
  if maindata!="":
   i=0
   while i==0:
    old_maindata=maindata
    maindata=maindata+v.s.recv(4096)
    if old_maindata==maindata:
     i=1
 except:
  pass
 if maindata!="":
  if maindata!="":
   maindata=maindata.decode()
 total_data=total_data+maindata
# if total_data.endswith("|end|"):
 if "|end|" in total_data:
  t=total_data[0:total_data.find("|end|")+len("|end|")]
  total_data=total_data.replace(t,"")
  return t
 else:
  return ""

def check_netloop():
 while 1:
  netloop()
def netloop():
 v.msp.reverb=-1
 v.msp.mix=0

 v.s.setblocking(0)
 getting_data=get_pakket()
 if getting_data !="":
  if getting_data != "":
   getting_data=getting_data.replace("|end|","")
   bytes_packet = bytes.fromhex(getting_data)
   getting_data = aes_decipher(bytes_packet, v.packet_key)+"|n|"
#   getting_data=decompress_data(bytes.fromhex(getting_data))+"|n|"
   lines=getting_data.split("|n|")
   for data in lines:
    if data=="":
     continue
    parsed=data.split()
    if parsed[0]=="speedhacked":
     dlg.dlg("speedhacking is not allowed")
     disconnect()
     v.mainmenu=True
    elif parsed[0]=="start_game":
     v.start_game=True
    elif parsed[0]=="restart":
     v.sp.destroy_all()
     v.msp.destroy_all()
     disconnect()
     v.reconnecting=True
    elif parsed[0]=="disconnect":
     v.mainmenu=True
    elif parsed[0]=="go_lobby":
     v.which_menu="lobby"
     v.mainmenu=True

    elif parsed[0]=="kick":
     dlg.dlg("you've been kicked from the server")
     disconnect()
     v.which_menu="mainmenu"
     v.mainmenu=True
     return
    elif parsed[0]=="ban":
     dlg.dlg("you've been banned from the server")
     disconnect()
     v.which_menu="mainmenu"
     v.mainmenu=True
    elif parsed[0]=="code_menu" and len(parsed)>1:
     question=data.replace(parsed[0]+" ","")

     send("server_menu_answer "+question.replace(" ","_")+" "+menus.code_menu(question))

    elif parsed[0]=="start_rapid_fire":
     v.rapid_fire=True
     v.rapid_firetimer.restart()

    elif parsed[0]=="start_sprint":
     v.sprinttimer.restart()
     v.sprint_stage=0
     v.sprinting=True
    elif parsed[0]=="start_match":
     v.start_match=True
    elif parsed[0]=="open_chest" and len(parsed)>2:
     v.chest=parsed[1]
     v.chest_data=ast.literal_eval(data.replace(parsed[0]+" "+parsed[1]+" ",""))
    elif parsed[0]=="disable_infrared_scanner" and len(parsed)>1:
     v.infraredscanner=False
     v.infrared_scanner_timer.restart()
     v.infrared_scanner_time=int(parsed[1])
    elif parsed[0]=="table_menu" and len(parsed)>1:
     menus.table_menu(data.replace("table_menu ",""))

    elif parsed[0]=="play_sound_dlg" and len(parsed)>2:
     play_sound_dlg(parsed[1],int(parsed[2]),True)

    elif parsed[0]=="set_skill_data" and len(parsed)>1:
     v.skill_data=ast.literal_eval(data.replace(parsed[0]+" ",""))
    elif parsed[0]=="delete_server_menu":
     del v.last_sm_name[0]
     del v.last_sm_options[0]
    elif parsed[0]=="last_server_menu":
     v.first_sm_check-=1
     f=v.last_sm_name[0]
     del v.last_sm_name[0]
     del v.last_sm_options[0]
     menus.server_menu(f,["a","b"],True)
    elif parsed[0]=="server_menu_ferify":
     v.server_menu_ferify=True

    elif parsed[0]=="admin_player_menu" and len(parsed)>1:
     menus.admin_menu(parsed[1])
    elif parsed[0]=="server_menu" and len(parsed)>2:
     menus.server_menu(parsed[1],data.replace("server_menu "+parsed[1]+" ",""))
    elif parsed[0]=="phone_menu" and len(parsed)>1:
     menus.online_menu("phone_menu",data.replace("phone_menu ",""),False, click_sound="sounds\phonemenuclick.ogg")
    elif parsed[0]=="tool_box_menu" and len(parsed)>1:
     menus.online_menu("tool_box_menu",data.replace("tool_box_menu ",""),False, open_sound=r"sounds\\toolboxopen.ogg", close_sound=r"sounds\\toolboxclose.ogg", enter_sound=r"sounds\\toolboxclose.ogg")

    elif parsed[0]=="locker_menu" and len(parsed)>1:
     menus.online_menu("locker_menu",data.replace("locker_menu ",""),False, click_sound="sounds\lockermove1.ogg", open_sound="sounds\lockermove2.ogg", close_sound="sounds\lockermove3.ogg")
    elif parsed[0]=="server_mega_menu" and len(parsed)>2:
     menus.server_mega_menu(parsed[1],data.replace("server_mega_menu "+parsed[1]+" ",""))
    elif parsed[0]=="locker_simon" and len(parsed)>1:
     speak("lets do a simon of "+str(parsed[1])+" sounds.")
     s=simon.simon(int(parsed[1]))
     if s==True:
      send("locker_simon_good")
     else:
      speak("fail")
      send(r"player_sound "+v.name+" sounds\\simonfail.ogg 0|n|locker_simon_fail")

    elif parsed[0]=="calculation" and len(parsed)>1:
     f=parsed[1].replace("_"," ")
     text=virtual_input.calculation(f)
     if text!="":
      send("calculation_answer "+parsed[1]+" "+text)
     else:
      send("calculation_answer "+parsed[1]+" -1")

    elif parsed[0]=="audio_player" and len(parsed)>1:
     audio_player.audio_player(r"sounds\\"+parsed[1])

    elif parsed[0]=="input" and len(parsed)>1:
     text=virtual_input.input(parsed[1].replace("_"," "),True,data.replace("input "+parsed[1]+" ",""))
     if text!="":
      send("input_answer "+parsed[1]+" "+text)
      v.closing=1
     else:
      try:
#       if v.last_sm_name[0]!="":
#        if v.closing==0:
#         del v.last_sm_name[0]
#         del v.last_sm_options[0]

        del v.last_sm_name[0]
        del v.last_sm_options[0]
        v.closing=1
        send("server_menu_answer "+v.last_sm_name[0]+" "+v.last_sm_options[0])
      except:
       send(v.first_sm)
       v.first_sm=""

    elif parsed[0]=="builder_menu":
     menus.buildermenu()
    elif parsed[0]=="death" and v.dieing==False:
     v.dieing=True
     v.death=True
    elif parsed[0]=="buffer_sound" and len(parsed)>2 and v.death==False:
         for b in v.buffers:
           if b.name==parsed[1] and b.muted==False:
            v.msp.play_stationary(r"sounds\\"+parsed[2])
    elif parsed[0]=="add_buffer_item" and len(parsed)>1:
     v.add_buffer_item(parsed[1],data.replace("add_buffer_item "+parsed[1]+" ",""))
    elif parsed[0]=="players_check" and len(parsed)>1:
     players=data.replace("players_check ","").split("\n")
     final={}
     for f in v.players:
      p=v.players[f]
      if p.name in players:
       final[f]=p
     v.players=final
    elif parsed[0]=="set_team" and len(parsed)>2:
     index=player.get_player_index(parsed[1])
     if index!="":
      v.players[index].team=parsed[2]
    elif parsed[0]=="spawn_player" and len(parsed)>3 and v.lobby==False:
     player.spawn_player(float(parsed[1]),float(parsed[2]),float(parsed[3]),parsed[4])
    elif parsed[0]=="set_filter" and len(parsed)>1:
     v.standart_filter=int(parsed[1])

#     for i in v.sp.items:
#      i.handle.set_filter(v.standart_filter)
    elif parsed[0]=="remove_object" and len(parsed)>=1:
     o=map.get_objects_index(int(parsed[1]))
     if o!=-1:
      map.remove_object(int(parsed[1]))
    elif parsed[0]=="change_objects_z" and len(parsed)>2:
     index=map.get_objects_index(int(parsed[1]))
     if index!=-1:
      map.objects[index].minz+=int(parsed[2])
      map.objects[index].maxz+=int(parsed[2])
      for p in map.platforms:
       if p.id==int(parsed[1]):
        p.minz+=int(parsed[2])
        p.maxz+=int(parsed[2])
      for p in map.walls:
       if p.id==int(parsed[1]):
        p.minz+=int(parsed[2])
        p.maxz+=int(parsed[2])
      for p in map.zones:
       if p.id==int(parsed[1]):
        p.minz+=int(parsed[2])
        p.maxz+=int(parsed[2])

    elif parsed[0]=="remove_player" and len(parsed)>=1:
     player.remove_player(parsed[1])
    elif parsed[0]=="stun_reset":
     v.stunned=False
    elif parsed[0]=="activate_c4":
     v.c4_use=True
    elif parsed[0]=="stun" and len(parsed)>1:
     v.stunned=True
     v.stuntime=int(parsed[1])
     v.stuntimer.restart()

    elif parsed[0]=="set_objlist" and len(parsed)>1:
     data=data.replace("set_objlist ","")
     v.objlist=data.split("\n")
    elif parsed[0]=="set_itemlist" and len(parsed)>1:
     data=data.replace("set_itemlist ","")
     v.itemlist=data.split("\n")
    elif parsed[0]=="add_object_sound" and len(parsed)>3 and v.death==False:
      index=map.get_objects_index(int(parsed[1]))
      if index>-1:
        map.objects[index].add_sound(parsed[2],int(parsed[3]))
    elif parsed[0]=="remove_object_sound" and len(parsed)>2:
      index=map.get_objects_index(int(parsed[1]))
      if index>-1:
        map.objects[index].remove_sound(parsed[2])

    elif parsed[0]=="set_object_mapdata" and len(parsed)>1 and v.lobby==False:
     o=map.get_objects_index(int(parsed[1]))
     if o!=-1:
      data=data.replace("set_object_mapdata "+parsed[1]+" ","")
      map.objects[o].mapdata=data
      map.objects[o].load_mapdata()
      v.listener_facing=-1
    elif parsed[0]=="object_sound" and len(parsed)>=2 and v.dieing==False and v.death==False and v.lobby==False:
     o=map.get_objects_index(int(parsed[1]))
     if o!=-1:
      map.objects[o].play_sound(parsed[2])
    elif parsed[0]=="stop_exiting":
     v.exiting=False
    elif parsed[0]=="move_object" and len(parsed)>=2:
     o=map.get_objects_index(int(parsed[1]))
     if o!=-1:
      map.objects[o].move(int(parsed[2]))
    elif parsed[0]=="spawn_object" and len(parsed)>9:
     map.spawn_object(float(parsed[1]),float(parsed[2]),float(parsed[3]),float(parsed[4]),float(parsed[5]),float(parsed[6]),parsed[7],int(parsed[8]),int(parsed[9]))
    elif parsed[0]=="holster_take" and len(parsed)>2:
     v.holster=parsed[1]
     v.holstertime=int(parsed[2])
     v.holstertimer.restart()
    elif parsed[0]=="get_weapons":
     data=data.replace("get_weapons ","")
     things=data.split("||")
     v.sorts=[["melee"],["pistols"],["revolvers"],["shotguns"],["sub_machine_guns"],["assault_rifles"],["machine_guns"],["marksman_rifles"],["sniper_rifles"]]
     done=[]
     for f in things:
      if f in done:
       continue
      if f=="knife" or f=="machete" or f=="flail":
       v.sorts[0].append(f)
      if f=="cold_m1911" or f=="FN_509_tactical" or f=="beretta92A1" or f=="colt_m1911":
       v.sorts[1].append(f)
      if f=="ruger_redhawk" or f=="smith_n_wesson_model29":
       v.sorts[2].append(f)
      if f=="Benelli_M4" or f=="Winchester_Model_24" or f=="remington870xs":
       v.sorts[3].append(f)
      if f=="MP7" or f=="fn_p90" or f=="mp5":
       v.sorts[4].append(f)
      if f=="fn_f2000" or f=="ARX160" or f=="ak47":
       v.sorts[5].append(f)
      if f=="hk_mg4" or f=="m2_browning":
       v.sorts[6].append(f)
      if f=="AR10" or f=="SVD_Dragunov":
       v.sorts[7].append(f)
      if f=="barrett_M107A1" or f=="dsr50":
       v.sorts[8].append(f)
      done.append(f)
    elif parsed[0]=="start_scoping" and len(parsed)>1:
     v.scope_viewing=True
     v.scoping=True
     v.max_scopedistance=int(parsed[1])
    elif parsed[0]=="set_weapon" and len(parsed)>1:
     v.scoping=False
     v.scope_viewing=False
     v.scopedistance=0
     v.current_weapon=parsed[1]
     v.firetimer.restart()
    elif parsed[0]=="set_facing" and len(parsed)>2:
     v.facing=int(parsed[1])
     v.updown=int(parsed[2])
    elif parsed[0]=="go" and len(parsed)>3:
     v.x=float(parsed[1])
     v.y=float(parsed[2])
     v.z=float(parsed[3])
     map.demper_zoneloop(v.x,v.y,v.z)

    elif parsed[0]=="move_player" and len(parsed)>4:
     index=player.get_player_index(parsed[1])
     if index!="":
      v.players[index].move(float(parsed[2]),float(parsed[3]),float(parsed[4]))
    elif parsed[0]=="set_shooting" and len(parsed)>2:
     index=player.get_player_index(parsed[1])
     if index!="":
      status=int(parsed[2])
      v.players[index].shooting=status
      if status==1 and v.players[index] not in player.shooting_players:
        player.shooting_players.append(v.players[index])
      elif status!=1 and v.players[index] in player.shooting_players:
        player.remove(v.players[index])
      we=weapons.weapon(v.players[index].weapon)
      try:
       if int(parsed[3])==1:
        v.players[index].empty=True
      except:
       pass
      if we.automatic==True and v.players[index].empty==False:
       v.players[index].tailing=True
      if int(parsed[2])==1:
       v.players[index].empty=False
      if int(parsed[2])==1 and v.dieing==False and v.death==False and we.automatic==False and get_3d_distance(v.x,v.y,v.z,v.players[index].x,v.players[index].y,v.players[index].z)<=150:
       if v.players[index].silenced==False:
        v.players[index].add_sound(r"sounds\\"+v.players[index].weapon+"fire"+str(random.randint(1,3))+".ogg",False,v.players[index].name)
        v.players[index].add_sound(r"sounds\\"+v.players[index].weapon+"dist.ogg",False,v.players[index].name)
       else:
        v.players[index].add_sound(r"sounds\\"+v.players[index].weapon+"supressedfire"+str(random.randint(1,3))+".ogg",False,v.players[index].name)
        v.players[index].add_sound(r"sounds\\"+v.players[index].weapon+"supresseddist.ogg",False,v.players[index].name)
       v.players[index].firetimer.restart()
    elif parsed[0]=="set_player_weapon" and len(parsed)>2:
     index=player.get_player_index(parsed[1])
     if index!="":
      v.players[index].weapon=parsed[2]
    elif parsed[0]=="stop_player_sound" and len(parsed)>2:
     index=player.get_player_index(parsed[1])
     if index!="":
      v.players[index].stop_sound(parsed[2])
    elif parsed[0]=="set_players_silencer" and len(parsed)>2:
     index=player.get_player_index(parsed[1])
     if index!="":
      if int(parsed[2])==1:
       v.players[index].silenced=True
      else:
       v.players[index].silenced=False
    elif parsed[0]=="player_sound" and len(parsed)>3 and v.dieing==False and v.death==False:
     if int(parsed[3])==1:
      index=player.get_player_index(parsed[1])
      if index!="":
        v.players[index].add_sound(parsed[2],True,parsed[1])
     else:
      index=player.get_player_index(parsed[1])
      if index!="":
        v.players[index].add_sound(parsed[2],False,parsed[1])
    elif parsed[0]=="play_sound" and len(parsed)>5 and v.dieing==False and v.death==False:
     v.sp.behind_pitch_decrease=0
     max_range=40
     if "dist.ogg" in parsed[1] or re.search(r'dist.{1}\.ogg$', parsed[1]):
      max_range=150
     sound_name=parsed[1]
     x=float(parsed[2])
     y=float(parsed[3])
     z=float(parsed[4])
     sterio=int(parsed[5])
     if sterio==1:
      v.msp.play_stationary(r"sounds\\"+sound_name,False)
     else:
      range=get_3d_distance(x,y,z,v.lx,v.ly,v.lz)
      if range>max_range:
       continue
      if "dist.ogg" in parsed[1] or re.search(r'dist.{1}\.ogg$', parsed[1]):
       v.sp.pan_step=1.7
       v.sp.volume_step=0.1
      if range<=150:
       v.sp.filter=map.calculate_walls(x,y,z,v.lx,v.ly,v.lz) 
      v.sp.reverb,v.sp.mix=map.get_reverb_zone(x,y,z)
      if v.lobby==False:
       v.sp.play_3d(r"sounds\\"+sound_name,v.lx,v.ly,v.lz,x,y,z,False,False)
      v.sp.filter=0
     v.sp.pan_step=8.5
     v.sp.volume_step=0.85
     v.sp.behind_pitch_decrease=0

    elif parsed[0]=="copie" and len(parsed)>1:
     data=data.replace("copie ","")
     pc.copy(data)
    elif parsed[0]=="speak":
     data=data.replace("speak ","")
     data=data.replace("_"," ")
     speak(data)
    elif parsed[0]=="server_menu_responce":
     v.server_menu_responce=False
    elif parsed[0]=="mapdata" :
     map.load_map(data.replace("mapdata ",""))
    elif parsed[0]=="block_fire":
     send("stop_shooting")
     v.can_fire=False
    elif parsed[0]=="pong" and v.pinging==True:
     v.pinging=False
     speak(str(v.pingtimer.elapsed()))
     v.msp.play_stationary("sounds\pong.ogg")
def send(message=""):
 if message!="":
  lines=message.split("|n|")
  for data in lines:
   if data=="":
    continue
   parsed=data.split()
   if parsed[0]=="player_sound" and len(parsed)>3 and v.dieing==False and v.death==False:
    if int(parsed[3])==1:
     index=player.get_player_index(parsed[1])
     if index!="":
      v.players[index].add_sound(parsed[2],True,parsed[1])
    else:
     index=player.get_player_index(parsed[1])
     if index!="":
      v.players[index].add_sound(parsed[2],False,parsed[3])
   elif parsed[0]=="move_player" and len(parsed)>4:
    try:
     map.demper_zoneloop(v.x,v.y,v.z)
    except Exception as e:
     error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
     speak(error_message)

    index=player.get_player_index(parsed[1])
    if index!="":
     v.players[index].move(float(parsed[2]),float(parsed[3]),float(parsed[4]))
  message=message+"|n|"
#  message=compress_data(message).hex()
  message=aes_cipher(message,v.packet_key).hex()
  message=message+"|end|"
  message=message.encode()
  try:
   v.s.sendall(message)
  except:
   pass




def disconnect():
 v.pinging=False
 try:
  v.s.close()
 except:
  pass
 s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 v.s=s
 v.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 10000000)
 v.s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 10000000)

def fallloop():
 if len(map.platforms)==0 or v.lobby==True:
  return
 gp=map.get_platform(v.x,v.y,v.z)
 if v.jumping==True and v.jumptimer.elapsed()>=100:
  v.jumptimer.restart()
  v.jumpdist+=1
  if map.get_platform(v.x,v.y,v.z+1)!="wall":
   v.z+=1
   send("move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z))
   gp=map.get_platform(v.x,v.y,v.z)
  else:
   v.jumping=False
   v.falling=True
   v.jumpdist=0
 if v.falling==False and v.falltimer.elapsed()>=60 and gp=="" and v.jumping==False or  v.falling==False and gp=="blank" and v.jumping==False and v.falltimer.elapsed()>=60:
  v.falling=True
  send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\fall.ogg 0|n|")

 if v.jumpdist>=5:
  v.jumpdist=0
  v.jumping=False
  if gp=="" or gp=="blank":
   v.falling=True
   v.falltimer.set(30)
 if v.falling==True and v.falltimer.elapsed()>=60:
  v.falltimer.restart()
  v.falldist+=1
  v.z-=1
  send("move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z))
  gp=map.get_platform(v.x,v.y,v.z)
 if v.jumping==True and gp!="" and gp!="blank" and gp!="wall" or v.falling==True and gp!="" and gp!="blank" and gp!="wall":
  v.jumpdist=0
  v.jumping=False
  v.falling=False
  if v.falldist<=10:
   send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\"+gp+"land.ogg 0|n|player_sound "+v.name+" sounds\\sub"+map.get_sub_tile(v.x,v.y,v.z)+"land.ogg 0|n|player_sound "+v.name+" sounds\\"+v.get_tile_type(map.get_platform(v.x,v.y,v.z),["metal","grass","gravel"])+"landbass.ogg 0")
  else:
   damage=v.falldist*20
   send(r"move_player "+v.name+" "+str(v.x)+" "+str(v.y)+" "+str(v.z)+"|n|player_sound "+v.name+" sounds\\"+gp+"fall.ogg 0|n|player_sound "+v.name+" sounds\\hardfall"+str(random.randint(1,3))+".ogg 0|n|falling_damage "+str(damage)+"|n|player_sound "+v.name+" sounds\\sub"+map.get_sub_tile(v.x,v.y,v.z)+"fall.ogg 0|n|")
  v.falldist=0
 if gp=="wall":
  if v.z<0 or v.falling==True or v.jumping==True:
   v.z+=1
  else:
   v.x,v.y=rotation.move(v.x,v.y,v.facing)



fallchecktimer=timer.timer()

def mainloop():
 v.clock.tick(600)
 try:
  if map.get_platform(v.x,v.y,v.z)=="swim":
   walktime=400
   if v.skill_data["Learn how to swim"]["active"]==True:
    min=1-v.skill_data["Learn how to swim"]["level"]/10
    walktime=walktime*min
   v.walktime=walktime
  else:
   walktime=180
   if v.current_weapon=="SVD_Dragunov" or v.current_weapon=="hk_mg4":
    walktime=260
   if v.current_weapon=="AR10":
    walktime=220
   try:
    if v.skill_data["sprint"]["active"]==True and v.sprinting==True:
     walktime=180-(v.sprint_stage*12)
   except:
    pass
   v.walktime=walktime
  if v.sprinting==True and v.sprint_stagetimer.elapsed()>400 and v.sprint_stage<5:
   v.sprint_stagetimer.restart()
   v.sprint_stage+=1
  if v.sprint_stage>0 and v.sprinting==False and v.sprint_stagetimer.elapsed()>400:
   v.sprint_stagetimer.restart()
   v.sprint_stage-=1
  if v.rapid_fire==True and v.rapid_firetimer.elapsed()>=1000+(300*v.skill_data["rapid fire"]["level"]):
   v.rapid_fire=False
   send(r"player_sound "+v.name+" sounds\\rapidfirestop.ogg 0")

  try:
   if v.sprinting==True and v.sprinttimer.elapsed()>=3000+(500*v.skill_data["sprint"]["level"]):
    v.sprinting=False
  except:
   pass
  netloop()
  if v.messages<3 and v.messagetimer.elapsed()>2500:
   v.messagetimer.restart()
   if v.messages<3:
    v.messages+=1
  v.sp.facing=v.facing
  keys = pygame.key.get_pressed()
  v.shift= keys[K_LSHIFT] or keys[K_RSHIFT]
  v.alt= keys[K_LALT] or keys[K_RALT]
  v.ctrl= keys[K_LCTRL] or keys[K_RCTRL]
  if v.step==True and v.steptimer.elapsed()>v.steptime:
   send("player_sound "+v.name+" sounds\\"+map.get_platform(v.x,v.y,v.z)+"step"+str(random.randint(1,5))+".ogg 0")
   v.step=False

  if v.scoping==True and v.scope_viewing==True:
   if v.updown==-2 and map.get_platform(v.x,v.y,v.z-1)=="wall":
    v.lx,v.ly=rotation.move(v.x,v.y,v.facing,1)
   else:
    v.lx,v.ly=rotation.move(v.x,v.y,v.facing,v.scopedistance)
   if v.updown>0:
    v.lz=v.z+v.scopedistance
   elif v.updown<0:
    v.lz=v.z-v.scopedistance
   else:
    v.lz=v.z
   map.demper_zoneloop(v.lx,v.ly,v.lz)
  else:
   v.lx=v.x
   v.ly=v.y
   v.lz=v.z
  if v.listener_x!=v.lx or v.listener_y!=v.ly or v.listener_z!=v.lz or v.listener_facing!=v.facing:
   if v.lobby==False and v.scoping==False:
    v.listener_x=v.lx
    v.listener_y=v.ly
    v.listener_z=v.lz
    v.listener_facing=v.facing
    v.sp.update_listener_3d(v.listener_x,v.listener_y,v.listener_z,v.listener_facing)
  if v.scoping==True:

   v.sp.update_listener_3d(v.lx,v.ly,v.lz,v.facing)
  if v.scoping==True:
   for p in v.players:
    if v.players[p].name==v.name:
     v.players[p].move(v.lx,v.ly,v.lz)

  if v.infrascanning==True and v.infrascannertimer.elapsed()>250:
   v.infrascannertimer.restart()
   result=""
   for f in v.players:
    p=v.players[f]
    if get_3d_distance(v.x,v.y,v.z,p.x,p.y,p.z)<=40 and p.name not in v.infrascanninglist and v.name!=p.name:
     v.infrascanninglist.append(p.name)
     result=p.name
     index=player.get_player_index(v.name)
     if index!="":
      v.sp.filter=map.calculate_walls(p.x,p.y,p.z,v.lx,v.ly,v.lz) 
      if v.players[index].team!=p.team or v.players[index].team=="":
       v.sp.play_3d("sounds\infrared_scannerfound.ogg",v.lx,v.ly,v.lz,p.x,p.y,p.z,True,False,False,100)
      else:
       v.sp.play_3d("sounds\infrared_scannerteamfound.ogg",v.lx,v.ly,v.lz,p.x,p.y,p.z,True,False,False,100)
      v.sp.filter=0
     break
   if result=="":
    v.infrascanning=False
   if len(v.infrascanninglist)==0:
    v.msp.play_stationary("sounds\infrared_scannerfailed.ogg")
#  index=player.get_player_index(v.name)
#  if  index>-1:
#   v.players[index].move(v.lx,v.ly,v.lz)
  if fallchecktimer.elapsed()>=50:
   fallloop()
  if v.lobby==False:
   map.zoneloop()
  v.sp.reverb,v.sp.mix=map.get_reverb_zone(v.lx,v.ly,v.lz)
  if v.stunned==True and v.stuntimer.elapsed()>v.stuntime:
   v.stunned=False
  if speedhacktimer.elapsed()>=1000:
   speedhacktimer.restart()
   send("speedhackcheck")
  if v.holster!="" and v.holstertimer.elapsed()>v.holstertime:
   v.current_weapon=v.holster
   v.scoping==False
   send("draw_weapon "+v.holster)
   v.holster=""
  if v.can_fire==False:
   index=player.get_player_index(v.name)
   if  index!="":
    if v.players[index].shooting==1:
     send("stop_shooting")
  for p in player.shooting_players:
   if p not in v.players.values():
    player.shooting_players.remove(p)
   if p.weapon!="" and p.shooting==1:
    we=weapons.weapon(p.weapon)
    if p.firetimer.elapsed()>we.firetime:
     p.firetimer.restart()
     if v.death==False and get_3d_distance(v.lx,v.ly,v.lz,p.x,p.y,p.z)<=150:
      if p.silenced==False:
       p.add_sound(r"sounds\\"+we.name+"fire"+str(random.randint(1,3))+".ogg",False)
       p.add_sound(r"sounds\\"+we.name+"dist.ogg",False)
      else:
       p.add_sound(r"sounds\\"+we.name+"supressedfire"+str(random.randint(1,3))+".ogg",False)
       p.add_sound(r"sounds\\"+we.name+"supresseddist.ogg",False)

   if p.tailing==True and p.weapon!="":
    we=weapons.weapon(p.weapon)
    if p.firetimer.elapsed()>we.firetime:
     p.firetimer.restart()
     p.tailing=False
     if v.death==False:
      if p.silenced==False:
       p.add_sound(r"sounds\\"+we.name+"firetail.ogg",False,p.name)
       p.add_sound(r"sounds\\"+we.name+"taildist.ogg",False,p.name)
      else:
       p.add_sound(r"sounds\\"+we.name+"supressedfiretail.ogg",False,p.name)
       p.add_sound(r"sounds\\"+we.name+"supressedtaildist.ogg",False,p.name)

  if v.current_weapon=="barrett_M107A1" or v.current_weapon=="m2_browning" or v.current_weapon=="dsr50":
   v.heavy_weapon=True
  else:
   v.heavy_weapon=False
  if v.dieing==True:
   return 1
  else:
   return 0
 except:
  pass


def play_sound_dlg(sound,time,online=True):
 v.msp.play_stationary(sound)
 endtimer=timer.timer()
 while endtimer.elapsed()<time:
  for event in pygame.event.get():
   pass

  if online==True:
    mainloop()
