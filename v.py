import pygame, pygame.locals as pl
pygame.init()
import translator
import traceback
import ssl
import math
import datetime
def get_time():
 nu = datetime.datetime.now()
 datum = nu.strftime("%d %B %Y")
 tijd = nu.strftime("%H:%M")
 return datum,tijd
import os

import wmi

def get_hard_drive_serial_numbers():
    try:
        # Gebruik de wmi-module om de UUID op te halen
        c = wmi.WMI()
        for product in c.Win32_ComputerSystemProduct():
            uuid = product.UUID
            return uuid
    except Exception as e:
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        dlg.dlg("error: " + error_message)

import secrets
import random
import socket
import rotation
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 text=vertaal_tekst(text,language)
 speatch.output(text)


import sound_pool
from sound_pool.sound import o
import timer
import buffer

def get():
 global clock
 clock = pygame.time.Clock()

 global start_match
 start_match=False
 global language
 language=""
 global t
 t=translator.translator(language,r"languages\\"+language+".txt")

 global standart_filter
 standart_filter=15000
 global beta
 beta=False
 global rules_data
 rd="""City of Division rules 
We from FireGaming, want to create a great  gaming experience for everyone. To make this happen, we have some rules that every player has to follow. If you don't follow these rules, an admin can take any of the following actions but is not obligated to use them in this particular order. Admins can:
• Send a warning
• Temporarily disable your chat or PM’s
• Kick you from the server
• Temporarily or permanently ban you from the game

Spamming
Spamming covers a lot of things. It can be sending many chat messages in a row with no useful content or repeatedly using an in-game action for no reason. If it annoys other players, it's probably spamming. If you spam, the staff will take action against   you!

Public Chat
Everyone can read the public chat, so the following things are not allowed:
• Spamming or sending screen reader crash codes. Screen reader spamming, defined as sending excessively long or repetitive messages in order to delay lag or otherwise impede screen readers is expressly banned. 
• Sharing links to illegal software or sensitive personal information,, this includes but is not limited to clones, pirated software  or any documentation related to activity that is deemed illegal in whatever jurisdiction the player may be in. Personal information includes things like bank details, real life addresses, phone numbers or other details people don’t want shared.
• Content not suitable for children. Discuss these topics in private messages or the unfiltered chat channel. This includes sexually explicit content, threats of violence or personal harm, topics of self-harm, illicit substance use, racially or nationally motivated insults and other things not necessarily named in this document. The general rule should be if a staff member tells you that a certain topic is off limits, you should listen. Importantly, it is not the case that any discussion of these sorts of topics are expressly banned, it’s that great care should be taken when expressing possibly problematic things. 
• personal attacks towards other players, the staff, or the game as a whole. As stated previously, nationalistic insults will be treated the same as personal or racial insults. 
 
No Cheating
Cheating is not allowed. This includes:
• Using cheat software or auto key pressers  to change game variables, finish tasks for you,  or use speed hacks.
• Intentionally exploiting game bugs for extra kills or items.

Avoiding Punishment
Avoiding punishment, either through lying about actions or making new characters to avoid sanctions put on you by staff is expressly forbidden and will be viewed negatively and as enhancements to whatever action precipitated it. If you are banned for action on one character, you are banned not the character. This means for the duration of your ban you are not welcome in City of Division. Attempts to get around this may be cause for a permanent ban. 
Sharing passwords is generally discouraged. If you share your password and someone is disciplined for behavior they committed on your character, you will be the one accountable for it. It’s generally best to use a password you feel is strong and not give it out to anyone!

Administrators
Admins are here to enforce the rules and keep the game fun for all. If an admin asks you to stop doing something, you have to do so. If you think an admin is abusing their rank, report it to Firegaming through other channels, (not via staff-messages), as the admin could close these.
Staff Messages
Staff messages are there to help players out and report bugs easily to the developers. Don’t use this for nonsense. 
If you encounter any typical game problems, please use the staph messages to tell the administrators about it. Please do not use private messages for this, as they are much harder for the administrator to keep track of. In simplest terms, using staff messages Is much more likely to get your message seen and considered by the staff. 

We hope you understand these rules that are here to make City of Division enjoyable for everyone. Generally speaking, if you just play and behave normally, you won’t have to worry about them.
Thanks for reading this document.
The FireGaming team"""
 rules_data=rd.split("\n")
 global rules
 rules=0
 global packet_key
 packet_key=b"hallo goars jaja"
 global lobby
 lobby=False
 global exiting
 exiting=False
 global version
 version="1.55"
 global c4_use
 c4_use=False
 global which_menu
 which_menu=""
 global start_game
 start_game=False
 global mainmenu
 mainmenu=False
 global messagetimer
 messagetimer=timer.timer()
 global messages
 messages=3
 global reconnecting
 reconnecting=False
 global srclist
 srclist=["abandoned_place2","birds1","birds2","birds3","birds4","birds5","birds6","birds7","birds8","birds9","birds10","birds11","birds12","building","buzzy_parkingstructure","calm1","calm2","canal1","forest1","forest2","landscape1","landscape2","landscape3","smallpark","stream","stream1","stream2","stream3","waves","building2","water_under_bridge","fountain","abandoned_place","birds13","road","ditch","birds14","bunker","calm4","canyion","rockscanyon","rockscanyon1","rockscanyon2","rocksquarry","rocksquarry1","rocksquarry2","watertankloop","wind","calm3","waterfallloop","waterfallloop2","waves2","dripping_water1","dripping_water2","sewer","smallpipe","largepipe"]

 global itemlist
 itemlist=[]
 global objlist
 objlist=[]
 global firing
 global rapid_fire
 rapid_fire=False
 global rapid_firetimer
 rapid_firetimer=timer.timer()
 global sprinting
 sprinting=False
 global sprinttimer
 sprinttimer=timer.timer()
 global sprint_stagetimer
 sprint_stagetimer=timer.timer()
 global sprint_stage
 sprint_stage=0
 global walktime
 walktime=180

 firing=False
 global ctrl
 ctrl=False
 global shift
 shift=False
 global alt
 alt=False
 global infrascanninglist
 infrascanninglist=[]
 global infrascanning
 infrascanning=False
 global infrascannertimer
 infrascannertimer=timer.timer()

 global infrascannerusetimer
 infrascannerusetimer=timer.timer()
 global infraredscanner
 infraredscanner=True
 global infrared_scanner_timer
 infrared_scanner_timer=timer.timer()
 global infrared_scanner_time
 infrared_scanner_time=0

 global closing
 closing=0
 global first_sm_check
 first_sm_check=0
 global first_sm
 first_sm=""
 global first_sm_backup
 first_sm_backup=""

 global server_menu_responce
 server_menu_responce=False
 global server_menu_actif
 server_menu_actif=False
 global new_sm
 new_sm=0
 global last_sm
 last_sm=None
 global last_sm_name
 last_sm_name=[]
 global last_sm_options
 last_sm_options=[]

 global step
 step=False
 global steptime
 steptime=0
 global steptimer
 steptimer=timer.timer()
 global heavy_weapon
 heavy_weapon=False
 global chest
 chest=""
 global chest_data
 chest_data={}
 global skill_data
 skill_data={}
 global stunned
 stunned=False
 global scoping
 scoping=False
 global scope_viewing
 scope_viewing=False
 global scopedistance
 scopedistance=0
 global max_scopedistance
 max_scopedistance=0

 global stuntime
 stuntime=0
 global stuntimer
 stuntimer=timer.timer()
 global sorts
 sorts=[["melee"],["pistols"],["revolvers"],["shotguns"],["sub_machine_guns"],["assault_rifles"],["machine_guns"],["marksman_rifles"],["sniper_rifles"]]

 global s
 s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s= ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")
 global dieing
 dieing=False
 global death
 death=False
 global can_fire
 can_fire=True
 global firetimer
 firetimer=timer.timer()
 global current_weapon
 current_weapon=""
 global musics
 musics=[]
 global musicvolume
 musicvolume=-15
 global radartime
 radartime=190
 global speak_cap
 speak_cap=1
 global allow_log_buffers
 allow_log_buffers=1
 global shiftexit
 shiftexit=0
 global speak_chars
 speak_chars=1
 global typing_sounds
 typing_sounds=1

 global allow_wait
 allow_wait=0
 global askexit
 askexit=1
 global precize_turning
 precize_turning=True
 global right_ctrl
 right_ctrl=1
 global name
 name=""
 global comp_id
 comp_id = get_hard_drive_serial_numbers()
 global mapdata
 mapdata=""
 global key
 key=b"Dit is een gehei"
 global password
 password=""
 global holster
 holster=""
 global holstertimer
 holstertimer=timer.timer()
 global holstertime
 holstertime=0
 global players
 players={}
 global pinging
 pinging=False
 global pingtimer
 pingtimer=timer.timer()
 global buffers
 buffers=[buffer.buffer("all"),buffer.buffer("chats"),buffer.buffer("pm"),buffer.buffer("team_chats"),buffer.buffer("online_and_offline"),buffer.buffer("misc"),buffer.buffer("death_messages"),buffer.buffer("team"),buffer.buffer("important")]
 global bufferpos
 bufferpos=0
 global sp
 sp=sound_pool.sound_pool
 sp.pan_step=1.0
 sp.volume_step=1.0
 global msp
 msp=sound_pool.sound_pool
