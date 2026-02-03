import pygame, pygame.locals as pl
pygame.init()

import music
import numpy as np
import cmath
import math
maxx=1000
maxy=1000
def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)

import v
v.get()
import timer
import random
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 text=v.vertaal_tekst(text,"nl")
 speatch.output(text)
import sound_pool
import rotation
def create_formule(x1,y1,x2,y2):
 delta_x=x2-x1
 delta_y=y2-y1
 a=0
 try:
  a=delta_y/delta_x
 except:
  pass
 b=x1*a
 b=y1-b
 return a,b
class platform():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,tile,id):
  self.id=id
  self.minx=minx
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.tile=tile


platforms=[]
platforms_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    platforms_x.append(row)
def get_platform(x, y, z):
    x=round(x)
    y=round(y)
    z=round(z)

    final = ""
    
    check_x = round(x / 10)  
    check_y = round(y / 10)  

    check_x = max(0, min(check_x, 60))  
    check_y = max(0, min(check_y, 60))  

    # Zorg ervoor dat je toegang krijgt tot de juiste platformen
    platforms = platforms_x[check_x - 1][check_y - 1]  

    if not platforms:
        return final

    for p in reversed(platforms):
        if p.minx <= x <= p.maxx and p.miny <= y <= p.maxy and p.minz <= z <= p.maxz:
            return p.tile
    
    return final


def spawn_platform(minx,maxx,miny,maxy,minz,maxz,tile,id=0):
 p=platform(minx,maxx,miny,maxy,minz,maxz,tile,id)
 platforms.append(p)
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
   platforms_x[l][m].append(p)


class sub_tile():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,tile,id):
  self.id=id
  self.minx=minx
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.tile=tile
def get_sub_tile(x,y,z):
 if get_platform(x,y,z)=="" or get_platform(x,y,z)=="blank":
  return ""
 x=round(x)
 y=round(y)
 z=round(z)
 final=""
 for p in sub_tiles:
  if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz:
   final=p.tile
 return final
sub_tiles=[]
def spawn_sub_tile(minx,maxx,miny,maxy,minz,maxz,tile,id=0):
 sub_tiles.append(sub_tile(minx,maxx,miny,maxy,minz,maxz,tile,id))
class wall():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,tile,id=0,strength=5000):
  self.id=id
  self.minx=minx
  self.maxx=maxx
  self.miny=miny
  self.strength=strength
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.tile=tile
  spawn_platform(minx,maxx,miny,maxy,minz,maxz,"wall",id)

walls=[]

def get_wall(x,y,z):
 x=round(x)
 y=round(y)
 z=round(z)
 final=""
 check_x=x
 if check_x<0:
  check_x=0
 if check_x>600:
  check_x=600
 check_x=round(check_x/10)
 check_y=y
 if check_y<0:
  check_y=0
 if check_y>600:
  check_y=600
 check_y=round(check_y/10)
 for p in reversed(walls_x[check_x-1][check_y-1]):
  if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz and get_platform(x,y,z)=="wall":
   return p.tile
 return final

def get_walls_index(x,y,z):
 x=round(x)
 y=round(y)
 z=round(z)

 final=-1
 check_x=x
 if check_x<0:
  check_x=0
 if check_x>600:
  check_x=600
 check_x=round(check_x/10)
 check_y=y
 if check_y<0:
  check_y=0
 if check_y>600:
  check_y=600
 check_y=round(check_y/10)
 for p in reversed(walls_x[check_x-1][check_y-1]):
  if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz and get_platform(x,y,z)=="wall":
   return walls.index(p)
 return final

walls_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    walls_x.append(row)

def spawn_wall(minx,maxx,miny,maxy,minz,maxz,tile,id=0,strength=5000):
 p=wall(minx,maxx,miny,maxy,minz,maxz,tile,id,strength)
 walls.append(p)
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
   walls_x[l][m].append(p)

class demper_zone():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,name,volume,id=0):
  self.id=id
  self.minx=minx
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.name=name
  self.volume=volume

demper_zones=[]
demper_zones_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    demper_zones_x.append(row)

def get_demper_zones(x,y,z):
 x=round(x)
 y=round(y)
 z=round(z)

 result={}
 check_x=x
 if check_x<0:
  check_x=0
 if check_x>600:
  check_x=600
 check_x=round(check_x/10)
 check_y=y
 if check_y<0:
  check_y=0
 if check_y>600:
  check_y=600
 check_y=round(check_y/10)
 for p in demper_zones_x[check_x-1][check_y-1]:
  if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz:
   result[p.name]=p.volume
 return result

