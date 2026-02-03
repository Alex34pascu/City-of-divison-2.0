import map
import v
v.get()
import rotation
class radar():
 def __init__(self,x,y,z,facing,updown):
  self.updown=updown
  self.air=0
  self.dist=0
  self.x=x
  self.y=y
  self.z=z
  self.facing=facing
radars=[]
def spawn_radar(x,y,z,facing,updown):
 radars.append(radar(x,y,z,facing,updown))
 radarloop()
def remove_radar(r):
 for ra in radars:
  if r==ra:
   del radars[radars.index(r)]
   return
def radarloop():
 for r in radars:
  for i in range(1,30):
   if r.updown==0:
    r.x,r.y=rotation.move(r.x,r.y,r.facing)
   if r.updown==1:
    r.z+=1
   if r.updown==-1:
    r.z-=1
   w=map.get_wall(r.x,r.y,r.z)
   if w!="" and map.get_platform(r.x,r.y,r.z)=="wall":
    v.sp.play_3d(r"sounds\\"+w+".ogg",v.lx,v.ly,v.lz,r.x,r.y,r.z,False,False,False,200)
    remove_radar(r)
    break
   if map.get_platform(r.x,r.y,r.z)=="" or map.get_platform(r.x,r.y,r.z)=="blank":
    if r.air==0 and r.updown==0 and v.jumping==False and v.falling==False:
     v.sp.play_3d(r"sounds\\radarair.ogg",v.lx,v.ly,v.lz,r.x,r.y,r.z)
     r.air=1
   r.dist+=1
  remove_radar(r)
  break