# msp.reverb_pool=False
 global falling
 falling=False
 global jumptimer
 jumptimer=timer.timer()
 global falltimer
 falltimer=timer.timer()
 global jumping
 jumping=False
 global falldist
 falldist=0
 global jumpdist
 jumpdist=0
 global z
 global track_thing
 track_thing=""
 global tracked
 tracked=-1
 global x
 x=0
 global y
 y=0
 global lx
 lx=0
 global ly
 ly=0
 global lz
 lz=0
 global listener_x
 listener_x=0
 global listener_y
 listener_y=0
 global listener_z
 listener_z=0
 global listener_facing
 listener_facing=0


 global facing
 facing=0
 global updown
 updown=0

 z=0
 global current_zone
 current_zone=""
def change_master_volume(mode):
 if mode==1:
  if o.volume<1:
   o.volume+=0.1
  else:
   speak("maximum game volume reached.")
   o.volume=1.0
 if mode==0: 
  if o.volume>0.1:
   o.volume-=0.1
  else:
   speak("game sounds muted")
   o.volume=0.0

import re
from functools import lru_cache

# Precompileer wildcard patronen
@lru_cache(maxsize=1024)
def compile_wildcard_pattern(pattern):
    # Vervang de jokertekens door non-greedy regex-tekens
    regex_pattern = pattern.replace('%s', '(.+)')
    return re.compile(regex_pattern)

