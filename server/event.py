import map
import sd
import random
import math

import timer
import v
v.get()

def send_all(message):
 v.send_packet_to_clients(message,v.clients,"")


def get_players_index(name):
 for p in v.clients:
  if p.data["name"].lower()==name.lower():
   return v.clients.index(p)
 return -1

class event():
 def __init__(self,name,max_time):
  list=[]
  for a in v.events:
   list.append(a.id)
  self.id=random.randint(0,100000000)
  while self.id in list:
   self.id=random.randint(0,100000000)
  self.name=name
  self.timer=timer.timer()
  self.scores={}
  self.max_time=max_time
  self.max_score=0
  self.information={}
  self.get_max_score()
 def get_max_score(self):
  if self.name=="examine objects":
   self.max_score+=100
  if self.name=="kill the VIP":
   self.max_score+=50
   self.information["new_viptimer"]=timer.timer()
   self.information["new_vip"]=False
   self.information["vip_locationtimer"]=timer.timer()
   self.information["vip"]=""
   self.information["vip_points"]=0
   self.information["last_vip"]=""
  if self.name=="weapons competition":
   self.max_score+=10
   self.information["new_weapontimer"]=timer.timer()
   self.information["weapon"]=""
  if self.name=="making head shots":
   self.max_score+=30

  if self.name=="kill players":
   self.max_score+=50
  if self.name=="destroy objects":
   self.max_score+=30

 def save(self):
  data={
"name": self.name,
"time": self.timer.elapsed(),
"max_time": self.max_time,
"scores": self.scores,
}

  return data

 def load(self,data):
  self.name=data["name"]
  self.max_time=data["max_time"]
  self.timer.set(data["time"])
  try:
   self.scores=data["scores"]
  except:
   pass

 def stop(self):
  sorted_keys = sorted(self.scores, key=lambda x: self.scores[x], reverse=True)
  irange=1
  if len(sorted_keys)>=5:
   irange=3
  elif len(sorted_keys)>=3:
   irange=2
  elif len(sorted_keys)==0:
   irange=0
  for i in range(0,irange):
   if i==0:
    price=100
    position="first"
   if i==1:
    price=50
    position="second"
   if i==2:
    price=25
    position="tirth"

   index=get_players_index(sorted_keys[i])
   if index>-1:
    v.clients[index].data["event_points"]+=price
    v.clients[index].send("add_buffer_item misc well done; you received "+str(price)+" event points for beeing in the "+position+" place in the "+self.name+" event|n|buffer_sound misc eventpoint.ogg 0 0 0 1 0")
   else:
    try:
     data=sd.get("data",sorted_keys[i]+".plr",{},"players")
     data["event_points"]+=price
     sd.save("data",data,sorted_keys[i]+".plr","players")
    except:
     pass
  send_all("add_buffer_item misc the event "+self.name+" has ended and "+sorted_keys[0]+" was the winner|n|buffer_sound misc eventnotify.ogg 0 0 0 1 0")
  self.information={}
  v.events.remove(self)

def start_event(name,max_time):
 for e in v.events:
  if e.name==name:
   e.max_time+=max_time
   return
 e=event(name,max_time)
 for c in v.clients:
  e.scores[c.data["name"].lower()]=0
 send_all("add_buffer_item misc the "+name+" event has started.|n|buffer_sound misc eventnotify.ogg 0 0 0 1 0")
 v.events.append(e)
def add_score(playername,name,amount):
 index=get_players_index(playername)
 if index>-1:
  if v.clients[index].match_id>-1:
   return
 org_playername=playername
 for e in v.events:
  if e.name==name:
   old_amount=0
   try:
    old_amount=e.scores[playername.lower()]
   except:
    pass
   e.scores[playername.lower()]=amount+old_amount
   old_percent=math.floor(old_amount/e.max_score*100/5)
   new_percent=math.floor(e.scores[playername.lower()]/e.max_score*100/5)
   if new_percent>old_percent and new_percent<=20:
    index=get_players_index(org_playername)
    if index>-1:
     v.clients[index].data["event_points"]+=(new_percent*5)-(old_percent*5)
     if (new_percent*5)-(old_percent*5)==1:
      v.clients[index].send("add_buffer_item misc well done; you received an event point for progressing in the "+name+" event|n|buffer_sound misc eventpoint.ogg 0 0 0 1 0")
     else:
      v.clients[index].send("add_buffer_item misc well done; you received "+str((new_percent*5)-(old_percent*5))+" event points for progressing in the "+name+" event|n|buffer_sound misc eventpoint.ogg 0 0 0 1 0")


