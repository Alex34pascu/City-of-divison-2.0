import armor
import rotation
import teams
import event
import threading
import asyncio
import math
import numpy as np
import random
import timer
import map
import threading
from _thread import *
import v
v.get()


def send_all(message,map=""):
 v.send_packet_to_clients(message,v.clients,map)

def get_1d_distance(x1, x2):
	"""returns the distance on a 1-dimensional plane from x1 to x2"""
	if x1>x2:
		return x1 - x2
	else:
		return x2 - x1


def get_2d_distance(x1, y1, x2, y2):
 """returns the pythagorean distance between two points on an x-y plane."""
 x = get_1d_distance(x1 - x2)
 y = get_1d_distance(y1, y2)
 return math.sqrt(x * x + y * y)


def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)
def get_players_index(name):
 for p in v.clients:
  if p.data["name"].lower()==name.lower():
   return v.clients.index(p)
 return -1

class weapon():
 def __init__(self,name):
  self.name=name
  self.tier=0
  if self.name=="knife":
   self.melee=True
   self.max_ammo=0
   self.reloadtime=0
   self.damage=600
   self.range=3
   self.spread=1
   self.needed_ammo=""
   self.sort="melee"
   self.level=1
   self.tier=1
  elif self.name=="machete":
   self.melee=True
   self.max_ammo=0
   self.reloadtime=0
   self.damage=500
   self.range=6
   self.spread=2
   self.needed_ammo=""
   self.sort="melee"
   self.level=1
   self.tier=2
  elif self.name=="flail":
   self.melee=True
   self.max_ammo=0
   self.reloadtime=0
   self.damage=500
   self.range=6
   self.spread=2
   self.needed_ammo=""
   self.sort="melee"
   self.level=25
   self.tier=3
  elif self.name=="Winchester_Model_24":
   self.melee=False
   self.max_ammo=2
   self.reloadtime=3260
   self.damage=850
   self.spread=2
   self.range=16
   self.needed_ammo="12_gauge_ammo"
   self.sort="shotgun"
   self.level=1
   self.tier=2
  elif self.name=="barrett_M107A1":
   self.melee=False
   self.max_ammo=5
   self.reloadtime=5237
   self.damage=800
   self.spread=2
   self.range=90
   self.needed_ammo="50bmg_round"
   self.sort="sniper_rifle"
   self.level=1
   self.tier=2
  elif self.name=="dsr50":
   self.melee=False
   self.max_ammo=1
   self.reloadtime=2550
   self.damage=800
   self.spread=2
   self.range=120
   self.needed_ammo="50bmg_round"
   self.sort="sniper_rifle"
   self.level=35
   self.tier=3

  elif self.name=="SVD_Dragunov":
   self.melee=False
   self.max_ammo=10
   self.reloadtime=5700
   self.damage=650
   self.spread=2
   self.range=60
   self.needed_ammo="7.62mm_ammo"
   self.sort="marksman_rifle"
   self.level=50
   self.tier=3
  elif self.name=="AR10":
   self.melee=False
   self.max_ammo=15
   self.reloadtime=3130
   self.damage=400
   self.spread=2
   self.range=45
   self.needed_ammo="7.62mm_ammo"
   self.sort="marksman_rifle"
   self.level=1
   self.tier=2

  elif self.name=="Benelli_M4":
   self.melee=False
   self.max_ammo=6
   self.reloadtime=2110
   self.spread=2
   self.damage=650
   self.range=17
   self.needed_ammo="12_gauge_ammo"
   self.sort="shotgun"
   self.level=1
   self.tier=1
  elif self.name=="remington870xs":
   self.melee=False
   self.max_ammo=4
   self.reloadtime=6300
   self.spread=2
   self.damage=750
   self.range=20
   self.needed_ammo="12_gauge_ammo"
   self.sort="shotgun"
   self.level=40
   self.tier=3
  elif self.name=="fn_f2000":
   self.melee=False
   self.max_ammo=20
   self.reloadtime=3500
   self.spread=2
   self.damage=130
   self.range=30
   self.needed_ammo="5.56mm_ammo"
   self.sort="assault_rifle"
   self.level=1
   self.tier=2
  elif self.name=="fn_p90":
   self.melee=False
   self.max_ammo=50
   self.reloadtime=2700
   self.spread=2
   self.damage=80
   self.range=25
   self.needed_ammo="5.7x28mm_ammo"
   self.sort="sub_machine_gun"
   self.level=1
   self.tier=3
  elif self.name=="ARX160":
   self.melee=False
   self.max_ammo=30
   self.reloadtime=3900
   self.spread=2
   self.damage=100
   self.range=30
   self.needed_ammo="5.56mm_ammo"
   self.sort="assault_rifle"
   self.level=1
   self.tier=1
  elif self.name=="ak47":
   self.melee=False
   self.max_ammo=30
   self.reloadtime=4400
   self.spread=2
   self.damage=120
   self.range=30
   self.needed_ammo="7.62mm_ammo"
   self.sort="assault_rifle"
   self.level=15
   self.tier=3

  elif self.name=="MP7":
   self.melee=False
   self.max_ammo=40
   self.reloadtime=2550
   self.spread=2
   self.damage=75
   self.range=25
   self.needed_ammo="4.6x30mm_ammo"
   self.sort="sub_machine_gun"
   self.level=1
   self.tier=1
  elif self.name=="mp5":
   self.melee=False
   self.max_ammo=30
   self.reloadtime=3600
   self.spread=2
   self.damage=100
   self.range=20
   self.needed_ammo="9mm_ammo"
   self.sort="sub_machine_gun"
   self.level=30
   self.tier=3
  elif self.name=="hk_mg4":
   self.melee=False
   self.max_ammo=30
   self.reloadtime=2333
   self.spread=2
   self.damage=140
   self.range=40
   self.needed_ammo="5.56mm_ammo"
   self.sort="machine_gun"
   self.level=20
   self.tier=2
  elif self.name=="m2_browning":
   self.melee=False
   self.max_ammo=50
   self.reloadtime=6180
   self.spread=2
   self.damage=180
   self.range=50
   self.needed_ammo="50bmg_round"
   self.sort="machine_gun"
   self.level=1
   self.tier=3
  elif self.name=="FN_509_tactical":
   self.melee=False
   self.max_ammo=10
   self.reloadtime=2200
   self.spread=2
   self.damage=300
   self.range=30
   self.needed_ammo="9mm_ammo"
   self.sort="pistol"
   self.level=1
   self.tier=3

  elif self.name=="ruger_redhawk":
   self.melee=False
   self.max_ammo=6
   self.reloadtime=6930
   self.spread=2
   self.damage=500
   self.range=20
   self.needed_ammo=".44_magnum_ammo"
   self.sort="revolver"
   self.level=10
   self.tier=2
  elif self.name=="smith_n_wesson_model29":
   self.melee=False
   self.max_ammo=6
   self.reloadtime=4950
   self.spread=2
   self.damage=350
   self.range=23
   self.needed_ammo=".44_magnum_ammo"
   self.sort="revolver"
   self.level=1
   self.tier=2

  elif self.name=="colt_m1911":
   self.melee=False
   self.max_ammo=8
   self.reloadtime=2245
   self.spread=2
   self.damage=250
   self.range=25
   self.needed_ammo="45ACP_ammo"
   self.sort="pistol"
   self.level=1
   self.tier=1
  elif self.name=="beretta92A1":
   self.melee=False
   self.max_ammo=17
   self.reloadtime=3250
   self.spread=2
   self.damage=225
   self.range=25
   self.needed_ammo="9mm_ammo"
   self.sort="pistol"
   self.level=1
   self.tier=2
  else:
   self.level=0
   self.spread=0
   self.melee=False
   self.max_ammo=0
   self.reloadtime=0
   self.damage=0
   self.range=0
   self.needed_ammo=""
   self.sort=""
 def get_tier_formula(self):
   return 0.5 * self.tier + 0.5

