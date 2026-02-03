import timer
import v
v.get()
def get_players_index(name):
 for p in v.clients:
  if p.data["name"].lower()==name.lower():
   return v.clients.index(p)
 return -1

class team():
 def __init__(self,name):
  self.name=name
  self.members=[]
  self.data={
"tokens": 0,
"notes": {},
"max_members": 6,
"kills": 0,
"requests": [],
"invites": [],
"leader": "",
"metal_fortresstime": 0,
"lockertime": 0,
}
  self.lockertimer=timer.timer()
  self.metal_fortresstimer=timer.timer()
  self.metal_fortresstimer.set(22000000)
  self.rights={
"can kick players": [],
"can invite players": [],
"can accept players": [],
"can place lockers": [],
"can change rights": [],
}
  self.token_kills=15
 def remove(self):
  import map
  all_objects=map.objects
  removing=[]
  for f in all_objects:
   o=map.objects[f]
   if o.name=="metal_fortress" and o.team==self.name:
    o.health=-1000
    removing.append(o)

  for o in removing:
    o.check_health()
    map.remove_object(o.id)
#    del map.objects[str(o.id)]
 def add_kill(self):
  self.data["kills"]+=1
  if self.data["kills"]%self.token_kills==0:
   self.data["tokens"]+=1
   self.send("add_buffer_item team this team has earned 1 token for killing "+str(self.token_kills)+" players|n|play_sound tokenget.ogg 0 0 0 1 0")

 def remove_members_rights(self, name):
  for r in self.rights:
   new_r=[]
   for t in self.rights[r]:
    if t!=name:
     new_r.append(t)
   self.rights[r]=new_r

 def load(self,data):
  self.members=data["members"]
  for d in data["data"]:
   self.data[d]=data["data"][d]
  self.rights=data["rights"]
  self.lockertimer.set(self.data["lockertime"])
  self.metal_fortresstimer.set(self.data["metal_fortresstime"])
  for r in self.rights:
   for t in self.rights[r]:
    if t not in self.members:
     self.rights[r].remove(t)

 def save(self):
  self.data["lockertime"]=self.lockertimer.elapsed()
  self.data["metal_fortresstime"]=self.metal_fortresstimer.elapsed()
  data={
"members": self.members,
"data": self.data,
"rights": self.rights,
}
  return data
 def send(self,message):
  for t in self.members:
   index=get_players_index(t)
   if index>-1:
    v.clients[index].send(message)
 def profile_menu(self):
  options=[self.name,"members","total kills: "+str(self.data["kills"]),"team tokens: "+str(self.data["tokens"]),"leader: "+self.data["leader"]]
  return options

def get_team(name):
 final=""
 index=get_players_index(name)
 if index>-1:
  if v.clients[index].match_id>-1:
   return ""
 for t in v.teams:
  if name.lower() in (member.lower() for member in t.members):
   final=t.name
 return final

def get_teams_index(name):
 for p in v.teams:
  if p.name==name:
   return v.teams.index(p)
 return -1
