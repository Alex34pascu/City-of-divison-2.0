import timer
import scanner
import healing
import explosives as expl
import sd
import answer as server_menu
import match
import trap
import math
import rotation
import os
import weapons
import quests
import random
import teams
import map
import datetime
import v
v.get()

def get_current_time():
    nu = datetime.datetime.now()
    tijd = nu.strftime("%H:%M:%S")
    return tijd


def get_current_date():
    nu = datetime.datetime.now()
    datum = nu.strftime("%Y %m %d")

    return datum


def get_players_index(name):
    for p in v.clients:
        if p.data["name"].lower() == name.lower():
            return v.clients.index(p)
    return -1


def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def send_all(message, map=""):
    v.send_packet_to_clients(message, v.clients, map)


class packet_handler():
    def __init__(self, client):
        self.client = client
        self.data=""

    def lobby(self, parsed):
        if self.client.lobby == False:
            for e in v.events:
                if e.name == "kill the VIP":
                    if e.information["vip"] == self.client.data["name"]:
                        e.information["vip"] = ""
                        send_all(
                            "add_buffer_item misc the current VIP has gone to the lobby and is no longer a VIP|n|buffer_sound misc eventnotify.ogg 0 0 0 1 0")
            for c in v.clients:
                if c.data["name"] != self.client.data["name"] and self.client.data["map"] == c.data["map"] and c.lobby == False:
                    c.send("play_sound mapleave.ogg 0 0 0 1 0")
        self.client.lobby = True
        self.client.survivetimer.pause()
        self.client.send("players_check  ")
        send_all("remove_player "+self.client.data["name"])
    def use_skill(self, parsed):
                    skill_name = self.client.get_usable_skills(int(parsed[1]))
                    if skill_name == "":
                        self.client.send(
                            "speak there is no skil on skill slot "+parsed[1])
                    else:
                        self.client.use_skill(skill_name)
    def player_info(self, parsed):
                    self.client.data["selected_player"] = parsed[1]
                    server_menu.server_menu_answer(
                        self.client, "select_an_option_for_"+self.client.data["selected_player"], "view the profile of this player")
    def team_chat(self,parsed):
                    if teams.get_team(self.client.data["name"]) == "":
                        self.client.send("speak you aren't in a team.")
                        return
                    self.client.send("input type_your_team_chat ")
    def staff_chat(self, parsed):
                    if self.client.data["admin"] == 1 or self.client.data["builder"] == 1 or self.client.data["moderator"] == 1:
                        self.client.send(
                            "input type_your_staff_chat._Press_enter_when_you_are_done. ")
    def mute_chat(self, parsed):
                    index = get_players_index(parsed[1])
                    if index > -1:
                        v.clients[index].data["org_mutetime"] = int(parsed[2])
                        v.clients[index].mutetimer.restart()
                        self.client.send("speak succesfully muted")
    def stop_finding_match(self, parsed):
                    index = match.get_matches_index(self.client.match_id)
                    if index > -1 and v.matches[index].status == "waiting":
                        v.matches[index].players.remove(self.client.data["name"])
                        if len(v.matches[index].players) == 0:
                            del v.matches[index]
                        else:
                         v.matches[index].send("speak "+str(len(v.matches[index].players))+" players")
                        self.client.match_id = -1

    def server_menu_answer(self,parsed):
                    data=self.data
                    server_menu.server_menu_answer(self.client, parsed[1], data.replace(
                        "server_menu_answer "+parsed[1]+" ", ""))
    def server_mega_menu_answer(self,parsed):
                    data=self.data
                    server_menu.server_mega_menu_answer(self.client, parsed[1], parsed[2], data.replace(
                        "server_mega_menu_answer "+parsed[1]+" "+parsed[2]+" ", ""))

    def calculation_answer(self, parsed):
                    things = parsed[1].split("_")
                    n1, operator, n2 = things[0], things[1], things[2]
                    answer = 0
                    try:
                        if operator == "+":
                            answer = int(n1)+int(n2)
                        if operator == "-":
                            answer = int(n1)-int(n2)
                        if operator == "*":
                            answer = int(n1)*int(n2)
                        if operator == "/":
                            answer = int(n1)/int(n2)
                    except:
                        self.client.send("speak error: please contact the admins.")
                    answer = round(answer)
                    if int(parsed[2]) == answer:
                        send_all(
                            r"player_sound "+self.client.data["name"]+" sounds\\lockerinputcorrect.ogg 0")
                        o = map.get_objects_index(
                            self.client.data["calculation_locker"])
                        if o != "":
                            map.objects[o].math += 1
                            if map.objects[o].math >= map.objects[o].max_math:
                                map.objects[o].data["opened"] = True
                                self.client.send(
                                    "speak you open the door of the locker")
                                send_all(
                                    r"player_sound "+self.client.data["name"]+" sounds\\lockeropen.ogg 0")
                                return
                            n1, n2, operator = map.objects[o].create_calculation(
                            )
                            self.client.send("calculation "+str(n1) +
                                      "_"+operator+"_"+str(n2))
                    else:
                        o = map.get_objects_index(
                            self.client.data["calculation_locker"])
                        if o != "":
                            map.objects[o].math = 0
                        self.client.send("speak wrong")
                        send_all(
                            r"player_sound "+self.client.data["name"]+" sounds\\lockerinputfail.ogg 0")
    def locker_simon_fail(self, parsed):
                    o = map.get_objects_index(self.client.data["calculation_locker"])
                    if o != "":
                        if map.objects[o].name == "metal_fortress":
                            self.client.data["health"] -= 200
                            self.client.data["last_hit"] = "the alarm system of the " + \
                                map.objects[o].team+"'s metal fortress"
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\electricityhit"+str(random.randint(1, 3))+".ogg 0")

    def locker_simon_good(self, parsed):
                    o = map.get_objects_index(self.client.data["calculation_locker"])
                    if o != "":
                        if map.objects[o].name == "locker":
                            map.objects[o].data["opened"] = True
                            self.client.send("speak you open the door of the locker")
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\lockeropen.ogg 0|n|player_sound "+self.client.data["name"]+" sounds\\simoncomplete.ogg 0")
                        elif map.objects[o].name == "metal_fortress":
                            map.objects[o].data["alarm"] = False
                            map.objects[o].alarm_players = {}
                            self.client.send("speak alarm turned off.")
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\simoncomplete.ogg 0")

    def input_answer(self, parsed):
                    data=self.data
                    server_menu.input_answer(self.client, parsed[1], data.replace(
                        "input_answer "+parsed[1]+" ", ""))

    def server_menu(self, parsed):
                    name = "server_menu._Select_an_item"
                    options = ["announcements", "view active events", "view levels", "changes", "set chat channel", "contact staff",
                               "your current_ staff messages", "view staff members", "view documentation", "account settings"]
                    if len(self.client.data["mutelist"]) > 0:
                        options.append("unmute someone")
                    if self.client.data["admin"] == 1 or self.client.data["builder"] == 1 or self.client.data["moderator"] == 1:
                        options.append("options that belong to your rank")
                    optionslist = "\n".join(options)
                    self.client.send("server_menu "+name+" "+optionslist)
    def lobby_menu(self, parsed):
                    name = "lobby_menu._Select_an_item"
                    options = ["enter the map", "ranked mode", "view events", "visit the event shop",
                               "teams", "story and quests", "manage skills", "my account"]
                    optionslist = "\n".join(options)
                    self.client.send("server_menu "+name+" "+optionslist)
    def start_game(self, parsed):
                    self.client.survivetimer.resume()
                    self.client.lobby = False
    def set_name(self, parsed):
                    self.client.survivetimer.resume()
                    self.client.lobby = False
                    self.client.data["name"] = parsed[1]
                    for c in v.clients:
                        if c.data["name"] != self.client.data["name"] and self.client.data["map"] == c.data["map"] and c.lobby == False:
                            c.send("spawn_player "+str(self.client.data["x"])+" "+str(self.client.data["y"])+" "+str(self.client.data["z"])+" "+self.client.data["name"]+"|n|set_player_weapon "+self.client.data["name"]+" "+self.client.data["weapon"]+"|n|set_player_weapon " +
                                   self.client.data["name"]+" "+self.client.data["weapon"]+"|n|set_players_silencer "+self.client.data["name"]+" "+str(self.client.has_silencer(self.client.data["weapon"]))+"|n|set_team "+self.client.data["name"]+" "+teams.get_team(self.client.data["name"]))
                            c.send("play_sound mapjoin.ogg 0 0 0 1 0|n|")
                        if c.data["death"] == False and c.lobby == False and c.data["map"] == self.client.data["map"]:
                            self.client.send("spawn_player "+str(c.data["x"])+" "+str(c.data["y"])+" "+str(c.data["z"])+" "+c.data["name"]+"|n|set_player_weapon "+c.data["name"]+" "+c.data["weapon"] +
                                      "|n|set_players_silencer "+c.data["name"]+" "+str(c.has_silencer(c.data["weapon"]))+"|n|set_team "+c.data["name"]+" "+teams.get_team(c.data["name"]))
                    self.client.send("go "+str(self.client.data["x"])+" "+str(self.client.data["y"])+" "+str(self.client.data["z"])+"|n|set_weapon "+self.client.data["weapon"] +
                              "|n|set_facing "+str(self.client.data["facing"])+" "+str(self.client.data["updown"])+"|n|get_weapons "+"||".join(self.client.data["weapons"]))

    def object_mapdata(self, parsed):
                    l = ""
                    for f in map.objects:
                        o = map.objects[f]
                        if o.map != self.client.data["map"]:
                            continue
                        l = l+"|n|spawn_object "+str(int(o.minx))+" "+str(int(o.maxx))+" "+str(int(o.miny))+" "+str(
                            int(o.maxy))+" "+str(int(o.minz))+" "+str(o.maxz)+" "+o.name+" "+str(o.dir)+" "+str(o.id)+"|n|"
                        m = ""
                        if o.actif:
                            m="set_object_mapdata "+str(o.id)+" "+o.mapdata+"|n|"
                        else:
                         for i in o.mapdata.split("\n"):
                             if "permanent" in i:
                                 m = m+"set_object_mapdata " + \
                                     str(o.id)+" "+i+"|n|"
                        l = l+m
                    self.client.send(l)

    def falling_damage(self, parsed):
                    damage = int(parsed[1])
                    self.client.data["fall_distance"] = round(damage/20)
                    damage -= 200
                    if self.client.skill_data["landing knowledge"]["active"] == True:
                        min = 1 - \
                            self.client.skill_data["landing knowledge"]["level"]/10
                        damage = damage*min
                    self.client.data["health"] -= damage
                    self.client.data["last_weapon"] = "grafity"
                    self.client.data["last_hit"] = "a " + \
                        str(self.client.data["fall_distance"])+" meter fall"
                    if self.client.drawn_weapon and self.client.drawn_weapon.sort != "melee":
                        self.client.drawn_weapon.degradation += self.client.data["fall_distance"]*2
                        send_all(
                            r"player_sound "+self.client.data["name"]+" sounds\\"+self.client.drawn_weapon.sort+"fall.ogg 0")
    def connect(self, parsed):
                    self.client.loggin(parsed[1], parsed[2], parsed[3], parsed[4])
    def password_reset2(self, parsed):
                    try:
                        key = int(parsed[1])
                    except:
                        self.client.send("dlg key isn't valid")
                        v.clients.remove(self.client)
                        return
                    try:
                        name = v.password_resets[str(key)]
                        if name != "":
                            new_data = sd.get(
                                "data", name+".plr", {}, "players")
                            dec_key = b"Dit is een gehei"
                            p = v.aes_cipher(parsed[2], dec_key)
                            password = ""+p.hex()
                            new_data["password"] = password
                            self.client.send("dlg password has been set")
                            sd.save("data", new_data, name+".plr", "players")
                            del v.password_resets[str(key)]
                            v.clients.remove(self.client)
                            return
                        else:
                            self.client.send("dlg key isn't valid")
                            v.clients.remove(self.client)
                            return
                    except:
                        self.client.send("dlg key isn't valid")
                        v.clients.remove(self.client)
                        return

    def password_reset(self, parsed):
                    self.client.send("dlg this feature has been disabled for now")
                    return
                    name = parsed[1]
                    new_data = sd.get("data", name+".plr", {}, "players")
                    if new_data == {}:
                        self.client.send("not_exsist")
                        v.clients.remove(self.client)
                        return
                    key = random.randint(1000, 9999)
                    v.password_resets[str(key)] = name
                    body = """
hello """+name+""",
this is your password reset key that you've requested.
"""+str(key)+"""
If this wasn't you, you can ignore this email.
kind regards,
the Firegaming team
"""
                    e = v.mail(new_data["mail"], "password reset", body)
                    if e != "succes":
                        self.client.send("dlg error with sending the mail "+str(e))
                    else:
                        self.client.send(
                            "dlg e-mail has been send. Make sure you check your spam folder.")
                    return

    def create_account(self, parsed):
                    self.client.loggin(parsed[1], parsed[2],
                                parsed[3], parsed[4], True)

    def go_player(self, parsed):
                    index = get_players_index(parsed[4])
                    if index == -1:
                        self.client.send("speak this player isn't online")
                        return
                    v.clients[index].data["x"] = int(parsed[1])
                    v.clients[index].data["y"] = int(parsed[2])
                    v.clients[index].data["z"] = int(parsed[3])
                    v.clients[index].send("go "+str(v.clients[index].data["x"])+" "+str(
                        v.clients[index].data["y"])+" "+str(v.clients[index].data["z"]))
                    send_all("move_player "+v.clients[index].data["name"]+" "+str(v.clients[index].data["x"])+" "+str(
                        v.clients[index].data["y"])+" "+str(v.clients[index].data["z"]))
                    self.client.send("speak moved")
    def kick(self, parsed):
                    index = get_players_index(parsed[1])
                    if index == -1:
                        self.client.send("speak this player isn't online")
                        return
                    send_all("add_buffer_item misc " +
                             v.clients[index].data["name"]+" has been kicked from the server")
                    v.clients[index].send("kick")
                    v.clients[index].disconnect(True)
    def ban(self, parsed):
                    index = get_players_index(parsed[1])
                    if index == -1:
                        self.client.send("speak this player isn't online")
                        return
                    send_all("add_buffer_item misc " +
                             v.clients[index].data["name"]+" has been banned from the server")
                    v.clients[index].send("ban")
                    v.banlist[v.clients[index].data["name"]
                              ] = v.clients[index].comp_id
                    v.clients[index].disconnect(True)
    def spawn_c4(self, parsed):
                    self.client.give("c4", -1)
                    c = expl.c4(self.client.data["x"], self.client.data["y"], self.client.data["z"],
                                self.client.data["map"], self.client.data["name"], int(parsed[1])*1000)
                    v.c4s.append(c)
    def use_item(self, parsed):
                    if self.client.invpos == -1:
                        self.client.send("speak not focussed on an item.")
                        return
                    dic = list(self.client.inventory.keys())
                    if len(dic) == 0:
                        return
                    percent = self.client.data["health"]/self.client.data["max_health"]
                    percent = percent*100
                    try:
                        item = (dic[self.client.invpos])
                    except:
                        return
                    if item == "tool_box":
                        upgrades = self.client.drawn_weapon.get_upgrades()
                        if len(upgrades) <= 0:
                            self.client.send(
                                "speak there are no upgrades available for this weapon")
                            return
                        self.client.send("tool_box_menu "+"\n".join(upgrades))
                    if item == "spike_trap":
                        if self.client.can_place_trap():
                            trap.spawn_trap(self.client.data["x"], self.client.data["x"], self.client.data["y"], self.client.data["y"], self.client.data["z"],
                                            self.client.data["z"], self.client.data["map"], item, self.client.data["name"], teams.get_team(self.client.data["name"]))
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\"+item+"place.ogg 0")
                            self.client.give(item, -1)
                            self.client.send("stun 3000")
                    if item == "tripwire":
                        if self.client.can_place_trap():
                            trap.spawn_trap(self.client.data["x"], self.client.data["x"], self.client.data["y"], self.client.data["y"], self.client.data["z"],
                                            self.client.data["z"], self.client.data["map"], item, self.client.data["name"], teams.get_team(self.client.data["name"]))
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\"+item+"place.ogg 0")
                            self.client.give(item, -1)
                            self.client.send("stun 3000")

                    if item == "team_phone":
                        team_name = teams.get_team(self.client.data["name"])
                        if team_name == "":
                            self.client.send("speak you aren'tin a team.")
                            return
                        if map.has_metal_fortress(team_name) == False:
                            self.client.send(
                                "speak your team doesn't have a metal fortress.")
                            return
                        options = ["place an order", "view my shipment status", "my team's traps", "view team notes",
                                   "place a team note", "remove a team note", "alarm for the metal fortress switch"]
                        self.client.shopping_cart = {}
                        self.client.send("phone_menu "+"\n".join(options))
                        send_all(
                            r"player_sound "+self.client.data["name"]+" sounds\\\phoneactivate.ogg 0")

                    if item == "metal_fortress":
                        if self.client.data["map"]!="main":
                         self.client.send("speak you have to place a "+item+" on the main map")
                         return

                        if teams.get_team(self.client.data["name"]) == "":
                            self.client.send(
                                "speak you must be in a team to place a metal fortress.")
                            return
                        i = 0
