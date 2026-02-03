import quests
def remove_figures_from_string(string):
    result = ''
    for karakter in string:
        if not karakter.isnumeric():
            result += karakter
    return result
import math
import random
import rotation
import numpy as np
import map
import v
v.get()

def get_players_index(name):
 for p in v.clients:
  if p.data["name"].lower()==name.lower():
   return v.clients.index(p)
 return -1

def send_all(message,map=""):
 v.send_packet_to_clients(message,v.clients,map)


def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)
class scanner():
 def __init__(self,x,y,z,scanner_map,dir,updown,owner,mode):
  self.mode=mode
  self.id=len(scanners)
  self.last_gap=0
  self.updown=updown
  self.range=30
  self.x=x
  self.y=y
  self.z=z
  self.ox=self.x
  self.oy=self.y
  self.oz=self.z
  self.map=scanner_map
  self.dir=dir
  self.owner=owner
  self.text=""
  self.got=[]
  self.dist=0
  self.spread=2
  self.up=self.spread+1
  self.down=self.spread+1
  self.left=self.spread+1
  self.right=self.spread+1
  self.front=self.spread+1
  self.back=self.spread+1
  if self.updown==-2 and map.get_platform(self.x,self.y,self.z-1,self.map)=="wall":
   self.x,self.y=rotation.move(self.x,self.y,self.dir)

  index=get_players_index(self.owner)
  if index>-1:
   if v.clients[index].skill_data["Eyes training"]["active"]==True:
    extra=(v.clients[index].skill_data["Eyes training"]["level"]/10)+1
    self.range=self.range*extra
  self.clients=[]
  self.check_clients()
 def check_clients(self):
  for c in v.clients:
   dist=get_3d_distance(self.x,self.y,self.z,c.data["x"],c.data["y"],c.data["z"])
   if dist<=self.spread+self.range and c.data["name"]!=self.owner and c.data["death"]==False and c.lobby==False  and c.data["map"]==self.map:
    self.clients.append(c)

 def update(self):
  for j in range(int(self.range)+1):
   self.dist+=1
   if self.updown==-1 or self.updown==0 or self.updown==1:
    if self.updown==-1:
      self.z-=1
    if self.updown==1:
      self.z+=1
    self.x,self.y=rotation.move(self.x,self.y,self.dir)
   if self.updown==-2:
     self.z-=1
   if self.updown==2:
     self.z+=1
   if map.get_platform(self.x,self.y,self.z,self.map)=="" and self.mode==2 and self.updown==0 or map.get_platform(self.x,self.y,self.z,self.map)=="blank" and self.mode==2 and self.updown==0:
    z=self.z
    gapdist=0
    while map.get_platform(self.x,self.y,z,self.map)=="" or map.get_platform(self.x,self.y,z,self.map)=="blank":
     z-=1
     gapdist+=1
     if gapdist>=100:
      break
    if self.last_gap!=gapdist:
     self.text=self.text+" A "+str(gapdist)+" meter deep gap is "+str(self.dist)+" meter away,"
     self.last_gap=gapdist
     self.remove()
     return


   for i in range(1, self.spread + 1):
    if self.left >= i and map.get_platform(self.x-i, self.y, self.z, self.map) == "wall":
     self.left = i - 1
    if self.right >= i and map.get_platform(self.x+i, self.y, self.z, self.map) == "wall":
     self.right = i - 1
    if self.up >= i and map.get_platform(self.x, self.y, self.z+1, self.map) == "wall":
     self.up = i - 1
    if self.down >= i and map.get_platform(self.x, self.y, self.z-i, self.map) == "wall":
     self.down = i - 1
    if self.back >= i and map.get_platform(self.x, self.y-i, self.z, self.map) == "wall":
     self.back = i - 1
    if self.front >= i and map.get_platform(self.x, self.y+i, self.z, self.map) == "wall":
     self.front = i - 1
   o=map.get_objects_index(map.get_object(self.x,self.y,self.z,self.map))
   if o!="" and str(o) not in self.got:
     if map.objects[o].name[0:6]=="corpse" and self.mode!=1:
      if hasattr(map.objects[o], "team"):
       map.objects[o].showname=map.objects[o].name+" of the "+map.objects[o].team+" team with "+str(map.objects[o].health)+" of "+str(map.objects[o].max_health)+" Solidity Points"
       self.text=self.text+" a "+map.objects[o].showname+" is "+str(self.dist)+" meter away"
      else:
       self.text=self.text+" a "+remove_figures_from_string(map.objects[o].showname)+" is "+str(self.dist)+" meter away"
      self.remove()
      return
   if map.get_quest_item(self.x,self.y,self.z,self.map)!="":
    for q in v.all_quests:
     qe=quests.quest(q)
     if qe.item==map.get_quest_item(self.x,self.y,self.z,self.map):
      index=get_players_index(self.owner)
      if index>-1:
       if v.clients[index].quests[q]==0:
        self.text=self.text+" the quest_item "+map.get_quest_item(self.x,self.y,self.z,self.map)+" is "+str(self.dist)+" meter away,"
        self.remove()
        return
   if map.get_platform(self.x,self.y,self.z,self.map)=="wall":
    id=0
    ob=map.get_walls_index(self.x,self.y,self.z,self.map)
    if ob!=-1:
     if map.walls[ob].id==0:
      f=remove_figures_from_string(map.get_wall(self.x,self.y,self.z,self.map))
      f=f.replace("wall","")
      f=f+" wall"
      self.text=self.text+" a "+f+" is "+str(self.dist)+" meter away"
      self.remove()
      return
     o=map.get_objects_index(map.walls[ob].id)
     if o!="" and o not in self.got:
      if map.objects[o].name[0:6]=="corpse" and self.mode==1:
       return
      if self.mode!=3 or self.mode==3 and map.objects[o].name!="window":
       if hasattr(map.objects[o], "team"):
        map.objects[o].showname=map.objects[o].name+" of the "+map.objects[o].team+" team with "+str(map.objects[o].health)+" of "+str(map.objects[o].max_health)+" Solidity Points"
        self.text=self.text+" a "+map.objects[o].showname+" is "+str(self.dist)+" meter away"
       else:
        self.text=self.text+" a "+remove_figures_from_string(map.objects[o].showname)+" is "+str(self.dist)+" meter away"

      if map.get_wall(self.x,self.y,self.z,self.map)!="wallglass":
       self.remove()
       return
      else:
       self.got.append(o)

   for c in self.clients:
    dist=get_3d_distance(self.x,self.y,self.z,c.data["x"],c.data["y"],c.data["z"])
    if dist<=self.spread and c.data["name"] not in self.got:
     delta_left=self.x-c.data["x"]
     delta_back=self.y-c.data["y"]
     delta_down=self.z-c.data["z"]
     delta_right=c.data["x"]-self.x
     delta_front=c.data["y"]-self.y
     delta_up=c.data["z"]-self.z
     if delta_left-0.5<=self.left and delta_right-0.5<=self.right and delta_up-0.5<=self.up and delta_down-0.5<=self.down and delta_back-0.5<=self.back and delta_front-0.5<=self.front:
      self.got.append(c.data["name"])
      self.text=self.text+c.data["name"]+" is "+str(round(self.dist+dist))+" meter away"
   if self.dist>self.range:
    if self.text=="":
     self.text="nothing in front of you"
    self.remove()
    return
 def remove(self):
  index=get_players_index(self.owner)
  if index!=-1:
   v.clients[index].send("speak "+self.text)
   scanners.remove(self)

scanners=[]
def spawn_scanner(x,y,z,map,dir,updown,owner,mode):
 scanners.append(scanner(x,y,z,map,dir,updown,owner,mode))
