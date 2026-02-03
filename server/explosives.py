import v
import math
import teams
import rotation
import map as ma
import random
import timer

v.get()


def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def tile_dependant_explotion(x, y, z, map):
    f = ma.get_platform(x, y, z, map)
    w = v.get_tile_type(f, ["water", "gravel"])
    return r"play_sound "+w+"explode"+str(random.randint(1, 3)) + ".ogg "+str(x)+" "+str(y)+" "+str(z)+" 0 0"


def explode(x, y, z, map, owner, range, damage, range_damage, object_damage, name, strength=7500):
    final_data = []
    final_data.append(tile_dependant_explotion(x, y, z, map))
    for f in ma.objects:
        o = ma.objects[f]
        try:
            fx, fy, fz = o.calculate_closed_point(x, y, z)
            dist = get_3d_distance(x, y, z, fx, fy, fz)
            if dist <= range and o.map == map and o.hitable == True and o.actif == True:
                if o.name != "locker":
                    o.health -= object_damage
                    o.last_hit = owner+"'s "+name
                else:
                    o.health -= round(object_damage/2)
                if hasattr(o, "team"):
                    o.last_team = teams.get_team(owner)

                if o.name != "window":
                    final_data.append(
                        "object_sound "+str(o.id)+" "+o.hitsounds+"explode"+str(random.randint(1, 3))+".ogg")
                o.check_health(True)
        except:
            pass
    for c in v.clients:
        if c.lobby == True:
            continue
        dist = get_3d_distance(x, y, z, c.data["x"], c.data["y"], c.data["z"])
        if dist <= range and map == c.data["map"]:
            try:
                w = ma.calculate_walls(round(x), round(y), round(
                    z), c.data["x"], c.data["y"], c.data["z"], c.data["map"], -1, strength)
            except:
                w = strength
            if w <= 0:
                continue
            e = 1
            try:
                e = w/strength
            except:
                pass
            c.exittimer.restart()
            c.data["health"] -= e*(damage-(range_damage*dist))
            c.data["last_weapon"] = name
            c.data["last_hit"] = owner+"'s "+name
            if e == 1:
                final_data.append(
                    r"player_sound "+c.data["name"]+" sounds\\explotionhit"+str(random.randint(1, 5))+".ogg 0")
            else:
                final_data.append(
                    r"player_sound "+c.data["name"]+" sounds\\explotionhit"+str(random.randint(1, 5))+"f.ogg 0")

    send_all("|n|".join(final_data),map)


def send_all(message, map=""):
    v.send_packet_to_clients(message, v.clients, map)


def get_players_index(name):
    for p in v.clients:
        if p.data["name"].lower() == name.lower():
            return v.clients.index(p)
    return -1