blocking_bmg_objects=["planter","machine","metal_fortress","lamppost","tree"]

class bullet():
 def __init__(self,x,y,z,owner,dir,updown,bullet_map,name,sort,damage,range,spread):
  we=weapon(name)
  self.ammo=we.needed_ammo
  self.gotten_objects=[]
  self.id=random.randint(0,999999999)
  self.team=""
  self.landing=False
  self.power=random.randint(1,4000)
  self.owner=owner
  self.updown=updown
  self.spread=spread
  self.x=x
  self.y=y
  self.z=z
  self.dir=dir
  self.map=bullet_map
  self.name=name
  self.sort=sort
  self.damage=damage
  self.org_damage=damage
  self.range=range
  self.dist=0
  self.gotimer=timer.timer()
  self.gotime=50
  self.org_facing=0
  index=get_players_index(self.owner)
  if index>-1:
   self.scatter=False
   if v.clients[index].drawn_weapon and "choke_tube" in v.clients[index].drawn_weapon.modifications:
    self.scatter=True

   self.org_facing=v.clients[index].data["facing"]

  self.type=self.name
  if self.updown==-2 and map.get_platform(self.x,self.y,self.z-1,self.map)=="wall":
   self.x,self.y=rotation.move(self.x,self.y,self.dir)