class ranked_event():
 def __init__(self,name):
  list=[]
  for a in v.ranked_events:
   list.append(a.id)
  self.id=random.randint(0,100000000)
  while self.id in list:
   self.id=random.randint(0,100000000)

  self.name=name
  self.scores={}
  self.rewards={}
  self.read_rewards()
 def read_rewards(self):
  self.rewards={}
  try:
   with open(r"reward_tracks/"+self.name+".txt", 'r') as f:
    items=f.read().split("\n")
    for i in items:
     parsed=i.split(":")
     try:
      self.rewards[items.index(i)]={
"name": parsed[0],
"amount": int(parsed[1]),
"points": int(parsed[2]),
"players": []}
     except:
      pass
  except:
   pass
 def save(self):
  data={
"name": self.name,
"rewards": self.rewards,
"scores": self.scores,
}

  return data

 def load(self,data):
  self.name=data["name"]
  self.rewards=data["rewards"]
  self.scores=data["scores"]

def get_ranked_events_index(name):
 for r in v.ranked_events:
  if r.name==name:
   return v.ranked_events.index(r)
 return -1

def eventloop():
        for e in v.events:
            if e.name == "weapons competition" and e.information["new_weapontimer"].elapsed() > 900000:
                e.information["new_weapontimer"].restart()
                if len(v.clients) > 0:
                    all_weapons = v.weapon_names
                    new_weapon = all_weapons[random.randint(
                        0, len(all_weapons)-1)]
                    while new_weapon == "m2_browning":
                        new_weapon = all_weapons[random.randint(
                            0, len(all_weapons)-1)]
                    e.information["weapon"] = new_weapon
                    send_all("add_buffer_item misc the current weapon has been changed to " +
                             e.information["weapon"]+"|n|buffer_sound misc eventnotify.ogg 0 0 0 1 0")

            if e.name == "kill the VIP" and e.information["vip_locationtimer"].elapsed() > 60000 and e.information["vip"] != "":
                e.information["vip_locationtimer"].restart()
                index = get_players_index(e.information["vip"])
                if index > -1:
                    send_all("add_buffer_item misc the current VIP  ("+e.information["vip"]+") is at "+map.get_region(v.clients[index].data["x"], v.clients[index].data["y"], v.clients[index].data["z"], v.clients[index].data["map"])+", at cordinates "+str(
                        round(v.clients[index].data["x"]))+", "+str(round(v.clients[index].data["y"]))+", "+str(round(v.clients[index].data["z"]))+"|n|buffer_sound misc vipnotify.ogg 0 0 0 1 0")
                else:
                    e.information["vip"] = ""

            if e.name == "kill the VIP" and e.information["new_viptimer"].elapsed() > 300000:
                e.information["new_viptimer"].restart()
                e.information["new_vip"] = True
                if e.information["vip"] != "":
                    send_all("add_buffer_item misc "+e.information["vip"]+" survived as vip and made "+str(
                        e.information["vip_points"])+" kills.")
                    add_score(
                        e.information["vip"], "kill the VIP", 15+(e.information["vip_points"]*3))
                    e.information["vip_points"] = 0
                    e.information["vip"] = ""

            if e.name == "kill the VIP" and e.information["new_vip"] == True:
                e.information["vip_points"] = 0
                clients = []
                for c in v.clients:
                    if c.lobby == False and c.data["name"] != e.information["last_vip"] and c.data["death"] == False and c.data["map"] == "main":
                        clients.append(c.data["name"])
                if len(clients) > 1:
                    number = random.randint(0, len(clients)-1)
                    e.information["vip"] = clients[number]
                    e.information["last_vip"] = clients[number]
                    e.information["new_vip"] = False
                    send_all("add_buffer_item misc " +
                             e.information["vip"]+" is now the VIP|n|buffer_sound misc vipnotify.ogg 0 0 0 1 0")
                else:
                    pass
