import explosives
import teams
import random
import map as ma
import v
v.get()
import timer

def get_players_index(name):
 for p in v.clients:
  if p.data["name"].lower()==name.lower():
   return v.clients.index(p)
 return -1

def send_all(message,map=""):
 v.send_packet_to_clients(message,v.clients,map)


activated_traps=[]
traps_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    traps_x.append(row)

class trap():
 def __init__(self,minx,maxx,miny,maxy,minz,maxz,map,name,owner,team):
  list=[]
  for t in v.traps:
   list.append(t.id)

  self.id=random.randint(0,100000000)
  while self.id in list:
   self.id=random.randint(0,100000000)
  self.minx=minx
  self.maxx=maxx
  self.miny=miny
  self.maxy=maxy
  self.minz=minz
  self.maxz=maxz
  self.map=map
  self.name=name
  self.owner=owner
  self.team=team
  self.activatetimer=timer.timer()
  self.target=""
  if self.name=="spike_trap":
   self.activatetime=125
  if self.name=="tripwire":
   self.activatetime=1500
  minx,maxx,miny,maxy=ma.get_mmmm(self)
  for l in range(round(minx/10)-1,round(maxx/10)):
   for m in range(round(miny/10)-1,round(maxy/10)):
    traps_x[l][m].append(self)

 def activate(self):
  index=get_players_index(self.target)
  if index>-1:
   v.clients[index].data["last_hit"]=self.owner+"'s "+self.name
   if self.name=="tripwire":
    send_all("play_sound tripwireexplodedist.ogg "+str(self.minx)+" "+str(self.miny)+" "+str(self.minz)+" 0 0|n|play_sound tripwireexplode"+str(random.randint(1,3))+".ogg "+str(self.minx)+" "+str(self.miny)+" "+str(self.minz)+" 0 0",self.map)
    explosives.explode((self.minx+self.maxx)/2,(self.miny+self.maxy)/2,(self.minz+self.maxz)/2,self.map,self.owner,12,900,60,1000,"tripwire")
   if self.name=="spike_trap":
    v.clients[index].data["health"]-=900
    send_all(r"player_sound "+v.clients[index].data["name"]+" sounds\\"+self.name+"hit"+str(random.randint(1,3))+".ogg 0")
  self.remove()
 def remove(self):
  global traps_x
  try:
   v.traps.remove(self)
  except:
   pass
  list = []
  for _ in range(60):
      row = [[] for _ in range(60)]
      list.append(row)

  for l in range(0,60):
   for m in range(0,60):
    for b in traps_x[l][m]:
     if b.id!=self.id:
      list[l][m].append(b)
  traps_x=list

 def check(self,x,y,z,map,player_name):
  if self.minx <= x <= self.maxx and self.miny <= y <= self.maxy and self.minz <= z <= self.maxz and self.map==map and self not in activated_traps and teams.get_team(player_name)!=self.team:
   self.activatetimer.restart()
   self.target=player_name
   send_all("play_sound "+self.name+"activate.ogg "+str(x)+" "+str(y)+" "+str(z)+" 0 0",map)
   activated_traps.append(self)

 def save(self):
  data={
"minx": self.minx,
"maxx": self.maxx,
"miny": self.miny,
"maxy": self.maxy,
"minz": self.minz,
"maxz": self.maxz,
"map": self.map,
"owner": self.owner,
"name": self.name,
"team": self.team,
}
  return data



def spawn_trap(minx,maxx,miny,maxy,minz,maxz,map,name,owner,team):
 v.traps.append(trap(round(minx),round(maxx),round(miny),round(maxy),round(minz),round(maxz),map,name,owner,team))

def trap_check(x,y,z,map,player_name):
    x=round(x)
    y=round(y)
    z=round(z)
    x=round(x)
    y=round(y)
    z=round(z)
    check_x = round(x / 10)  
    check_y = round(y / 10)  

    check_x = max(0, min(check_x, 60))  
    check_y = max(0, min(check_y, 60))  
    traps = traps_x[check_x - 1][check_y - 1]  
    for t in traps:
     t.check(x,y,z,map,player_name)

def activated_traploop():
 for t in activated_traps:
  if t.activatetimer.elapsed()>t.activatetime:
   t.activate()
   activated_traps.remove(t)
   break

def remake_traps_x():
 global traps_x
 traps_x = []
 for _ in range(60):
     row = [[] for _ in range(60)]
     traps_x.append(row)

 for t in v.traps:
  minx,maxx,miny,maxy=ma.get_mmmm(t)
  for l in range(round(minx/10)-1,round(maxx/10)):
   for m in range(round(miny/10)-1,round(maxy/10)):
    traps_x[l][m].append(t)