def demper_zoneloop(x,y,z):
 x=round(x)
 y=round(y)
 z=round(z)
 dzs=get_demper_zones(x,y,z)

 for a in ambiences:
  if x>=a.minx and x<=a.maxx and y>=a.miny and y<=a.maxy and z>=a.minz and z<=a.maxz:
   if a.muted==True:
    a.muted=False
    a.sound.change_volume(a.volume)
  else:
   if a.muted==False:
    a.muted=True
    a.sound.change_volume(a.volume-100)

  if a.soundname in dzs.keys():
   if a.demped==False:
    a.demped=True
    a.sound.change_volume(a.volume-dzs[a.soundname])
  elif not a.soundname in dzs.keys():
   if a.demped==True:
    a.demped=False
    a.sound.change_volume(a.volume)

 for s in srcs:
  svolume=s.volume
  if s.soundname in dzs.keys():
   svolume=s.volume-dzs[s.soundname]
  if svolume!=s.last_volume:
   s.last_volume=svolume
   s.sound.change_volume(svolume)
 for a in bounded_sources:
  for p in a.bounded_zones:
   if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz :
    if a.muted==True:
     a.muted=False
     a.sound.change_volume(a.volume)
     a.current_zone_id=a.bounded_zones.index(p)
   elif x<=p.minx or x>=p.maxx or y<=p.miny or y>=p.maxy or z<=p.minz or z>=p.maxz:
    if a.muted==False and a.bounded_zones.index(p)==a.current_zone_id:
     a.muted=True
     a.sound.change_volume(a.volume-100)
     a.current_zone_id=-1

def spawn_demper_zone(minx,maxx,miny,maxy,minz,maxz,name,volume,id=0):
 p=demper_zone(minx,maxx,miny,maxy,minz,maxz,name,volume,id)
 demper_zones.append(p)
 demper_zoneloop(v.x,v.y,v.z)

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
   demper_zones_x[l][m].append(p)


class zone():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,text,id=0):
  self.id=id
  self.minx=minx
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.text=text

zones_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    zones_x.append(row)

def zoneloop():
 new_zone=get_zone(v.x,v.y,v.z)
 if new_zone!=v.current_zone:
  v.current_zone=new_zone
  speak(new_zone)

def get_zone(x,y,z):
 x=round(x)
 y=round(y)
 z=round(z)

 final="unnamed area"
 check_x=x
 if check_x<0:
  check_x=0
 if check_x>600:
  check_x=600
 check_x=round(check_x/10)
 check_y=y
 if check_y<0:
  check_y=0
 if check_y>600:
  check_y=600
 check_y=round(check_y/10)
 for p in reversed(zones_x[check_x-1][check_y-1]):
  if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz:
   return p.text
 return final

zones=[]

def spawn_zone(minx,maxx,miny,maxy,minz,maxz,text,id=0):
 p=zone(minx,maxx,miny,maxy,minz,maxz,text,id)
 zones.append(p)
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
   zones_x[l][m].append(p)

class intercepting_source():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,filter=0,id=0):
  self.id=id
  self.minx=minx
  self.filter=filter
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.sources=[]
 def check_sources(self):
  pass

 def set_filter(self,filter):
  pass


class src():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,soundname,volume=0,id=0):
  self.id=id
  self.dempid=-1
  self.minx=minx
  self.demped=False
  self.volume=volume
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.soundname=soundname
  v.sp.behind_pitch_decrease=0
  self.sound=v.sp.play_3d(r"sounds\\"+soundname,v.x,v.y,v.z,minx,miny,minz,False,False,True)
  v.sp.update_sound_range_3d(self.sound,0,self.maxx-self.minx,0,self.maxy-self.miny,0,self.maxz-self.minz)
  v.sp.behind_pitch_decrease=4
  self.last_volume=self.volume
  self.sound.change_volume(self.volume)
#  if v.lobby==False:

srcs=[]
srcs_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    srcs_x.append(row)

def pause_all_sources(volume=100):
 for s in srcs:
    s.sound.change_volume(s.volume-(volume))
def resume_all_sources():
 for s in srcs:
    s.sound.change_volume(s.volume)
def get_sounds(x,y,z):
 x=round(x)
 y=round(y)
 z=round(z)

 final=[]
 list=get_demper_zones(x,y,z)
 for p in srcs:
  if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz and p.soundname not in list:
   final.append(p.soundname)
 for p in ambiences:
  if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz:
   final.append(p.soundname)
 return final

def fade_all_sources(time,steps):
 fadetimer=timer.timer()
 betweentime=time/steps
 total=0
 while 1:
  if fadetimer.elapsed()>betweentime:
   fadetimer.restart()
   total-=1
   for s in srcs:
#    if s.dempid>-1:
     s.sound.change_volume(total)
  if total<=-100:
   break
def spawn_src(minx,maxx,miny,maxy,minz,maxz,soundname,volume=0,id=0):
 p=src(minx,maxx,miny,maxy,minz,maxz,soundname,volume,id)
 srcs.append(p)
 demper_zoneloop(v.x,v.y,v.z)
 v.sp.update_listener_3d(v.x,v.y,v.z,v.facing)

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
   srcs_x[l][m].append(p)

