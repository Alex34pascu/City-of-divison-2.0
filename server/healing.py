import math
def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)


import teams
import timer
import v
v.get()
def get_players_index(name):
 for p in v.clients:
  if p.data["name"].lower()==name.lower():
   return v.clients.index(p)
 return -1

class heal():
 def __init__(self,owner,name,health,steps,begintime=0,max_percent=100):
  self.max_percent=max_percent
  self.owner=owner
  self.name=name
  self.health=health
  self.max_steps=steps
  self.steps=0
  self.steptime=self.health/self.max_steps
  self.steptimer=timer.timer()
  self.begintimer=timer.timer()
  self.begintime=begintime
  self.beginning=True
 def loop(self):
  if self.begintimer.elapsed()>self.begintime and self.beginning==True:
   self.beginning=False
   self.steptimer.restart()
  if self.steptimer.elapsed()>1000 and self.beginning==False:
   self.steptimer.restart()
   getting_health=self.health/self.max_steps
   index=get_players_index(self.owner)
   if index>-1:
    v.clients[index].data["health"]+=getting_health
    max_health=v.clients[index].data["max_health"]/100
    max_health=max_health*self.max_percent
    if v.clients[index].data["health"]>max_health:
     v.clients[index].data["health"]=max_health
    if v.clients[index].skill_data["beeing a docter"]["active"]==True and teams.get_team(v.clients[index].data["name"])!="" and self.name=="first_aid_kit":
     for c in v.clients:
      dist=get_3d_distance(v.clients[index].data["x"],v.clients[index].data["y"],v.clients[index].data["z"],c.data["x"],c.data["y"],c.data["z"])
      if dist<=5+v.clients[index].skill_data["beeing a docter"]["level"] and c.data["name"]!=self.owner and teams.get_team(v.clients[index].data["name"])==teams.get_team(c.data["name"]) :
       c.data["health"]+=6+v.clients[index].skill_data["beeing a docter"]["level"]
       if c.data["health"]>max_health:
        c.data["health"]=max_health
       c.send("speak you got healed by "+v.clients[index].data["name"]+" beeing a docter skill.")

   self.steps+=1
   if self.steps>=self.max_steps:
    v.heals.remove(self)

def set_heal(owner,name,health,steps,begintime,max_percent):
 v.heals.append(heal(owner,name,health,steps,begintime,max_percent))
