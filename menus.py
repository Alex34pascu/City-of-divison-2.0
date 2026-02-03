import square_menu
import updater
import translator
import requests
from bs4 import BeautifulSoup
import os


def get_downloads_folder():
    if os.name == 'nt':  # Windows
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:  # macOS/Linux
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def get_txt_filenames_from_url(url):
    response = requests.get(url)
    
    # Controleer of de response succesvol was
    if response.status_code == 200:
        # Parseer de HTML van de pagina
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Zoek naar alle link-elementen
        txt_files = []
        for link in soup.find_all('a'):
            href = link.get('href')
            # Controleer of de link eindigt op .txt
            if href and href.endswith('.txt'):
                # Voeg alleen de bestandsnaam toe
                txt_files.append(os.path.basename(href))
        
        return txt_files
    else:
        print(f"Error: {response.status_code}")
        return []
import key_constants as kc

import sound_pool
import timer
import re
def custom_sort(word_list):
 def sort_key(word):
  match = re.match(r'([a-zA-Z]+)(\d*)', word)
  alpha_part, num_part = match.groups() if match else (word, "")

  num_part = int(num_part) if num_part.isdigit() else float('inf')

  return alpha_part, num_part

 sorted_words = sorted(word_list, key=sort_key)

 return sorted_words

import numpy as np
import math
def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)
from threading import Thread
import pygame, pygame.locals as pl
pygame.init()

import mega_menu
import v
v.get()
import map
import pyperclip as pc
import virtual_input
import menu
import net
om=menu.online_menu()
sqm=square_menu.square_menu()
m=menu.Menu()

import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 text=v.vertaal_tekst(text,v.language)
 speatch.output(text)
sub_tilelist=["glass","wooddebris","puddle","debris"]
platformlist=["blank","broken_glass","carpet1","carpet2","carpet3","carpet4","carpet5","carpet6","carpet7","concrete1","concrete2","concrete3","deck","grass","grass1","grass2","grass3","grass4","gravel","gravel1","gravel2","hardwood","hardwood1","hardwood2","hardwood3","hardwood4","ladder","metal1","metal4","metal2","metal3","metal5","metal6","metal7","metal8","metal9","metal10","mud","rocks","rocks1","rocks2","rocks3","sand","stone","swim","tree","water","wood","dirt1","dirt2","concrete4","concrete5","water1","water2","glass","beam","cement1","cement2","marble1","marble2","fence","shallow","cloth","ladder1","ladder2","concrete6","concrete7","concrete8","concrete9","concrete10","wood2","concrete11","concrete12","cave","grass5","metal11","dirt3","gravel3","water3"]
walllist=["brick","brush","brush1","brush2","brushtangle","building","car","car1","car2","cloth","door","door1","fence","glass","grass","lamppost","metal","metal1","metal2","metal3","net","rail","rock","stone","stone2","table","desk","wood","furniture","metal5","wood2","metal4","water_tank","tire","vehicle","rock3","rock4","rock5","rock1","rock2"]
srclist=custom_sort(v.srclist)
walllist=custom_sort(walllist)
platformlist=custom_sort(platformlist)
sub_tilelist=custom_sort(sub_tilelist)

def preview_menu(type):
 while True:
  for event in pygame.event.get():
   if event.type==pygame.KEYDOWN:
    if event.key==pl.K_SPACE:
     if type=="wall":
      speak("kaas")
      v.msp.play_stationary(r"sounds\\"+m.get_item()+".ogg")