class bounded_source():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,soundname,volume,data=""):
  self.current_zone_id=-1
  self.data=data
  self.bounded_zones=[]
  self.minx=minx
  self.muted=True
  self.volume=volume
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.soundname=soundname
  v.sp.behind_pitch_decrease=0
  self.sound=v.sp.play_3d(r"sounds\\"+soundname,0,0,0,minx,miny,minz,False,False,True)
  v.sp.update_sound_range_3d(self.sound,0,self.maxx-self.minx,0,self.maxy-self.miny,0,self.maxz-self.minz)
  v.sp.behind_pitch_decrease=4
  v.sp.update_sound_range_3d(self.sound,0,self.maxx-self.minx,0,self.maxy-self.miny,0,self.maxz-self.minz)
  self.sound.change_volume(-100)
  lines=self.data.split("||")
  for l in lines:
   l=l.strip()
   words=l.split(" ")
   if len(words)>5:
    self.bounded_zones.append(bounded_zone(int(words[0]),int(words[1]),int(words[2]),int(words[3]),int(words[4]),int(words[5])))

bounded_sources=[]
def pause_all_bounded_sources(volume=100):
 for s in bounded_sources:
    s.sound.change_volume(s.volume-(volume))
def resume_all_bounded_sources():
 for s in bounded_sources:
    s.sound.change_volume(s.volume)
def fade_all_bounded_sources(time,steps):
 fadetimer=timer.timer()
 betweentime=time/steps
 total=0
 while 1:
  if fadetimer.elapsed()>betweentime:
   fadetimer.restart()
   total-=1
   for s in bounded_sources:
    if s.muted==False:
     s.sound.change_volume(total)
  if total<=-100:
   break
def spawn_bounded_source(minx,maxx,miny,maxy,minz,maxz,soundname,volume,data=""):
 bounded_sources.append(bounded_source(minx,maxx,miny,maxy,minz,maxz,soundname,volume,data))

class bounded_zone():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz):

  self.minx=minx
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
class ambience():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,soundname,volume=0):
  self.dempid=-1
  self.minx=minx
  self.muted=True
  self.demped=False
  self.volume=volume
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.soundname=soundname
  v.sp.behind_pitch_decrease=0
  self.sound=v.sp.play_3d(r"sounds\\"+soundname,0,0,0,minx,miny,minz,False,False,True)
  v.sp.update_sound_range_3d(self.sound,0,self.maxx-self.minx,0,self.maxy-self.miny,0,self.maxz-self.minz)
  v.sp.behind_pitch_decrease=4
  self.sound.change_volume(-100)


ambiences=[]
ambiences_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    ambiences_x.append(row)


def pause_all_ambiences(volume=100):
 for s in ambiences:
    s.sound.change_volume(s.volume-(volume))
def resume_all_ambiences():
 for s in ambiences:
    s.sound.change_volume(s.volume)
def fade_all_ambiences(time,steps):
 fadetimer=timer.timer()
 betweentime=time/steps
 total=0
 while 1:
  if fadetimer.elapsed()>betweentime:
   fadetimer.restart()
   total-=1
   for s in ambiences:
    if s.muted==False:
     s.sound.change_volume(total)
  if total<=-100:
   break
def spawn_ambience(minx,maxx,miny,maxy,minz,maxz,soundname,volume=0):
 p=ambience(minx,maxx,miny,maxy,minz,maxz,soundname,volume)
 ambiences.append(p)
 v.sp.update_listener_3d(v.x,v.y,v.z,v.facing)

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
   ambiences_x[l][m].append(p)


class reverb_zone():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,mix,reverb,id=0):
  self.id=id
  self.mix=mix
  self.minx=minx
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.reverb=reverb
def get_reverb_zone(x,y,z):
 x=round(x)
 y=round(y)
 z=round(z)

 final=0,0
 check_x=x
 if check_x<0:
  check_x=0
 if check_x>600:
  check_x=600
 check_x=round(check_x/10)
 check_y=y
 if check_y<0:
  check_y=0
 if check_y>600:
  check_y=600
 check_y=round(check_y/10)
 for p in reversed(reverb_zones_x[check_x-1][check_y-1]):
  if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz:
   return p.reverb,p.mix
 return final


reverb_zones=[]
reverb_zones_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    reverb_zones_x.append(row)


def spawn_reverb_zone(minx,maxx,miny,maxy,minz,maxz,mix,reverb,id=0):
 p=reverb_zone(minx,maxx,miny,maxy,minz,maxz,mix,reverb,id)
 reverb_zones.append(p)
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
   reverb_zones_x[l][m].append(p)