def match_with_wildcard(pattern, string):
    compiled_pattern = compile_wildcard_pattern(pattern)
    match = compiled_pattern.fullmatch(string)
    if match:
        return match.groups()  # Retourneer de gevonden groepen
    return None

def vertaal_tekst(tekst, doeltaal):
    if language == "English":
        return tekst

    if tekst in t.lang_data:
        return t.lang_data[tekst]

    for key in t.lang_data:
        key_length_string=key.replace("%s","")
        key_length_string=key_length_string.replace("%o","")
        if len(key_length_string)>len(tekst):
            continue
        if key[0]!=tekst[0] and key[0:2]!="%s" and key[0:2]!="%o":
         continue
        try:
         result = match_with_wildcard(key, tekst)
         if result:
             values = result
             final = t.lang_data[key]
             for i, va in enumerate(values, 1):
                 old_final=final
                 final = final.replace("%" + str(i), vertaal_tekst(va, doeltaal))
                 if final==old_final:
                     final = final.replace("#" + str(i),va)

             return final
        except:
         pass

    return tekst

def get_master_volume():
 return o.volume
def set_master_volume(volume):
 o.volume=volume


def add_buffer_item(name,text):
 i=0
 for b in buffers:
  if b.name==name:
   i=1
   if b.muted==False:
    buffers[0].add(text)
   buffers[buffers.index(b)].add(text)
 if i==0:
  buffers.append(buffer.buffer(name))
  for b in buffers:
   if b.name==name:
    if b.muted==False:
     buffers[0].add(text)
    buffers[buffers.index(b)].add(text)