def lines_menu(data,mode):
 m.reset()
 m.edge_sound="sounds\menuedge.ogg"
 m.click_sound="sounds\menuclick.ogg"
 m.enter_sound="sounds\menuenter.ogg"
 m.close_sound="sounds\menuclose.ogg"
 m.open_sound="sounds\menuopen.ogg"
 items=data.split("\n")
 for i in items:
  if i!="":
   m.add_item(i)
 item=m.loop("which line do you want to "+mode,True)
 if item!="":
  if mode=="remove":
   v.mapdata=v.mapdata.replace(item,"")
   v.mapdata=v.mapdata.replace("\n","|||")
   net.send("new_mapdata "+v.mapdata)
  if mode=="edit":
   new_item=virtual_input.input("edit the line. Press enter when you are done.",True,item)
   if new_item!="":
    v.mapdata=v.mapdata.replace(item,new_item)
    v.mapdata=v.mapdata.replace("\n","|||")
    net.send("new_mapdata "+v.mapdata)
def server_menu(name,itemlist,backup=False):
 v.server_menu_responce=False
 if v.new_sm==1:
  v.new_sm=0
  v.last_sm_name=[]
  v.last_sm_options=[]
  v.first_sm_check=0
 wname=name.replace("_"," ")
 if backup==False:
  m.reset()
  m.edge_sound="sounds\menuedge.ogg"
  m.click_sound="sounds\menuclick.ogg"
  m.enter_sound="sounds\menuenter.ogg"
  m.close_sound="sounds\menuclose.ogg"
  m.open_sound="sounds\menuopen.ogg"
  items=itemlist.split("\n")
  for i in items:
   if i!="":
    m.add_item(i)
 item=m.loop(wname,True)
 if item!="":
  v.last_sm_name.insert(0,name)
  v.last_sm_options.insert(0,item)
  v.closing=1
  v.first_sm_check+=1
#  v.server_menu_responce=True
  net.send("server_menu_answer "+name+" "+item)
 else:
  try:
#    if v.closing==1:
#     del v.last_sm_name[0]
#     del v.last_sm_options[0]
#     v.closing=0
#    g=v.last_sm_name[0]
    del v.last_sm_name[0]
#    h=v.last_sm_options[0]
    del v.last_sm_options[0]
    v.closing=0
    net.send("server_menu_answer "+v.last_sm_name[0]+" "+v.last_sm_options[0])
  except:
   if v.first_sm_check>=1:
    v.first_sm_check=0
    net.send(v.first_sm)

def online_menu(name,itemlist,backup=False,  **kwargbs):
 if v.new_sm==1:
  v.new_sm=0
  v.last_sm_name=[]
  v.last_sm_options=[]
  v.first_sm_check=0
 wname=name.replace("_"," ")
 if backup==False:
  om.reset()
  om.edge_sound=kwargbs.get("edge_sound", "")
  om.click_sound=kwargbs.get("click_sound", "")
  om.enter_sound=kwargbs.get("enter_sound", "")
  om.close_sound=kwargbs.get("close_sound", "")
  om.open_sound=kwargbs.get("open_sound", "")

  items=itemlist.split("\n")
  for i in items:
   if i!="":
    om.add_item(i.replace("weapon_",""),i)
 item=om.loop(name,True)
 if item!="":
  v.last_sm_name.insert(0,name)
  v.last_sm_options.insert(0,item)
  v.closing=1
  v.first_sm_check+=1
  net.send("server_menu_answer "+name+" "+item)
 else:
  try:
    del v.last_sm_name[0]
    del v.last_sm_options[0]
    v.closing=0
    net.send("server_menu_answer "+v.last_sm_name[0]+" "+v.last_sm_options[0])
  except:
   if v.first_sm_check>=1:
    v.first_sm_check=0
    net.send(v.first_sm)



