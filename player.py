import os
import math
def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)
import timer
import map
import sound_pool
sp=sound_pool.sound_pool
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 speatch.output(text)
import v
v.get()

shooting_players=[]

class player():
 def __init__(self,x,y,z,name):
  self.silenced=False
  self.scope=False
  self.weapon=""
  self.empty=True
  self.shooting=0
  self.tailing=False
  self.firetimer=timer.timer()
  self.x=x
  self.y=y
  self.z=z
  self.team=""
  self.name=name
  self.sounds=[]
  self.move(x,y,z)
 def move(self,x,y,z):
  self.x=x
  self.y=y
  self.z=z
  self.update_sounds()

 def stop_sound(self,name):
  for s in self.sounds:
   try:
    if s.handle.handle.is_playing:
     if self.name!=v.name:
      v.sp.update_sound_3d(s,self.x,self.y,self.z,v.facing)
     else:
      v.sp.behind_pitch_decrease=0
      v.sp.update_sound_3d(s,v.lx,v.ly,v.lz,v.facing)
      v.sp.behind_pitch_decrease=4

    else:
     self.sounds.remove(s)
   except:
    self.sounds.remove(s)
  for p in self.sounds:
   if p.handle.name==name:
    p.handle.stop()
    self.sounds.remove(p)

 def add_sound(self,soundname,looping=False,name=""):
  distance=get_3d_distance(self.x,self.y,self.z,v.lx,v.ly,v.lz)
  if not os.path.exists(soundname.replace(".ogg",".bin")) or distance>200:
   return
  v.sp.facing=v.facing
  v.sp.reverb,v.sp.mix=map.get_reverb_zone(self.x,self.y,self.z)
  if self.name==v.name:
   v.sp.behind_pitch_decrease=0
   v.sp.pan_step=0
  if "dist.ogg" in soundname and v.name!=self.name:
   v.sp.pan_step=1.7
   v.sp.volume_step=0.1
   if looping==True:
    if get_3d_distance(self.x,self.y,self.z,v.lx,v.ly,v.lz)<=150:
#     if self.name!=v.name:
     v.sp.filter=map.calculate_walls(v.lx,v.ly,v.lz,self.x,self.y,self.z) 
    f=v.sp.play_3d(soundname,v.lx,v.ly,v.lz,self.x,self.y,self.z,False,False,True)
    self.sounds.append(f)
   else:
    if get_3d_distance(self.x,self.y,self.z,v.lx,v.ly,v.lz)<=150:
#     if self.name!=v.name:
     v.sp.filter=map.calculate_walls(v.lx,v.ly,v.lz,self.x,self.y,self.z)
    f=v.sp.play_3d(soundname,v.lx,v.ly,v.lz,self.x,self.y,self.z,False,False,False)
    self.sounds.append(f)
  else:
   if looping==True:
    if get_3d_distance(self.x,self.y,self.z,v.lx,v.ly,v.lz)<=40:
#     if self.name!=v.name:
     v.sp.filter=map.calculate_walls(v.lx,v.ly,v.lz,self.x,self.y,self.z)
    f=v.sp.play_3d(soundname,v.lx,v.ly,v.lz,self.x,self.y,self.z,False,False,True)
    self.sounds.append(f)
   else:
    if get_3d_distance(self.x,self.y,self.z,v.lx,v.ly,v.lz)<=40:
#     if self.name!=v.name:
     v.sp.filter=map.calculate_walls(v.lx,v.ly,v.lz,self.x,self.y,self.z)
    f=v.sp.play_3d(soundname,v.lx,v.ly,v.lz,self.x,self.y,self.z,False,False,False)
    self.sounds.append(f)
  v.sp.pan_step=8.5
  v.sp.volume_step=0.85
  v.sp.behind_pitch_decrease=4
  v.sp.filter=0

 def update_sounds(self):
  sounds=self.sounds
  removing=False
  for s in self.sounds:
   try:
    if s.handle.handle.is_playing:
     if self.name!=v.name:
      v.sp.update_sound_3d(s,self.x,self.y,self.z,v.facing)
     else:
      v.sp.behind_pitch_decrease=0
      v.sp.update_sound_3d(s,self.x,self.y,self.z,v.facing)
      v.sp.behind_pitch_decrease=4
    else:
     removing=True
     sounds.remove(s)
   except:
    pass
  if removing:
   self.sounds=sounds

def remove_player(name):
 for p in v.players:
  if p==name:
   del v.players[p]
   if p in shooting_players:
     shooting_players.remove(p)
   break
def spawn_player(x,y,z,name):
 v.players[name]=player(x,y,z,name)
def get_player_index(name):
 names=list(v.players.keys())
 if name in names:
  return name
 else:
  return ""
