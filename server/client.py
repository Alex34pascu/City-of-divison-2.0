import hashlib
import packet_handler
import bodyfall
import trap
import healing
import teams
import rotation
import quests
import select
import skills
import weapons
import player_weapon
import random
import v
import armor
import timer
import match
import event
import sd
import explosives as expl
import socket
import datetime
import scanner
import answer as server_menu
import map
import math
import os


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


v.get()


def send_all(message, map=""):
    v.send_packet_to_clients(message, v.clients, map)


class client():
    def __init__(self, conn, addr):
        self.starter_inventory = {
            "45ACP_ammo": 30,
        }
        self.starter_weapons=["knife", "colt_m1911"]
        self.updatelooptimer = timer.timer()
        self.force_packet_exit = False
        self.packet_handler = packet_handler.packet_handler(self)
        self.send_buffer = ""
        self.partial_send = False
        self.sended = False
        self.shopping_cart = {}
        self.losing_loot = True
        self.flash_grenade_inpecttimer = timer.timer()
        self.savetimer = timer.timer()
        self.to_send = []
        self.updatetimer = timer.timer()
        self.updatetimer.set(5000)
        self.lobby = True
        self.exittimer = timer.timer()
        self.exittimer.set(300000)
        self.quest_zone = ""
        self.timeouttimer = timer.timer()
        self.interacttimer = timer.timer()
        self.examine = ""
        self.examining = False
        self.comp_id = ""
        self.total_data = ""
        self.key = b"hallo goars jaja"
        self.s = conn
        self.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.getting_data = ""
        self.addr = addr
        self.s.setblocking(0)
        self.reloading = False
        self.reloadtimer = timer.timer()
        self.speedhackchecktimer = timer.timer()
        self.grenadetimer = timer.timer()
        self.max_speedhack = 0
        self.speedhacktimer = timer.timer()
        self.speedhackchecks = 0
        self.recoil = 1
        self.match_id = -1
        self.using_potions = {}
        self.armor = {}
        for a in armor.armor_types:
            ar = armor.armor(a)
            self.armor[a] = {
                "wearing": False,
                "health": ar.health,
            }
        self.quests = {
            "chapter 1 intro": 1,
        }
        for q in v.all_quests:
            self.quests[q] = -1
        self.mutetimer = timer.timer()
        self.playtimer = timer.timer()
        self.survivetimer = timer.timer()
        self.careful_aimingtimer = timer.timer()
        self.data = {
            "statistics": {},
            "flash_grenade_inpect": False,
            "ip_address": self.addr[0],
            "warnings": [],
            "dmr_shoot": False,
            "dmr_streak": 0,
            "smg_streak": 0,
            "last_matched_players": [],
            "ranked_points": 0,
            "mail": "",
            "silencer_list": [],
            "death_messages": "everyone",
            "careful_aiming": False,
            "documentation_path": "documentation",
            "logs_path": "logs",

            "current_locker_upgrade": "",
            "calculation_locker": -1,
            "store_item": "",
            "take_item": "",
            "store-item": "",
            "fall_distance": 0,
            "machete_swing_got": [],
            "machete_swing": False,
            "knife_throw": False,
            "edit_skills": [],
            "comp_id": "",
            "playtime": 0,
            "survivetime": 0,
            "kills": 0,
            "mutetime": 0,
            "org_mutetime": 0,
            "language": "English",
            "last_killed": "",
            "level": 1,
            "xp": 0,
            "needed_xp": 0,
            "mutelist": [],
            "selected_player": "",
            "input": "",
            "scanner_mode": 0,
            "shooting": 0,
            "weapons": self.starter_weapons.copy(),
            "password": "",
            "chests": {
                "bronze": 0,
                "silver": 0,
                "golden": 0,
                "platinum": 0,
                "diamond": 0,
            },
            "event_points": 0,
            "builder": 0,
            "moderator": 0,
            "admin": 0,
            "holster": "",
            "last_pm": "",
            "death": False,
            "name": "",
            "last_hit": "",
            "last_hit_dir": 0,
            "last_weapon": "",
            "weapon": "colt_m1911",
            "health": 1000,
            "max_health": 1000,
            "x": 300,
            "y": 300,
            "z": 0,
            "facing": 0,
            "updown": 0,
            "invpos": -1,
            "chosen_map": "main",
            "map": "main",
        }

        self.spawn()
        self.drawn_weapon = None
        self.weapons = []
        for w in v.weapon_names:
            new_weapon = player_weapon.player_weapon(w)
            if w in self.data["weapons"]:
                self.weapons.append(new_weapon)
            if w == "colt_m1911":
                new_weapon.loaded_ammo = 8
                self.drawn_weapon = new_weapon

        self.skill_data = {
            "Learn how to swim": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "Learn how to climb": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "Eyes training": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "landing knowledge": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "machete swing": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "knife throw": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "jump endurance": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "sprint": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "DMR precision": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "steady aim": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "recoil mastery": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "sniper mastery": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },

            "extended pistol clip": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },

            "beeing a docter": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "holster augmentation": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "sharpshooter mastery": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "careful aiming": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "grenade knowledge": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "rapid fire": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "SMG experience": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
            "infrared scanner interference": {
                "level": 1,
                "unlocked": False,
                "active": False,
                "skill_points": 0,
            },
        }
        self.backup_skill_data = self.skill_data
        self.skill_timers = {}
        for s in self.skill_data:
            self.skill_timers[s] = timer.timer()
            sk = skills.skill(s)
            self.skill_timers[s].set(sk.cool_downtime)

        self.invpos = -1
        self.account_inventory = {
        }
        self.inventory=self.starter_inventory.copy()
        self.team_phone_check()
        self.disconnected = False
        self.ending = 0
        self.readable, self.writable, exceptional = select.select([], [
                                                                  self.s], [], 0)

    @property
    def kd(self):
        try:
            return round(self.get_statistic("kills")/self.get_statistic("deaths"), 2)
        except:
            return 0

    @property
    def accuracy(self):
        try:
            return str(round((self.get_statistic("shots hit") / self.get_statistic("shots fired")) * 100, 1))+"%"
        except:
            return "0%"

    def show_statistics(self):
        wanted_sequence = ["kills", "deaths", "kd",
                           "objects examined", "shots fired", "shots hit", "accuracy"]
        self.change_statistic("kd", self.kd, False)
        self.change_statistic("accuracy", self.accuracy, False)
        final = []
        extra = []
        for s in self.data["statistics"].keys():
            if s not in wanted_sequence:
                extra.append(s+": "+str(self.get_statistic(s)))

        for s in wanted_sequence:
            if s in self.data["statistics"].keys():
                final.append(s+": "+str(self.get_statistic(s)))
            else:
                final.append(s+": 0")
        extra.sort
        return final+extra

    def get_statistic(self, name):
        if name in self.data["statistics"].keys():
            return self.data["statistics"][name]
        else:
            return 0

    def change_statistic(self, stat, value, increase):
        if stat not in self.data["statistics"].keys() or increase == False:
            self.data["statistics"][stat] = value
        else:
            self.data["statistics"][stat] += value

    def inventory_is_starter_inventory(self):
     inventory=self.starter_inventory
     if teams.get_team(self.data["name"])!="":
      inventory["team_phone"]=1
     return self.inventory==inventory

    def spawn(self):
        s = random.randint(0, len(map.respawn_zones)-1)
        while s in map.get_respawn_zone(self.data["x"], self.data["y"], self.data["z"], self.data["map"]) or map.respawn_zones[s].map!=self.data["map"]:
            s = random.randint(0, len(map.respawn_zones)-1)
        self.data["x"] = random.randint(
            map.respawn_zones[s].sminx, map.respawn_zones[s].smaxx)
        self.data["y"] = random.randint(
            map.respawn_zones[s].sminy, map.respawn_zones[s].smaxy)
        self.data["z"] = random.randint(
            map.respawn_zones[s].sminz, map.respawn_zones[s].smaxz)


    def enter_map(self):
            if self.data["map"][0:13] == "chose_weapons":
                f = open("maps/chose_weapons.txt", "r+")
            else:
                f = open("maps/"+self.data["map"]+".txt", "r+")
            data = f.read()
            f.close()
            l = "set_skill_data "+str(self.skill_data)
            self.send("go "+str(int(self.data["x"]))+" "+str(int(self.data["y"]))+" " +
                   str(self.data["z"])+"|n|start_game|n|mapdata "+data+"|n|"+l)
    def add_weapon(self, weapon_name):
        self.data['weapons'].append(weapon_name)
        weapon = player_weapon.player_weapon(weapon_name)
        self.weapons.append(weapon)

    def add_weapon_instance(self, weapon):
        self.data['weapons'].append(weapon.name)
        self.weapons.append(weapon)

    def remove_weapon(self, weapon_name):
        self.data["weapons"].remove(weapon_name)
        weapon = self.get_weapon_in_list(weapon_name)
        self.weapons.remove(weapon)

        if weapon == self.drawn_weapon:
            self.change_weapon(None)

    def remove_weapon_instance(self, weapon):
        self.data['weapons'].remove(weapon.name)
        self.weapons.remove(weapon)
        if weapon == self.drawn_weapon:
            self.change_weapon(None)
        if weapon.name == self.data["weapon"]:
            self.data["weapon"] = ""
        if weapon.name == self.data["holster"]:
            self.data["holster"] = ""
        self.send("get_weapons "+"||".join(self.data["weapons"]))

    def get_weapon_in_list(self, name):
        for w in self.weapons:
            if w.name == name:
                return w
        return None

    def change_weapon(self, weapon):
        self.drawn_weapon = weapon
        if weapon:
            self.data["weapon"] = weapon.name
        else:
            self.data["weapon"] = ""

    def get_current_weapon(self):
        return self.drawn_weapon.name

    def flash_grenade_inpect_loop(self):
        if self.flash_grenade_inpecttimer.elapsed() > 8000:
            self.send("set_filter 15000")
            self.data["flash_grenade_inpect"] = False

    def check_unlock_quests(self):
        for q in self.quests:
            qe = quests.quest(q)
            if qe.unlock_by_level == True and self.data["level"] >= qe.level and self.quests[q] <= -1:
                if qe.needed_quest == "" or self.quests[qe.needed_quest] == 1:
                    self.send(
                        "add_buffer_item misc You have unlocked the "+q+" quest.")
                    self.quests[q] = 0

    def check_unlock_skills(self):
        for s in self.skill_data:
            sk = skills.skill(s)
            if self.data["level"] >= sk.unlocklevel and self.skill_data[s]["unlocked"] == False and self.match_id == -1:
                self.skill_data[s]["unlocked"] = True
                self.send("add_buffer_item misc you have unlocked the " +
                          s+" skill|n|play_sound skillunlocklevel.ogg 0 0 0 1 0")

    def can_place_barricade(self):
        check_x, check_y = rotation.move(
            self.data["x"], self.data["y"], self.data["facing"])
        check_x = round(check_x)
        check_y = round(check_y)

        if map.get_objects_index_by_cords(check_x, check_y, self.data["z"], self.data["map"]) != "":
            self.send("speak can't place a barricade on an unstable surface.")
            return False

        if teams.get_team(self.data["name"]) == "":
            self.send("speak you need to be in a team to place a barricade.")
            return False
        if not map.has_metal_fortress(teams.get_team(self.data["name"])):
            self.send("speak your team doesn't have a metal fortress")
            return False

        i = 0
        for f in map.objects:
            o = map.objects[f]
            if o.name == "metal_fortress" and o.team == teams.get_team(self.data["name"]):
                fx, fy, fz = o.calculate_closed_point(
                    self.data["x"], self.data["y"], self.data["z"])
                if get_3d_distance(self.data["x"], self.data["y"], self.data["z"], fx, fy, fz) <= 30 and o.map == self.data["map"]:
                    i = 1
        if i == 0:
            self.send(
                "speak you need to be in a 30 tile radius of your fortress to place a barricade.")
            return False

        return True

    def can_place_trap(self):
        if map.get_platform(self.data["x"], self.data["y"], self.data["z"], self.data["map"]) == "" or map.get_platform(self.data["x"], self.data["y"], self.data["z"], self.data["map"]) == "blank":
            self.send("speak can't place a trap when you are in the air.")
            return False
        for t in v.traps:
            if teams.get_team(self.data["name"]) == t.team and get_3d_distance((t.minx+t.maxx)/2, (t.miny+t.maxy)/2, (t.minz+t.maxz)/2, self.data["x"], self.data["y"], self.data["z"]) <= 2:
                self.send("speak your team has already a trap nearby.")
                return False
        if teams.get_team(self.data["name"]) == "":
            self.send("speak you need to be in a team to place a trap.")
            return False
        if not map.has_metal_fortress(teams.get_team(self.data["name"])):
            self.send("speak your team doesn't have a metal fortress")
            return False

        i = 0
        for f in map.objects:
            o = map.objects[f]
            if o.name == "metal_fortress" and o.team == teams.get_team(self.data["name"]):
                fx, fy, fz = o.calculate_closed_point(
                    self.data["x"], self.data["y"], self.data["z"])
                if get_3d_distance(self.data["x"], self.data["y"], self.data["z"], fx, fy, fz) <= 30 and o.map == self.data["map"]:
                    i = 1
        if i == 0:
            self.send(
                "speak you need to be in a 30 tile radius of your fortress to place a trap.")
            return False

        return True

    def calculate_shopping_cart_total(self, source):
        total = 0
        source_keys = source.keys()
        for s in self.shopping_cart:
            if s in source_keys:
                price = source[s]["price"]
                total += price*self.shopping_cart[s]
        return total

    def team_phone_check(self):
        if map.has_metal_fortress(teams.get_team(self.data["name"])) and self.inv_check("team_phone") == 0:
            self.give("team_phone", 1)

    def is_potion_used(self, potion):
        try:
            test = self.using_potions[potion]
            return True
        except:
            return False

    def reset(self):
        match_id = self.match_id
        last_matched_players = self.data["last_matched_players"]
        comp_id = self.comp_id
        event_points = self.data["event_points"]
        old_map = self.data["map"]
        statistics = self.data["statistics"]
        death_messages = self.data["death_messages"]
        chosen_map=self.data["chosen_map"]
        moderator = self.data["moderator"]
        admin = self.data["admin"]
        warnings = self.data["warnings"]
        builder = self.data["builder"]
        account_inventory = self.account_inventory
        using_potions = self.using_potions
        mutelist = self.data["mutelist"]
        scanner_mode = self.data["scanner_mode"]
        chests = self.data["chests"]
        org_mutetime = self.data["org_mutetime"]
        mutetime = self.mutetimer.elapsed()

        playtime = self.playtimer.elapsed()
        mail = self.data["mail"]
        level = self.data["level"]
        xp = self.data["xp"]
        needed_xp = self.data["needed_xp"]
        password = self.data["password"]
        old_language = self.data["language"]
        lobby = self.lobby
        name = self.data["name"]
        ranked_points = self.data["ranked_points"]
        last_pm = self.data["last_pm"]
        skill_data = self.skill_data
        new_quests = self.quests
        self.__init__(self.s, self.addr)
        self.data["name"] = name
        self.data["password"] = password
        self.data["mutelist"] = mutelist
        self.data["statistics"] = statistics
        self.data["last_matched_players"] = last_matched_players
        self.data["chosen_map"] = chosen_map
        self.data["map"] = chosen_map

        self.data["scanner_mode"] = scanner_mode
        self.skill_data = skill_data
        self.data["org_mutetime"] = org_mutetime

        self.lobby = lobby
        self.quests = new_quests
        self.data["chests"] = chests
        self.data["ranked_points"] = ranked_points

        self.match_id = match_id
        self.data["language"] = old_language
        self.data["death_messages"] = death_messages
        self.data["last_pm"] = last_pm
        self.data["event_points"] = event_points
        self.data["level"] = level
        self.data["mail"] = mail
        self.comp_id = comp_id
        self.data["xp"] = xp
        self.mutetimer.set(mutetime)
        self.playtimer.set(playtime)
        self.data["needed_xp"] = needed_xp
        self.survivetimer = timer.timer()
        we = weapons.weapon(self.data["weapon"])
        max_ammo = we.max_ammo
        if self.skill_data["extended pistol clip"]["active"] == True and we.sort == "pistol" and we.name != "ruger_redhawk":
            max_ammo += self.skill_data["extended pistol clip"]["level"]
        self.drawn_weapon.loaded_ammo = max_ammo

        self.data["admin"] = admin
        self.data["warnings"] = warnings
        self.data["moderator"] = moderator
        self.data["builder"] = builder
        self.account_inventory = account_inventory
        self.data["health"] = self.data["max_health"]
        self.using_potions = using_potions

        self.data["death"] = False

    def get_quest_rewards(self, quest_name):
        qe = quests.quest(quest_name)
        rewards = []
        for w in qe.reward:
            if " chest" in w:
                we = w.replace(" chest", "")
                self.data["chests"][we] += 1
                self.send("play_sound chestget.ogg 0 0 0 1 0")
            rewards.append(str(qe.reward[w])+" "+w)
        if len(rewards) <= 0:
            return
        self.send("add_buffer_item misc you got "+v.get_list_in_text(rewards) +
                  " for completing the "+quest_name+" quest.")

    def get_documentation_files(self):
        if not os.path.exists(self.data["documentation_path"]):
            return []
        items = os.listdir(self.data["documentation_path"])
        directories = [item for item in items if os.path.isdir(
            os.path.join(self.data["documentation_path"], item))]
        files = [item for item in items if not os.path.isdir(
            os.path.join(self.data["documentation_path"], item))]
        directories.sort()
        files.sort()
        items = directories + files
        return items

    def get_log_files(self):
        if not os.path.exists(self.data["logs_path"]):
            return []
        items = os.listdir(self.data["logs_path"])
        directories = [item for item in items if os.path.isdir(
            os.path.join(self.data["documentation_path"], item))]
        files = [item for item in items if not os.path.isdir(
            os.path.join(self.data["documentation_path"], item))]
        directories.sort()
        files.sort()
        items = directories + files
        return items

    def use_skill(self, name):
        sk = skills.skill(name)
        if self.skill_timers[name].elapsed() < sk.cool_downtime:
            self.send("speak you can't use this skill right now. Wait " +
                      v.get_time_in_mm(sk.cool_downtime-self.skill_timers[name].elapsed()))
            return
        self.skill_timers[name].restart()
        if name == "rapid fire":
            we = weapons.weapon(self.data["weapon"])
            if we.sort != "pistol":
                self.send(
                    "speak you need to have a pistol in your hand to let this work.")
                self.skill_timers[name].set(500000)
                return
            send_all(r"player_sound " +
                     self.data["name"]+" sounds\\rapidfirestart.ogg 0")
            self.send("start_rapid_fire")
        if name == "infrared scanner interference":
            send_all(r"player_sound " +
                     self.data["name"]+" sounds\\infrared_scannerfailed.ogg 0")
            for c in v.clients:
                dist = get_3d_distance(
                    self.data["x"], self.data["y"], self.data["z"], c.data["x"], c.data["y"], c.data["z"])
                bonus_range = 3 * \
                    self.skill_data["infrared scanner interference"]["level"]
                if dist <= (50+bonus_range) and c.data["name"] != self.data["name"]:
                    send_all(
                        r"player_sound "+c.data["name"]+" sounds\\infrared_scannerinterferencestart.ogg 0")
                    time = 20000 + \
                        (4000 *
                         (self.skill_data["infrared scanner interference"]["level"]-1))
                    c.send("disable_infrared_scanner "+str(time))
        if name == "careful aiming":
            if teams.get_team(self.data["name"]) == "":
                self.send("speak you're not in a team.")
                self.skill_timers[name].set(500000)
                return
            send_all(r"player_sound " +
                     self.data["name"]+" sounds\\careful_aiming.ogg 0")
            self.data["careful_aiming"] = True
            self.careful_aimingtimer.restart()

        if name == "grenade knowledge":
            for g in v.grenades:
                if g.status == "in_hand" and g.owner == self.data["name"]:
                    g.range = 20 + \
                        (self.skill_data["grenade knowledge"]["level"]*2)
                    g.boost = (self.skill_data["grenade knowledge"]["level"])
                    send_all(
                        r"player_sound "+self.data["name"]+" sounds\\grenadeknowledgeactivate.ogg 0")
                    self.send("stun 500")
                    return
            self.send(
                "speak you need to have a grenade with it's pin removed to activate this skill.")
            self.skill_timers[name].set(5000)
        if name == "machete swing":
            if self.data["weapon"] != "machete":
                self.send("speak you have to draw a machete to use this skill.")
                self.skill_timers[name].set(30000)
                return
            self.data["machete_swing"] = True
            self.send(
                "speak you grab the machete so that you can perform the machete swing skill|n|stun 350")
            send_all(r"player_sound " +
                     self.data["name"]+" sounds\\macheteswingstart.ogg 0")
        if name == "knife throw":
            if self.data["weapon"] != "knife":
                self.send("speak you have to draw a knife to use this skill.")
                self.skill_timers[name].set(30000)
                return
            self.data["knife_throw"] = True
            self.send(
                "speak you grab the knife so that you can perform the knife throw skill|n|stun 350")
            send_all(r"player_sound " +
                     self.data["name"]+" sounds\\knifegrab.ogg 0")

        if name == "sprint":
            self.send("start_sprint|n|stun 750")
            send_all(r"player_sound " +
                     self.data["name"]+" sounds\\sprintstart.ogg 0")

    def has_silencer(self, name):
        the_weapon = self.get_weapon_in_list(name)
        if the_weapon is not None and the_weapon.silenced:
            return 1
        return 0

    def get_usable_skills(self, number):
        i = 0
        for s in self.skill_data:
            sk = skills.skill(s)
            if sk.permanent == False and self.skill_data[s]["active"] == True:
                i += 1
            if i >= number:
                return s
        return ""

    def send(self, message=""):
        v.packet_queue.put((self, message))

    def store_data(self, force=False):
        if self.match_id > -1 and force == False:
            return
        self.data["comp_id"] = self.comp_id
        self.data["playtime"] = self.playtimer.elapsed()
        self.data["survivetime"] = self.survivetimer.elapsed()
        self.data["mutetime"] = self.mutetimer.elapsed()
        skill_timers = {}
        for s in self.skill_timers:
            skill_timers[s] = self.skill_timers[s].elapsed()

        using_potions = {}
        for p in self.using_potions:
            using_potions[p] = self.using_potions[p]
            a = self.using_potions[p]["timer"].elapsed()
            using_potions[p]["timer"] = a

        weapons = {}
        for w in self.weapons:
            w.data["name"] = w.name
            weapons[str(self.weapons.index(w))] = w.data

        saving_data = {
            "skill_data": self.skill_data,
            "data": self.data,
            "quests": self.quests,
            "armor": self.armor,
            "skill_timers": skill_timers,
            "inventory": self.inventory,
            "using_potions": using_potions,
            "account_inventory": self.account_inventory,
            "weapons": weapons,
        }
        sd.save_multiple_things(
            saving_data, self.data["name"]+".plr", "players")

    def get_data(self):
        all_data = sd.get_all_data(self.data["name"]+".plr", "players")
        try:
            new_data = all_data["data"]
            for n in new_data:
                if n in self.data:
                    self.data[n] = new_data[n]
        except Exception as e:
            print(str(e))

        try:
            new_quests = all_data["quests"]
            for n in new_quests:
                if n in self.quests:
                    self.quests[n] = new_quests[n]
        except:
            pass

        try:
            new_armor = all_data["armor"]
            for n in new_armor:
                if n in self.armor:
                    self.armor[n] = new_armor[n]
        except:
            pass

        try:
            new_skill_data = all_data["skill_data"]
            for n in new_skill_data:
                if n in self.skill_data:
                    self.skill_data[n] = new_skill_data[n]
        except:
            pass

        try:
            new_skill_timers = all_data["skill_timers"]
            for n in new_skill_timers:
                if n in self.skill_timers:
                    self.skill_timers[n].set(new_skill_timers[n])
        except:
            pass

        try:
            new_inventory = all_data["inventory"]
            for n in new_inventory:
                self.inventory[n] = new_inventory[n]
        except:
            pass

        try:
            new_using_potions = all_data["using_potions"]
            for n in new_using_potions:
                self.using_potions[n] = new_using_potions[n]
        except:
            pass

        try:
            new_account_inventory = all_data["account_inventory"]
            for n in new_account_inventory:
                self.account_inventory[n] = new_account_inventory[n]
        except:
            pass

        try:
            new_weapons = all_data["weapons"]
            self.weapons = []
            for n in new_weapons:
                new_weapon = player_weapon.player_weapon(
                    new_weapons[n]["name"])
                new_weapon.load(new_weapons[n])
                self.weapons.append(new_weapon)

        except Exception as e:
            pass

