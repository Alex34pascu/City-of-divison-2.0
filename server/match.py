import teams
import random
import os
import event
import map
import timer
import weapons

import random
import v
v.get()

def get_players_index(name):
 for p in v.clients:
  if p.data["name"].lower()==name.lower():
   return v.clients.index(p)
 return -1

class match():
 def __init__(self,name,owner):
  list=[]
  for o in v.matches:
   list.append(o.id)
  self.id=random.randint(0,10000000)
  while id in list:
   self.id=random.randint(0,10000000)
  self.goodwin=True
  self.wintimer=timer.timer()
  self.winning=False
  self.name=name
  self.ranked_players=[]
  self.players=[owner]
  self.status="waiting"
  self.start_sound="rmstart_clock.ogg"
  self.map=""
  if self.name=="1v1_match":
   self.needed_players=2
   self.winning_players=1
   self.start_sound="rmstart_clock.ogg"
  elif self.name=="last_man_standing":
   self.needed_players=4
   self.winning_players=1
   self.start_sound="rmstart_hearbeat.ogg"
  else:
   self.needed_players=0
   self.winning_players=0

  self.gained_points={}
  index=get_players_index(owner)
  if index>-1:
   v.clients[index].store_data()
   v.clients[index].match_id=self.id
  self.weapons=self.chose_weapons(6)
  self.ranking_players={}
  self.friendly=False
  self.password=""

 def start(self):
        import answer as server_menu
        for p in self.players:
         index=get_players_index(p)
         if index>-1 and v.clients[index].match_id>-1:
          self.gained_points[p]=0
          v.clients[index].reset()
          try:
           for s in v.clients[index].skill_data:
            v.clients[index].skill_data[s]["active"]=False
          except:
           print("error with resetting skills.")
          if self.name=="1v1_match":
           v.clients[index].data["map"]="chose_weapons"+str(self.id)
          v.clients[index].change_weapon("")
          v.clients[index].inventory={}
          v.clients[index].remove_weapon("colt_m1911")
          v.clients[index].data["x"]=0
          v.clients[index].data["y"]=0
          v.clients[index].data["z"]=0
          against_players=self.players.copy()
          against_players.remove(v.clients[index].data["name"])
          v.clients[index].data["last_matched_players"]=sorted(against_players)
          if self.name=="1v1_match":
           server_menu.server_menu_answer(v.clients[index],"lobby_menu._Select_an_item","enter the map")
           v.clients[index].send("|n|stun 2000000|n|add_buffer_item misc you are matching against  "+v.get_list_in_text(against_players)+"|n|play_sound matchfound.ogg 0 0 0 1 0")
          if self.name=="last_man_standing":
           points=0
           if v.clients[index].data["ranked_points"]>=1000:
            points = round(v.clients[index].data["ranked_points"]*0.01)
           self.gained_points[v.clients[index].data["name"]]-=points
           v.clients[index].send("add_buffer_item misc you put in "+str(points)+" points in for the match.")
        if self.name=="1v1_match":
         self.status="chosing_weapons"
         self.ranked_players=self.get_lowest_rank_players()
         self.ranked_players[0].send("table_menu "+"\n".join(self.weapons))
        else:
         self.send("start_game|n|play_sound matchfound.ogg 0 0 0 1 0")
         self.choose_map()
         loot_out = map.get_loot_out(self.map)
         if loot_out:
          for p in self.players:
           index=get_players_index(p)
           if index>-1:
            loot_out.give(v.clients[index])
         self.send("add_buffer_item misc You are playing on "+self.map+". Description: "+v.get_description(self.map))
         self.status="playing"


 def chose_weapons(self,amount):
  final=[]
  all_weapons=v.weapon_names
  for i in range(amount):
   i=0
   while i==0:
    we=weapons.weapon(all_weapons[random.randint(0,len(all_weapons)-1)])
    if we.melee==False and we.name not in final and we.sort!="sniper_rifle" and we.sort!="machine_gun" and we.sort!="marksman_rifle":
     final.append(we.name)
     i=1
  return final
 def get_lowest_rank_players(self):
  players=[]
  for p in self.players:
   index=get_players_index(p)
   if index>-1:
    players.append(v.clients[index])
    self.ranking_players[p]=v.clients[index].data["ranked_points"]

  sorted_players = sorted(players, key=lambda p: p.data['ranked_points'], reverse=False)
  return sorted_players

 def gain_ranked_points(self, player_name, win, disconnection):
  text=""
  index=get_players_index(player_name)
  if index>-1:
   points=self.calculate_ranking_points(player_name,win, disconnection)
   v.clients[index].data["ranked_points"]+=points
   if points <0:
    text = "you lose"
   elif points >0:
    text = "you win"
   else:
    text="you get"
   v.clients[index].send("add_buffer_item misc "+text+" "+str(abs(points))+" ranking points")
   pindex = event.get_ranked_events_index(
   self.name)
   if pindex > -1 and self.friendly == False:
    v.ranked_events[pindex].scores[player_name.lower(
    )] = v.clients[index].data["ranked_points"]

 def calculate_ranking_points(self,playername,win, disconnection=False):
  if self.friendly==True:
   return 0
  elif self.name=="1v1_match":
   index=get_players_index(playername)
   if index>-1:
    if win==False:
     if v.clients[index].data["ranked_points"]<100:
      return 0
     else:
      try:
       a=round(v.clients[index].data["ranked_points"]-v.calculate_sum(self.ranking_players.values())+50)
      except:
       a=50
      if a>70:
       a=70
      if a<20:
       a=20
      return a*-1
   else:
    try:
     a=round((v.calculate_sum(self.ranking_players.values())-v.clients[index].data["ranked_points"])+65)
    except:
     a=65
    if a>85:
     a=70
    if a<35:
     a=35
    return a

  elif self.name=="last_man_standing":
   if playername in self.gained_points:
    return self.gained_points[playername]
   else:
    return 0
  else:
   return 0



 def send(self,message):
  for c in v.clients:
   if c.data["name"] in self.players:
    c.send(message)

 def select_map(self):
                    script_path = os.path.dirname(os.path.abspath(__file__))
                    folder_path = os.path.join(script_path, 'maps')
                    options = []
                    for filename in os.listdir(folder_path):
                        map_name = filename.replace(".txt", "")
                        spawn_list = map.get_spawn_points(map_name)
                        if len(spawn_list) == self.needed_players:
                            options.append(map_name)
                    return options[random.randint(0, len(options)-1)]

 def choose_map(self):
                    chosen_map=self.select_map()
                    self.map=chosen_map
                    map.copy_map(chosen_map, chosen_map +
                                 str(self.id))
                    f = open("maps/"+chosen_map+".txt", "r+")
                    data = f.read()
                    f.close()
                    l = ""
                    for f in map.objects:
                        o = map.objects[f]
                        if o.map != chosen_map+str(self.id):
                            continue
                        l = l+"|n|spawn_object "+str(o.minx)+" "+str(o.maxx)+" "+str(o.miny)+" "+str(
                            o.maxy)+" "+str(o.minz)+" "+str(o.maxz)+" "+o.name+" "+str(o.dir)+" "+str(o.id)+"|n|"
                        m = ""
                        for i in o.mapdata.split("\n"):
                            if o.actif == True or "permanent" in i:
                                m = m+"set_object_mapdata " + \
                                    str(o.id)+" "+i+"|n|"
                        l = l+m
                    to_send = ""
                    to_send=to_send+r"mapdata "+data+"|n|stun_reset|n|"+l +"|n|play_sound_dlg sounds\\"+self.start_sound+" 7525|n|"
                    spawn_list = map.get_spawn_points(chosen_map)
                    for p in self.players:
                        pindex = get_players_index(p)
                        if pindex > -1:
                            v.clients[pindex].data["map"] = chosen_map + \
                                str(self.id)
                            v.clients[pindex].data["x"] = spawn_list[self.players.index(
                                p)].x
                            v.clients[pindex].data["y"] = spawn_list[self.players.index(
                                p)].y
                            v.clients[pindex].data["z"] = spawn_list[self.players.index(
                                p)].z
                            v.clients[pindex].data["facing"] = spawn_list[self.players.index(
                                p)].facing
                            to_send = to_send+"spawn_player "+str(v.clients[pindex].data["x"])+" "+str(v.clients[pindex].data["y"])+" "+str(v.clients[pindex].data["z"])+" "+v.clients[pindex].data["name"]+"|n|set_player_weapon "+v.clients[pindex].data["name"]+" "+v.clients[pindex].data["weapon"]+"|n|set_player_weapon " + \
                                v.clients[pindex].data["name"]+" "+v.clients[pindex].data["weapon"]+"|n|set_players_silencer "+v.clients[pindex].data["name"]+" "+str(
                                    v.clients[pindex].has_silencer(v.clients[pindex].data["weapon"]))

                            v.clients[pindex].send("go "+str(v.clients[pindex].data["x"])+" "+str(v.clients[pindex].data["y"])+" "+str(v.clients[pindex].data["z"]) +
                                                   "|n|set_weapon "+v.clients[pindex].data["weapon"]+"|n|set_facing "+str(v.clients[pindex].data["facing"])+" "+str(v.clients[pindex].data["updown"]))
                    self.send(to_send)

 def remove_player(self, player_name, killer):
  self.players.remove(player_name)
  if self.name=="last_man_standing":
   self.send("play_sound lms_death.ogg 0 0 0 1 0")
   if killer in self.gained_points.keys():
    self.gained_points[killer]+=50
   if len(self.players) == self.winning_players*2:
    for p in self.gained_points:
     self.gained_points[p]+=100
   if len(self.players) == self.winning_players:
    for p in self.gained_points:
     self.gained_points[p]+=200
  if player_name in self.gained_points:
   del self.gained_points[player_name]
  if len(self.players) == self.winning_players:
   self.goodwin = killer != ""
   self.winning = True
   self.wintimer.restart()
   self.send(
   "play_sound matchwin.ogg 0 0 0 1 0|n|add_buffer_item misc Congratulations! You have won the match|n|stun 10000")

