import timer
import math
import random
import rotation
import map as mp
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
class bf():
 def __init__(self,x,y,z,map,owner,dir,weapontype,inv={}, weapon_list=[]):
  self.weapon_list=weapon_list
  self.inv=inv
  self.x=x
  self.y=y
  self.z=z
  self.map=map
  self.owner=owner
  self.dir=dir
  self.falltimer=timer.timer()
  self.falltime=0
  if weapontype=="melee":
   self.falltime=1550
  else:
   self.falltime=random.randint(650,900)
  nx,ny=rotation.move(self.x,self.y,self.dir)
  if mp.get_platform(nx, ny, self.z, self.map)=="wall":
   send_all("play_sound bodyfallwall"+v.get_wall_tile_type(mp.get_wall(nx,ny,self.z,self.map),["bush","wood","cabinet","metal","generic","stone2","furniture"])+".ogg "+str(nx)+" "+str(ny)+" "+str(self.z)+" 0 0",self.map)
  else:
   self.x=round(nx)
   self.y=round(ny)
 def fall(self):
   tile=mp.get_platform(self.x,self.y,self.z,self.map)
   if tile!="" and tile!="blank":
    self.x=round(self.x)
    self.y=round(self.y)
    o=mp.object(self.x-1,self.x+1,self.y-1,self.y+1,self.z,self.z+1,"corpse_of_"+self.owner,1,self.map)
    o.weapons=self.weapon_list
    mp.objects[str(o.id)]=o
    minx,maxx,miny,maxy=o.minx,o.maxx,o.miny,o.maxy
    if minx<0:
     minx=0
    if maxx<0:
     maxx=0
    if minx>600:
     minx=600
    if maxx>600:
     maxx=600
    if miny<0:
     miny=0
    if maxy<0:
     maxy=0
    if miny>600:
     miny=600
    if maxy>600:
     maxy=600
    for l in range(round(minx/10)-1,round(maxx/10)):
     for m in range(round(miny/10)-1,round(maxy/10)):
      mp.objects_x[l][m].append(o)
    forbidden_list = ["locker", "team_phone", "metal_fortress", "metal_fortress_construction_kit", "metal_sheat"]
    self.inv = {key: value for key, value in self.inv.items() if key not in forbidden_list}
    o.loot=self.inv
    send_all("play_sound "+v.get_tile_type(tile,["dirt","gravel","water","grass","metal"])+"bodyfall"+str(random.randint(1,3))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0",self.map)
    v.bodyfalls.remove(self)
   else:
    self.z-=1
    if mp.get_platform(self.x,self.y,self.z,self.map)!="blank" and mp.get_platform(self.x,self.y,self.z,self.map)!="":
     send_all("play_sound bodyland.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0",self.map)
def spawn_bodyfall(x,y,z,map,owner,dir,weapontype,inv={},weapon_list=[]):
 v.bodyfalls.append(bf(x,y,z,map,owner,dir,weapontype,inv,weapon_list))