#  try:
        self.drawn_weapon = self.get_weapon_in_list(self.data["weapon"])
        self.mutetimer.set(self.data["mutetime"])
        self.survivetimer.set(self.data["survivetime"])
        self.playtimer.set(self.data["playtime"])
        self.data["death"] = False
        self.data["needed_xp"] = (self.data["level"]*3)*500+1000
        for p in self.using_potions:
            new_timer = timer.timer()
            new_timer.set(self.using_potions[p]["timer"])
            self.using_potions[p]["timer"] = new_timer
        forbidden_object = False
        id = map.get_object(
            self.data["x"], self.data["y"], self.data["z"], self.data["map"], False)
        o = map.get_objects_index(id)
        if o != "":
                forbidden_object = True
        if map.get_platform(self.data["x"], self.data["y"], self.data["z"], self.data["map"]) == "wall" or forbidden_object:
         self.spawn()
        self.team_phone_check()

        self.check_unlock_quests()
        self.check_unlock_skills()

    def loggin(self, name, password, comp_id, version, create=False):
        if create == True:
            if len(name) < 3:
                self.send("dlg your name is to short")
                v.clients.remove(self)
                return
            if len(name) > 25:
                self.send("dlg your name is to long")
                v.clients.remove(self)
                return
        #  if "\\" in name or "/" in name or r'"' in name or "+" in name or "?" in name or "*" in name or "<" in name or ">" in name:
        #   self.send("dlg error: forbidden charracter in your name")
        #   v.clients.remove(self)
        #   return
        if v.min_version != version:
            self.send("dlg Error: your client is out of date. Download the new client at https://fire-gaming.eu/city_of_division/city of division setup.exe")
            return
        pad = "players"
        file = name+".plr"
        file_pad = os.path.join(pad, file)
        if os.path.exists(file_pad) and create == True:
            self.send("already_exsist")
            return

        if comp_id in v.banlist.values() or name in v.banlist.keys():
                    self.send("banned")
                    return

        try:
            new_data = sd.get("data", name+".plr", {}, "players")
        except:
            self.send("dlg error: forbidden charracter in your name")
            v.clients.remove(self)
            return
        if new_data == {} and create == False:
            self.send("not_exsist")
            return
        self.comp_id = comp_id
        try:
            org_password = new_data["password"]
        except:
            org_password = ""
        if create == True:
            password_bytes = password.encode('utf-8')

            hash_object = hashlib.sha256(password_bytes)
            password = hash_object.hexdigest()
            new_data["password"] = password
            self.data = new_data
            self.data["name"] = name
            try:
                self.store_data()
            except:
                self.send("dlg error: forbidden charracter in your name")
                v.clients.remove(self)
                return

            self.send("loggedin")
            v.send_packetloop()

            self.ending = 1
            v.clients.remove(self)
            return
        new_data = sd.get("data", name+".plr", {}, "players")
        password_bytes = password.encode('utf-8')

        hash_object = hashlib.sha256(password_bytes)
        password = hash_object.hexdigest()
        if password != new_data["password"]:
            self.send("wrong_password")
            return

        for c in v.clients:
            if c.data["name"] == name:
                self.send("samename")
                return
        self.data["name"] = name
        self.send("loggedin")
        v.send_packetloop()

        self.get_data()
        for a in v.announcements:
            if self.data["name"] not in a.read:
                self.send(
                    "buffer_sound misc unread_anouncement.ogg 0 0 0 1 0|n|add_buffer_item misc You have 1 or more unread announcements.")
                break
        for a in v.admin_messages:
            if a.owner == self.data["name"] and self.data["name"] not in a.read:
                self.send(
                    "buffer_sound misc staffmsgplayerreceive.ogg 0 0 0 1 0|n|add_buffer_item misc You have 1 or more unread admin_messages")
                break

        i = 0
        for e in v.events:
            scores = list(e.scores.keys())
            if self.data["name"].lower() not in (member.lower() for member in scores):
                e.scores[self.data["name"].lower()] = 0
                i += 1
                self.send(
                    "add_buffer_item misc A new event has been started while you were offline: "+e.name)
        if i > 0:
            self.send("buffer_sound misc eventnotifyonline.ogg 0 0 0 1 0|n|")
        send_all("add_buffer_item online_and_offline " +
                 self.data["name"]+" has connected|n|buffer_sound online_and_offline online.ogg 0 0 0 1 0")

    def get_pakket(self):
        try:
            # Controleer of de socket leesbaar is (timeout op 0 = non-blocking poll)
            ready_to_read, _, _ = select.select([self.s], [], [], 0)
            if self.s in ready_to_read:
                chunk = self.s.recv(4096)
                if not chunk:
                    return ""  # Verbinding is verbroken

                self.total_data += chunk.decode()
        except BlockingIOError:
            return ""  # Geen data beschikbaar op dit moment
        except Exception as e:
            print(f"Socketfout: {e}")
            return ""

        # Check of er een volledig pakket aanwezig is
        end_marker = "|end|"
        if end_marker in self.total_data:
            idx = self.total_data.find(end_marker) + len(end_marker)
            pakket = self.total_data[:idx]
            self.total_data = self.total_data[idx:]
            return pakket

        return ""

    def inv_check(self, item):
        try:
            return self.inventory[item]
        except:
            return 0

    def account_inv_check(self, item):
        try:
            return self.account_inventory[item]
        except:
            return 0


    def give(self, name, amount):
        a = 0
        try:
            a = self.inventory[name]
        except:
            pass
        if amount >= 0:
            self.inventory[name] = a+amount
        else:
            amount = amount*(-1)
            self.inventory[name] -= amount
            if self.inventory[name]<=0:
                dic = list(self.inventory.keys())
                if self.invpos == dic.index(name):
                    self.invpos = -1
                del self.inventory[name]
                return 0
        max = 0
        try:
            max = v.max_items[name]
        except:
            max = 10
        if self.inventory[name] > max:
            amount = self.inventory[name]
            self.inventory[name] = max
            self.send("speak you have already the maximum of "+name+".")
            return amount-max

        return 0

    def give_account(self, name, amount):
        if "_chest" in name:
            we = name.replace("_chest", "")
            self.data["chests"][we] += amount
            self.send("play_sound chestget.ogg 0 0 0 1 0")
            return
        a = 0
        try:
            a = self.account_inventory[name]
        except:
            pass
        if amount >= 0:
            self.account_inventory[name] = a+amount
        else:
            amount = amount*(-1)
            self.account_inventory[name] -= amount
        for i in self.account_inventory:
            if self.account_inventory[i] <= 0:
                del self.account_inventory[i]
                break

    def check_potions(self):
        for p in self.using_potions:
            try:
                if self.using_potions[p]["timer"].elapsed() > self.using_potions[p]["max_time"]:
                    self.send("speak the effects of the "+p+" have been ended")
                    del self.using_potions[p]
                    break
            except:
                new_timer = timer.timer()
                new_timer.set(self.using_potions[p]["timer"])
                self.using_potions[p]["timer"] = new_timer

    def update(self):
        self.send("offline_check")
        l = ""
        self.updatetimer.restart()
        if self.data["xp"] >= self.data["needed_xp"] and self.data["level"] < v.max_level and self.data["needed_xp"] > 0:
            self.data["xp"] -= self.data["needed_xp"]
            self.data["level"] += 1
            self.data["needed_xp"] = (self.data["level"]*3)*500+1000
            self.send("add_buffer_item misc you leveled up to level " +
                      str(self.data["level"])+"|n|play_sound levelup.ogg 0 0 0 1 0")
            self.check_unlock_quests()
            self.check_unlock_skills()
        if self.data["org_mutetime"] > 0 and self.mutetimer.elapsed() > self.data["org_mutetime"]:
            self.data["org_mutetime"] = 0

    def handle_death(self):
        self.change_statistic("deaths", 1, True)
        self.data["shooting"] = 0
        send_all("set_shooting "+self.data["name"]+" 0")
        self.send("death|n|stun_reset")
        self.store_data()
        for h in v.heals:
            if h.owner == self.data["name"]:
                v.heals.remove(h)
        parsed = self.data["last_hit"].split(" ")
        killer = parsed[0].replace("'s", "")
        for e in v.events:
            if e.name == "weapons competition":
                if self.data["last_weapon"] == e.information["weapon"]:
                    index = get_players_index(killer)
                    if index > -1:
                        event.add_score(killer, "weapons competition", 1)

            if e.name == "kill the VIP":
                if killer == e.information["vip"] and self.data["last_hit"] != "a "+str(self.data["fall_distance"])+" meter fall":
                    e.information["vip_points"] += 1
                if self.data["name"] == e.information["vip"]:
                    send_all(
                        "add_buffer_item misc the current VIP has been killed|n|buffer_sound misc eventnotify.ogg 0 0 0 1 0")
                    if killer != self.data["name"]:
                        index = get_players_index(killer)
                        if index > -1:
                            event.add_score(killer, "kill the VIP", 10)
                    e.information["vip"] = ""
        if self.data["last_hit"] != "a "+str(self.data["fall_distance"])+" meter fall":
            index = get_players_index(killer)
            if index > -1:
                if teams.get_team(v.clients[index].data["name"]) == "" or teams.get_team(v.clients[index].data["name"]) != teams.get_team(self.data["name"]):
                    v.clients[index].data["last_killed"] = self.data["name"]
                    v.clients[index].change_statistic("kills", 1, True)
                    v.clients[index].data["kills"] += 1
                    we = weapons.weapon(self.data["last_weapon"])
                    if we.sort == "sub_machine_gun" and v.clients[index].skill_data["SMG experience"]["active"] == True and v.clients[index].data["smg_streak"] < v.clients[index].skill_data["SMG experience"]["level"]+2:
                        v.clients[index].data["smg_streak"] += 1
                        v.clients[index].send(
                            "play_sound smgstreak.ogg 0 0 0 1 0")

                    if killer != self.data["name"]:
                        for s in v.clients[index].skill_data:
                            if v.clients[index].skill_data[s]["active"] == True and v.clients[index].skill_data[s]["level"] < 8:
                                we = weapons.weapon(
                                    self.data["last_weapon"])
                                sk = skills.skill(s)
                                if we.sort == sk.weapon_sort and we.sort != "":
                                    if self.is_potion_used("mastery_potion") == True:
                                        v.clients[index].skill_data[s]["skill_points"] += random.randint(
                                            2, 6)
                                    else:
                                        v.clients[index].skill_data[s]["skill_points"] += random.randint(
                                            1, 3)

                        if teams.get_team(killer) != teams.get_team(self.data["name"]) or teams.get_team(killer) == "":
                            tindex = teams.get_teams_index(
                                teams.get_team(v.clients[index].data["name"]))
                            if tindex > -1:
                                v.teams[tindex].add_kill()

                            event.add_score(killer, "kill players", 1)
                            v.clients[index].data["xp"] += random.randint(
                                480, 520)
                            if self.data["level"] > v.clients[index].data["level"]:
                                v.clients[index].data["xp"] += (
                                    self.data["level"]-v.clients[index].data["level"])*15
            if not self.data["last_hit"].startswith("the alarm system"):
                send_all(r"player_sound "+self.data["name"]+" sounds\\deathplayer"+str(
                    random.randint(1, 5))+".ogg 0|n|remove_player "+self.data["name"]+"|n|")
            else:
                send_all(r"player_sound "+self.data["name"]+" sounds\\deathplayerelec"+str(
                    random.randint(1, 3))+".ogg 0|n|remove_player "+self.data["name"]+"|n|")

            f = "|n|"
            for c in v.clients:
                report = False
                if c.data["death_messages"] == "only your self" and killer == c.data["name"] or c.data["death_messages"] == "only your self" and self.data["name"] == c.data["name"]:
                    report = True
                if c.data["death_messages"] == "only your team members" and teams.get_team(killer) == teams.get_team(c.data["name"]) or c.data["death_messages"] == "only your team members" and teams.get_team(self.data["name"]) == teams.get_team(c.data["name"]):
                    if teams.get_team(c.data["name"]) != "":
                        report = True
                if c.data["death_messages"] == "only people on your map" and c.data["map"]==self.data["map"]:
                    report = True

                if c.data["death_messages"] == "only people on your map" and c.data["map"]==self.data["map"]:
                    report = True
                if c.data["death_messages"] == "everyone":
                    report = True
                if report == True:
                    c.send("add_buffer_item death_messages "+self.data["name"]+" has been killed by "+self.data["last_hit"]+" at "+map.get_region(
                        self.data["x"], self.data["y"], self.data["z"], self.data["map"]))
                    if c.data["name"] != self.data["name"]:
                        f = f+"|n|player_sound " + \
                            c.data["name"]+" sounds\\report" + \
                            str(random.randint(1, 3))+".ogg 0|n|"
        else:
            send_all(r"player_sound " +
                     self.data["name"]+" sounds\\deathplayerfall.ogg 0")
            f = "|n|"
            for c in v.clients:
                report = False
                if c.data["death_messages"] == "only your self" and killer == c.data["name"] or c.data["death_messages"] == "only your self" and self.data["name"] == c.data["name"]:
                    report = True
                if c.data["death_messages"] == "only your team members" and teams.get_team(killer) == teams.get_team(c.data["name"]) or c.data["death_messages"] == "only your team members" and teams.get_team(self.data["name"]) == teams.get_team(c.data["name"]):
                    if teams.get_team(c.data["name"]) != "":
                        report = True
                if c.data["death_messages"] == "everyone":
                    report = True
                if report == True:
                    c.send("add_buffer_item death_messages "+self.data["name"]+" has been killed by "+self.data["last_hit"]+" at "+map.get_region(
                        self.data["x"], self.data["y"], self.data["z"], self.data["map"])+"|n|")
                    if c.data["name"] != self.data["name"]:
                        f = f+"|n|player_sound " + \
                            c.data["name"]+" sounds\\report" + \
                            str(random.randint(1, 3))+".ogg 0|n|"
        send_all(f)
        log_file_path = os.path.join(
            "logs", "kills", str(get_current_date())+".log")
        v.add_log_file(log_file_path, self.data["name"]+" has been killed by "+self.data["last_hit"]+" at "+map.get_region(
            self.data["x"], self.data["y"], self.data["z"], self.data["map"])+": send on "+str(get_current_time()))

        we = weapons.weapon(self.data["last_weapon"])
        for i in self.inventory:
            self.inventory[i] = round(self.inventory[i]*0.75)
        if self.data["last_hit"] != "a "+str(self.data["fall_distance"])+" meter fall":
            new_weapons = []
            weapon_names = []
            for w in self.weapons:
                if w.name not in weapon_names and w.name in v.weapon_names:
                    new_weapons.append(w)
                    weapon_names.append(w.name)

            bodyfall.spawn_bodyfall(round(self.data["x"]), round(self.data["y"]), self.data["z"], self.data["map"],
                                    self.data["name"], self.data["last_hit_dir"], we.sort, self.inventory, new_weapons)
        else:
            o = map.object(self.data["x"]-1, self.data["x"]+1, self.data["y"]-1, self.data["y"]+1,
                           self.data["z"], self.data["z"]+1, "corpse_of_"+self.data["name"], 1, self.data["map"])
            new_weapons = []
            weapon_names = []
            for w in self.weapons:
                if w.name not in weapon_names:
                    new_weapons.append(w)
                    weapon_names.append(w.name)
            o.weapons = new_weapons
            map.objects[str(o.id)] = o
            minx, maxx, miny, maxy = o.minx, o.maxx, o.miny, o.maxy
            if minx < 0:
                minx = 0
            if maxx < 0:
                maxx = 0
            if minx > 600:
                minx = 600
            if maxx > 600:
                maxx = 600
            if miny < 0:
                miny = 0
            if maxy < 0:
                maxy = 0
            if miny > 600:
                miny = 600
            if maxy > 600:
                maxy = 600
            for l in range(round(minx/10)-1, round(maxx/10)):
                for m in range(round(miny/10)-1, round(maxy/10)):
                    map.objects_x[l][m].append(o)

            forbidden_list = ["locker", "team_phone", "metal_fortress",
                              "metal_fortress_construction_kit", "metal_sheat"]
            self.inventory = {
                key: value for key, value in self.inventory.items() if key not in forbidden_list}
            o.loot = self.inventory
        if self.match_id > -1:
            index = match.get_matches_index(self.match_id)
            if index > -1:
                last_pm = self.data["last_pm"]
                my_map = self.data["map"]
                self.get_data()
                v.matches[index].gain_ranked_points(
                    self.data["name"], False, False)

                self.store_data(True)
                self.data["last_pm"] = last_pm
                self.data["map"] = my_map
                v.matches[index].remove_player(self.data["name"],killer)
            self.match_id = -2
            for b in v.bullets:
                if b.owner == self.data["name"]:
                    v.bullets.remove(b)
        self.data["death"] = True

    def handle_packets(self):
        getting_data = self.get_pakket()
        if getting_data != "":
            getting_data = getting_data.replace("|end|", "")
            bytes_packet = bytes.fromhex(getting_data)
            getting_data = v.aes_decipher(bytes_packet, self.key)+"|n|"

            self.to_send = []
            self.player_data = ""
            lines = getting_data.split("|n|")
            self.force_packet_exit = False
            for data in lines:
                if data == "" or self.force_packet_exit:
                    continue
                if "connect" not in data:
                    if v.packet_printing == True:
                        print(self.data["name"]+": "+data)
                parsed = data.split()
                packet_name = parsed[0]

                handler_func = getattr(self.packet_handler, packet_name, None)
                if callable(handler_func):
                    self.packet_handler.data=data
                    handler_func(parsed)

            if len(self.to_send) >= 0:
                self.send("|n|".join(self.to_send))
            if self.player_data != "":
                for c in v.clients:
                    if c.data["name"] != self.data["name"] and c.lobby == False and c.data["map"] == self.data["map"] and get_3d_distance(c.data["x"], c.data["y"], c.data["z"], self.data["x"], self.data["y"], self.data["z"]) <= 200:
                        c.send(self.player_data)

    def disconnect(self, special=False):
        if self.exittimer.elapsed() < 30000:
            return
        if self.match_id > -1:
            index = match.get_matches_index(self.match_id)
            if index > -1:
                self.get_data()
                v.matches[index].gain_ranked_points(
                    self.data["name"], False, True)
                self.store_data(True)
                v.matches[index].remove_player(self.data["name"], "")
        self.store_data()
        self.disconnected = True
        if self.data["death"] == True:
            self.__init__(self.s, self.s)
        self.store_data()
        self.s.close()