class location():
 def __init__(self,x,y,z,name):
  self.x=x
  self.y=y
  self.z=z
  self.name=name
  self.id=random.randint(0,100000000)
 def get_instructions(self,x,y,z):
  x=round(x)
  y=round(y)
  z=round(z)
  nx, ny = rotation.rotate_matrix(self.x, self.y, v.facing, x, y)
  nx=round(nx)
  ny=round(ny)
  delta_x = nx - x
  delta_y = ny - y
  delta_z = self.z - z
  final=""
  if delta_x>=0:
   final=final+"right "+str(delta_x)
  else:
   final=final+"left "+str(delta_x*-1)
  if delta_y>=0:
   final=final+", in front "+str(delta_y)
  else:
   final=final+", behind "+str(delta_y*-1)
  if delta_z>=0:
   final=final+" and up "+str(delta_z)
  else:
   final=final+" and down "+str(delta_z*-1)
  final=v.vertaal_tekst(final,v.language)
  return final

locations=[]
def spawn_location(x,y,z,name):
 locations.append(location(x,y,z,name))
def get_locations_index(id):
 for l in locations:
  if id==l.id:
   return locations.index(l)
 return -1
class staircase():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,tile,walltile,dir,zonetext=""):
  self.zonetext=zonetext
  self.dir=dir
  self.walltile=walltile
  self.minx=minx
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.tile=tile
  if self.dir==1:
   for i in range(self.miny,self.maxy+1):
    spawn_platform(self.minx,self.maxx,i,i,self.minz+i-self.miny,self.minz+i-self.miny,self.tile)
    spawn_wall(self.minx,self.maxx,i,i,self.minz+i-self.miny-1,self.minz+i-self.miny-1,self.walltile)
    if self.zonetext!="":
     spawn_zone(self.minx,self.maxx,i,i,self.minz+i-self.miny-1,self.maxz,self.zonetext)
  if self.dir==2:
   count=0
   for i in reversed(range(self.miny,self.maxy+1)):
    spawn_platform(self.minx,self.maxx,i,i,self.minz+count,self.minz+count,self.tile)
    spawn_wall(self.minx,self.maxx,i,i,self.minz+count-1,self.minz+count-1,self.walltile)
    if self.zonetext!="":
     spawn_zone(self.minx,self.maxx,i,i,self.minz+count-1,self.maxz,self.zonetext)
    count+=1
  if self.dir==3:
   for i in range(self.minx,self.maxx+1):
    spawn_platform(i,i,self.miny,self.maxy,self.minz+i-self.minx,self.minz+i-self.minx,self.tile)
    spawn_wall(i,i,self.miny,self.maxy,self.minz+i-self.minx-1,self.minz+i-self.minx-1,self.walltile)
    if self.zonetext!="":
     spawn_zone(i,i,self.miny,self.maxy,self.minz+i-self.minx-1,self.maxz,self.zonetext)
  if self.dir==4:
   count=0
   for i in reversed(range(self.minx,self.maxx+1)):
    spawn_platform(i,i,self.miny,self.maxy,self.minz+count,self.minz+count,self.tile)
    spawn_wall(i,i,self.miny,self.maxy,self.minz+count-1,self.minz+count-1,self.walltile)
    if self.zonetext!="":
     spawn_zone(i,i,self.miny,self.maxy,self.minz+count-1,self.maxz,self.zonetext)
    count+=1

def get_staircase(x, y, z):
    x=round(x)
    y=round(y)
    z=round(z)
    final = -1
    
    check_x = round(x / 10)  
    check_y = round(y / 10)  

    check_x = max(0, min(check_x, 60))  
    check_y = max(0, min(check_y, 60))  

    # Zorg ervoor dat je toegang krijgt tot de juiste staircaseen
    staircases = staircases_x[check_x - 1][check_y - 1]  

    if not staircases:
        return final

    for p in reversed(staircases):
        if p.minx <= x <= p.maxx and p.miny <= y <= p.maxy and p.minz <= z <= p.maxz:
         return staircases.index(p)

    
    return final



staircases=[]
staircases_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    staircases_x.append(row)


def spawn_staircase(minx,maxx,miny,maxy,minz,maxz,tile,walltile,dir=0,zonetext=""):
 p=staircase(minx,maxx,miny,maxy,minz,maxz,tile,walltile,dir,zonetext)
 staircases.append(p)
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
   staircases_x[l][m].append(p)