class c4():
    def __init__(self, x, y, z, map, owner, time):
        self.x = x
        self.y = y
        self.z = z
        self.map = map
        self.alert = False
        self.owner = owner
        self.time = time
        self.timer = timer.timer()

    def explode(self):
        for c in v.clients:
            if c.data["map"] == self.map:
                c.send("play_sound c4dist.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z) +
                       " 0 0|n|play_sound c4explode.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
        try:
            explode(self.x, self.y, self.z, self.map,
                    self.owner, 30, 1015, 5, 8000, "c4", 15000)
        except:
            pass
        v.c4s.remove(self)


class RCE():
    def __init__(self, x, y, z, map, owner, code):
        self.x = x
        self.y = y
        self.z = z
        self.map = map
        self.alert = False
        self.code = code
        self.owner = owner
        self.explodetimer = timer.timer()

    def explode(self):
        for c in v.clients:
            if c.data["map"] == self.map:
                c.send("play_sound RCEdist.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z) +
                       " 0 0|n|play_sound RCEexplode.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
        try:
            explode(self.x, self.y, self.z, self.map,
                    self.owner, 15, 900, 5, 3000, "RCE", 10000)
        except:
            pass
        v.RCEs.remove(self)


class grenade():
    def __init__(self, x, y, z, map, owner):
        self.x = x
        self.y = y
        self.z = z
        self.map = map
        self.owner = owner
        self.range = 20
        self.boost = 0
        self.dir = 0
        self.updown = 0
        self.dist = 0
        self.status = "in_hand"
        self.movetimer = timer.timer()
        self.endflytimer = timer.timer()
        self.movetime = 60
        self.time = 3000
        self.timer = timer.timer()
        self.allow_falling = True
        self.falltimer = timer.timer()

    def fall(self):
        self.falltimer.restart()
        if ma.get_platform(self.x, self.y, self.z, self.map) == "" and self.allow_falling == True or ma.get_platform(self.x, self.y, self.z, self.map) == "blank" and self.allow_falling == True:
            if self.dist > 20:
                self.z -= 1
        if ma.get_platform(self.x, self.y, self.z, self.map) != "" and ma.get_platform(self.x, self.y, self.z, self.map) != "blank" and self.dist >= self.range:
            for c in v.clients:
                if c.data["map"] == self.map:
                    c.send("play_sound grenade"+v.get_tile_type(ma.get_platform(self.x, self.y, self.z, self.map), [
                           "grass", "water", "gravel"])+"land"+str(random.randint(1, 3))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
            self.status = "landed"
            return

    def fly(self):
        if self.dist >= self.range:
            if self.falltimer.elapsed() > 30:
                self.fall()
#        return
        if self.updown > 0 and self.dist >= 7:
            self.allow_falling = False
        else:
            self.allow_falling = True
        self.movetimer.restart()
        if self.updown >= -1 and self.updown <= 1:
            cx, cy = rotation.move(self.x, self.y, self.dir)
            self.x = cx
            self.y = cy
        if self.updown < 0:
            self.z -= 1
        if self.updown > 0:
            self.z += 1
        if ma.get_platform(self.x, self.y, self.z, self.map) == "wall":
            index = ma.get_objects_index(
                ma.get_object(self.x, self.y, self.z, self.map))
            if index != "":
                if ma.objects[index].name == "window" and self.dist <= 13:
                    for c in v.clients:
                        if c.data["map"] == self.map:
                            c.send("play_sound windowgrenadehit"+str(random.randint(1, 3)) +
                                   ".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0 ")
                    ma.objects[index].health = -1
                    ma.objects[index].check_health()
                    return
            for c in v.clients:
                if c.data["map"] == self.map:
                    c.send("play_sound grenadebouncegeneric.ogg " +
                           str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0 ")
            if self.updown < 0:
                self.z += 1
                if ma.get_platform(self.x, self.y, self.z, self.map) != "" and ma.get_platform(self.x, self.y, self.z, self.map) != "blank":
                    for c in v.clients:
                        if c.data["map"] == self.map:
                            c.send("play_sound grenade"+v.get_tile_type(ma.get_platform(self.x, self.y, self.z, self.map), [
                                   "grass", "water", "gravel"])+"land"+str(random.randint(1, 3))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
                self.status = "landed"
                return
            if self.dir < 180:
                self.dir += 180
            else:
                self.dir -= 180
            self.movetime += 70
        self.dist += 1
        if self.dist >= 7 and self.updown > 0:
            self.allow_falling = True
            self.updown = self.updown*-1
        for c in v.clients:
            if self.x == c.data["x"] and self.y == c.data["y"] and self.z == c.data["z"] and self.map == c.data["map"] and self.owner != c.data["name"]:
                for cl in v.clients:
                    if cl.data["map"] == self.map:
                        cl.send("play_sound grenadebounceplayer.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+"0 0 |n|play_sound grenade"+v.get_tile_type(ma.get_platform(
                            self.x, self.y, self.z, self.map), ["grass", "water", "gravel"])+"land"+str(random.randint(1, 3))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
                self.status = "landed"
                return

    def follow(self):
        index = get_players_index(self.owner)
        if index > -1:
            self.x = v.clients[index].data["x"]
            self.z = v.clients[index].data["z"]
            self.y = v.clients[index].data["y"]
            self.z = v.clients[index].data["z"]
            self.map = v.clients[index].data["map"]

    def explode(self):
        for c in v.clients:
            if c.data["map"] == self.map:
                c.send("play_sound grenadedist.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0|n|play_sound grenadeexplode" +
                       str(random.randint(1, 3))+".ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
        try:
            explode(self.x, self.y, self.z, self.map, self.owner,
                    12+self.boost, 800, 30, 2000, "grenade")
        except:
            pass
        if self.status == "in_hand":
            index = get_players_index(self.owner)
            if index > -1:
                v.clients[index].give("grenade", -1)
        v.grenades.remove(self)


class flash_grenade(grenade):
    def __init__(self, x, y, z, map, owner):
        super().__init__(x, y, z, map, owner)
        self.time = 2500

    def explode(self):
        send_all(tile_dependant_explotion(self.x, self.y, self.z, self.map),self.map)
        for c in v.clients:
            if c.data["map"] == self.map:
                c.send("play_sound flash_grenadedist.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z) +
                       " 0 0|n|play_sound flash_grenadeexplode.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0")
                dist = get_3d_distance(
                c.data["x"], c.data["y"], c.data["z"], self.x, self.y, self.z)
                if dist <= 10 and c.data["death"] == False and c.lobby == False:
                 c.data["flash_grenade_inpect"] = True
                 c.flash_grenade_inpecttimer.restart()
                 c.send(
                 "set_filter 4000|n|play_sound flash_grenadeimpact.ogg 0 0 0 1 0")
                if dist <= 5:
                 c.exittimer.restart()
                 c.data["health"] -= 100
                 c.data["last_weapon"] = "flash grenade"
                 c.data["last_hit"] = self.owner+"'s flash grenade"

        if self.status == "in_hand":
            index = get_players_index(self.owner)
            if index > -1:
                v.clients[index].give("flash_grenade", -1)
        v.grenades.remove(self)


def explosivesloop():
    for item in v.c4s:
        if item.timer.elapsed() > item.time-900 and item.alert == False:
            item.alert = True
            send_all("play_sound c4alert.ogg "+str(item.x) +
                     " "+str(item.y)+" "+str(item.z)+" 0 0", item.map)
        if item.timer.elapsed() > item.time:
            item.explode()

    [item.explode() for item in v.RCEs if item.explodetimer.elapsed()
     > 2500 and item.alert == True]
    for item in v.grenades:
        if item.timer.elapsed() > item.time:
            item.explode()
        if item.status == "in_hand":
            item.follow()
        if item.allow_falling == True and item.falltimer.elapsed() >= 10 and item.status == "flying":
                item.fall()
        if item.status == "flying" and item.movetimer.elapsed() >= item.movetime:
                item.fly()