#  for e in v.events:
#   if e.name=="kill the VIP":
#    if e.information["vip"]==self.data["name"]:
#     e.information["vip"]=""
#     send_all("add_buffer_item misc the current VIP has been gone offline and is no longer a VIP|n|buffer_sound misc eventnotify.ogg 0 0 0 1 0")

        disconnect(self.addr, special)

    def updateloop(self):
        if self.skill_data["careful aiming"]["active"]:
            if self.data["careful_aiming"] == True and self.careful_aimingtimer.elapsed() > 10000+(2000*self.skill_data["careful aiming"]["level"]):
                self.data["careful_aiming"] = False
                self.send("speak careful aiming's effects are no longer active")
        if self.data["flash_grenade_inpect"]:
            self.flash_grenade_inpect_loop()
        self.check_potions()
        if self.updatetimer.elapsed() > 5000:
            self.update()
        if self.speedhacktimer.elapsed() > 1000:
            self.speedhacktimer.restart()
            if self.speedhackchecks > 5 and self.max_speedhack <= 250:
                self.send("speedhacked")
                send_all("add_buffer_item important " +
                         self.data["name"]+" is a cheater and got disconnected by the anti cheat system")
                self.disconnect(True)
            self.max_speedhack = 0
            self.speedhackchecks = 0
        if self.reloading:
            if self.reloadtimer.elapsed() >= self.drawn_weapon.reloadtime:
                self.reloading = False

    def run(self):
        if self.updatelooptimer.elapsed() > 5:
            self.updatelooptimer.restart()
            self.updateloop()
        if self.data["health"] <= 0 and self.data["death"] == False and self.lobby == False:
            self.handle_death()
        self.handle_packets()


def disconnect(id, special=False):
    for c in v.clients:
        if c.addr == id:
            c.ending = 1
            v.clients.remove(c)
            if c.data["name"] != "":
                if special == False:
                    send_all("buffer_sound online_and_offline offline.ogg 0 0 0 1 0|n|add_buffer_item online_and_offline " +
                             c.data["name"]+" has disconnected|n|remove_player "+c.data["name"])
                else:
                    send_all(
                        "buffer_sound important offline_special.ogg 0 0 0 1 0|n|")