class object():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,name,dir,id):
  self.id=id
  self.minx=minx
  self.maxx=maxx
  self.mapdata="""
"""
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.name=name
  self.dir=dir
  self.load_mapdata()
  self.sounds=[]

 def add_sound(self,sound_name,pitch):
    v.sp.reverb,v.sp.mix=get_reverb_zone(self.minx,self.miny,self.minz)
    v.sp.behind_pitch_decrease=0
    sound=v.sp.play_3d(r"sounds\\"+sound_name,v.x,v.y,v.z,self.minx,self.miny,self.minz,False,False,True,pitch)
    v.sp.update_sound_range_3d(sound,0,self.maxx-self.minx,0,self.maxy-self.miny,0,self.maxz-self.minz)
    v.sp.update_sound_3d(sound,self.minx,self.miny,self.minz,v.facing)
    v.sp.behind_pitch_decrease=4
    self.sounds.append(sound)

 def remove_sound(self,sound_name):
   for s in self.sounds:
     if s.handle.name==r"sounds\\"+sound_name:
       v.sp.destroy_sound(s)
       self.sounds.remove(s)
 def get_instructions(self,x,y,z):
  x=round(x)
  y=round(y)
  z=round(z)

  nx, ny = rotation.rotate_matrix(math.floor((self.minx+self.maxx)/2), math.floor((self.miny+self.maxy)/2), v.facing, x, y)
  nx=round(nx)
  ny=round(ny)
  delta_x = nx - x
  delta_y = ny - y
  delta_z = math.floor((self.minz+self.maxz)/2) - z
  final=""
  if delta_x>=0:
   final=final+"right "+str(delta_x)
  else:
   final=final+"left "+str(delta_x*-1)
  if delta_y>=0:
   final=final+", in front "+str(delta_y)
  else:
   final=final+", behind "+str(delta_y*-1)
  if delta_z>=0:
   final=final+" and up "+str(delta_z)
  else:
   final=final+" and down "+str(delta_z*-1)
  return final
 def rotate(self, direction,minx,maxx,miny,maxy):
  theta_radians = np.radians(direction)
  x=(self.minx+self.maxx)/2
  y=(self.miny+self.maxy)/2  
  relative_minx = minx - x
  relative_miny = miny - y
  relative_maxx = maxx - x
  relative_maxy = maxy - y
  rotation_matrix = np.array([[np.cos(theta_radians), -np.sin(theta_radians)],
  [np.sin(theta_radians), np.cos(theta_radians)]])

  rotated_min_point = np.dot(rotation_matrix, [relative_minx, relative_miny])
  rotated_max_point = np.dot(rotation_matrix, [relative_maxx, relative_maxy])
    
  minx = rotated_min_point[0] + x
  miny = rotated_min_point[1] + y
  maxx = rotated_max_point[0] + x
  maxy = rotated_max_point[1] + y

  if minx>maxx:
   f=0
   f=minx
   minx=maxx
   maxx=f
  if miny>maxy:
   f=0
   f=miny
   miny=maxy
   maxy=f
  """
  minx=math.floor(minx)
  maxx=math.floor(maxx)
  miny=math.floor(miny)
  maxy=math.floor(maxy)
  """

  return minx,maxx,miny,maxy
 def load_mapdata(self):
  lines=self.mapdata.split("\n")
  for l in lines:
   parsed=l.split(" ")
   if parsed[0]=="mute_sounds" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    for s in v.srclist:
     spawn_demper_zone(minx,maxx,miny,maxy,minz,maxz,s+".ogg",int(parsed[7]),self.id)

   if parsed[0]=="rv" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    spawn_reverb_zone(minx,maxx,miny,maxy,minz,maxz,int(parsed[7]),int(parsed[8]),self.id)

   if parsed[0]=="platform" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    if "permanent" not in parsed[7]:
     spawn_platform(minx,maxx,miny,maxy,minz,maxz,parsed[7],self.id)
    else:
     parsed[7]=parsed[7].replace("permanent","")
     spawn_platform(minx,maxx,miny,maxy,minz,maxz,parsed[7],0)

   elif parsed[0]=="flex_platform" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    minx,maxx,miny,maxy=self.rotate((self.dir*90)-90,minx,maxx,miny,maxy)
    spawn_platform(minx,maxx,miny,maxy,minz,maxz,parsed[7],self.id)
   elif parsed[0]=="sub_tile" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    spawn_sub_tile(minx,maxx,miny,maxy,minz,maxz,parsed[7],self.id)
   elif parsed[0]=="flex_sub_tile" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    minx,maxx,miny,maxy=self.rotate((self.dir*90)-90,minx,maxx,miny,maxy)
    spawn_sub_tile(minx,maxx,miny,maxy,minz,maxz,parsed[7],self.id)
   elif parsed[0]=="flex_wall" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    minx,maxx,miny,maxy=self.rotate((self.dir*90)-90,minx,maxx,miny,maxy)
    spawn_wall(minx,maxx,miny,maxy,minz,maxz,parsed[7],self.id)

   elif parsed[0]=="wall" and len(parsed)>8:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+float(parsed[1].replace("%",""))
    else:
     minx=self.minx+float(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+float(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+float(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+float(parsed[3].replace("%",""))
    else:
     miny=self.miny+float(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+float(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+float(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+float(parsed[5].replace("%",""))
    else:
     minz=self.minz+float(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+float(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+float(parsed[6])
    if "permanent" not in parsed[7]:
     spawn_wall(minx,maxx,miny,maxy,minz,maxz,parsed[7],self.id)
    else:
     parsed[7]=parsed[7].replace("permanent","")
     spawn_wall(minx,maxx,miny,maxy,minz,maxz,parsed[7],0)


   elif parsed[0]=="wall" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    spawn_wall(minx,maxx,miny,maxy,minz,maxz,parsed[7],self.id)
   elif parsed[0]=="src" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    spawn_src(minx,maxx,miny,maxy,minz,maxz,parsed[7],-5,self.id)
   elif parsed[0]=="zone" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    if "permanent" in parsed[7]:
     spawn_zone(minx,maxx,miny,maxy,minz,maxz,l.replace("zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" permanent",""),0)
    else:
     spawn_zone(minx,maxx,miny,maxy,minz,maxz,l.replace("zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" ",""),self.id)
   elif parsed[0]=="flex_zone" and len(parsed)>7:
    minx=0
    maxx=0
    miny=0
    maxy=0
    minz=0
    maxz=0
    if "%" in parsed[1]:
     minx=self.maxx+int(parsed[1].replace("%",""))
    else:
     minx=self.minx+int(parsed[1])
    if "%" in parsed[2]:
     maxx=self.minx+int(parsed[2].replace("%",""))
    else:
     maxx=self.maxx+int(parsed[2])
    if "%" in parsed[3]:
     miny=self.maxy+int(parsed[3].replace("%",""))
    else:
     miny=self.miny+int(parsed[3])
    if "%" in parsed[4]:
     maxy=self.miny+int(parsed[4].replace("%",""))
    else:
     maxy=self.maxy+int(parsed[4])
    if "%" in parsed[5]:
     minz=self.maxz+int(parsed[5].replace("%",""))
    else:
     minz=self.minz+int(parsed[5])
    if "%" in parsed[6]:
     maxz=self.minz+int(parsed[6].replace("%",""))
    else:
     maxz=self.maxz+int(parsed[6])
    minx,maxx,miny,maxy=self.rotate((self.dir*90)-90,minx,maxx,miny,maxy)
    spawn_zone(minx,maxx,miny,maxy,minz,maxz,l.replace("flex_zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" ",""),self.id)

 def play_sound(self,soundname):
  if get_3d_distance(self.minx,self.miny,self.minz,v.x,v.y,v.z)<=40:
   v.sp.filter=calculate_walls(self.minx,self.miny,self.minz,v.x,v.y,v.z,self.id) 
  v.sp.reverb,v.sp.mix=get_reverb_zone(self.minx,self.miny,self.minz)
  sound=v.sp.play_3d(r"sounds\\"+soundname,v.lx,v.ly,v.lz,self.minx,self.miny,self.minz,False,False,False)
  v.sp.update_sound_range_3d(sound,0,self.maxx-self.minx,0,self.maxy-self.miny,0,self.maxz-self.minz)
  v.sp.filter=0
  v.listener_facing=-1
 def move(self,dir):
  self.minx,self.miny=rotation.move(self.minx,self.miny,dir)
  self.maxx,self.maxy=rotation.move(self.maxx,self.maxy,dir)
  for s in self.sounds:
    v.sp.update_sound_3d(s,self.minx,self.miny,self.minz)
  for p in platforms:
   if p.id==self.id:
    p.minx,p.miny=rotation.move(p.minx,p.miny,dir)
    p.maxx,p.maxy=rotation.move(p.maxx,p.maxy,dir)
    for l in platforms_x:
     for m in l:
      try:
       l[m].remove(p)
      except:
       pass
    minx,maxx,miny,maxy=get_mmmm(p)
    for l in range(round(minx/10)-1,round(maxx/10)):
     for m in range(round(miny/10)-1,round(maxy/10)):
      platforms_x[l][m].append(p)
  for p in reverb_zones:
   if p.id==self.id:
    p.minx,p.miny=rotation.move(p.minx,p.miny,dir)
    p.maxx,p.maxy=rotation.move(p.maxx,p.maxy,dir)
    for l in reverb_zones_x:
     for m in l:
      try:
       l[m].remove(p)
      except:
       pass
    minx,maxx,miny,maxy=get_mmmm(p)
    for l in range(round(minx/10)-1,round(maxx/10)):
     for m in range(round(miny/10)-1,round(maxy/10)):
      reverb_zones_x[l][m].append(p)

  for p in srcs:
   if p.id==self.id:
    p.minx,p.miny=rotation.move(p.minx,p.miny,dir)
    p.maxx,p.maxy=rotation.move(p.maxx,p.maxy,dir)
    for l in srcs_x:
     for m in l:
      try:
       l[m].remove(p)
      except:
       pass
    minx,maxx,miny,maxy=get_mmmm(p)
    for l in range(round(minx/10)-1,round(maxx/10)):
     for m in range(round(miny/10)-1,round(maxy/10)):
      srcs_x[l][m].append(p)

  for p in zones:
   if p.id==self.id:
    p.minx,p.miny=rotation.move(p.minx,p.miny,dir)
    p.maxx,p.maxy=rotation.move(p.maxx,p.maxy,dir)
    for l in zones_x:
     for m in l:
      try:
       l[m].remove(p)
      except:
       pass
    minx,maxx,miny,maxy=get_mmmm(p)
    for l in range(round(minx/10)-1,round(maxx/10)):
     for m in range(round(miny/10)-1,round(maxy/10)):
      zones_x[l][m].append(p)

#  for p in sub_tiles:
#   if p.id==self.id:
#    p.minx,p.miny=rotation.move(p.minx,p.miny,dir)
#    p.maxx,p.maxy=rotation.move(p.maxx,p.maxy,dir)
  for p in walls:
   if p.id==self.id:
    p.minx,p.miny=rotation.move(p.minx,p.miny,dir)
    p.maxx,p.maxy=rotation.move(p.maxx,p.maxy,dir)
    for l in walls_x:
     for m in l:
      try:
       l[m].remove(p)
      except:
       pass
    minx,maxx,miny,maxy=get_mmmm(p)
    for l in range(round(minx/10)-1,round(maxx/10)):
     for m in range(round(miny/10)-1,round(maxy/10)):
      walls_x[l][m].append(p)


  for p in srcs:
   if p.id==self.id:
    p.minx,p.miny=rotation.move(p.minx,p.miny,dir)
    p.maxx,p.maxy=rotation.move(p.maxx,p.maxy,dir)
    p.sound.update_sound_3d(p.minx,p.miny,p.minz,v.facing)

def remove_object(id):
    global platforms, walls, demper_zones, reverb_zones, platforms_x
    global srcs_x, zones_x, walls_x, reverb_zones_x, demper_zones_x
    global srcs, sub_tiles, zones, objects

    def filter_grid(grid):
        return [
            [
                [item for item in cell if item.id != id]
                for cell in row
            ] for row in grid
        ]

    # Filter 60x60 grids
    platforms_x = filter_grid(platforms_x)
    reverb_zones_x = filter_grid(reverb_zones_x)
    zones_x = filter_grid(zones_x)
    demper_zones_x = filter_grid(demper_zones_x)
    srcs_x = filter_grid(srcs_x)
    walls_x = filter_grid(walls_x)

    # Filter gewone lijsten
    platforms = [b for b in platforms if b.id != id]
    reverb_zones = [b for b in reverb_zones if b.id != id]
    zones = [b for b in zones if b.id != id]
    demper_zones = [b for b in demper_zones if b.id != id]
    walls = [b for b in walls if b.id != id]

    # Speciaal geval: srcs
    new_srcs = []
    for b in srcs:
        if b.id != id:
            new_srcs.append(b)
        else:
            soundname = b.soundname.replace(".ogg", "")
            sound = v.sp.play_3d(
                f"sounds\\{soundname}destroy.ogg", 0, 0, 0,
                b.minx, b.miny, b.minz, False, False, False
            )
            v.sp.update_sound_range_3d(
                sound,
                0, b.maxx - b.minx,
                0, b.maxy - b.miny,
                0, b.maxz - b.minz
            )
            b.sound.handle.handle.stop()
    srcs = new_srcs

    # Verwijder object uit objects
    index=get_objects_index(id)
    if index>-1:
      object=objects[index]
      for s in object.sounds:
        v.sp.destroy_sound(s)
    objects[:] = [b for b in objects if b.id != id]

objects=[]
def get_objects_index(id):
 for p in objects:
  if p.id==id:
   return objects.index(p)
 return -1
def spawn_object(minx,maxx,miny,maxy,minz,maxz,name,dir,id):
 objects.append(object(minx,maxx,miny,maxy,minz,maxz,name,dir,id))

my_map={}


musics=[]
def load_map(data=""):
 v.sp.update_listener_3d(v.x,v.y,v.z,v.facing)
 v.mapdata=data
 global musics
 for m in musics:
  m.stop()
 musics=[]
 global maxx
 maxx=0
 global maxy
 maxy=0
 global sub_tiles
 v.sp.destroy_all()
 global objects
 global platforms_x
 platforms_x = []
 for _ in range(60):
     row = [[] for _ in range(60)]
     platforms_x.append(row)
 global staircases_x
 staircases_x = []
 for _ in range(60):
     row = [[] for _ in range(60)]
     staircases_x.append(row)

 global ambiences_x
 ambiences_x = []
 for _ in range(60):
     row = [[] for _ in range(60)]
     ambiences_x.append(row)

 global demper_zones_x
 demper_zones_x = []
 for _ in range(60):
     row = [[] for _ in range(60)]
     demper_zones_x.append(row)

 global srcs_x
 srcs_x = []
 for _ in range(60):
     row = [[] for _ in range(60)]
     srcs_x.append(row)
 global reverb_zones_x
 reverb_zones_x = []
 for _ in range(60):
     row = [[] for _ in range(60)]
     reverb_zones_x.append(row)

 global zones_x
 zones_x = []
 for _ in range(60):
     row = [[] for _ in range(60)]
     zones_x.append(row)

 global walls_x
 walls_x = []
 for _ in range(60):
     row = [[] for _ in range(60)]
     walls_x.append(row)

 global locations
 global demper_zones
 global bounded_sources
 global srcs
 global reverb_zones
 global platforms
 platforms=[]
 global walls
 global ambiences
 global zones
 bounded_sources=[]
 sub_tiles=[]
 objects=[]
 locations=[]
 ambiences=[]
 srcs=[]
 demper_zones=[]
 global staircases
 staircases=[]
 walls=[]
 zones=[]
 reverb_zones=[]
 data+="\n end"
 lines=data.split("\n")
 for l in lines:
  for event in pygame.event.get():
   pass

  parsed=l.split(" ")
  if parsed[0]=="maxx" and len(parsed)>1:
   try:
    maxx=round(parsed[1])
   except:
    pass
  elif parsed[0]=="maxy" and len(parsed)>1:
   try:
    maxy=round(parsed[1])
   except:
    pass
  elif parsed[0]=="music" and len(parsed)>1:
   musics.append(music.music(parsed[1],v.musicvolume))
  elif parsed[0]=="platform" and len(parsed)>7:
   try:
    spawn_platform(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7])
   except:
    pass
  elif parsed[0]=="sub_tile" and len(parsed)>7:
   try:
    spawn_sub_tile(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7])
   except:
    pass
  elif parsed[0]=="staircase" and len(parsed)>9:
   try:
    spawn_staircase(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7],parsed[8],int(parsed[9]),l.replace("staircase "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" "+parsed[7]+" "+parsed[8]+" "+parsed[9],""))
   except:
    pass
  elif parsed[0]=="wall" and len(parsed)>8:
   try:
    spawn_wall(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7],0,int(parsed[8]))
   except:
    pass
  elif parsed[0]=="wall" and len(parsed)>7:
   try:
    spawn_wall(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7])
   except:
    pass

  elif parsed[0]=="location" and len(parsed)>4:
   try:
    spawn_location(int(parsed[1]),int(parsed[2]),int(parsed[3]),l.replace("location "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" ",""))
   except:
    pass
  elif parsed[0]=="src" and len(parsed)>8:
   try:
    spawn_src(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7],int(parsed[8]))
   except:
    pass
  elif parsed[0]=="src" and len(parsed)>7:
   try:
    spawn_src(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7])
   except:
    pass
  elif parsed[0]=="bounded_source" and len(parsed)>8:
   try:
    spawn_bounded_source(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7],int(parsed[8]),l.replace("bounded_source "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" "+parsed[7]+" "+str(parsed[8])+" ",""))
   except:
    pass
  elif parsed[0]=="ambience" and len(parsed)>8:
   try:
    spawn_ambience(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7],int(parsed[8]))
   except:
    pass
  elif parsed[0]=="ambience" and len(parsed)>7:
   try:
    spawn_ambience(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7])
   except:
    pass
  elif parsed[0]=="dz" and len(parsed)>8:
   try:
    spawn_demper_zone(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),parsed[7],int(parsed[8]))
   except:
    pass
  elif parsed[0]=="rv" and len(parsed)>8:
   try:
    spawn_reverb_zone(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),int(parsed[7]),int(parsed[8]))
   except:
    pass
  elif parsed[0]=="zone" and len(parsed)>7:
   try:
    spawn_zone(int(parsed[1]),int(parsed[2]),int(parsed[3]),int(parsed[4]),int(parsed[5]),int(parsed[6]),l.replace("zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" ",""))
   except:
    pass
 v.sp.update_listener_3d(v.x,v.y,v.z,v.facing)
# demper_zoneloop(v.x,v.y,v.z)

def calculate_walls(x1,y1,z1,x2,y2,z2,forbidid=-1):
 final=v.standart_filter
 x=round(x1)
 y=round(y1)
 z=round(z1)
 x2=round(x2)
 y2=round(y2)
 z2=round(z2)

 while (x, y, z) != (x2, y2, z2):
  if x != x2:
   x += 1 if x2 > x1 else -1
  if y != y2:
   y += 1 if y2 > y1 else -1
  if z != z2:
   z += 1 if z2 > z1 else -1
  if get_platform(x,y,z)=="wall":
   index=get_walls_index(x,y,z)
   if index>-1:
    if walls[index].id!=forbidid:
     final-=walls[index].strength
  
  if final<=1200:
   final =1200
   return final
 if final==v.standart_filter and v.standart_filter==15000:
  final=0
 return final

def get_mmmm(p):
    minx,maxx,miny,maxy=p.minx,p.maxx,p.miny,p.maxy
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
    return minx,maxx,miny,maxy