def get_matches_index(id):
 for p in v.matches:
  if p.id==id:
   return v.matches.index(p)
 return -1


def exsist_match(password):
 for m in v.matches:
  if m.friendly==True and m.password==password and m.status=="waiting":
   return m
 return None

def matchloop():
            for m in v.matches:
                if len(m.players) == 0:
                    v.matches.remove(m)
                    break
                if m.status == "chosing_weapons":
                    m.send("stun 2000000")
                if m.winning == True and m.wintimer.elapsed() > 3000:
                    for p in m.players:
                        index = get_players_index(p)
                        if index > -1:
                                map.reset_map(v.clients[index].data["map"])
                                v.clients[index].get_data()
                                points = m.calculate_ranking_points(
                                    v.clients[index].data["name"], True)
                                if m.goodwin == True:
                                    v.clients[index].data["ranked_points"] += points
                                    pindex = event.get_ranked_events_index(
                                        m.name)
                                    if pindex > -1 and m.friendly == False:
                                        v.ranked_events[pindex].scores[v.clients[index].data["name"].lower(
                                        )] = v.clients[index].data["ranked_points"]
                                    v.clients[index].send(
                                        "add_buffer_item misc you win "+str(points)+" ranking points for winning this match.")
                                    v.clients[index].match_id = -1
                                    v.clients[index].send("go_lobby")
                    v.matches.remove(m)
                    break
                i = 0
                if len(m.players) == 1 and m.status == "waiting":
                    index=get_players_index(m.players[0])
                    for m2 in v.matches:
                        pindex = get_players_index(m.players[0])
                        if pindex > -1 and v.clients[index].match_id == -1:
                            continue
                        the_players = sorted(m2.players)
#and the_players != v.clients[pindex].data["last_matched_players"] 
                        if m2.status == "waiting" and m2.name == m.name and m.id != m2.id and len(m2.players) < m2.needed_players and v.clients[index].data["name"] not in m2.players and m2.password == m.password:
                            m2.players.append(m.players[0])
                            index = get_players_index(m.players[0])
                            if index > -1 and v.clients[index].match_id > -1:
                                v.clients[index].match_id = m2.id
                            if m2.status == "waiting" and len(m2.players) >= m2.needed_players:
                                for p in m2.players:
                                    index = get_players_index(p)
                                    if index > -1 and v.clients[index].match_id > -1:
                                        against_players = m2.players.copy()
                                        against_players.remove(
                                            v.clients[index].data["name"])
                                        v.clients[index].data["last_matched_players"] = sorted(
                                            against_players)
                                        v.clients[index].store_data(True)
                                m2.start()
                            else:
                             m2.send("speak "+str(len(m2.players))+" players|n|play_sound notification_pop_.ogg 0 0 0 1 0")
                            i = 1
                            break
                if i == 1:
                    v.matches.remove(m)
                    break