def log_buffers():
 if allow_log_buffers==0:
  return
 try:
  for b in buffers:
   if len(b.items)<1:
    continue

   documents_folder = os.path.join(os.path.expanduser('~'), 'Documents')

   if not os.path.exists(documents_folder):
    os.makedirs(documents_folder)

   log_folder = os.path.join(documents_folder, 'city of division logs')

   if not os.path.exists(log_folder):
    os.makedirs(log_folder)

   log_file_path = os.path.join(log_folder, b.name+".log")
   with open(log_file_path, "a+") as log_file:
    existing_logs = log_file.read()
    if existing_logs:
     log_file.write(existing_logs+"\n")
    datum,tijd=get_time()
    log_file.write("exported on "+datum+"  "+tijd+"\n")
    log_file.write("\n".join(b.items)+"\n")
 except:
  pass
def get_list_in_text(list):
 if len(list)==0:
  return ""
 if len(list)==1:
  return list[0]
 final=""
 for l in list:
  if list.index(l)==len(list)-1:
   final=final+"and "+l
  elif list.index(l)==0:
   final=final+l+" "
  else:
   final=final+", "+l+" "
 return final


def get_time_in_mm(mm):
 final={
"second": 0,
"minute": 0,
"hour": 0,
"day": 0,
"week": 0,
"month": 0,
}
 final["second"]=math.floor(mm/1000)
 final["minute"]=math.floor(final["second"]/60)
 final["second"]-=final["minute"]*60
 final["hour"]=math.floor(final["minute"]/60)
 final["minute"]-=final["hour"]*60
 final["day"]=math.floor(final["hour"]/24)
 final["hour"]-=final["day"]*24
 final["week"]=math.floor(final["day"]/7)
 final["day"]-=final["week"]*7
 final["month"]=math.floor(final["week"]/4)
 final["week"]-=final["month"]*4
 good={}
 for f in final:
  if final[f]!=0:
   good[f]=final[f]
 final=good
 end=""
 text_list=[]
 for f in reversed(final):
  i=f
  if final[f]>1:
   i=i+"s"
  text_list.append(str(final[f])+" "+i)
 end=get_list_in_text(text_list)
 if end=="":
  end="no time at all"
 return end

import sys

def remove_py_files_if_not_from_source():
    # Controleer of het script niet vanuit de broncode wordt uitgevoerd
    if getattr(sys, 'frozen', False):
        current_dir = os.getcwd()
        # Loop door alle bestanden in de huidige directory
        for filename in os.listdir(current_dir):
            # Controleer of het bestand een .py bestand is
            if filename.endswith(".py"):
                file_path = os.path.join(current_dir, filename)
                try:
                    os.remove(file_path)  # Verwijder het bestand
                except Exception as e:
                    pass

def sound__exists(name):
 folder="sounds"
 files=[]
 if os.path.exists(folder) and os.path.isdir(folder):
  for file in os.listdir(folder):
   file_path = os.path.join(folder, file)
   if os.path.isfile(file_path):
    files.append(file)
 name=name.replace(".ogg",".bin")
 if name in files:
  return True
 else:
  return False

def get_tile_type(name,tiles=[]):
 if name=="":
     return ""
 i=""
 if name.startswith("dirt") or name.startswith("sand"):
  i="dirt"
 elif name.startswith("grass") or name.startswith("tree"):
  i="grass"
 elif name.startswith("gravel")  or name.startswith("rocks"):
  i="gravel"
 elif name=="swim" or name=="shallow" or name.startswith("water"):
  i="water"
 elif name[0:5]=="metal" or name[0:6]=="ladder"  or name=="beam":
  i="metal"
 else:
  i="generic"
 if i in tiles:
  return i
 else:
  return "generic"