def buildermenu():
 m.reset()
 m.edge_sound="sounds\menuedge.ogg"
 m.click_sound="sounds\menuclick.ogg"
 m.enter_sound="sounds\menuenter.ogg"
 m.close_sound="sounds\menuclose.ogg"
 m.open_sound="sounds\menuopen.ogg"
 m.add_item("platform")
 m.add_item("wall")
 m.add_item("staircase")
 m.add_item("zone")
 m.add_item("region")
 m.add_item("object")
 m.add_item("reverb zone")
 m.add_item("demper zone")
 m.add_item("sound source")
 m.add_item("bounded sound source")
 m.add_item("ambience")
 m.add_item("location")
 m.add_item("allow_zone")
 m.add_item("respawn_zone")
 m.add_item("sub_tile")
 m.add_item("edit line")
 m.add_item("remove line")
 m.add_item("past the map data that is on your clib board")
 m.add_item("get the map data")
 item=m.loop("builder menu. Please select an option",True)
 item=item.replace("reverb zone","rv")
 item=item.replace("bounded sound source","bounded_source")
 item=item.replace("demper zone","dz")
 item=item.replace("sound source","src")
 if item=="create a custom object.":
  name=virtual_input.input("type the name for this object",True)
  if name=="":
   return
  m.reset()
  hitsoundslist=["table","cabinet","planter","tree","lamppost"]
  hitsoundslist.sort()
  for i in hitsoundslist:
   m.add_item(i)
  hitsounds=m.loop("select the hitsound set",True)
  if hitsounds=="":
   return
  try:
   health=int(virtual_input.input("Enter the health. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  mapdata=virtual_input.input("type the map data for this object. Use || for a new line.",True)
  if mapdata=="":
   return

#guur
  return
 if item=="remove line":
  lines_menu(v.mapdata,"remove")
  return
 if item=="edit line":
  lines_menu(v.mapdata,"edit")
  return
 if item=="past the map data that is on your clib board":
  q=yesno("do you want to oferwrite the map data?")
  if q==1:
   net.send("new_mapdata "+pc.paste())
  return
 if item=="get the map data":
  net.send("mapdata")
  return
 if item=="":
  return
 if item!="location":
  try:
   minx=int(virtual_input.input("Enter the minimum x. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   maxx=int(virtual_input.input("Enter the maximum x. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   miny=int(virtual_input.input("Enter the minimum y. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   maxy=int(virtual_input.input("Enter the maximum y. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   minz=int(virtual_input.input("Enter the minimum z. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   maxz=int(virtual_input.input("Enter the maximum z. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
 else:
  try:
   minx=int(virtual_input.input("Enter the x. Press enter when you're done.",True))
   maxx=minx
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   miny=int(virtual_input.input("Enter the y. Press enter when you're done.",True))
   maxy=miny
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   minz=int(virtual_input.input("Enter the z. Press enter when you're done.",True))
   maxz=minz
  except ValueError:
   speak("this input isn't legal.")
   return

 extra=""
 if item=="platform":
  m.reset()
  for p in platformlist:
   m.add_item(p)
  m.preview="%namestep1.ogg"
  name=m.loop("select a platform",True)
  if name!="":
   extra=name
  else:
   return
 if item=="sub_tile":
  m.reset()
  for p in sub_tilelist:
   m.add_item(p)
  m.preview="sub%namestep1.ogg"
  name=m.loop("select a tile",True)
  if name!="":
   extra=name
  else:
   return
 if item=="staircase":
  m.reset()
  for p in platformlist:
   m.add_item(p)
  m.preview="%namestep1.ogg"
  pname=m.loop("select a platform",True)
  if pname=="":
   return
  m.reset()
  for p in walllist:
   m.add_item("wall"+p)
  m.preview="%name.ogg"
  wname=m.loop("select a wall",True)
  if wname=="wall":
   return
  try:
   dir=int(virtual_input.input("Enter the direction of the staircase. 1 for south to north, 2 for north to south, 3 for east to west and 4 for west to east. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  zone=virtual_input.input("Enter the zone which belongs to this staircase. Leave blank for empty Press enter when you're done.",True)
  extra=pname+" "+wname+" "+str(dir)+" "+zone

 if item=="object":
  m.reset()
  v.objlist.sort()
  for p in v.objlist:
   m.add_item(p)
  name=m.loop("select an object",True)
  try:
   dir=int(virtual_input.input("Enter the direction of the object. 1 for north, 2 for east, 3 for south and 4 for west. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
  extra=name+" "+str(dir)
 if item=="src":
  m.reset()
  for p in srclist:
   m.add_item(p)
  m.preview="%name.ogg"
  soundname=m.loop("select a sound",True)+".ogg"
  if soundname=="":
   return
  try:
   volume=int(virtual_input.input("Enter the volume of the sound source. The defalt is 0. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
  extra=soundname+" "+str(volume)

 if item=="bounded_source":
  m.reset()
  for p in srclist:
   m.add_item(p)
  m.preview="%name.ogg"
  soundname=m.loop("select a sound",True)+".ogg"
  if soundname=="":
   return
  try:
   volume=int(virtual_input.input("Enter the volume of the bounded source. The defalt is 0. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
  bzones=virtual_input.input("type here your bounded_zones for example 0 10 0 10 0 10 use || to split the bounded_zones",True)
  extra=soundname+" "+str(volume)+" "+bzones
 if item=="ambience":
  m.reset()
  for p in srclist:
   m.add_item(p)
  m.preview="%name.ogg"
  soundname=m.loop("select a sound",True)+".ogg"
  if soundname=="":
   return
  try:
   volume=int(virtual_input.input("Enter the volume of the ambience. The defalt is 0. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
  extra=soundname+" "+str(volume)
 if item=="wall":
  m.reset()
  for p in walllist:
   m.add_item(p)
  m.preview="wall%name.ogg"
  wall="wall"
  wall=wall+m.loop("select a wall",True)
  if wall!="wall":
   name=wall
  else:
   return
  try:
   strength=int(virtual_input.input("Enter the strength of the wall. The defalt is 5000. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  extra=name+" "+str(strength)
 if item=="zone":
  extra=virtual_input.input("type the text of the zone here.",True)
 if item=="region":
  extra=virtual_input.input("type the text of the region here.",True)
 if item=="location":
  extra=virtual_input.input("type the text of the location here.",True)
 if item=="rv":
  try:
   mix=int(virtual_input.input("Enter the reverb mix. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   time=int(virtual_input.input("Enter the reverb time. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  extra=str(mix)+" "+str(time)
 if item=="dz":
  name=virtual_input.input("Enter the name of the sound_source which should be effected. Press enter when you're done.",True)
  try:
   volume=int(virtual_input.input("Enter the volume of the sound_source[how many it should lower it]. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  extra=name+" "+str(volume)
 if item=="allow_zone":
  data=""
  flag=True
  while flag:
   m.reset()
   for p in v.itemlist:
    m.add_item(p)
   name=m.loop("select a item",True)
   if name!="":
    try:
     number=int(virtual_input.input("Enter the chanse to find this item. Press enter when you're done.",True))
    except:
     number=0
    if number<=0:
     continue
    else:
     data=data+name+";"+str(number)+":"
   else:
    flag=False
  if data=="":
   rreturn
  else:
   extra=data[0:len(data)-1]
 if item=="respawn_zone":
  try:
   sminx=int(virtual_input.input("Enter the spawn minimum x. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   smaxx=int(virtual_input.input("Enter the spawn maximum x. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   sminy=int(virtual_input.input("Enter the spawn minimum y. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   smaxy=int(virtual_input.input("Enter the spawn maximum y. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   sminz=int(virtual_input.input("Enter the spawn minimum z. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   smaxz=int(virtual_input.input("Enter the spawn maximum z. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  extra=str(sminx)+" "+str(smaxx)+" "+str(sminy)+" "+str(smaxy)+" "+str(sminz)+" "+str(smaxz)
 if item!="location":
  net.send("build "+item+" "+str(minx)+" "+str(maxx)+" "+str(miny)+" "+str(maxy)+" "+str(minz)+" "+str(maxz)+" "+str(extra))
 else:
  net.send("build "+item+" "+str(minx)+" "+str(miny)+" "+str(minz)+" "+str(extra))
def yesno(message,online=True):
 m.reset()
 m.edge_sound="sounds\confirmedge.ogg"
 m.click_sound="sounds\confirmclick.ogg"
 m.enter_sound="sounds\confirmenter.ogg"
 m.close_sound="sounds\confirmclose.ogg"
 m.open_sound="sounds\confirm.ogg"
 m.add_item("yes")
 m.add_item("no")
 item=m.loop(message,online)
 if item=="yes":
  return 1
 else:
  return 0
def admin_menu(name):
 m.reset()
 m.edge_sound="sounds\menuedge.ogg"
 m.click_sound="sounds\menuclick.ogg"
 m.enter_sound="sounds\menuenter.ogg"
 m.close_sound="sounds\menuclose.ogg"
 m.open_sound="sounds\menuopen.ogg"
 m.add_item("send "+name+" a warning")
 m.add_item("move this player")
 m.add_item("disable this players chat")
 m.add_item("kick this player")
 m.add_item("ban this player")
 item=m.loop("select an option",True)
 if item=="disable this players chat":
  time=0
  m.reset()
  m.edge_sound="sounds\menuedge.ogg"
  m.click_sound="sounds\menuclick.ogg"
  m.enter_sound="sounds\menuenter.ogg"
  m.close_sound="sounds\menuclose.ogg"
  m.open_sound="sounds\menuopen.ogg"
  m.add_item("5 minutes","300000")
  m.add_item("15 minutes","900000")
  m.add_item("1 hour","3600000")
  m.add_item("3 hours","10800000")
  time=int(m.loop("how long should the chat been disabled for this player?",True))
  net.send("mute_chat "+name+" "+str(time))

 if item=="send "+name+" a warning":
  if name==v.name:
   speak("error: can't send a warning to your self.")
   return
  message=virtual_input.input("type your warning to "+name+" here.",True)
  if message!="":
   net.send("warning "+name+" "+message)
 if item=="move this player":
  try:
   x=int(virtual_input.input("Enter the x. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   y=int(virtual_input.input("Enter the y. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  try:
   z=int(virtual_input.input("Enter the z. Press enter when you're done.",True))
  except ValueError:
   speak("this input isn't legal.")
   return
  net.send("go_player "+str(x)+" "+str(y)+" "+str(z)+" "+name)

 if item=="kick this player":
  q=yesno("are you sure you want to kick "+name+"?")
  if q==1:
   net.send("kick "+name)
 if item=="ban this player":
  q=yesno("are you sure you want to ban "+name+"?")
  if q==1:
   net.send("ban "+name)

def locationsmenu():
 m.reset()
 m.edge_sound=r"sounds\\tracking_menuedge.ogg"
 m.click_sound=r"sounds\\tracking_menuclick.ogg"
 m.enter_sound=r"sounds\\tracking_menuenter.ogg"
 m.close_sound=r"sounds\\tracking_menuclose.ogg"
 m.open_sound=r"sounds\\tracking_menuopen.ogg"
 numbers=[]
 things=[]
 for i in map.locations:
  things.append(i.id)
  numbers.append(get_3d_distance(v.x,v.y,v.z,i.x,i.y,i.z))
 numbers.sort()
 for n in numbers:
  for t in things:
   i=map.get_locations_index(t)
   if i>-1:
    if get_3d_distance(map.locations[i].x,map.locations[i].y,map.locations[i].z,v.x,v.y,v.z)==n:
     m.add_item(map.locations[i].name+" at "+str(map.locations[i].x)+", "+str(map.locations[i].y)+", "+str(map.locations[i].z),str(map.locations[i].id))
     things.remove(t)
     break
 if v.tracked!=-1:
  m.add_item("stop tracking")
 item=m.loop("which location do you want to track? There are currently "+str(len(map.locations))+" locations on the map.",True)
 if item=="stop tracking":
  speak("stopped tracking")
  v.tracked=-1
 elif item!="":
  try:
   v.tracked=int(item)
   index=map.get_locations_index(v.tracked)
   if index>-1:
    v.track_thing="location"
    speak("tracking "+map.locations[index].name)
  except:
   speak("error with tracking the location")

def corpses_menu(corpses=[]):
 m.reset()
 m.edge_sound=r"sounds\\tracking_menuedge.ogg"
 m.click_sound=r"sounds\\tracking_menuclick.ogg"
 m.enter_sound=r"sounds\\tracking_menuenter.ogg"
 m.close_sound=r"sounds\\tracking_menuclose.ogg"
 m.open_sound=r"sounds\\tracking_menuopen.ogg"
 numbers=[]
 things=[]
 for c in corpses:
  i=map.get_objects_index(c)
  if i==-1:
   continue
  things.append(c)
  numbers.append(get_3d_distance(v.x,v.y,v.z,(map.objects[i].minx+map.objects[i].maxx)/2,(map.objects[i].miny+map.objects[i].maxy)/2,(map.objects[i].minz+map.objects[i].maxz)/2))
 numbers.sort()
 for n in numbers:
  for t in things:
   i=map.get_objects_index(t)
   if i>-1:
    if get_3d_distance((map.objects[i].minx+map.objects[i].maxx)/2,(map.objects[i].miny+map.objects[i].maxy)/2,(map.objects[i].minz+map.objects[i].maxz)/2,v.x,v.y,v.z)==n:
     m.add_item(map.objects[i].name+" at "+str(math.floor((map.objects[i].minx+map.objects[i].maxx)/2))+", "+str(math.floor((map.objects[i].miny+map.objects[i].maxy)/2))+", "+str(math.floor((map.objects[i].minz+map.objects[i].maxz)/2)),str(map.objects[i].id))
     things.remove(t)
     break
 if v.tracked!=-1:
  m.add_item("stop tracking")
 item=m.loop("which corpse do you want to track? There are currently "+str(len(numbers))+" corpses in the range of 30 meter away.",True)
 if item=="stop tracking":
  speak("stopped tracking")
  v.tracked=-1
 elif item!="":
  try:
   v.tracked=int(item)
   index=map.get_objects_index(v.tracked)
   if index>-1:
    v.track_thing="corpse"
    speak("tracking "+map.objects[index].name)
  except:
   speak("error with tracking the corpse")

def server_mega_menu(name,data):
 me=mega_menu.mega_menu()
 me.reset()
 items=data.split("\n")
 for i in items:
  d=i.split(":")
  me.add_item(d[0],d[len(d)-1])
  if d[0]=="check_box":
   me.change_check_box(d[len(d)-1],int(d[1]))
 item=me.loop(name.replace("_"," "),True)
 if item!="":
  send_data=""
  for f in me.items:
   if f.name=="check_box":
    send_data=send_data+f.text.replace(" ","_")+":"+str(f.onoff)+"\n"

  net.send("server_mega_menu_answer "+name+" "+item.replace(" ","_")+" "+send_data)
  v.closing=1
 else:
  try:
   del v.last_sm_name[0]
   del v.last_sm_options[0]
   v.closing=1
   net.send("server_menu_answer "+v.last_sm_name[0]+" "+v.last_sm_options[0])
  except:
   send(v.first_sm)
   v.first_sm=""


def settings_menu(online=False,start_pos=0):
 pos=0
 flag=True
 while flag:
  me=mega_menu.mega_menu()
  me.reset()
  me.add_item("dlg","this is the settings menu. Press tab and shift tab to navigate through the options. Press enter on the ok button when you're done")
  if online==False:
   me.add_item("button","set up account")
  me.add_item("check_box","enable ask to exit")
  me.change_check_box("enable ask to exit",v.askexit)
  me.add_item("check_box","enable shift escape to exit")
  me.change_check_box("enable shift escape to exit",v.shiftexit)
  me.add_item("check_box","enable right control to shoot")
  me.change_check_box("enable right control to shoot",v.right_ctrl)
  me.add_item("check_box","enable speaking characters in input boxes")
  me.change_check_box("enable speaking characters in input boxes",v.speak_chars)
  me.add_item("check_box","enable speaking capital letters in input boxes")
  me.change_check_box("enable speaking capital letters in input boxes",v.speak_cap)
  me.add_item("check_box","enable typing sounds in input boxes")
  me.change_check_box("enable typing sounds in input boxes",v.typing_sounds)
  me.add_item("check_box","enable logging of buffers")
  me.change_check_box("enable logging of buffers",v.allow_log_buffers)
  me.add_item("button","set radar scanning time. currently it is "+str(v.radartime)+" miliseconds")
  me.add_item("button","set language")
  me.add_item("button","reload current language. Useful when you are creating one")
  me.add_item("button","ok")
  item=me.loop(me.items[me.pos].text+", "+me.items[me.pos].sort,online)
  if item=="set up account":
   new_name=virtual_input.input("type your name here. Currently it is "+v.name,online)
   if new_name=="":
    pos=me.pos
   else:
    v.name=new_name
    v.name=v.name.replace(" ","_")
    new_password=virtual_input.input("type your password here.",online,"",True)
    if new_password=="":
     pos=me.pos
    else:
     new_password=new_password.replace(" ","_")
     v.password=new_password
     pos=me.pos

  if item=="set radar scanning time. currently it is "+str(v.radartime)+" miliseconds":
   time=-1
   try:
    time=int(virtual_input.input("Type here your new radar scan time. It must be a figure between 100 and 2000",online,"",False,True))
   except:
    pos=me.pos
   if time==-1:
    pos=me.pos
    speak("this input isn't legal.")
   if time<100 or time>=2001:
    pos=me.pos
    speak("this input isn't legal.")
   else:
    v.radartime=time
    pos=me.pos
  if item=="":
   speak("canceled")
   flag=False
  if item=="set language":
   language_menu(online)
  if item=="reload current language. Useful when you are creating one":
   speak(v.language)
   v.t=translator.translator(v.language,r"languages\\"+v.language+".txt")
   speak("done")

  if item=="ok":
   v.speak_cap=me.get_check_box("enable speaking capital letters in input boxes")
   v.typing_sounds=me.get_check_box("enable typing sounds in input boxes")
   v.speak_chars=me.get_check_box("enable speaking characters in input boxes")
   v.askexit=me.get_check_box("enable ask to exit")
   v.right_ctrl=me.get_check_box("enable right control to shoot")
   v.shiftexit=me.get_check_box("enable shift escape to exit")
   v.allow_log_buffers=me.get_check_box("enable logging of buffers")
   flag=False
   speak("settings saved")
 return

def rules_menu():
 v.msp.play_stationary(r"sounds\\menuopen.ogg")
 flag=True
 while flag:
  me=mega_menu.mega_menu()
  me.reset()
  me.add_item("dlg","Before you can continue you have to agree to our rules. Please use tab and shift tab to navigate through the options.")
  me.add_item("button","view rules")
  me.add_item("check_box","I agree to the rules")
  me.add_item("button","continue")
  item=me.loop(me.items[me.pos].text+", "+me.items[me.pos].sort,False)
  if item=="view rules":
   m.reset()
   for l in v.rules_data:
    m.add_item(l)
   m.loop("view the rules here")
  if item=="continue":
   if me.get_check_box("I agree to the rules")==1:
    v.rules=1
    flag=False
   else:
    speak("you haven't agreed to the rules yet.")

def learn_sounds_menu():
 m.reset()
 m.edge_sound="sounds\menuedge.ogg"
 m.click_sound="sounds\menuclick.ogg"
 m.close_sound="sounds\menuclose.ogg"
 m.open_sound="sounds\menuopen.ogg"
 m.add_item("You start to check with your infrared scanner","infrared_scannerclick.ogg")
 m.add_item("The infrared scanner didn't found any player","infrared_scannerfailed.ogg")
 m.add_item("The infrared scanner found a player. This sound will play at the player's position","infrared_scannerfound.ogg")
 m.add_item("The infrared scanner found a player that is a member of your team. This sound will play at the player's position","infrared_scannerteamfound.ogg")
 m.add_item("you hit a object that is more than 10 meter away from you","objectping.ogg")
 m.add_item("you hit a player that is more than 10 meter away from you","playerpingsmall.ogg")
 m.add_item("you hit a player with a headshot","headshotping.ogg")
 m.add_item("a player joins the map","mapjoin.ogg")
 m.add_item("a player leaves the map","mapleave.ogg")
 m.add_item("The simon sound that corresponds with the down arrow key.","simon1.ogg")
 m.add_item("The simon sound that corresponds with the left arrow key.","simon2.ogg")
 m.add_item("The simon sound that corresponds with the up arrow key.","simon3.ogg")
 m.add_item("The simon sound that corresponds with the right arrow key.","simon4.ogg")
 m.add_item("The radar detects a gap","radarair.ogg")
 m.add_item("You're tracking a location. This sound plays at the position that you are tracking.","location.ogg")
 m.add_item("You found the location that you are tracking.","locationfind.ogg")

 f=True
 while f:
  item=m.loop("press enter on a sound to hear it.",False)
  if item !="":
   s=sound_pool.sound.sound()
   s.load(r"sounds\\"+item,True)
   s.play()
  if item=="":
   break

def language_menu(online=False):
 m.reset()
 m.edge_sound="sounds\menuedge.ogg"
 m.click_sound="sounds\menuclick.ogg"
 m.enter_sound="sounds\menuenter.ogg"
 m.close_sound="sounds\menuclose.ogg"
 m.open_sound="sounds\menuopen.ogg"
 script_path = os.path.dirname(os.path.abspath(__file__))
 folder_path = os.path.join(script_path, 'languages')
 m.add_item("English. Default","English")
 for filename in os.listdir(folder_path):
  m.add_item(filename.replace(".txt",""))
 item=m.loop("select a language",online)
 v.language=item
 v.t=translator.translator(v.language,r"languages\\"+v.language+".txt")

def table_menu(itemlist):
 sqmo=square_menu.online_square_menu()
 weapons=itemlist.split("\n")
 sqmo.reset()
 sqmo.enter_sound="sounds\weaponpick.ogg"
 sqmo.set_cords(math.ceil(len(weapons)/2),2)
 for w in weapons:
   sqmo.add_item(math.floor(weapons.index(w)/2),weapons.index(w)%2,w) 
 sqmo.stopping=True
 sqmo.stoptime=30000

 i=0
 while i==0:
  item = sqmo.loop("select a weapon", True)
  if item!="":
   net.send(f"server_menu_answer table_menu {item}")
   i=1

def code_menu(question):
 sqmo=square_menu.online_square_menu()
 sqmo.reset()
 sqmo.enter_sound="sounds\%name.ogg"
 sqmo.set_cords(3,4)
 sqmo.add_item(0,0,"1")
 sqmo.add_item(1,0,"2")
 sqmo.add_item(2,0,"3")
 sqmo.add_item(0,1,"4")
 sqmo.add_item(1,1,"5")
 sqmo.add_item(2,1,"6")
 sqmo.add_item(0,2,"7")
 sqmo.add_item(1,2,"8")
 sqmo.add_item(2,2,"9")
 sqmo.add_item(0,3,"read code","readcode")
 sqmo.add_item(1,3,"0")
 sqmo.add_item(2,3,"delete")

 speak(question)
 i=0
 total_code=""
 while i<4:
  item=sqmo.loop("",True)
  if item!="": 
   if item=="readcode":
    if total_code!="":
     speak(total_code)
    else:
     speak("no input")
   elif item=="delete":
    items=list(total_code)
    try:
     items[len(items)-1]=""
     i-=1
    except:
     pass
    total_code="".join(items)
   else:
    total_code=total_code+item
    i+=1
  else:
   speak("canceled")
   return ""
 return total_code