#                        for c in v.clients:
#                            if get_3d_distance(c.data["x"], c.data["y"], c.data["z"], self.client.data["x"], self.client.data["y"], self.client.data["z"]) <= 5 and self.client.data["map"] == c.data["map"] and c.data["name"] != self.client.data["name"] and teams.get_team(c.data["name"]) == teams.get_team(self.client.data["name"]):
#                                i = 1
                        i = 1
                        if i == 0:
                            self.client.send(
                                "speak you need to have a team mate near you to build the fortress.")
                            return
                        index = teams.get_teams_index(
                            teams.get_team(self.client.data["name"]))
                        if index == -1:
                            self.client.send("speak your team doesn't exsist")
                            return
                        for f in map.objects:
                            o = map.objects[f]
                            if o.name == "metal_fortress" and o.team == teams.get_team(self.client.data["name"]):
                                self.client.send(
                                    "speak your team has already a metal_fortress.")
                                return
                        metal_fortress_x = self.client.data["x"]
                        metal_fortress_y = self.client.data["y"]
                        metal_fortress_z = self.client.data["z"]
                        metal_fortress = map.get_things_in_area(
                            metal_fortress_x-10, metal_fortress_x+10, metal_fortress_y-10, metal_fortress_y+10, metal_fortress_z, metal_fortress_z+30, self.client.data["map"])
                        f = metal_fortress.replace("|wall|", "")
                        if f == metal_fortress:
                            metal_fortress = map.get_things_in_area(
                                metal_fortress_x-5, metal_fortress_x+5, metal_fortress_y-5, metal_fortress_y+5, metal_fortress_z-1, metal_fortress_z-1, self.client.data["map"], True, False)
                            f = metal_fortress.replace("||", "")
                            f = f.replace("|blank|", "")
                            count = f.count("wall")
                            if f == metal_fortress and map.get_object(metal_fortress_x, metal_fortress_y, self.client.data["z"]-1, self.client.data["map"]) != "" and count >= 100:
                                if map.get_platform(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"]) != "" and map.get_platform(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"]) != "blank":
                                    l = map.metal_fortress(metal_fortress_x-5, metal_fortress_x+5, metal_fortress_y-5, metal_fortress_y+5,
                                                           metal_fortress_z, metal_fortress_z+23, self.client.data["map"], teams.get_team(self.client.data["name"]))
                                    map.objects[str(l.id)] = l
                                    self.client.give(item, -1)
                                    send_all(
                                        r"player_sound "+self.client.data["name"]+" sounds\\metal_fortressplace.ogg 0")
                                    self.client.send("stun 8000")
                                    tindex = teams.get_teams_index(
                                        teams.get_team(self.client.data["name"]))
                                    if tindex > -1:
                                        for t in v.teams[tindex].members:
                                            index = get_players_index(t)
                                            if index > -1:
                                                v.clients[index].give(
                                                    "team_phone", 1)
                                else:
                                    self.client.send(
                                        "speak can't place a metal fortress while you are in the air.")
                            else:
                                self.client.send(
                                    "speak can't place a metal fortress here.")
                        else:
                            self.client.send(
                                "speak can't place a metal fortress here.")

                    if item == "metal_sheat":
                        if self.client.inv_check(item) < 6:
                            self.client.send(
                                "speak you need to have 6 metal sheats to build a fortress.")
                            return
                        if self.client.inv_check("welding_machine") <= 0 or self.client.inv_check("welding_machine_battery") < 2:
                            self.client.send(
                                "speak you need to have a welding machine and two welding_machine_batterys to build a fortress.")
                            return
                        self.client.give(item, -6)
                        self.client.give("metal_fortress", 1)
                        self.client.give("welding_machine_battery",-2)
                        send_all(
                            r"player_sound "+self.client.data["name"]+" sounds\\metal_fortressbuild.ogg 0")
                        self.client.send("stun 22000")

                    if item == "metal_fortress_construction_kit":
                        self.client.give(item, -1)
                        self.client.give("metal_sheat", 6)
                        send_all(r"player_sound " +
                                 self.client.data["name"]+" sounds\\"+item+"open.ogg 0")
                        self.client.send("stun 2750")
                    if item == "RCE_controller":
                        send_all(
                            r"player_sound "+self.client.data["name"]+" sounds\\RCEcontrolerdraw.ogg 0")
                        self.client.send(
                            "code_menu type_the_code_you_want_to_explode")
                    if item == "R_C_E":
                        self.client.send(
                            "code_menu type_the_code_for_detenating_this_R_C_E")

                    if item == "RCE_package":
                        self.client.give("RCE_package", -1)
                        self.client.give("R_C_E", 1)
                        self.client.give("RCE_controller", 1)
                        send_all(
                            r"player_sound "+self.client.data["name"]+" sounds\\RCE_packageopen.ogg 0")
                        self.client.send("stun 3000")
                    if item == "ladder":
                        check_z = self.client.data["z"]
                        check_x, check_y = rotation.move(
                            self.client.data["x"], self.client.data["y"], self.client.data["facing"])
                        check_x = round(check_x)
                        check_y = round(check_y)
                        dir = 0
                        if self.client.data["facing"] == 0:
                            dir = 3
                        if self.client.data["facing"] == 90:
                            dir = 2
                        if self.client.data["facing"] == 180:
                            dir = 1
                        if self.client.data["facing"] == 270:
                            dir = 4
                        if dir == 0:
                            self.client.send(
                                "speak you need to be facing north, east ,south or west to place a ladder")
                            return
                        if dir == 3:
                            check = map.get_things_in_area(
                                check_x-1, check_x+1, check_y, check_y+1, check_z, check_z+20, self.client.data["map"])
                        if dir == 1:
                            check = map.get_things_in_area(
                                check_x-1, check_x+1, check_y-1, check_y, check_z, check_z+20, self.client.data["map"])
                        if dir == 4:
                            check = map.get_things_in_area(
                                check_x-1, check_x, check_y-1, check_y+1, check_z, check_z+20, self.client.data["map"])
                        if dir == 2:
                            check = map.get_things_in_area(
                                check_x, check_x+1, check_y-1, check_y+1, check_z, check_z+20, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        good_tiles = check.count("||")+check.count("|blank|")
                        f = f.replace("|player|", "")
                        if f == check and good_tiles >= 120:
                            if dir == 3:
                                check = map.get_things_in_area(
                                    check_x-1, check_x+1, check_y, check_y+1, check_z-1, check_z-1, self.client.data["map"], True, False)
                            if dir == 1:
                                check = map.get_things_in_area(
                                    check_x-1, check_x+1, check_y, check_y-1, check_z-1, check_z-1, self.client.data["map"], True, False)
                            if dir == 4:
                                check = map.get_things_in_area(
                                    check_x-1, check_x, check_y-1, check_y+1, check_z-1, check_z-1, self.client.data["map"], True, False)
                            if dir == 2:
                                check = map.get_things_in_area(
                                    check_x, check_x+1, check_y-1, check_y+1, check_z-1, check_z-1, self.client.data["map"], True, False)
                            f = check.replace("||", "")
                            f = f.replace("|blank|", "")
                            if f == check and map.get_object(check_x, check_y, self.client.data["z"]-1, self.client.data["map"]) != "":
                                if dir == 3:
                                    check = map.get_things_in_area(
                                        check_x-1, check_x+1, check_y+2, check_y+2, check_z, check_z+20, self.client.data["map"], True, False)
                                if dir == 1:
                                    check = map.get_things_in_area(
                                        check_x-1, check_x+1, check_y-2, check_y-2, check_z, check_z+20, self.client.data["map"], True, False)
                                if dir == 4:
                                    check = map.get_things_in_area(
                                        check_x-2, check_x-2, check_y-1, check_y+1, check_z, check_z+20, self.client.data["map"], True, False)
                                if dir == 2:
                                    check = map.get_things_in_area(
                                        check_x+2, check_x+2, check_y-1, check_y+1, check_z, check_z+20, self.client.data["map"], True, False)
                                walls = check.count("wall")
                                if walls >= 57:
                                    if map.get_platform(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"]) != "" and map.get_platform(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"]) != "blank":
                                        map.spawn_object(
                                            check_x-1, check_x+1, check_y, check_y, check_z, check_z+20, "ladder", dir, self.client.data["map"], False)

                                        self.client.give(item, -1)
                                        send_all(
                                            r"player_sound "+self.client.data["name"]+" sounds\\ladderplace.ogg 0")
                                        self.client.send("stun 3000")

                                    else:
                                        self.client.send(
                                            "speak can't place a ladder while you are in the air.")
                                else:
                                    self.client.send(
                                        "speak you need to place a ladder against a wall.")

                            else:
                                self.client.send(
                                    "speak can't place a ladder here, since the surface is unstable")
                        else:
                            self.client.send("speak can't place a ladder here.")
                    if item == "barricade":
                        self.client.data["x"] = round(self.client.data["x"])
                        self.client.data["y"] = round(self.client.data["y"])

                        check_z = self.client.data["z"]
                        check_x, check_y = rotation.move(
                            self.client.data["x"], self.client.data["y"], self.client.data["facing"])
                        check_x = round(check_x)
                        check_y = round(check_y)
                        dir = 0
                        if self.client.data["facing"] == 0:
                            dir = 3
                        if self.client.data["facing"] == 90:
                            dir = 2
                        if self.client.data["facing"] == 180:
                            dir = 1
                        if self.client.data["facing"] == 270:
                            dir = 4
                        if dir == 0:
                            self.client.send(
                                "speak you need to be facing north, east ,south or west to place a barricade")
                            return
                        if dir == 3:
                            check = map.get_things_in_area(
                                check_x-1, check_x+1, check_y, check_y, check_z, check_z+7, self.client.data["map"])
                        if dir == 1:
                            check = map.get_things_in_area(
                                check_x-1, check_x+1, check_y, check_y, check_z, check_z+7, self.client.data["map"])
                        if dir == 4:
                            check = map.get_things_in_area(
                                check_x, check_x, check_y-1, check_y+1, check_z, check_z+7, self.client.data["map"])
                        if dir == 2:
                            check = map.get_things_in_area(
                                check_x, check_x, check_y-1, check_y+1, check_z, check_z+7, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            if dir == 3:
                                check = map.get_things_in_area(
                                    check_x-1, check_x+1, check_y, check_y, check_z-1, check_z-1, self.client.data["map"], True, False)
                            if dir == 1:
                                check = map.get_things_in_area(
                                    check_x-1, check_x+1, check_y, check_y, check_z-1, check_z-1, self.client.data["map"], True, False)
                            if dir == 4:
                                check = map.get_things_in_area(
                                    check_x, check_x, check_y-1, check_y+1, check_z-1, check_z-1, self.client.data["map"], True, False)
                            if dir == 2:
                                check = map.get_things_in_area(
                                    check_x, check_x, check_y-1, check_y+1, check_z-1, check_z-1, self.client.data["map"], True, False)
                            f = check.replace("||", "")
                            f = f.replace("|blank|", "")
                            if f == check and map.get_object(check_x, check_y, self.client.data["z"]-1, self.client.data["map"]) != "":
                                if self.client.can_place_barricade():
                                    if map.get_platform(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"]) != "" and map.get_platform(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"]) != "blank":
                                        if dir == 3:
                                            map.spawn_object(self.client.data["x"]-1, self.client.data["x"]+1, self.client.data["y"]+1,
                                                             self.client.data["y"]+1, check_z, check_z+7, "barricade", dir, self.client.data["map"], False)
                                        elif dir == 1:
                                            map.spawn_object(self.client.data["x"]-1, self.client.data["x"]+1, self.client.data["y"]-1,
                                                             self.client.data["y"]-1, check_z, check_z+7, "barricade", dir, self.client.data["map"], False)
                                        elif dir == 2:
                                            map.spawn_object(self.client.data["x"]+1, self.client.data["x"]+1, self.client.data["y"]-1,
                                                             self.client.data["y"]+1, check_z, check_z+7, "barricade", dir, self.client.data["map"], False)
                                        elif dir == 4:
                                            map.spawn_object(self.client.data["x"]-1, self.client.data["x"]-1, self.client.data["y"]-1,
                                                             self.client.data["y"]+1, check_z, check_z+7, "barricade", dir, self.client.data["map"], False)

                                        self.client.give(item, -1)
                                        send_all(
                                            r"player_sound "+self.client.data["name"]+" sounds\\barricadeplace.ogg 0")
                                        self.client.send("stun 3000")

                                    else:
                                        self.client.send(
                                            "speak can't place a barricade while you are in the air.")

                            else:
                                self.client.send(
                                    "speak can't place a barricade here, since the surface is unstable")
                        else:
                            self.client.send("speak can't place a barricade here.")

                    if item == "helmet":
                        if self.client.armor[item]["wearing"] == False:
                            self.client.armor[item]["wearing"] = True
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\"+item+"wear.ogg 0")
                            self.client.send("speak you put the " +
                                      item+" on.|n|stun 2500")
                        else:
                            self.client.armor[item]["wearing"] = False
                            self.client.send("speak you put the " +
                                      item+" off|n|stun 1500")
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\"+item+"remove.ogg 0")

                    if item == "bulletproof_vest":
                        if self.client.armor[item]["wearing"] == False:
                            self.client.armor[item]["wearing"] = True
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\"+item+"wear.ogg 0")
                            self.client.send("speak you put the " +
                                      item+" on.|n|stun 8800")
                        else:
                            self.client.armor[item]["wearing"] = False
                            self.client.send("speak you put the " +
                                      item+" off|n|stun 4500")
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\"+item+"remove.ogg 0")
                    if item == "bandage":
                        if percent >= 100:
                            self.client.send("speak you can only heal to " +
                                      str(round(percent))+"% health with this item.")
                        else:
                            self.client.send("stun 5500")
                            self.client.give(item, -1)
                            send_all(
                                "player_sound "+self.client.data["name"]+" sounds\\bandageuse.ogg 0")
                            healing.set_heal(
                                self.client.data["name"], item, 500, 20, 5500, 100)
                    if item == "first_aid_kit":
                        if percent >= 100:
                            self.client.send("speak you can only heal to " +
                                      str(round(percent))+"% health with this item.")
                        else:
                            self.client.send("stun 17200")
                            self.client.give(item, -1)
                            send_all(
                                "player_sound "+self.client.data["name"]+" sounds\\first_aid_kituse.ogg 0")
                            healing.set_heal(
                                self.client.data["name"], item, 1000, 1, 17200, 100)
                    if item == "locker":
                        if self.client.data["map"]!="main":
                         self.client.send("speak you have to place a "+item+" on the main map")
                         return
                        if teams.get_team(self.client.data["name"]) == "":
                            self.client.send(
                                "speak you must be in a team to place a locker.")
                            return
                        index = teams.get_teams_index(
                            teams.get_team(self.client.data["name"]))
                        if index == -1:
                            self.client.send("speak your team doesn't exsist")
                            return
                        for f in map.objects:
                            o = map.objects[f]
                            if o.name == "locker" and o.team == teams.get_team(self.client.data["name"]):
                                self.client.send(
                                    "speak your team has already a locker.")
                                return

                        allowed_facings = [0, 90, 180, 270]
                        if self.client.data["facing"] not in allowed_facings:
                            self.client.send(
                                "speak you need to be facing north, east ,sotuh or west to place a locker.")
                            return
                        check_z = self.client.data["z"]
                        check_x, check_y = rotation.move(
                            self.client.data["x"], self.client.data["y"], self.client.data["facing"])
                        check_x, check_y = rotation.move(
                            check_x, check_y, self.client.data["facing"])
                        check_x = round(check_x)
                        check_y = round(check_y)

                        check = map.get_things_in_area(
                            check_x-1, check_x+1, check_y-1, check_y+1, check_z, check_z+5, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            check = map.get_things_in_area(
                                check_x-1, check_x+1, check_y-1, check_y+1, check_z-1, check_z-1, self.client.data["map"], True, False)
                            f = check.replace("||", "")
                            f = f.replace("|blank|", "")
                            if f == check and map.get_object(check_x, check_y, self.client.data["z"]-1, self.client.data["map"]) != "":
                                object_below = map.get_object(
                                    check_x, check_y, check_z-1, self.client.data["map"])
                                metal_fortress_below = map.get_metal_fortress(
                                    check_x, check_y, check_z-1, self.client.data["map"])
                                if object_below != -1 and object_below != metal_fortress_below:
                                    self.client.send(
                                        "speak can't place a locker on an unstable object.")
                                    return
                                if map.get_platform(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"]) != "" and map.get_platform(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"]) != "blank":
                                    l = map.locker(check_x-1, check_x+1, check_y-1, check_y+1, check_z,
                                                   check_z+4, self.client.data["map"], teams.get_team(self.client.data["name"]))
                                    map.objects[str(l.id)] = l
                                    self.client.give(item, -1)
                                    send_all(
                                        r"player_sound "+self.client.data["name"]+" sounds\\lockerplace.ogg 0")
                                    self.client.send("stun 3000")

                                else:
                                    self.client.send(
                                        "speak can't place a locker while you are in the air.")
                            else:
                                self.client.send("speak can't place a locker here.")
                        else:
                            self.client.send("speak can't place a locker here.")
                    if item == "welding_machine":
                        cx, cy = rotation.move(
                            self.client.data["x"], self.client.data["y"], self.client.data["facing"])
                        id = map.get_walls_index(
                            cx, cy, self.client.data["z"], self.client.data["map"])
                        if id == -1:
                            final_id = map.get_object(
                                cx, cy, self.client.data["z"], self.client.data["map"])
                        else:
                            final_id = map.walls[id].id
                        o = map.get_objects_index(final_id)
                        if o == "" or not hasattr(map.objects[o], "team"):
                            self.client.send(
                                "speak you aren't standing in front of a locker")
                            return
                        try:
                            bat = self.client.inventory["welding_machine_battery"]
                        except:
                            bat = 0
                        if bat == 0:
                            self.client.send(
                                "speak you don't have a welding machine battery")
                            return
                        if map.objects[o].health >= map.objects[o].max_health:
                            self.client.send(
                                "speak this "+map.objects[o].name+" is already on it's maximum health")
                            return
                        self.client.give("welding_machine_battery", -1)
                        self.client.send("stun 14000")
                        extra = 15000
                        if self.client.inv_check("metal_sheat") > 0:
                            self.client.give("metal_sheat", -1)
                            extra = 40000
                        map.objects[o].health = round(
                            map.objects[o].health+extra)
                        if map.objects[o].health >= map.objects[o].max_health:
                            map.objects[o].health = map.objects[o].max_health
                        try:
                            if map.objects[o].health > map.objects[o].data["highest_health"]:
                                map.objects[o].data["highest_health"] = map.objects[o].health
                        except Exception as e:
                            print(str(e))
                        send_all(r"player_sound " +
                                 self.client.data["name"]+" sounds\\lockerrepair.ogg 0")
                    if item == "flash_grenade":
                        i = 0
                        for g in v.grenades:
                            if g.status == "in_hand" and g.owner == self.client.data["name"]:
                                if g.timer.elapsed() < 700:
                                    self.client.send(
                                        "speak you can't throw the grenade yet")
                                    return
                                i = 1
                                g.dir = self.client.data["facing"]
                                g.updown = self.client.data["updown"]
                                if g.updown == -2 and map.get_platform(g.x, g.y, g.z-1, g.map) == "wall":
                                    g.x, g.y = rotation.move(g.x, g.y, g.dir)
                                g.status = "flying"
                                self.client.grenadetimer.restart()
                                self.client.give("flash_grenade", -1)
                                send_all(
                                    r"player_sound "+self.client.data["name"]+" sounds\\flash_grenadethrow.ogg 0")
                        if i == 0:
                            if self.client.grenadetimer.elapsed() < 3300:
                                self.client.send("speak you can't use a grenade yet")
                                return
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\flash_grenadepin.ogg 0")
                            c = expl.flash_grenade(
                                self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"], self.client.data["name"])
                            v.grenades.append(c)

                    if item == "grenade":
                        i = 0
                        for g in v.grenades:
                            if g.status == "in_hand" and g.owner == self.client.data["name"]:
                                if g.timer.elapsed() < 700:
                                    self.client.send(
                                        "speak you can't throw the grenade yet")
                                    return
                                i = 1
                                g.dir = self.client.data["facing"]
                                g.updown = self.client.data["updown"]
                                if g.updown == -2 and map.get_platform(g.x, g.y, g.z-1, g.map) == "wall":
                                    g.x, g.y = rotation.move(g.x, g.y, g.dir)
                                g.status = "flying"
                                self.client.grenadetimer.restart()
                                self.client.give("grenade", -1)
                                send_all(
                                    r"player_sound "+self.client.data["name"]+" sounds\\grenadethrow.ogg 0")
                        if i == 0:
                            if self.client.grenadetimer.elapsed() < 3300:
                                self.client.send("speak you can't use a grenade yet")
                                return
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\grenadepin.ogg 0")
                            c = expl.grenade(
                                self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"], self.client.data["name"])
                            v.grenades.append(c)
                    if item == "c4":
                        cx, cy = rotation.move(
                            self.client.data["x"], self.client.data["y"], self.client.data["facing"])
                        index = map.get_walls_index(
                            cx, cy, self.client.data["z"], self.client.data["map"])
                        if index == -1:
                            self.client.send(
                                "speak you are not standing in front of an object")
                            return
                        o = map.get_objects_index(map.walls[index].id)
                        if o == "":
                            self.client.send(
                                "speak you are not standing in front of an object")
                            return
                        if map.objects[o].name == "window":
                            self.client.send("speak you can't place a c4 on a window")
                            return
                        self.client.send("stun 6700|n|activate_c4")
                        send_all(r"player_sound " +
                                 self.client.data["name"]+" sounds\\c4place.ogg 0")
                    if item == "Painkiller_injection":
                        if percent >= 75:
                            self.client.send(
                                "speak you can only heal to 75% health with this item.")
                        else:
                            self.client.send("stun 1200")
                            self.client.give(item, -1)
                            send_all(
                                "player_sound "+self.client.data["name"]+" sounds\\Painkiller_injectionuse.ogg 0")
                            healing.set_heal(
                                self.client.data["name"], item, 150, 3, 1200, 75)
    def builder_menu(self, parsed):
                    if self.client.data["admin"] == 1 or self.client.data["builder"] == 1:
                        objlist = ["lamppost", "large_glass_cabinet", "small_glass_cabinet",
                                   "table", "tree", "desk", "planter", "window"]
                        for o in v.object_presets:
                            objlist.append(o.name)
                        itemlist = list(v.max_items.keys())
                        for w in v.weapon_names:
                            itemlist.append("weapon_"+w)
                        itemlist.append("nothing")
                        self.client.send("set_itemlist "+"\n".join(itemlist) +
                                  "|n|set_objlist "+"\n".join(objlist)+"|n|builder_menu")
    def speedhackcheck(self, parsed):
                    self.client.speedhackchecks += 1
                    if self.client.speedhackchecktimer.elapsed() > self.client.max_speedhack:
                        self.client.max_speedhack = self.client.speedhackchecktimer.elapsed()
                    self.client.speedhackchecktimer.restart()
    def start_scoping(self, parsed):
                    we = self.client.get_weapon_in_list(self.client.data["weapon"])
                    if we.sort == "sniper_rifle" or we.sort == "assault_rifle" and self.client.skill_data["sharpshooter mastery"]["active"] == True or we.scope == True:
                        index = get_players_index(self.client.data["name"])
                        if index > -1:
                            if v.clients[index].skill_data["sharpshooter mastery"]["active"] == True and we.sort == "assault_rifle":
                                old_weapon = weapons.weapon(we.name)
                                we.range = old_weapon.range + \
                                    round(
                                        v.clients[index].skill_data["sharpshooter mastery"]["level"]*3)
                        self.client.send(r"start_scoping "+str(we.range)+"|n|speak you start to look through the scope of your " +
                                  we.name+"|n|player_sound "+self.client.data["name"]+" sounds\\scopelookstart.ogg 0")
                    else:
                        self.client.send("speak this weapon doesn't have a scope.")
    def holster_put(self, parsed):
                    if self.client.reloading == True:
                        return
                    if self.client.data["holster"] == parsed[1]:
                        self.client.send(
                            "speak you already have this weapon in your holster.")
                        return
                    if parsed[1] == "nothing":
                        self.client.send("speak you have no weapon in your hand.")
                        return
                    we = self.client.get_weapon_in_list(parsed[1])
                    if we == None:
                        self.client.send("speak you haven't drawn any weapon")
                        return
                    if we.name != "flail":
                        if we.sort == "pistol" or we.sort == "revolver" or we.sort == "sub_machine_gun" or we.sort == "melee" or self.client.skill_data["holster augmentation"]["active"] == True and we.sort == "shotgun" and self.client.skill_data["holster augmentation"]["level"] >= 1 or we.sort == "assault_rifle" and self.client.skill_data["holster augmentation"]["level"] >= 2 and self.client.skill_data["holster augmentation"]["active"] == True or we.sort == "sniper_rifle" and self.client.skill_data["holster augmentation"]["level"] >= 3 and self.client.skill_data["holster augmentation"]["active"] == True:
                            self.client.send(
                                "speak "+parsed[1]+" put in your holster.")
                            self.client.data["holster"] = parsed[1]
                            we = weapons.weapon(parsed[1])
                            send_all(r"player_sound "+self.client.data["name"]+" sounds\\"+we.sort +
                                     "holsterin.ogg 0|n|player_sound "+self.client.data["name"]+" sounds\\"+we.name+"holsterin.ogg 0")
                            if self.client.data["weapon"] == self.client.data["holster"]:
                                self.client.change_weapon(None)
                                self.client.send("set_weapon nothing")
                        else:
                            self.client.send(
                                "speak this weapon can't fit in your holster.")
                            return
                    else:
                        self.client.send(
                            "speak this weapon can't fit in your holster.")
                        return

    def holster_information(self, parsed):
                    if self.client.data["holster"] == "":
                        self.client.send("speak there is nothing in your holster")
                        return
                    l = "you have a "+self.client.data["holster"]+" in your holster. "
                    we = self.client.get_weapon_in_list(self.client.data["holster"])
                    if we.melee == False:
                        max_ammo = we.max_ammo
                        if self.client.skill_data["extended pistol clip"]["active"] == True and we.sort == "pistol" and we.name != "ruger_redhawk":
                            max_ammo += self.client.skill_data["extended pistol clip"]["level"]
                        l = l+"It has " + \
                            str(self.client.get_weapon_in_list(we.name).loaded_ammo) + \
                            " of "+str(max_ammo)+" bullets loaded."
                    self.client.send("speak "+l)

    def holster_take(self, parsed):
                if self.client.reloading == False:
                    if self.client.data["holster"] == "":
                        self.client.send(
                            "speak there is nothing in your holster|n|set_weapon "+self.client.data["weapon"])
                        return
                    self.client.send("holster_take "+self.client.data["holster"]+" 130|n|speak " +
                              self.client.data["holster"]+" has been taken out of your holster")
                    we = weapons.weapon(self.client.data["holster"])
                    send_all(r"player_sound "+self.client.data["name"]+" sounds\\"+we.sort +
                             "holsterout.ogg 0|n|player_sound "+self.client.data["name"]+" sounds\\"+we.name+"holsterout.ogg 0")
                    self.client.data["holster"] = ""
    def warning(self, parsed):
                    data=self.data
                    name = parsed[1]
                    index = get_players_index(name)
                    if index == -1:
                        self.client.send("speak this player isn't online")
                        return
                    message = data.replace("warning "+name+" ", "")
                    v.clients[index].send("add_buffer_item important this is an official warning from the staff: " +
                                          message+"|n|buffer_sound important warn.ogg 0 0 0 1 0")
                    self.client.send("speak your warning has been sent")
    def pm(self, parsed):
                    data=self.data
                    name = parsed[1]
                    index = get_players_index(name)
                    if index == -1:
                        self.client.send("speak this player isn't online")
                        return
                    message = data.replace("add_buffer_item pm "+name+" ", "")
                    v.clients[index].send("add_buffer_item pm private message from " +
                                          self.client.data["name"]+": "+message+"|n|buffer_sound pm pm.ogg 0 0 0 1 0")
                    self.client.send("add_buffer_item pm private message to " +
                              v.clients[index].data["name"]+": "+message+"|n|buffer_sound pm pm.ogg 0 0 0 1 0")
                    self.client.data["last_pm"] = v.clients[index].data["name"]
                    v.clients[index].data["last_pm"] = self.client.data["name"]
    def reply(self, parsed):
                    data=self.data
                    name = self.client.data["last_pm"]
                    if name == "":
                        self.client.send("speak you haven't got any private message")
                        return
                    index = get_players_index(name)
                    if index == -1:
                        self.client.send("speak this player isn't online")
                        return
                    if self.client.data["name"] in v.clients[index].data["mutelist"]:
                        self.client.send("speak "+name+" has muted you")
                        return
                    if v.clients[index].data["name"] in self.client.data["mutelist"]:
                        self.client.send("speak you have muted "+name)
                        return

                    message = data.replace("reply ", "")
                    v.clients[index].send("add_buffer_item pm reply from "+self.client.data["name"] +
                                          ": "+message+"|n|buffer_sound pm pm.ogg 0 0 0 1 0")
                    self.client.send("add_buffer_item pm reply to " +
                              v.clients[index].data["name"]+": "+message+"|n|buffer_sound pm pm.ogg 0 0 0 1 0")
                    self.client.data["last_pm"] = v.clients[index].data["name"]
                    v.clients[index].data["last_pm"] = self.client.data["name"]
    def scanner_mode(self, parsed):
                    if self.client.data["scanner_mode"] == 0:
                        self.client.data["scanner_mode"] = 1
                        self.client.send("speak scanner scanning only players.")
                    elif self.client.data["scanner_mode"] == 1:
                        self.client.data["scanner_mode"] = 2
                        self.client.send("speak scanner gap mode")
                    elif self.client.data["scanner_mode"] == 2:
                        self.client.data["scanner_mode"] = 3
                        self.client.send("speak scanner speaking no windows")
                    else:
                        self.client.data["scanner_mode"] = 0
                        self.client.send(
                            "speak scanner scanning everything|n|play_sound scanner_divold.ogg 0 0 0 1 0")
    def scanner(self, parsed):
                    if self.client.data["flash_grenade_inpect"] == True:
                        self.client.send(
                            "speak You're temporarily blinded by the flash of a flashbang ")
                        return
                    if len(parsed) > 1:
                        s = scanner.scanner(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"],
                                            self.client.data["facing"], self.client.data["updown"], self.client.data["name"], self.client.data["scanner_mode"])
                        s.range += int(parsed[1])
                        s.check_clients()
                        scanner.scanners.append(s)
                    else:
                        scanner.spawn_scanner(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"],
                                              self.client.data["facing"], self.client.data["updown"], self.client.data["name"], self.client.data["scanner_mode"])
    def interact(self, parsed):
                if self.client.interacttimer.elapsed() > 800:
                    for h in v.heals:
                        if h.begintimer.elapsed() < h.begintime and h.owner == self.client.data["name"]:
                            return
                    cx, cy = rotation.move(
                        self.client.data["x"], self.client.data["y"], self.client.data["facing"])
                    cx = round(cx)
                    cy = round(cy)
                    if self.client.examining == True:
                        self.client.interacttimer.restart()
                        self.client.send(
                            "stun_reset|n|speak you stop examining the "+self.client.examine)
                        self.client.examining = False
                        for o in map.examining_objects:
                            if o.examiner == self.client.data["name"]:
                                o.examining = False
                                o.examiner = ""
                                send_all(r"stop_player_sound "+self.client.data["name"]+" sounds\\"+o.examinesounds +
                                         "examine.ogg|n|player_sound "+self.client.data["name"]+" sounds\\"+o.examinesounds+"examinestop.ogg 0")
                                self.client.examine = ""
                                self.client.examining = False

                    else:
                        #       cx,cy=rotation.move(self.client.data["x"],self.client.data["y"],self.client.data["facing"])
                        id = map.get_walls_index(
                            cx, cy, self.client.data["z"], self.client.data["map"])
                        if id == -1:
                            final_id = map.get_object(
                                cx, cy, self.client.data["z"], self.client.data["map"])
                        else:
                            final_id = map.walls[id].id
                        o = map.get_objects_index(final_id)
                        if o == "" or map.objects[o].examine == False or map.objects[o].actif == False:
                            if map.get_quest_item(cx, cy, self.client.data["z"], self.client.data["map"]) != "":
                                for q in self.client.quests:
                                    qe = quests.quest(q)
                                    if self.client.quests[q] == 0 and qe.item == map.get_quest_item(cx, cy, self.client.data["z"], self.client.data["map"]):
                                        send_all(r"player_sound "+self.client.data["name"]+" sounds\\"+map.get_quest_item(
                                            cx, cy, self.client.data["z"], self.client.data["map"], True)+" 0")
                                        qe = quests.quest(q)
                                        self.client.quests[q] = 1
                                        self.client.get_quest_rewards(q)
                                        self.client.send("add_buffer_item misc you have completed the "+q +
                                                  " quest.|n|buffer_sound misc quest_complete.ogg 0 0 0 1 0")
                                        if qe.unlock_quest != "":
                                            self.client.quests[qe.unlock_quest] = 0
                                            self.client.send(
                                                "add_buffer_item misc you have unlocked the "+qe.unlock_quest+" quest")
                                        self.client.check_unlock_quests()
                                        return
                            self.client.send(
                                "speak you aren't standing in front of an object that is searchable")
                            return
                        if map.objects[o].name == "locker":
                            if map.objects[o].data["opened"] == False:
                                self.client.send(
                                    "speak the door of the locker is closed.")
                            else:
                                items = []
                                for i in map.objects[o].loot:
                                    items.append(
                                        i+": "+str(map.objects[o].loot[i]))
                                weapon_names = [
                                    w.name for w in map.objects[o].weapons]
                                weapon_counts = {}
                                for w in weapon_names:
                                    weapon_counts[w] = weapon_names.count(w)
                                for w in weapon_counts:
                                    items.append(w+": "+str(weapon_counts[w]))
                                if map.objects[o].team == teams.get_team(self.client.data["name"]):
                                    items.append("view upgrades")
                            if len(items) > 0:
                                self.client.send("locker_menu "+"\n".join(items))
                            else:
                                self.client.send("speak the locker is empty")
                            return
                        if map.objects[o].examinetimer.elapsed() < map.objects[o].examineendtime:
                            self.client.send(
                                "speak this object is not ready to examine yet")
                            return
                        if map.objects[o].examining == True:
                            self.client.send(
                                "speak someone is already searching in this object.")
                            return
                        if self.client.match_id != -1 and map.objects[o].name.startswith("corpse"):
                            self.client.send(
                                "speak you can't loot a corpse in ranked mode")
                            return
                        map.objects[o].examining = True
                        self.client.examine = map.objects[o].name
                        self.client.examining = True
                        self.client.interacttimer.restart()
                        map.objects[o].examinetimer.restart()
                        map.examining_objects.append(map.objects[o])
                        map.objects[o].examiner = self.client.data["name"]
                        self.client.send(
                            "stun "+str(map.objects[o].examineendtime)+"|n|")
                        if map.objects[o].name[0:6] == "corpse":
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\corpseexamine.ogg 0")
                        else:
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\"+map.objects[o].examinesounds+"examine.ogg 0")
    def push_object(self, parsed):
                    cx, cy = rotation.move(
                        self.client.data["x"], self.client.data["y"], self.client.data["facing"])
                    cx = round(cx)
                    cy = round(cy)
                    id = map.get_walls_index(
                        cx, cy, self.client.data["z"], self.client.data["map"])
                    if id == -1:
                        final_id = map.get_object(
                            cx, cy, self.client.data["z"], self.client.data["map"])
                    else:
                        final_id = map.walls[id].id
                    o = map.get_objects_index(final_id)
                    if o == "" or map.objects[o].actif == False:
                        self.client.send(
                            "speak you aren't standing in front of an object.")
                        return
                    if map.objects[o].name == "locker":
                        if map.objects[o].team != teams.get_team(self.client.data["name"]):
                            options = ["yes", "no"]
                            self.client.send(
                                "server_menu this_locker_belongs_to_a_team_that_you_aren't_a_member_of._Would_you_like_to_break_the_security_by_doing_a_simon_game? "+"\n".join(options))
                            return
                        if map.objects[o].pushtimer.elapsed() > map.objects[o].pushtime:
                            map.objects[o].pushtimer.restart()
                            if map.objects[o].data["opened"] == False:
                                map.objects[o].data["opened"] = True
                                self.client.send(
                                    "speak you open the door of the locker")
                                send_all(
                                    r"player_sound "+self.client.data["name"]+" sounds\\lockeropen.ogg 0")
                            else:
                                map.objects[o].data["opened"] = False
                                self.client.send(
                                    "speak you close the door of the locker")
                                send_all(
                                    r"player_sound "+self.client.data["name"]+" sounds\\lockerclose.ogg 0")
                        else:
                            pass
                        return
                    if map.objects[o].name == "metal_fortress":
                        if map.objects[o].team != teams.get_team(self.client.data["name"]):
                            options = ["yes", "no"]
                            self.client.send(
                                "server_menu this_metal_fortress_belongs_to_a_team_that_you_aren't_a_member_of._Would_you_like_to_turn_off_the_alarm_by_doing_a_simon_game? "+"\n".join(options))
                            return
                    if map.objects[o].moveable == False:
                        self.client.send("speak this object is too heavy to move.")
                        return

                    if map.objects[o].pushtimer.elapsed() < map.objects[o].pushtime:
                        return
                    map.objects[o].pushtimer.restart()
                    check = ""
                    if self.client.data["facing"] == 0:
                        check = map.get_things_in_area(map.objects[o].minx, map.objects[o].maxx, map.objects[o].maxy+1,
                                                       map.objects[o].maxy+1, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            l = map.objects[o].move(self.client.data["facing"])
                            if l == 0:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"move"+str(random.randint(1, 3))+".ogg")
                            else:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"movefall.ogg")

                        else:
                            send_all(
                                r"object_sound "+str(map.objects[o].id)+" "+map.objects[o].movesounds+"movewall.ogg")
                    if self.client.data["facing"] == 45:
                        check = map.get_things_in_area(map.objects[o].minx, map.objects[o].maxx, map.objects[o].maxy+1, map.objects[o].maxy+1, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])+map.get_things_in_area(
                            map.objects[o].maxx+1, map.objects[o].maxx+1, map.objects[o].miny, map.objects[o].maxy, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            l = map.objects[o].move(self.client.data["facing"])
                            if l == 0:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"move"+str(random.randint(1, 3))+".ogg")
                            else:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"movefall.ogg")
                        else:
                            send_all(
                                r"object_sound "+str(map.objects[o].id)+" "+map.objects[o].movesounds+"movewall.ogg")
                    if self.client.data["facing"] == 90:
                        check = map.get_things_in_area(map.objects[o].maxx+1, map.objects[o].maxx+1, map.objects[o].miny,
                                                       map.objects[o].maxy, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            l = map.objects[o].move(self.client.data["facing"])
                            if l == 0:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"move"+str(random.randint(1, 3))+".ogg")
                            else:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"movefall.ogg")
                        else:
                            send_all(
                                r"object_sound "+str(map.objects[o].id)+" "+map.objects[o].movesounds+"movewall.ogg")
                    if self.client.data["facing"] == 135:
                        check = map.get_things_in_area(map.objects[o].minx, map.objects[o].maxx, map.objects[o].miny-1, map.objects[o].miny-1, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])+map.get_things_in_area(
                            map.objects[o].maxx+1, map.objects[o].maxx+1, map.objects[o].miny, map.objects[o].maxy, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            l = map.objects[o].move(self.client.data["facing"])
                            if l == 0:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"move"+str(random.randint(1, 3))+".ogg")
                            else:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"movefall.ogg")
                        else:
                            send_all(
                                r"object_sound "+str(map.objects[o].id)+" "+map.objects[o].movesounds+"movewall.ogg")
                    if self.client.data["facing"] == 180:
                        check = map.get_things_in_area(map.objects[o].minx, map.objects[o].maxx, map.objects[o].miny-1,
                                                       map.objects[o].miny-1, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            l = map.objects[o].move(self.client.data["facing"])
                            if l == 0:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"move"+str(random.randint(1, 3))+".ogg")
                            else:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"movefall.ogg")
                        else:
                            send_all(
                                r"object_sound "+str(map.objects[o].id)+" "+map.objects[o].movesounds+"movewall.ogg")
                    if self.client.data["facing"] == 225:
                        check = map.get_things_in_area(map.objects[o].minx, map.objects[o].maxx, map.objects[o].miny-1, map.objects[o].miny-1, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])+map.get_things_in_area(
                            map.objects[o].minx-1, map.objects[o].minx-1, map.objects[o].miny, map.objects[o].maxy, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            l = map.objects[o].move(self.client.data["facing"])
                            if l == 0:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"move"+str(random.randint(1, 3))+".ogg")
                            else:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"movefall.ogg")
                        else:
                            send_all(
                                r"object_sound "+str(map.objects[o].id)+" "+map.objects[o].movesounds+"movewall.ogg")
                    if self.client.data["facing"] == 270:
                        check = map.get_things_in_area(map.objects[o].minx-1, map.objects[o].minx-1, map.objects[o].miny,
                                                       map.objects[o].maxy, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            l = map.objects[o].move(self.client.data["facing"])
                            if l == 0:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"move"+str(random.randint(1, 3))+".ogg")
                            else:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"movefall.ogg")
                        else:
                            send_all(
                                r"object_sound "+str(map.objects[o].id)+" "+map.objects[o].movesounds+"movewall.ogg")
                    if self.client.data["facing"] == 315:
                        check = map.get_things_in_area(map.objects[o].minx, map.objects[o].maxx, map.objects[o].maxy+1, map.objects[o].maxy+1, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])+map.get_things_in_area(
                            map.objects[o].minx-1, map.objects[o].minx-1, map.objects[o].miny, map.objects[o].maxy, map.objects[o].minz, map.objects[o].maxz, self.client.data["map"])
                        f = check.replace("|wall|", "")
                        f = f.replace("|player|", "")
                        if f == check:
                            l = map.objects[o].move(self.client.data["facing"])
                            if l == 0:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"move"+str(random.randint(1, 3))+".ogg")
                            else:
                                send_all("move_object "+str(map.objects[o].id)+" "+str(self.client.data["facing"])+"|n|object_sound "+str(
                                    map.objects[o].id)+" "+map.objects[o].movesounds+"movefall.ogg")
                        else:
                            send_all(
                                r"object_sound "+str(map.objects[o].id)+" "+map.objects[o].movesounds+"movewall.ogg")
    def respawn(self, parsed):
                    old_map = self.client.data["map"]
                    if self.client.losing_loot == True:
                        old_weapons = []
                        old_inv = {}
                        if self.client.match_id == -2:
                            old_weapons = self.client.weapons
                            old_inv = self.client.inventory
                        self.client.reset()
                        if old_weapons != []:
                            for w in old_weapons:
                                self.client.add_weapon_instance(w)

                        if old_inv != {}:
                            for i in old_inv:
                                if i[0:7] != "weapon_":
                                    self.client.inventory[i] = old_inv[i]
                            self.client.match_id = -1

                    else:
                        self.client.losing_loot = True
                        weapon_list = self.client.weapons
                        inventory = self.client.inventory
                        self.client.reset()
                        for w in self.client.weapon_list:
                            self.client.add_weapon_instance(w)
                        for i in inventory:
                            if i[0:7] != "weapon_":
                                self.client.inventory[i] = inventory[i]
                        self.client.give_account("magical_reappearance", -1)
                        self.client.send(
                            "speak you use  the magical reappearance' to regain your loot|n|play_sound magical_reappearance.ogg 0 0 0 1 0")
                    self.client.spawn()
                    self.client.store_data(True)
                    self.client.get_data()
                    self.client.data["map"]=self.client.data["chosen_map"]
                    if self.client.lobby == False:
                        for c in v.clients:
                            if c.data["map"] == self.client.data["map"]:
                                self.client.send("spawn_player "+str(c.data["x"])+" "+str(c.data["y"])+" "+str(c.data["z"])+" "+c.data["name"]+"|n|set_player_weapon "+c.data["name"]+" "+c.data["weapon"] +
                                          "|n|set_players_silencer "+c.data["name"]+" "+str(c.has_silencer(c.data["weapon"]))+"|n|set_team "+c.data["name"]+" "+teams.get_team(c.data["name"]))
                                c.send("spawn_player "+str(self.client.data["x"])+" "+str(self.client.data["y"])+" "+str(self.client.data["z"])+" "+self.client.data["name"]+"|n|set_player_weapon "+self.client.data["name"]+" "+self.client.data["weapon"]+"|n|move_player "+self.client.data["name"]+" "+str(
                                    self.client.data["x"])+" "+str(self.client.data["y"])+" "+str(self.client.data["z"])+"|n|set_players_silencer "+self.client.data["name"]+" "+str(self.client.has_silencer(self.client.data["weapon"]))+"|n|set_team "+self.client.data["name"]+" "+teams.get_team(self.client.data["name"]))

                        if old_map == self.client.data["chosen_map"]:
                            self.client.send("speak you have been respawned|n|go "+str(self.client.data["x"])+" "+str(self.client.data["y"])+" "+str(
                                self.client.data["z"])+"|n|get_weapons "+"||".join(self.client.data["weapons"])+"|n|set_weapon "+self.client.data["weapon"]+"|n|")
                            return
                        data = ""
                        f = open("maps/"+self.client.data["map"]+".txt", "r+")
                        data = f.read()
                        f.close()
                        l = ""
                        for f in map.objects:
                            o = map.objects[f]
                            if o.map != self.client.data["map"]:
                                continue
                            l = l+"|n|spawn_object "+str(int(o.minx))+" "+str(int(o.maxx))+" "+str(int(o.miny))+" "+str(
                                int(o.maxy))+" "+str(int(o.minz))+" "+str(o.maxz)+" "+o.name+" "+str(o.dir)+" "+str(o.id)+"|n|"
                            m = ""
                            if o.actif:
                             m="set_object_mapdata "+str(o.id)+" "+o.mapdata+"|n|"
                            else:
                             for i in o.mapdata.split("\n"):
                                if o.actif == True or "permanent" in i:
                                    m = m+"set_object_mapdata " + \
                                        str(o.id)+" "+i+"|n|"
                            l = l+m
                        if self.client.lobby == False:
                            self.client.send("speak you have been respawned|n|go "+str(int(self.client.data["x"]))+" "+str(int(self.client.data["y"]))+" "+str(
                                int(self.client.data["z"]))+"|n|get_weapons "+"||".join(self.client.data["weapons"])+"|n|set_weapon "+self.client.data["weapon"]+"|n|mapdata "+data+"|n|"+l)
                    self.client.match_id = -1
                    self.client.get_data()

    def belt_give(self, parsed):
                    if len(self.client.inventory) == 0:
                        self.client.send(r"speak you have no items in your belt|n|player_sound " +
                                  self.client.data["name"]+" sounds\\beltempty"+str(random.randint(1, 3))+".ogg 0")
                        return
                    dic = list(self.client.inventory.keys())
                    forbidden_list = ["locker", "team_phone", "metal_fortress",
                                      "metal_fortress_construction_kit", "metal_sheat"]
                    if dic[self.client.invpos] in forbidden_list:
                        self.client.send("speak you can't give this item.")
                        return
                    try:
                        if self.client.armor[dic[self.client.invpos]]["wearing"] == True:
                            self.client.send(
                                "speak can't give a armor piece that you're wearing")
                            return
                    except:
                        pass
                    near_players = []
                    for c in v.clients:
                        if get_3d_distance(c.data["x"], c.data["y"], c.data["z"], self.client.data["x"], self.client.data["y"], self.client.data["z"]) <= 4 and c.data["name"] != self.client.data["name"] and c.data["map"] == self.client.data["map"] and c.lobby == False and c.data["death"] == False:
                            near_players.append(c.data["name"])
                    if len(near_players) == 0:
                        self.client.send("speak no players around you.")
                        return
                    dic = list(self.client.inventory.keys())
                    iname = dic[self.client.invpos]
                    self.client.send("server_menu who_do_you_want_to_give_" +
                              iname+"? "+"\n".join(near_players))
    def give_weapon(self, parsed):
                    near_players = []
                    for c in v.clients:
                        if get_3d_distance(c.data["x"], c.data["y"], c.data["z"], self.client.data["x"], self.client.data["y"], self.client.data["z"]) <= 4 and c.data["map"] == self.client.data["map"] and c.lobby == False and c.data["death"] == False and c.data["name"] != self.client.data["name"]:
                            near_players.append(c.data["name"])
                    if len(near_players) == 0:
                        self.client.send("speak no players around you.")
                        return
                    self.client.send("server_menu who_do_you_want_to_give_the_weapon_" +
                              parsed[1]+"? "+"\n".join(near_players))
    def belt_information(self, parsed):
                    if len(self.client.inventory) == 0:
                        self.client.send(r"speak you have no items in your belt|n|player_sound " +
                                  self.client.data["name"]+" sounds\\beltempty"+str(random.randint(1, 3))+".ogg 0")
                        return
                    dic = list(self.client.inventory.keys())
                    iname = dic[self.client.invpos]
                    try:
                        self.client.send(r"speak "+v.get_description(iname) +
                                  " You can carry a total of "+str(v.max_items[iname])+" with you.")
                    except:
                        self.client.send("speak this item does not exist")
    def belt_store(self, parsed):
                    if len(self.client.inventory) == 0:
                        self.client.send(r"speak you have no items in your belt|n|player_sound " +
                                  self.client.data["name"]+" sounds\\beltempty"+str(random.randint(1, 3))+".ogg 0")
                        return
                    dic = list(self.client.inventory.keys())
                    iname = dic[self.client.invpos]
                    forbidden_list = ["locker", "team_phone", "metal_fortress", "metal_fortress_construction_kit",
                                      "metal_sheat", "welding_machine_battery", "welding_machine"]
                    if iname in forbidden_list:
                        self.client.send("speak can't store this item.")
                        return
                    try:
                        if self.client.armor[dic[self.client.invpos]]["wearing"] == True:
                            self.client.send(
                                "speak can't store a armor piece that you're wearing")
                            return
                    except:
                        pass
                    cx, cy = rotation.move(
                        self.client.data["x"], self.client.data["y"], self.client.data["facing"])
                    id = map.get_object(
                        cx, cy, self.client.data["z"], self.client.data["map"])
                    o = map.get_objects_index(id)
                    if o == "" or self.client.data["z"] >= map.objects[o].maxz or map.objects[o].actif == False and map.objects[o].name != "locker":
                        self.client.send(
                            "speak you aren't standing in front of a locker.")
                        return
                    if map.objects[o].data["opened"] == False:
                        self.client.send(
                            "speak the door of the locker is closed, so you can't store items in it. ")
                        return
                    self.client.data["store_item"] = iname
                    self.client.send("input how_many_"+iname +
                              "_do_you_want_to_store_in_the_locker? ")

    def belt_category_move(self, parsed):
                    categorys = ["medical", "ammo",
                                 "explosives", "misc", "attachments"]
                    f = 0
                    c = self.client.invpos
                    for i in self.client.inventory:
                        try:
                            item = v.item_categorys[i]
                        except:
                            return

                        if v.item_categorys[i] == categorys[int(parsed[1])] and c < list(self.client.inventory.keys()).index(i):
                            c = list(self.client.inventory.keys()).index(i)
                            f = 1
                            break
                    if f == 0:
                        for i in self.client.inventory:
                            if v.item_categorys[i] == categorys[int(parsed[1])]:
                                c = list(self.client.inventory.keys()).index(i)
                                f = 1
                                break
                    if f == 0:
                        self.client.send(r"speak you have no items in your belt that belong to the "+categorys[int(
                            parsed[1])]+" category.|n|player_sound "+self.client.data["name"]+" sounds\\beltempty"+str(random.randint(1, 3))+".ogg 0")
                    else:
                        self.client.invpos = c
                        dic = list(self.client.inventory.keys())
                        self.client.send(
                            r"speak "+dic[self.client.invpos]+": "+str(self.client.inventory[dic[self.client.invpos]])+"|n|")
                        send_all(
                            "player_sound "+self.client.data["name"]+" sounds\\beltmove"+str(random.randint(1, 6))+".ogg 0")

    def belt_move(self, parsed):
                    if len(self.client.inventory) == 0:
                        self.client.send(r"speak you have no items in your belt|n|player_sound " +
                                  self.client.data["name"]+" sounds\\beltempty"+str(random.randint(1, 3))+".ogg 0")
                        return
                    dir = int(parsed[1])
                    if dir == 0:
                        self.client.invpos -= 1
                    if dir == 1:
                        self.client.invpos += 1
                    if self.client.invpos < 0:
                        self.client.invpos = len(self.client.inventory)-1
                    if self.client.invpos > len(self.client.inventory)-1:
                        self.client.invpos = 0
                    dic = list(self.client.inventory.keys())
                    self.client.send(r"speak "+dic[self.client.invpos]+": " +
                              str(self.client.inventory[dic[self.client.invpos]])+"|n|")
                    send_all(
                        "player_sound "+self.client.data["name"]+" sounds\\beltmove"+str(random.randint(1, 6))+".ogg 0")
    def health(self, parsed):
                    percent = self.client.data["health"]/self.client.data["max_health"]
                    percent = percent*100
                    armor_data = []
                    for a in self.client.armor:
                        if self.client.armor[a]["wearing"] == True:
                            armor_data.append(
                                "a "+a+" with "+str(round(self.client.armor[a]["health"]))+" HP remaining")
                    final_armor_data = " You are wearing " + \
                        v.get_list_in_text(armor_data)
                    if final_armor_data == " You are wearing ":
                        final_armor_data = ""
                    self.client.send("speak "+str(math.ceil(percent))+"% health remaining. "+str(round(
                        self.client.data["health"]))+" of "+str(self.client.data["max_health"])+"."+final_armor_data)
    def player_sound(self, parsed):
                    data=" ".join(parsed)
                    self.client.player_data = self.client.player_data+data+"|n| "
    def facing(self, parsed):
                    self.client.data["facing"] = int(parsed[1])
    def updown(self, parsed):
                    self.client.data["updown"] = int(parsed[1])
    def move_player(self, parsed):
                    data=self.data
                    x = float(parsed[2])
                    y = float(parsed[3])
                    z = float(parsed[4])
                    """
      dist=round(get_3d_distance(x,y,z,self.client.data["x"],self.client.data["y"],self.client.data["z"]))
      if dist>=10 and self.client.data["death"]==False and self.client.survivetimer.elapsed()>10000:
       log_file_path = os.path.join("logs", "cheaters", "moving.log")
       v.add_log_file(log_file_path,self.client.data["name"]+" "+str(dist)+" tiles: "+str(get_current_date())+" "+str(get_current_time()))
       self.client.send("speedhacked")
       send_all("add_buffer_item important "+self.client.data["name"]+" is a cheater and got disconnected by the anti cheat system")
       self.client.disconnect(True)
      """

                    self.client.data["x"] = x
                    self.client.data["y"] = y
                    self.client.data["z"] = z
                    trap.trap_check(
                        self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"], self.client.data["name"])
                    id = map.get_metal_fortress(
                        self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"])
                    if id > 0:
                        o = map.objects[str(id)]
                        if self.client.data["name"] not in o.alarm_players.keys() and o.data["alarm"] == True:
                            o.alarm_players[self.client.data["name"]] = timer.timer()
                    self.client.player_data = self.client.player_data+data+"|n|"
                    f = map.get_quest_zone(
                        self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"])
                    if f != self.client.quest_zone and self.client.lobby == False and self.client.data["death"] == False:
                        b = -1
                        try:
                            b = self.client.quests[f]
                        except:
                            pass
                        if f != "" and b == 0:
                            text, completion = map.get_quest_zone(
                                self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"], True)
                            if completion != 1:
                                self.client.send(
                                    "stun 500|n|play_sound questhint.ogg 0 0 0 1 0|n|add_buffer_item misc "+text)
                            else:
                                self.client.send(
                                    "stun 500|n|play_sound questhint.ogg 0 0 0 1 0|n|add_buffer_item misc "+text)
                                qe = quests.quest(f)
                                self.client.quests[f] = 1
                                self.client.get_quest_rewards(f)
                                self.client.send("add_buffer_item misc you have completed the "+f +
                                          " quest.|n|buffer_sound misc quest_complete.ogg 0 0 0 1 0")
                                if qe.unlock_quest != "":
                                    self.client.quests[qe.unlock_quest] = 0
                                    self.client.send(
                                        "add_buffer_item misc you have unlocked the "+qe.unlock_quest+" quest")
                        self.client.quest_zone = f
    def start_shooting(self, arsed):
                    if self.client.reloading:
                        return
                    ammo = 0
                    try:
                        ammo = self.client.drawn_weapon.loaded_ammo
                    except:
                        pass
                    we = weapons.weapon(self.client.data["weapon"])
                    if ammo > 0 or we.melee == True:
                        if self.client.data["knife_throw"] == False and self.client.data["machete_swing"] == False:
                            if self.client.data["shooting"] != 1:
                                if self.client.drawn_weapon.jammed == False and not self.client.drawn_weapon.is_degradated:
                                    send_all("set_shooting " +
                                             self.client.data["name"]+" 1")
                            self.client.data["shooting"] = 1
    def stop_shooting(self, parsed):
                    self.client.recoil = 1

                    self.client.data["shooting"] = 0
                    if self.client.reloading == False:
                        send_all("set_shooting "+self.client.data["name"]+" 0")
                    else:
                        send_all("set_shooting "+self.client.data["name"]+" 0 1")

    def shoot(self, parsed):
                if self.client.data["death"] == False and self.client.drawn_weapon is not None:
                    if self.client.drawn_weapon.is_degradated:
                        self.client.send("speak this weapon is degraded")
                        self.client.force_packet_exit=True
                        return
                    if self.client.drawn_weapon.jammed == True:
                        self.client.send("speak this gun is jammed|n|block_fire")
                        send_all(r"player_sound "+self.client.data["name"]+" sounds\\"+self.client.drawn_weapon.sort +
                                 "jam.ogg 0")
                        self.client.force_packet_exit=True
                        return
                    if self.client.reloading == True:
                        self.client.drawn_weapon.jammed = True
                        self.client.drawn_weapon.degradation += 20
                        send_all(r"player_sound "+self.client.data["name"]+" sounds\\"+self.client.drawn_weapon.sort +
                                 "jam.ogg 0|n|stop_player_sound "+self.client.data["name"]+" sounds\\"+self.client.drawn_weapon.name+"reload.ogg")
                        self.client.force_packet_exit=True
                        return
                    self.client.data["machete_swing_got"] = []
                    if self.client.data["knife_throw"] == True:
                        self.client.data["knife_throw"] = False
                        send_all(r"player_sound "+self.client.data["name"]+" sounds\\thrown_knifethrow"+str(
                            random.randint(1, 3))+".ogg 0")
                        weapons.spawn_bullet(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["name"], self.client.data["facing"],
                                             self.client.data["updown"], self.client.data["map"], "thrown_knife", "melee", 600+(self.client.skill_data["knife throw"]["level"]*100), 16+self.client.skill_data["knife throw"]["level"], 1)
                        self.client.skill_timers["knife throw"].restart()
                        self.client.remove_weapon_instance(
                            self.client.get_weapon_in_list("knife"))
                        return
                    if self.client.data["machete_swing"] == True:
                        self.client.data["machete_swing_got"] = []
                        self.client.data["machete_swing"] = False
                        send_all(r"player_sound "+self.client.data["name"]+" sounds\\macheteswingfire"+str(
                            random.randint(1, 3))+".ogg 0")
                        weapons.spawn_bullet(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["name"], self.client.data["facing"]-45+360,
                                             self.client.data["updown"], self.client.data["map"], "machete_swing", "melee", 1000, 1+self.client.skill_data["machete swing"]["level"], 2)
                        weapons.spawn_bullet(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["name"], self.client.data["facing"],
                                             self.client.data["updown"], self.client.data["map"], "machete_swing", "melee", 1000, 1+self.client.skill_data["machete swing"]["level"], 2)
                        weapons.spawn_bullet(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["name"], self.client.data["facing"]+45,
                                             self.client.data["updown"], self.client.data["map"], "machete_swing", "melee", 1000, 1+self.client.skill_data["machete swing"]["level"], 2)
                        self.client.send("stun 800")
                        self.client.skill_timers["machete swing"].restart()
                        return
                    w = self.client.get_weapon_in_list(self.client.data["weapon"])
                    if w.name == "flail":
                        self.client.data["machete_swing_got"] = []
                        weapons.spawn_bullet(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["name"], self.client.data["facing"] -
                                             45+360, self.client.data["updown"], self.client.data["map"], "flail", "melee", w.damage, w.range, w.spread)
                        weapons.spawn_bullet(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["name"], self.client.data["facing"],
                                             self.client.data["updown"], self.client.data["map"], "flail", "melee", w.damage, w.range, w.spread)
                        weapons.spawn_bullet(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["name"], self.client.data["facing"] +
                                             45+360, self.client.data["updown"], self.client.data["map"], "flail", "melee", w.damage, w.range, w.spread)
                        return
                    am = 0
                    try:
                        am = self.client.drawn_weapon.loaded_ammo
                    except:
                        pass
                    if am > 0 or w.melee == True:
                        if w.melee == False:
                            self.client.drawn_weapon.loaded_ammo -= 1
                        updown = self.client.data["updown"]
                        self.client.recoil += 1
                        if self.client.recoil > 5:
                            max_recoil = 100
                            we = self.client.get_weapon_in_list(self.client.data["weapon"])
                            if self.client.skill_data["recoil mastery"]["active"] == True and we.sort == "sub_machine_gun":
                                max_recoil += self.client.skill_data["recoil mastery"]["level"]*8
                            if "stock" in self.client.drawn_weapon.modifications:
                                max_recoil += 30
                            recoil_chanse = random.randint(
                                1, math.ceil(max_recoil/self.client.recoil))
                            if recoil_chanse < 4:
                                updown += 1
                                if updown > 2:
                                    updown = 2
#         send_all(r"player_sound "+self.client.data["name"]+" sounds\\recoilimpact"+str(random.randint(1,3))+".ogg 0")

                        weapons.spawn_bullet(self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["name"],
                                             self.client.data["facing"], updown, self.client.data["map"], w.name, w.sort, w.damage, w.range, w.spread)
                        if w.sort != "melee":
                            self.client.change_statistic("shots fired", 1, True)
                    else:
                        self.client.send("block_fire|n|")
                        send_all(r"player_sound "+self.client.data["name"]+" sounds\\" +
                                 self.client.data["weapon"]+"empty.ogg 0|n|set_shooting "+self.client.data["name"]+" 0 1")
    def reload(self, parsed):
                if self.client.reloading == False and self.client.drawn_weapon is not None and self.client.drawn_weapon.jammed == False and not self.client.drawn_weapon.is_degradated:
                    w = self.client.get_weapon_in_list(self.client.data["weapon"])
                    if w is not None:
                        ammo = 0
                        try:
                            max_ammo = w.max_ammo
                            if self.client.skill_data["extended pistol clip"]["active"] == True and w.sort == "pistol" and w.name != "ruger_redhawk":
                                max_ammo += self.client.skill_data["extended pistol clip"]["level"]
                            ammo = max_ammo-self.client.drawn_weapon.loaded_ammo
                        except:
                            pass
                        if ammo > 0:
                            a = 0
                            try:
                                a = self.client.inventory[w.needed_ammo]
                            except:
                                pass
                            if a >= ammo:
                                self.client.reloadtimer.restart()
                                self.client.reloading = True
                                self.client.drawn_weapon.loaded_ammo = max_ammo
                                self.client.inventory[w.needed_ammo] -= ammo
                                if self.client.inventory[w.needed_ammo]<=0:
                                 del self.client.inventory[w.needed_ammo]
                                send_all(
                                    r"player_sound "+self.client.data["name"]+" sounds\\"+w.name+"reload.ogg 0")
                            else:
                                if a == 0:
                                    self.client.send("speak no ammo left!")
                                else:
                                    self.client.reloadtimer.restart()
                                    self.client.reloading = True
                                    self.client.drawn_weapon.loaded_ammo += a
                                    self.client.inventory[w.needed_ammo] -= a
                                    if self.client.inventory[w.needed_ammo]<=0:
                                     del self.client.inventory[w.needed_ammo]
                                    send_all(
                                        r"player_sound "+self.client.data["name"]+" sounds\\"+w.name+"reload.ogg 0")

                        else:
                            self.client.send("speak reloading is not needed.")
                    else:
                        self.client.send("speak you haven't drawn any weapon.")
    def unload(self, parsed):
                if self.client.reloading == False and self.client.drawn_weapon is not None and self.client.drawn_weapon.jammed == False and not self.client.drawn_weapon.is_degradated:
                    w = self.client.get_weapon_in_list(self.client.data["weapon"])
                    if w is not None:
                        ammo = 0
                        try:
                            ammo = self.client.drawn_weapon.loaded_ammo
                        except:
                            pass
                        if ammo > 0:
                            old_ammo = 0
                            try:
                                old_ammo = self.client.inventory[w.needed_ammo]
                            except:
                                pass
                            self.client.inventory[w.needed_ammo] = ammo+old_ammo
                            send_all(
                                r"player_sound "+self.client.data["name"]+" sounds\\"+w.sort+"unload.ogg 0")
                            self.client.drawn_weapon.loaded_ammo = 0
                            self.client.send("stun 500")
                        else:
                            if w.melee == True:
                                self.client.send(
                                    "speak you can't unload a melee weapon.")
                            else:
                                self.client.send("speak this weapon is already empty")

    def check_ammo(self, parsed):
                    w = self.client.get_weapon_in_list(self.client.data["weapon"])
                    if w is not None:
                        if w.melee == False:
                            max_ammo = w.max_ammo
                            if self.client.skill_data["extended pistol clip"]["active"] == True and w.sort == "pistol" and w.name != "ruger_redhawk":
                                max_ammo += self.client.skill_data["extended pistol clip"]["level"]
                            extra_amount = 0
                            try:
                                extra_amount = self.client.inventory[w.needed_ammo]
                            except:
                                pass
                            self.client.send("speak "+str(self.client.drawn_weapon.loaded_ammo)+" of "+str(max_ammo)+" bullets of "+w.needed_ammo +
                                      " loaded in your "+w.name+". You have "+str(extra_amount)+" bullets of "+w.needed_ammo+" in your belt.")
                        else:
                            self.client.send("speak this weapon doesn't use ammo")
                    else:
                        self.client.send("speak you haven't drawn any weapon.")
    def weapon_menu_ammo_check(self, parsed):
                    w = self.client.get_weapon_in_list(parsed[1])
                    if w is not None:
                        if w.melee == False:
                            max_ammo = w.max_ammo
                            if self.client.skill_data["extended pistol clip"]["active"] == True and w.sort == "pistol" and w.name != "ruger_redhawk":
                                max_ammo += self.client.skill_data["extended pistol clip"]["level"]
                            extra_amount = 0
                            try:
                                extra_amount = self.client.inventory[w.needed_ammo]
                            except:
                                pass
                            self.client.send("speak "+str(self.client.get_weapon_in_list(parsed[1]).loaded_ammo)+" of "+str(
                                max_ammo)+" bullets of "+w.needed_ammo+" loaded in your "+parsed[1]+". You have "+str(extra_amount)+" bullets of "+w.needed_ammo+" in your belt.")
                        else:
                            self.client.send("speak this weapon doesn't use ammo")
                    else:
                        self.client.send("speak weapon not found")
    def delete_weapon(self, parsed):
                    the_weapon = self.client.get_weapon_in_list(parsed[1])
                    if the_weapon:
                        self.client.remove_weapon_instance(the_weapon)
                        tile = v.get_tile_type(map.get_platform(
                            self.client.data["x"], self.client.data["y"], self.client.data["z"], self.client.data["map"]), ["water"])
                        send_all(r"player_sound "+self.client.data["name"]+" sounds\\"+the_weapon.name+"drop"+tile +
                                 ".ogg 0|n|player_sound "+self.client.data["name"]+" sounds\\"+the_weapon.sort+"drop"+tile+".ogg 0")
                    else:
                        self.client.send(
                            "speak this weapon is no longer in your inventory")
    def rotate_weapon(self, parsed):
                    the_weapon = self.client.get_weapon_in_list(parsed[1])
                    if self.client.data["weapons"].count(the_weapon.name) > 1:
                        self.client.weapons.remove(the_weapon)
                        self.client.weapons.append(the_weapon)
                        if self.client.drawn_weapon == the_weapon:
                            self.client.change_weapon(
                                self.client.get_weapon_in_list(parsed[1]))
                            send_all(
                                "set_players_silencer "+self.client.data["name"]+" "+str(self.client.has_silencer(self.client.data["weapon"])))
                        self.client.send("speak switched to an other " +
                                  parsed[1]+". "+self.client.get_weapon_in_list(parsed[1]).get_info())

                    else:
                        self.client.send("speak you only have one of this weapon")

    def weapon_amount(self, parsed):
                    amount = self.client.data["weapons"].count(parsed[1])
                    if amount > 1:
                        self.client.send("speak you have a total of " +
                                  str(amount)+" "+parsed[1]+"s")
                    else:
                        self.client.send("speak you only have 1 "+parsed[1])

    def weapon_store(self, parsed):
                    cx, cy = rotation.move(
                        self.client.data["x"], self.client.data["y"], self.client.data["facing"])
                    id = map.get_object(
                        cx, cy, self.client.data["z"], self.client.data["map"])
                    o = map.get_objects_index(id)
                    if o == "" or self.client.data["z"] >= map.objects[o].maxz or map.objects[o].actif == False and map.objects[o].name != "locker":
                        self.client.send(
                            "speak you aren't standing in front of a locker.")
                        return
                    if map.objects[o].data["opened"] == False:
                        self.client.send(
                            "speak the door of the locker is closed, so you can't store weapons in it. ")
                        return
                    if len(map.objects[o].weapons) >= map.objects[o].data["storage_level"]*20:
                        self.client.send(
                            "speak this locker already has the maximum of weapons")
                        return
                    the_weapon = self.client.get_weapon_in_list(parsed[1])
                    map.objects[o].weapons.append(the_weapon)
                    send_all(r"player_sound "+self.client.data["name"]+" sounds\\"+the_weapon.sort+"place.ogg 0|n|player_sound "+self.client.data["name"] +
                             " sounds\\"+the_weapon.name+"place.ogg 0|n|player_sound "+self.client.data["name"]+" sounds\\lockerplaceweapon.ogg 0")
                    self.client.remove_weapon_instance(the_weapon)
                    if the_weapon.name == self.client.data["weapon"]:
                        self.client.change_weapon(None)
                    if the_weapon.name == self.client.data["holster"]:
                        self.client.data["holster"] = ""
                    self.client.send("get_weapons "+"||".join(self.client.data["weapons"]))

    def weapon_spesific_info(self, parsed):
                    the_weapon = self.client.get_weapon_in_list(parsed[1])
                    self.client.send("speak "+the_weapon.get_info())

    def weapon_info(self, parsed):
                    extra = ""
                    w = self.client.get_weapon_in_list(parsed[1])
                    if w.sort == "sub_machine_gun" and self.client.skill_data["SMG experience"]["active"] == True:
                        extra = "Your streak with your SMG experience give's this gun a bonus of " + \
                            str(4*self.client.data["smg_streak"])+" damage"
                    if w.sort == "marksman_rifle" and self.client.skill_data["DMR precision"]["active"] == True:
                     extra="Your hit streak of "+str(self.client.data["dmr_streak"])+" gives this weapon a damage boost of "+str(self.client.data["dmr_streak"]*30)
                    if w.sort == "assault_rifle":
                        try:
                            index = get_players_index(self.client.data["name"])
                            if index > -1:
                                if v.clients[index].skill_data["sharpshooter mastery"]["active"] == True:
                                    old_weapon = weapons.weapon(w.name)
                                    w.range = old_weapon.range + \
                                        round(
                                            v.clients[index].skill_data["sharpshooter mastery"]["level"]*3)
                        except:
                            pass
                    i = "the "+w.name+" has a range of " + \
                        str(w.range)+" and has a damage of "+str(w.damage) + \
                        ". It is a tier "+str(w.tier)+" weapon."
                    if w.melee == False:
                        i = i+" It uses "+w.needed_ammo
                    else:
                        i = i+" It is a melee weapon"
                    i = i+". "+extra
                    self.client.send("speak "+i)
    def draw_weapon(self, parsed):
                    if self.client.reloading == True:
                        self.client.send("set_weapon "+self.client.data["weapon"])
                        return
                    self.client.data["machete_swing"] = False
                    self.client.data["knife_throw"] = False
                    if self.client.data["holster"] == parsed[1]:
                        self.client.send(
                            "speak you already have this weapon in your holster.")
                        return
                    if parsed[1] == self.client.data["weapon"]:
                        self.client.send("speak you've already drawn this weapon.")
                        return
                    self.client.change_weapon(self.client.get_weapon_in_list(parsed[1]))
                    self.client.send("set_weapon "+parsed[1])
                    send_all(r"player_sound "+self.client.data["name"]+" sounds\\"+parsed[1]+"draw.ogg 0|n|set_player_weapon "+self.client.data["name"] +
                             " "+self.client.data["weapon"]+"|n|set_players_silencer "+self.client.data["name"]+" "+str(self.client.has_silencer(self.client.data["weapon"])))
    def new_mapdata(self, parsed):
                    data=self.data
                    f = open("maps/"+self.client.data["map"]+".txt", "w")
                    mapdata = ""
                    mapdata = data.replace("new_mapdata ", "")
                    mapdata = mapdata.replace("|||", "\n")
                    mlines = mapdata.split("\n")
                    nlines = []
                    for m in mlines:
                        if m.strip() != "":
                            nlines.append(m)
                            mapdata = "\n".join(nlines)
                    f.write(mapdata)
                    f.close()
                    f = open("maps/"+self.client.data["map"]+".txt", "r")
                    data = f.readlines()
                    l = ""
                    for c in v.clients:
                        if c.lobby == False and c.data["map"] == self.client.data["map"]:
                            c.send("mapdata "+"".join(data)+"|n|")
                    f.close()
                    map.load_map(self.client.data["map"], "".join(data))
                    for f in map.objects:
                        o = map.objects[f]
                        if hasattr(o, "team") and o.map==self.client.data["map"] or o.name == "barricade" and o.map==self.client.data["map"]:
                            send_all("spawn_object "+str(o.minx)+" "+str(o.maxx)+" "+str(o.miny)+" "+str(o.maxy)+" "+str(o.minz)+" "+str(
                                o.maxz)+" "+o.name+" "+str(o.dir)+" "+str(o.id)+"|n|set_object_mapdata "+str(o.id)+" "+o.mapdata+"|n|")

    def mapdata(self, parsed):
                    f = open("maps/"+self.client.data["map"]+".txt", "r")
                    data = f.readlines()
                    newdata = """
"""
                    for n in data:
                        if n != "":
                            newdata = newdata+""+n
                    self.client.send(
                        "copie "+newdata+"|n|speak the map data has been copied to your clipboard")
                    f.close()
    def chat(self, parsed):
                    data=self.data
                    if self.client.data["org_mutetime"] > 0:
                        self.client.send("speak your chat has been disabled by the staff. You can chat again in "+str(v.get_time_in_mm(
                            self.client.data["org_mutetime"]-self.client.mutetimer.elapsed()))+"|n|play_sound chat_disabled.ogg 0 0 0 1 0")
                        return
                    if self.client.data["language"] == "disable chat":
                        self.client.send(
                            "speak you have turned off your chat. Please set a channel using the menu by pressing f4.")
                        return
                    if len(data) > 5000:
                        self.client.send("speak chat is to long")
                        return
                    log_file_path = os.path.join("logs", "chats", str(
                        get_current_date()) + "/"+self.client.data["language"]+".log")
                    v.add_log_file(log_file_path, teams.get_team(
                        self.client.data["name"])+" "+self.client.data["name"]+" says: "+data[5:len(data)]+": send on "+str(get_current_time()))
                    for c in v.clients:
                        if self.client.data["name"] not in c.data["mutelist"] and c.data["language"] == self.client.data["language"]:
                            c.send("add_buffer_item chats "+teams.get_team(self.client.data["name"])+" "+self.client.data["name"]+" says: "+data[5:len(
                                data)]+"|n|buffer_sound chats chat.ogg 0 0 0 1 0")
    def chat_reply(self, parsed):
                    data=self.data
                    if len(data) > 5000:
                        self.client.send("speak chat is to long")
                        return
                    if self.client.data["org_mutetime"] > 0:
                        self.client.send("speak your chat has been disabled by the staff. You can chat again in "+str(
                            v.get_time_in_mm(self.client.data["org_mutetime"]-self.client.mutetimer.elapsed())))
                        return
                    if self.client.data["language"] == "disable chat":
                        self.client.send(
                            "speak you have turned off your chat. Please set a channel using the menu by pressing f4.")
                        return
                    log_file_path = os.path.join("logs", "chats", str(
                        get_current_date()) + "/"+self.client.data["language"]+".log")
                    v.add_log_file(log_file_path, data.replace(
                        "chat_reply ", "")+": send on "+str(get_current_time()))
                    for c in v.clients:
                        if self.client.data["name"] not in c.data["mutelist"] and c.data["language"] == self.client.data["language"]:

                            c.send("add_buffer_item chats "+data.replace("chat_reply ",
                                   "")+"|n|buffer_sound chats chat.ogg 0 0 0 1 0")

    def build(self, parsed):
                    data = " ".join(parsed)
                    f = open("maps/"+self.client.data["map"]+".txt", "a+")
                    f.write("\n"+data.replace("build ", ""))
                    f.close()
                    f = open("maps/"+self.client.data["map"]+".txt", "r")
                    data = f.readlines()
                    l = ""
                    for c in v.clients:
                        if c.lobby == False and c.data["map"] == self.client.data["map"]:
                            c.send("mapdata "+"".join(data)+"|n|")
                    f.close()
                    map.load_map(self.client.data["map"], "".join(data))
                    for f in map.objects:
                        o = map.objects[f]
                        if hasattr(o, "team") and o.map==self.client.data["map"] or o.name == "barricade" and o.map==self.client.data["map"]:
                            send_all("spawn_object "+str(o.minx)+" "+str(o.maxx)+" "+str(o.miny)+" "+str(o.maxy)+" "+str(o.minz)+" "+str(
                                o.maxz)+" "+o.name+" "+str(o.dir)+" "+str(o.id)+"|n|set_object_mapdata "+str(o.id)+" "+o.mapdata+"|n|")

    def disconnect_check(self, parsed):
                    for f in map.objects:
                        o = map.objects[f]
                        if self.client.data["x"] >= o.ominx and self.client.data["x"] <= o.omaxx and self.client.data["y"] >= o.ominy and self.client.data["y"] <= o.omaxy and self.client.data["z"] >= o.ominz and self.client.data["z"] <= o.omaxz and self.client.data["map"] == o.map:
                            self.client.send(
                                "speak can't go to the lobby here.|n||n|stop_exiting")
                            return
                    tile = map.get_platform(self.client.data["x"],self.client.data["y"],self.client.data["z"],self.client.data["map"])
                    if tile==""  or tile=="blank":
                            self.client.send(
                                "speak can't go to the lobby here.|n||n|stop_exiting")
                            return

                    if self.client.match_id > -1:
                        self.client.send(
                            "speak can't go to the lobby while you are in a match.|n||n|stop_exiting")
                        return
                    if self.client.exittimer.elapsed() < 45000:
                        self.client.send(
                            "speak you can't go to the lobby right after you have been hit.|n|stop_exiting")
                    else:
                        i = 0
                        for c in v.clients:
                            dist = get_3d_distance(
                                c.data["x"], c.data["y"], c.data["z"], self.client.data["x"], self.client.data["y"], self.client.data["z"])
                            if dist <= 40 and c.data["map"] == self.client.data["map"] and c.lobby == False and c.data["name"] != self.client.data["name"] and c.data["death"] == False:
                                if teams.get_team(self.client.data["name"]) == "" or teams.get_team(self.client.data["name"]) != teams.get_team(c.data["name"]):
                                    i += 1
                        if i > 0:
                            self.client.send(
                                "speak you can't go to the lobby if someone is nearby.|n|stop_exiting")
                        else:
                            self.client.send("disconnect")
    def disconnect(self, parsed):
                    if self.client.exittimer.elapsed() < 15000:
                        self.client.send(
                            "speak you can't disconnect right after you have been hit.|n|stop_exiting")
                        return
                    self.client.send("disconnect")
                    self.client.disconnect(False)
    def player_menu(self, parsed):
                    l = ""
                    for p in v.clients:
                        if p.lobby == True:
                            l = l+p.data["name"]+": in the lobby\n"
                        elif p.match_id > -1:
                            l = l+p.data["name"]+": in a match\n"
                        else:
                            l = l+p.data["name"]+": on the " + \
                                p.data["map"]+" map\n"
                    searching_players=0
                    match_players = 0
                    lobby_players = 0
                    for i in v.clients:
                        if i.match_id > -1:
                            index=match.get_matches_index(i.match_id)
                            if index>-1:
                             if v.matches[index].status=="waiting":
                              searching_players+=1
                             else:
                              match_players += 1
                        elif i.lobby == True:
                            lobby_players += 1

                    if len(v.clients) > 1:
                        text = "player_menu._There_are_"+str(len(v.clients))+"_players_online._"+str(
                            lobby_players)+"_of_them_are_in_the_lobby,_"+str(match_players)+"_are_in_a_match_and_"+str(searching_players)+"_players_are_searching_for_a_match."
                    else:
                        text = "player_menu._There_is_"+str(len(v.clients))+"_player_online._"+str(
                            lobby_players)+"_of_them_are_in_the_lobby,_"+str(match_players)+"_are_in_a_match_and_"+str(searching_players)+"_players_are_searching_for_a_match."
                    self.client.send("server_menu "+text+" "+l)
    def ping(self, parsed):
                    self.client.send("pong")

    def who_on_my_map(self, parsed):
     clients=[]
     for c in v.clients:
      if c.data["map"]==self.client.data["map"] and c.lobby==False:
       clients.append(c.data["name"])
     if len(clients)<=1:
      self.client.send("speak you're the only one on this map")
     else:
      self.client.send("speak "+str(len(clients))+" players on this map: "+v.get_list_in_text(clients))