#  if self.sort=="assault_rifle":
#   try:
#    index=get_players_index(self.owner)
#    if index>-1:
#     if v.clients[index].skill_data["sharpshooter mastery"]["active"]==True and self.sort=="assault_rifle":
#      self.range=self.range+round((v.clients[index].skill_data["sharpshooter mastery"]["level"]*3))
#   except:
#    pass
  if self.sort=="pistol" or self.sort=="assault_rifle" or self.sort=="sub_machine_gun":
   self.type="small"
  if self.sort=="sniper_rifle" or self.sort=="shotgun" or self.sort=="machine_gun" or self.sort=="revolver" or self.sort=="marksman_rifle":
   self.type="large"
   self.mindamage=40
  try:
   index=get_players_index(self.owner)
   if index>-1:
    if v.clients[index].data["careful_aiming"]==True:
     self.team=teams.get_team(v.clients[index].data["name"])
    if v.clients[index].skill_data["steady aim"]["active"]==True:
     self.mindamage=40-(v.clients[index].skill_data["steady aim"]["level"]*3)
    if v.clients[index].skill_data["DMR precision"]["active"]==True and self.sort=="marksman_rifle":
     if v.clients[index].data["dmr_shooting"]:
      v.clients[index].data["dmr_shooting"]=False
      v.clients[index].data["dmr_streak"]=0
     v.clients[index].data["dmr_shooting"]=True
    else:
     v.clients[index].data["dmr_shooting"]=False
     v.clients[index].data["dmr_streak"]=0

    if v.clients[index].skill_data["SMG experience"]["active"]==True and self.sort=="sub_machine_gun":
     self.damage+=v.clients[index].data["smg_streak"]*4
    if v.clients[index].skill_data["SMG experience"]["active"]==True and self.sort!="sub_machine_gun":
     v.clients[index].data["smg_streak"]=0
    if v.clients[index].skill_data["sniper mastery"]["active"]==True and self.sort=="sniper_rifle":
     self.spread+=round((v.clients[index].skill_data["sniper mastery"]["level"]*0.2))
  except:
   pass
  if self.dir>=360:
   self.dir-=360
  if self.name=="thrown_knife":
   self.gotime=210
  if self.name=="flail":
   self.gotime=150
  if self.name=="machete_swing":
   self.gotime=850
  self.clients=[]
  self.send_clients=[]
  for c in v.clients:
   if c.lobby==True or c.data["map"]!=self.map or c.data["health"]<0:
    continue
   dist=get_3d_distance(self.x,self.y,self.z,c.data["x"],c.data["y"],c.data["z"])
   if dist<=(self.spread*2)+(self.range*2) and c.data["death"]==False and c.data["map"]==self.map or self.dist<=40 and c.data["map"]==self.map:
    self.clients.append(c)
   if dist<=(self.range*2)+self.spread+40 and c.data["death"]==False or self.dist<=40  and c.data["map"]==self.map:
    self.send_clients.append(c)

  self.up=self.spread+1
  self.down=self.spread+1
  self.left=self.spread+1
  self.right=self.spread+1
  self.front=self.spread+1
  self.back=self.spread+1
  if self.name=="thrown_knife":
   self.mindamage=25
 def increase_spread(self, amount):
         self.left=amount
         self.right=amount
         self.up=amount
         self.down=amount
         self.front=amount
         self.back=amount

 def send(self,message):
  v.send_packet_to_clients(message,self.send_clients,self.map)

 def run(self):
  if self.gotimer.elapsed()<self.gotime:
   if self.landing==True:
    if self.name!="thrown_knife":
     v.bullets.remove(self)
     return
    else:
     while map.get_platform(self.x,self.y,self.z,self.map)=="" or map.get_platform(self.x,self.y,self.z,self.map)=="blank":
      self.z-=1
     self.send("play_sound "+self.name+"land"+v.get_tile_type(map.get_platform(self.x,self.y,self.z,self.map),["grass","dirt","water"])+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
     v.bullets.remove(self)
    return


  else:
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

    if self.sort=="shotgun" or self.name=="thrown_knife":
     if self.damage>100:
      self.damage-=self.mindamage

    for i in range(1,self.spread + 1):
     if self.left >=i and map.get_platform(self.x-i, self.y, self.z, self.map) == "wall":
      self.left = i - 1
     if self.right >= i and map.get_platform(self.x+i, self.y, self.z, self.map) == "wall":
      self.right = i - 1
     if self.back >= i and map.get_platform(self.x, self.y-i, self.z, self.map) == "wall":
      self.back = i - 1
     if self.front >= i and map.get_platform(self.x, self.y+i, self.z, self.map) == "wall":
      self.front =  i - 1
     if self.up >= i and map.get_platform(self.x, self.y, self.z+i, self.map) == "wall":
      self.up = i - 1
     if self.down >= i and map.get_platform(self.x, self.y, self.z-i, self.map) == "wall":
      self.down = i - 1

    if self.dist>self.range:
     self.landing=True
     self.gotimer.restart()
    if self.name=="thrown_knife":
     self.gotime=400


    if map.get_platform(self.x,self.y,self.z,self.map)=="wall":
     id=0
     ob=map.get_walls_index(self.x,self.y,self.z,self.map)
     if ob!=-1:
      if map.walls[ob].id==0:
       index=get_players_index(self.owner)
       if index>-1:
        if self.org_facing==self.dir and self.name=="flail" or self.name!="flail":
         self.send("play_sound "+self.sort+"rico"+str(random.randint(1,5))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0|n|play_sound bullet"+self.type+v.get_wall_tile_type(map.get_wall(self.x,self.y,self.z,self.map),["metal"])+"hit"+str(random.randint(1,5))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0|n|play_sound "+self.name+"rico.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
       v.bullets.remove(self)
       return
      o=map.get_objects_index(map.walls[ob].id)
      index=get_players_index(self.owner)
      if index>-1:
       if str(o) in v.clients[index].data["machete_swing_got"]:
        v.bullets.remove(self)
        return

      if o!="" and map.objects[o].map==self.map:
       if map.objects[o].hit_bullets==False:
        if self.org_facing==self.dir and self.name=="flail" or self.name!="flail":
         self.send("play_sound "+self.sort+"rico"+str(random.randint(1,5))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0|n|play_sound bullet"+self.type+v.get_wall_tile_type(map.get_wall(self.x,self.y,self.z,self.map),["metal"])+"hit"+str(random.randint(1,5))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0|n|play_sound "+self.name+"rico.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
        v.bullets.remove(self)
        return
       if map.objects[o].hitable==True and map.objects[o].hitsounds!="bush" and map.objects[o].hit_bullets==True and o not in self.gotten_objects or map.objects[o].hitsounds=="bush" and self.power<=map.objects[o].health and o not in self.gotten_objects:
        self.gotten_objects.append(o)
        old_damage=self.damage
        if self.type=="small":
         self.damage=20
        if self.type=="large":
         self.damage=200
        if self.name=="m2_browning":
         self.damage=400
        if self.type=="machete_swing":
         self.damage=100
        if self.type=="thrown_knife":
         self.damage=20
        if self.name=="hk_mg4":
         self.damage=15
        if self.type=="knife":
         self.damage=5
         if hasattr(map.objects[o], "last_team"):
          self.damage=round(self.damage*0.1)
        if self.type=="machete":
         self.damage=50
         if hasattr(map.objects[o], "last_team"):
          self.damage=round(self.damage*0.1)
        if self.type=="flail":
         self.damage=100
         if hasattr(map.objects[o], "last_team"):
          self.damage=round(self.damage*0.5)

        map.objects[o].health-=self.damage
        map.objects[o].last_hit=self.owner+"'s "+self.name

        if hasattr(map.objects[o], "last_team"):
         map.objects[o].last_team=teams.get_team(self.owner)

        if map.objects[o].health<=0 and map.objects[o].destroytime==0 and map.objects[o].name=="window":
         b=self
         b.increase_spread(1)
         b.damage=old_damage/2
         v.bullets.append(b)
        index=get_players_index(self.owner)
        if index>-1:
          if self.dist>=10:
           v.clients[index].send("play_sound objectping.ogg 0 0 0 1 0|n|")
        if map.objects[o].name!="window":
         if self.name=="machete_swing":
          self.type="machete"
         if self.name=="thrown_knife":
          self.type="machete"

         self.send("play_sound "+map.objects[o].hitsounds+"hit"+self.type+str(random.randint(1,3))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
        else:
         if self.sort=="melee":
          self.send("play_sound "+map.objects[o].hitsounds+"meleehit"+str(random.randint(1,5))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
         else:
          self.send("play_sound "+map.objects[o].hitsounds+"bullethit"+str(random.randint(1,5))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
         if map.objects[o].health<=35:
          self.send("play_sound "+map.objects[o].hitsounds+"crack"+str(random.randint(1,5))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
        if map.objects[o].destroying==False:
         map.objects[o].check_health()
         if map.objects[o].name=="metal_fortress" and self.owner not in map.objects[o].alarm_players.keys() and map.objects[o].data["alarm"]==True:
          map.objects[o].alarm_players[self.owner]=timer.timer()
        if self.name=="machete_swing" or self.name=="flail":

         index=get_players_index(self.owner)
         if index>-1:
          v.clients[index].data["machete_swing_got"].append(str(map.objects[o].id))
        if self.ammo!="50bmg_round" or self.ammo=="50bmg_round" and map.objects[o].hitsounds in blocking_bmg_objects:
         v.bullets.remove(self)
         return
        else:
         self.increase_spread(0)


    for c in self.clients:
     dist=get_3d_distance(self.x,self.y,self.z,c.data["x"],c.data["y"],c.data["z"])
     if dist<=self.spread:
      delta_left=self.x-c.data["x"]
      delta_back=self.y-c.data["y"]
      delta_down=self.z-c.data["z"]
      delta_right=c.data["x"]-self.x
      delta_front=c.data["y"]-self.y
      delta_up=c.data["z"]-self.z
      index=get_players_index(self.owner)
      if index>-1:
       if c.data["name"] in v.clients[index].data["machete_swing_got"]:
        continue
      if delta_left-0.5<=self.left and delta_right-0.5<=self.right and delta_up-0.5<=self.up and delta_down-0.5<=self.down and delta_back-0.5<=self.back and delta_front-0.5<=self.front and c.data["death"]==False and c.data["name"]!=self.owner:
       if self.team!="" and self.team==teams.get_team(c.data["name"]):
        continue
       v.clients[index].data["machete_swing_got"].append(c.data["name"])
       headshot=False
       if self.z>c.data["z"] and self.sort!="melee" or self.updown<0 and self.sort!="melee":
        headshot=True
        event.add_score(self.owner,"making head shots",1)
       c.data["last_hit"]=self.owner+"'s "+self.name
       if headshot==True:
        self.damage=self.damage*1.5
       c.exittimer.restart()
       used_armor=""
       for a in c.armor:
        if c.armor[a]["wearing"]==True:
         ar=armor.armor(a)
         if ar.type=="head" and headshot==True or ar.type=="body" and headshot==False:
          c.armor[a]["health"]-=self.damage
          if c.armor[a]["health"]<ar.health/2:
           send_all(r"player_sound "+c.data["name"]+" sounds\\"+a+"crack"+str(random.randint(1,3))+".ogg 0")

          if c.armor[a]["health"]<=0:
           c.armor[a]["wearing"]=False
           c.give(a,-1)
           c.armor[a]["health"]=ar.health
           send_all(r"player_sound "+c.data["name"]+" sounds\\"+a+"destroy"+str(random.randint(1,3))+".ogg 0")


          used_armor=a
          if self.type=="small":
           self.damage=self.damage*ar.small_damage
          elif self.type=="large":
           self.damage=self.damage*ar.large_damage
          else:
           self.damage=self.damage*ar.melee_damage

       if used_armor!="":
        headshot=False
       c.data["health"]-=self.damage
       index=get_players_index(self.owner)
       if index>-1:
        v.clients[index].change_statistic("shots hit",1,True)
        if self.dist>v.clients[index].get_statistic("longest shot hit"):
          v.clients[index].change_statistic("longest shot hit",self.dist,False)
        to_send=""
        if headshot==True:
         to_send=to_send+"play_sound headshotping.ogg 0 0 0 1 0|n||n|"
        if used_armor!="":
         to_send=to_send+"play_sound "+used_armor+"ping.ogg 0 0 0 1 0|n||n|"

        if teams.get_team(v.clients[index].data["name"])!="" and teams.get_team(v.clients[index].data["name"])==teams.get_team(c.data["name"]):
         to_send=to_send+"play_sound teamping.ogg 0 0 0 1 0|n||n|"
        else:
         if v.clients[index].skill_data["DMR precision"]["active"]==True:
          v.clients[index].data["dmr_shooting"]=False
          c.data["health"]-=30*v.clients[index].data["dmr_streak"]
          if v.clients[index].data["dmr_streak"]<2+v.clients[index].skill_data["DMR precision"]["level"]:
           v.clients[index].send("play_sound smgstreak.ogg 0 0 0 1 0")
           v.clients[index].data["dmr_streak"]+=1
         if self.dist>=10:
          to_send=to_send+"play_sound playerping"+self.type+".ogg 0 0 0 1 0|n|"
        if to_send!="":
         v.clients[index].send(to_send)
       h=""
       if headshot==True:
        h="player_sound "+c.data["name"]+" sounds\\headshot"+str(random.randint(1,5))+".ogg 0|n|player_sound "+c.data["name"]+" sounds\\headshotlayer"+str(random.randint(1,3))+".ogg 0"
       if self.name=="machete_swing":
        self.send(r"play_sound macheteswinghit"+str(random.randint(1,3))+".ogg "+str(c.data["x"])+" "+str(c.data["y"])+" "+str(c.data["z"])+" 0 0|n|"+h)
       elif self.name=="thrown_knife":
        self.send(r"play_sound knifehit"+str(random.randint(1,5))+".ogg "+str(c.data["x"])+" "+str(c.data["y"])+" "+str(c.data["z"])+" 0 0|n|"+h)
       else:
        if used_armor=="" or self.org_damage==self.damage:
         packet=r"player_sound "+c.data["name"]+" sounds\\"+self.sort+"hit"+str(random.randint(1,5))+".ogg 0|n|player_sound "+c.data["name"]+" sounds\\"+self.name+"hit"+str(random.randint(1,5))+".ogg 0|n|"+h
         if self.scatter:
          packet=packet+"player_sound "+c.data["name"]+" sounds\\scattershotlayer"+str(random.randint(1,5))+".ogg 0"
         self.send(packet)
        else:
         self.send(r"player_sound "+c.data["name"]+" sounds\\"+used_armor+self.type+"hit"+str(random.randint(1,3))+".ogg 0")
       if self.name=="machete_swing":
        self.name="machete"
       if self.name=="thrown_knife":
        self.name="knife"

       c.data["last_weapon"]=self.name
       c.data["last_hit_dir"]=self.dir
       v.bullets.remove(self)
       return



def spawn_bullet(x,y,z,owner,dir,updown,map,name,sort,damage,range,spread):
 b=bullet(x,y,z,owner,dir,updown,map,name,sort,damage,range,spread)
 v.bullets.append(b)
def remove_bullet(id):
 for b in v.bullets:
  if b.id==id:
   del v.bullets[v.bullets.index(b)]