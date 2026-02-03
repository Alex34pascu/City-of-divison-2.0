import weapons
import quests
import random
from random import choice
import v
import timer
import rotation
import player_weapon
import os
import traceback
import event
import teams
import math
import numpy as np

v.get()


def get_players_index(name):
    for p in v.clients:
        if p.data["name"].lower() == name.lower():
            return v.clients.index(p)
    return -1


def send_all(map,message):
 for c in v.clients:
  if c.data["map"]==map and c.lobby==False:
   c.send(message)

def get_player(x, y, z, map, return_player_name=False):
    x=round(x)
    y=round(y)
    z=round(z)

    f = ""
    for p in v.clients:
        if x >= round(p.data["x"]) and x <= round(p.data["x"]) and y >= round(p.data["y"]) and y <= round(p.data["y"]) and z >= round(p.data["z"]) and z <= round(p.data["z"]) and map == p.data["map"]:
            if return_player_name == False:
                f = f+"player"
            else:
                f = f+p.data["name"]

    return f



maps ={}

class map():
 def __init__(self, name):
  self.name=name
  self.platforms_x = create_empty_grid()
  self.walls_x = create_empty_grid()
  self.objects_x = create_empty_grid()
  self.platforms=[]
  self.walls=[]
  self.zones=[]
  self.regions=[]
  self.allow_zones=[]
  self.staircases=[]
  self.respawn_zones=[]
  self.spawn_points=[]
  self.quest_items=[]
  self.quest_zones=[]

 def create_empty_grid(size=60):
  return [[[] for _ in range(size)] for _ in range(size)]



class platform():
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, tile, id=0, map=""):
        self.id = id
        self.map = map
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz
        self.tile = tile


def get_platform(x, y, z, map):
    x=round(x)
    y=round(y)
    z=round(z)
    final = ""

    check_x = round(x / 10)
    check_y = round(y / 10)

    check_x = max(0, min(check_x, 60))
    check_y = max(0, min(check_y, 60))

    # Zorg ervoor dat je toegang krijgt tot de juiste platformen
    platforms = platforms_x[check_x - 1][check_y - 1]

    if not platforms:
        return final

    for p in reversed(platforms):
        if p.minx <= x <= p.maxx and p.miny <= y <= p.maxy and p.minz <= z <= p.maxz and p.map == map:
            return p.tile

    return final


def get_platforms_index(x, y, z, map):
    x=round(x)
    y=round(y)
    z=round(z)

    final = -1
    check_x = x
    if check_x < 0:
        check_x = 0
    if check_x > 600:
        check_x = 600
    check_x = round(check_x/10)
    check_y = y
    if check_y < 0:
        check_y = 0
    if check_y > 600:
        check_y = 600
    check_y = round(check_y/10)
    for p in platforms_x[check_x-1][check_y-1]:
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map:
            final = platforms.index(p)
    return final


platforms_x = map.create_empty_grid()

platforms = []


def get_things_in_area(minx, maxx, miny, maxy, minz, maxz, map, cplatforms=True, cplayers=True, return_player_name=False):
    minx=round(minx)
    maxx=round(maxx)
    miny=round(miny)
    maxy=round(maxy)
    minz=round(minz)
    maxz=round(maxz)

    x = minx
    y = miny
    z = minz
    x=round(x)
    y=round(y)
    z=round(z)

    f = "|"
    while z <= maxz:
        if cplatforms == True:
            f = f+get_platform(x, y, z, map)+"|"
        if cplayers == True:
            f = f+get_player(x, y, z, map, return_player_name)+"|"
        x += 1
        if x > maxx:
            x = minx
            y += 1
            if y > maxy:
                y = miny
                z += 1
    return f


def spawn_platform(minx, maxx, miny, maxy, minz, maxz, tile, id=0, map=""):
    p = platform(minx, maxx, miny, maxy, minz, maxz, tile, id, map)
    platforms.append(p)
    minx, maxx, miny, maxy = get_mmmm(p)
    for l in range(round(minx/10)-1, round(maxx/10)):
        for m in range(round(miny/10)-1, round(maxy/10)):
            platforms_x[l][m].append(p)


loot_outs=[]

class loot_out():
 def __init__(self, map, loot):
  self.map=map
  self.weapons=[]
  self.inventory={}
  self.load_loot(loot)
  loot_outs.append(self)
 def load_loot(self, loot):
  for l in loot:
   if l.startswith("weapon_"):
    self.weapons.append(l.replace("weapon_",""))
   else:
    try:
     self.inventory[l]=int(loot[l])
    except:
     pass
 def give(self, player):
  player.weapons=[]
  player.inventory={}
  for w in self.weapons:
   player.add_weapon(w)
  player.send("get_weapons "+"||".join(player.data["weapons"]))
  for i in self.inventory:
   player.give(i,self.inventory[i])

def get_loot_out(map):
 for l in reversed(loot_outs):
  if l.map==map:
   return l
 return None

class allow_zone():
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, items, map):
        self.items = items
        self.max_number = 0
        for s in self.items.values():
            self.max_number += s
        self.map = map
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz


allow_zones = []


def get_allow_zone(x, y, z, map):
    x=round(x)
    y=round(y)
    z=round(z)

    final = -1
    for p in allow_zones:
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map:
            final = allow_zones.index(p)
    return final


def spawn_allow_zone(minx, maxx, miny, maxy, minz, maxz, items, map):
    allow_zones.append(allow_zone(
        minx, maxx, miny, maxy, minz, maxz, items, map))


class spawn_point():
    def __init__(self, x, y, z, facing, map):
        self.x = x
        self.y = y
        self.z = z
        self.facing = facing
        self.map = map


spawn_points = []


def spawn_spawn_point(x, y, z, facing, map):
    spawn_points.append(spawn_point(x, y, z, facing, map))


def get_spawn_points(map):
    final = []
    for s in spawn_points:
        if s.map == map:
            final.append(s)
    return final


class respawn_zone():
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, sminx, smaxx, sminy, smaxy, sminz, smaxz, map):
        self.map = map
        self.sminx = sminx
        self.smaxx = smaxx
        self.sminy = sminy
        self.smaxy = smaxy
        self.sminz = sminz
        self.smaxz = smaxz
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz


respawn_zones = []


def get_respawn_zone(x, y, z, map):
    x=round(x)
    y=round(y)
    z=round(z)

    final = []
    for p in respawn_zones:
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map:
            final.append(respawn_zones.index(p))
    return final


def spawn_respawn_zone(minx, maxx, miny, maxy, minz, maxz, sminx, smaxx, sminy, smaxy, sminz, smaxz, map):

    respawn_zones.append(respawn_zone(minx, maxx, miny, maxy,
                         minz, maxz, sminx, smaxx, sminy, smaxy, sminz, smaxz, map))


class staircase():
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, tile, walltile, dir, map):
        self.map = map
        self.dir = dir
        self.walltile = walltile
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz
        self.tile = tile
        if self.dir == 1:
            for i in range(self.miny, self.maxy+1):
                spawn_platform(self.minx, self.maxx, i, i, self.minz+i -
                               self.miny, self.minz+i-self.miny, self.tile, 0, self.map)
                spawn_wall(self.minx, self.maxx, i, i, self.minz+i-self.miny-2,
                           self.minz+i-self.miny-1, self.walltile, 5000, 0, self.map)
        if self.dir == 2:
            count = 0
            for i in reversed(range(self.miny, self.maxy+1)):
                spawn_platform(self.minx, self.maxx, i, i, self.minz +
                               count, self.minz+count, self.tile, 0, self.map)
                spawn_wall(self.minx, self.maxx, i, i, self.minz+count-2,
                           self.minz+count-1, self.walltile, 5000, 0, self.map)
                count += 1
        if self.dir == 3:
            for i in range(self.minx, self.maxx+1):
                spawn_platform(i, i, self.miny, self.maxy, self.minz+i -
                               self.minx, self.minz+i-self.minx, self.tile, 0, self.map)
                spawn_wall(i, i, self.miny, self.maxy, self.minz+i-self.minx-2,
                           self.minz+i-self.minx-1, self.walltile, 5000, 0, self.map)
        if self.dir == 4:
            count = 0
            for i in reversed(range(self.minx, self.maxx+1)):
                spawn_platform(i, i, self.miny, self.maxy, self.minz +
                               count, self.minz+count, self.tile, 0, self.map)
                spawn_wall(i, i, self.miny, self.maxy, self.minz+count-2,
                           self.minz+count-1, self.walltile, 5000, 0, self.map)
                count += 1


def get_staircase(x, y, z):
    x=round(x)
    y=round(y)
    z=round(z)

    final = -1
    for p in staircases:
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz:
            final = staircases.index(p)
    return final


staircases = []


def spawn_staircase(minx, maxx, miny, maxy, minz, maxz, tile, walltile, dir=0, map=""):
    staircases.append(staircase(minx, maxx, miny, maxy,
                      minz, maxz, tile, walltile, dir, map))


class wall():
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, tile, strength=5000, id=0, map=""):
        self.id = id
        self.minx = minx
        self.maxx = maxx
        self.strength = strength
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz
        self.map = map
        self.tile = tile
        spawn_platform(minx, maxx, miny, maxy, minz,
                       maxz, "wall", self.id, map)


walls = []


def get_wall(x, y, z, map):
    x=round(x)
    y=round(y)
    z=round(z)

    final = ""
    check_x = x
    if check_x < 0:
        check_x = 0
    if check_x > 600:
        check_x = 600
    check_x = round(check_x/10)
    check_y = y
    if check_y < 0:
        check_y = 0
    if check_y > 600:
        check_y = 600
    check_y = round(check_y/10)
    for p in reversed(walls_x[check_x-1][check_y-1]):
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map and get_platform(x, y, z, map) == "wall" and map == p.map and get_platform(x, y, z, map) == "wall":
            return p.tile
    return final


walls_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    walls_x.append(row)


def get_walls_index(x, y, z, map):
    x=round(x)
    y=round(y)
    z=round(z)
    final = -1
    check_x = x
    if check_x < 0:
        check_x = 0
    if check_x > 600:
        check_x = 600
    check_x = round(check_x/10)
    check_y = y
    if check_y < 0:
        check_y = 0
    if check_y > 600:
        check_y = 600
    check_y = round(check_y/10)
    for p in reversed(walls_x[check_x-1][check_y-1]):
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map and get_platform(x, y, z, map) == "wall":
            return walls.index(p)
    return final


def spawn_wall(minx, maxx, miny, maxy, minz, maxz, tile, strength=5000, id=0, map=""):
    p = wall(minx, maxx, miny, maxy, minz, maxz, tile, strength, id, map)
    walls.append(p)
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
            walls_x[l][m].append(p)


class zone():
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, text, id=0, map=""):
        self.id = id
        self.map = map
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz
        self.text = text


def get_zone(x, y, z, map):
    x=round(x)
    y=round(y)
    z=round(z)

    final = "unnamed area"
    for p in zones:
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map:
            final = p.text
    return final


zones = []


def spawn_zone(minx, maxx, miny, maxy, minz, maxz, text, id=0, map=""):
    zones.append(zone(minx, maxx, miny, maxy, minz, maxz, text, id, map))


class quest_item():
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, item, sound="", map=""):
        self.sound = sound
        self.map = map
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz
        self.item = item


def get_quest_item(x, y, z, map, sound=False):
    x=round(x)
    y=round(y)
    z=round(z)

    final = ""
    for p in quest_items:
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map:
            if sound == False:
                final = p.item
            else:
                final = p.sound

    return final


quest_items = []


def spawn_quest_item(minx, maxx, miny, maxy, minz, maxz, item, sound="", map=""):
    quest_items.append(quest_item(minx, maxx, miny, maxy,
                       minz, maxz, item, sound, map))


class quest_zone():
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, nquest, completion=0, text="", map=""):
        self.completion = completion
        self.text = text
        self.map = map
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz
        self.quest = nquest.replace("_", " ")


def get_quest_zone(x, y, z, map, info=False):
    x=round(x)
    y=round(y)
    z=round(z)

    final = ""
    for p in quest_zones:
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map:
            if info == False:
                final = p.quest
            else:
                final = p.text, p.completion

    return final


quest_zones = []


def spawn_quest_zone(minx, maxx, miny, maxy, minz, maxz, quest, completion=0, text="", map=""):
    quest_zones.append(quest_zone(minx, maxx, miny, maxy,
                       minz, maxz, quest, completion, text, map))


class region():
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, text, id=0, map=""):
        self.id = id
        self.map = map
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz
        self.text = text


def get_region(x, y, z, map):
    x=round(x)
    y=round(y)
    z=round(z)

    final = "unnamed area"
    for p in regions:
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map:
            final = p.text
    return final


regions = []


def spawn_region(minx, maxx, miny, maxy, minz, maxz, text, id=0, map=""):
    regions.append(region(minx, maxx, miny, maxy, minz, maxz, text, id, map))


examining_objects = []
destroying_objects = []
alarm_vehicles=[]
corpses = []
objects = {}
falling_objects = []


objects_x = []
for _ in range(60):
    row = [[] for _ in range(60)]
    objects_x.append(row)


def convert_object(obj):
    if obj.upper_class == "vehicle":
        new_vehicle=vehicle(obj.minx, obj.maxx, obj.miny, obj.maxy, obj.minz, obj.maxz, obj.name, obj.dir, obj.map,obj.id,False)
        return new_vehicle
    else:
        return obj


class object():
    def calculate_closed_point(self, x, y, z):
        final_x = 0
        final_y = 0
        final_z = 0
        if x > self.maxx:
            final_x = self.maxx
        elif x < self.minx:
            final_x = self.minx
        else:
            final_x = x
        if y > self.maxy:
            final_y = self.maxy
        elif y < self.miny:
            final_y = self.miny
        else:
            final_y = y
        if z > self.maxz:
            final_z = self.maxz
        elif z < self.minz:
            final_z = self.minz
        else:
            final_z = z
        return final_x, final_y, final_z

    def __init__(self, minx, maxx, miny, maxy, minz, maxz, name, dir, map, old_id=0, respawn=True,send_spawn=True):
        self.actif = True
        self.remove_after_examining = False
        self.upper_class = ""
        self.destroytimer = timer.timer()
        self.respawn = respawn
        self.hit_bullets = True
        self.last_hit = ""
        self.quest_item = ""
        self.destroytime = 0
        self.destroying = False
        self.falling = False
        self.falldist = 0
        self.falltimer = timer.timer()
        self.id = old_id
        if self.id == 0:
            self.id = random.randint(0, 100000000)
            while self.id in objects.keys():
                self.id = random.randint(0, 100000000)
        self.lifetimer = timer.timer()
        self.showname = name
        self.map = map
        self.hitsounds = name
        self.movesounds = name

        self.minx = round(minx)
        self.maxx = round(maxx)
        self.miny = round(miny)
        self.maxy = round(maxy)
        self.minz = round(minz)
        self.maxz = round(maxz)
        self.ominx = minx
        self.omaxx = maxx
        self.ominy = miny
        self.omaxy = maxy
        self.ominz = minz
        self.omaxz = maxz
        self.name = name
        self.dir = dir
        self.pushtimer = timer.timer()
        self.lootitems = 0
        self.examinetimer = timer.timer()
        self.examining = False
        self.examiner = ""
        self.examinesounds = name
        self.weapons = []
        self.loot = {}
        self.hitable = True
        self.examineendtime = 0
        self.mapdata = """
"""
        self.forbiddenlist = []
        self.examine = False
        self.examinetime = 1200
        if name[0:6] == "corpse":
            self.remove_after_examining = True
            self.examinesounds = "corpse"
            self.lootitems = 10
            self.respawn=False
            self.examineendtime = 4584
            self.examine = True
            self.examinetime = 4584
            self.pushtime = 3000
            self.health = 5000
            self.moveable = False
            self.hitable = False
        elif self.name == "small_glass_cabinet":
            self.lootitems = 3
            self.examine = True
            self.pushtime = 3000
            self.health = 5000
            self.moveable = True
            self.mapdata = """
platform 0 0 0 0 %0 0 hardwood
wall 0 0 0 0 0 -1 wallcabinet 0
"""
        elif self.name == "large_glass_cabinet":
            self.lootitems = 6
            self.examine = True
            self.pushtime = 3000
            self.health = 8000
            self.moveable = False
            self.mapdata = """
platform 0 0 0 0 %0 0 hardwood
wall 0 0 0 0 0 -1 wallcabinet 0
"""
        elif self.name == "tree":
            self.lootitems = 3
            self.examine = False
            self.examinetime = 1200
            self.pushtime = 1500
            self.health = 5000
            self.moveable = False
            self.mapdata = """
platform -1 1 -1 1 %0 3 grass2
wall 0 0 0 0 0 -1 walltree 0
"""
        elif self.name == "table":
            self.lootitems = 3
            self.examine = False
            self.examinetime = 1200
            self.pushtime = 800
            self.health = 1000
            self.moveable = True

            self.mapdata = """
platform 0 0 0 0 %0 0 hardwood1
wall 0 0 0 0 0 -1 walltable 0
"""
        elif self.name == "shipment":
            self.remove_after_examining = True
            self.lootitems = 3
            self.examine = True
            self.examinetime = 1200
            self.pushtime = 800
            self.hitable = False
            self.health = 1000
            self.moveable = False
            self.movesounds = "shipment"
            self.examinesounds = "shipment"
            self.mapdata = """
platform 0 0 0 0 %0 0 wood2
wall 0 0 0 0 0 -1 wallshipment 0
"""

        elif self.name == "window":
            self.lootitems = 3
            self.examine = False
            self.examinetime = 1200
            self.pushtime = 800
            self.health = random.randint(40, 60)
            self.moveable = False

            self.mapdata = """
platform 0 0 0 0 0 0 permanentblank
platform 0 0 0 0 0 %0 permanentbroken_glass
wall 0 0 0 0 0 0 wallglass 500
zone -1 1 -1 1 0 0 permanentwindow
"""
        elif self.name == "locker":
            self.hitsounds = "machine"
            self.lootitems = 3
            self.examine = True
            self.examinetime = 1200
            self.pushtime = 1200
            self.health = 20000
            self.moveable = False
            self.mapdata = """
wall 0 0 0 0 0 0 walllocker 1500
platform 0 0 0 0 %0 0 metal5
"""
        elif self.name == "barricade":
            self.hitsounds = "wood_object"
            self.lootitems = 3
            self.examine = False
            self.examinetime = 1200
            self.pushtime = 1200
            self.health = 8000
            self.moveable = False
            self.mapdata = """
platform 0 0 0 0 0 0 wood
wall 0 0 0 0 0 -1 wallwood2 1000
"""

        elif self.name == "metal_fortress":
            self.hitsounds = "metal_fortress"
            self.lootitems = 3
            self.examine = False
            self.examinetime = 1200
            self.pushtime = 1200
            self.health = 250000
            self.moveable = False
            self.mapdata = """
wall 0 0 0 0 0 0 wallmetalfortress 5000
wall 0 0 0 0 20 -1 wallrail
platform 0 0 0 0 %0 0 metal5
platform 1 -1 1 -1 0 %7 blank
platform 1 -1 1 -1 0 %0 hardwood
platform 1 -1 1 -1 10 %17 blank
platform 1 -1 1 -1 10 %10 hardwood2
platform 1 -1 1 -1 20 0 blank
platform 1 -1 1 -1 20 %20 metal9
zone 0 0 0 0 0 %19 in the fortress
zone 0 0 0 0 20 10 railing
zone 1 -1 1 -1 20 10 on the roof of the fortress
platform 1 %1 1 %1 0 %10 ladder
platform %-1 -1 %-1 -1 10 %20 ladder
zone 1 %1 1 %1 0 %19 ladder
zone %-1 -1 %-1 -1 10 %29 ladder
platform 4 -4 %0 0 0 %7 blank
platform 4 -4 %0 0 0 %0 metal8
zone 4 -4 %-1 1 0 %7 near doorway
zone 4 -4 %0 0 0 %7 doorway
rv 0 0 0 0 -1 %18 -22 400
mute_sounds 0 0 0 0 0 %19 15
"""

        elif self.name == "planter":
            self.lootitems = 1
            self.examine = True
            self.pushtime = 1500
            self.health = 9000
            self.moveable = False
            self.mapdata = """
platform 0 0 0 0 %0 0 stone
platform 1 -1 1 -1 0 0 grass2
wall 0 0 0 0 0 -1 wallstone2 0
"""
            self.forbiddenlist = ["weapon_barrett_M107A1", "weapon_Winchester_Model_24",
                                  "weapon_Benelli_M4", "weapon_fn_f2000", "weapon_hk_mg4"]
        elif self.name == "desk":
            self.movesounds = "table"
            self.lootitems = 2
            self.examine = True
            self.pushtime = 1500
            self.health = 1500
            self.moveable = True
            self.mapdata = """
platform 0 0 0 0 %0 0 hardwood1
wall 0 0 0 0 0 -1 walldesk 0
"""
        elif self.name == "lamppost":
            self.lootitems = 3
            self.examine = False
            self.examinetime = 1200
            self.pushtime = 1500
            self.health = 10000
            self.moveable = False
            self.mapdata = """
platform 0 0 0 0 %0 0 metal5
wall 0 0 0 0 0 -1 walllamppost 0
"""
        else:
            for o in v.object_presets:
                if self.name == o.name:
                    self.hitsounds = o.hitsounds
                    self.showname = o.name
                    self.movesounds = o.movesounds
                    self.examine = o.examinable
                    self.examinesounds = o.examinesounds
                    self.lootitems = o.lootitems
                    self.health = o.health
                    self.mapdata = o.mapdata
                    self.moveable = o.moveable
                    self.pushtime = o.movetime
                    self.upper_class = o.upper_class

        if send_spawn:
            global object_mapdata
            if map_loading == True:
                object_mapdata = object_mapdata+"spawn_object "+str(self.minx)+" "+str(self.maxx)+" "+str(self.miny)+" "+str(self.maxy)+" "+str(
                    self.minz)+" "+str(self.maxz)+" "+self.name+" "+str(self.dir)+" "+str(self.id)+"|n|set_object_mapdata "+str(self.id)+" "+self.mapdata+"|n||n|"
            else:
                send_all(self.map, "spawn_object "+str(int(self.minx))+" "+str(int(self.maxx))+" "+str(int(self.miny))+" "+str(int(self.maxy))+" "+str(int(self.minz)) +
                         " "+str(int(self.maxz))+" "+self.name+" "+str(self.dir)+" "+str(self.id)+"|n|set_object_mapdata "+str(self.id)+" "+self.mapdata+"|n|")

#  self.examinetimer.elapsed=3000
        self.load_mapdata()
        if self.hitsounds == "table" or self.hitsounds == "desk":
            self.destroytime = 700
        if self.hitsounds == "bridge":
            self.destroytime = 4800
            self.hit_bullets = False
        elif self.hitsounds == "metal_fortress":
            self.destroytime = 2000
        elif self.hitsounds == "large_glass_cabinet" or self.hitsounds == "small_glass_cabinet":
            self.destroytime = 1200
        elif self.hitsounds == "furniture":
            self.destroytime = 1250
        elif self.hitsounds == "glass_showcase":
            self.destroytime = 1400
        elif self.hitsounds == "tree":
            self.destroytime = 4000
        elif self.hitsounds == "lamppost":
            self.destroytime = 700
        elif self.hitsounds == "planter":
            self.destroytime = 900
        elif self.hitsounds == "wood_object":
            self.destroytime = 1500
        elif self.hitsounds == "machine":
            self.destroytime = 1200

        if self.examinesounds == "desk":
            self.examineendtime = 2900
            self.examinetime = 1675
        if self.examinesounds == "shipment":
            self.examineendtime = 6500
            self.examinetime = 4700

        elif self.examinesounds == "bed":
            self.examinetime = 2600
            self.examineendtime = 4000
        elif self.examinesounds == "store_shellf":
            self.examinetime = 1700
            self.examineendtime = 2300
        elif self.examinesounds == "misc":
            self.examinetime = 2000
            self.examineendtime = 2600

        elif self.examinesounds == "metal_filing_cabinet":
            self.examineendtime = 2200
            self.examinetime = 1450
        elif self.examinesounds == "large_glass_cabinet":
            self.examineendtime = 2300
            self.examinetime = 1200
        elif self.examinesounds == "small_glass_cabinet":
            self.examineendtime = 2300
            self.examinetime = 1200
        elif self.examinesounds == "planter":
            self.examineendtime = 2800
            self.examinetime = 2400
        elif self.examinesounds == "woodbox":
            self.examineendtime = 4000
            self.examinetime = 2500
        elif self.examinesounds == "corpse":
            self.examineendtime = 4000
            self.examinetime = 4400
        self.examinetimer.set(5000)
        if self.name[0:6] == "corpse":
            corpses.append(self)
        if get_quest_item(self.minx, self.miny, self.minz, self.map, False) != "":
            self.quest_item = get_quest_item(
                self.minx, self.miny, self.minz, self.map, False)
        if self.name == "shipment":
            self.fall_check()

    def load(self, data):
        self.health = data["health"]

    def save(self):
        data = {
            "minx": self.minx,
            "maxx": self.maxx,
            "miny": self.miny,
            "maxy": self.maxy,
            "minz": self.minz,
            "maxz": self.maxz,
            "map": self.map,
            "health": self.health,
        }
        return data

    def rotate(self, direction, minx, maxx, miny, maxy):
        theta_radians = np.radians(direction)
        x = (self.minx+self.maxx)/2
        y = (self.miny+self.maxy)/2
        relative_minx = minx - x
        relative_miny = miny - y
        relative_maxx = maxx - x
        relative_maxy = maxy - y
        rotation_matrix = np.array([[np.cos(theta_radians), -np.sin(theta_radians)],
                                    [np.sin(theta_radians), np.cos(theta_radians)]])

        rotated_min_point = np.dot(
            rotation_matrix, [relative_minx, relative_miny])
        rotated_max_point = np.dot(
            rotation_matrix, [relative_maxx, relative_maxy])

        minx = rotated_min_point[0] + x
        miny = rotated_min_point[1] + y
        maxx = rotated_max_point[0] + x
        maxy = rotated_max_point[1] + y

        if minx > maxx:
            f = 0
            f = minx
            minx = maxx
            maxx = f
        if miny > maxy:
            f = 0
            f = miny
            miny = maxy
            maxy = f
        minx = math.floor(minx)
        maxx = math.floor(maxx)
        miny = math.floor(miny)
        maxy = math.floor(maxy)

        return int(minx), int(maxx), int(miny), int(maxy)

    def load_mapdata(self):
        lines = self.mapdata.split("\n")
        for l in lines:
            parsed = l.split(" ")
            if parsed[0] == "platform" and len(parsed) > 7:
                minx = 0
                maxx = 0
                miny = 0
                maxy = 0
                minz = 0
                maxz = 0
                if "%" in parsed[1]:
                    minx = self.maxx+int(parsed[1].replace("%", ""))
                else:
                    minx = self.minx+int(parsed[1])
                if "%" in parsed[2]:
                    maxx = self.minx+int(parsed[2].replace("%", ""))
                else:
                    maxx = self.maxx+int(parsed[2])
                if "%" in parsed[3]:
                    miny = self.maxy+int(parsed[3].replace("%", ""))
                else:
                    miny = self.miny+int(parsed[3])
                if "%" in parsed[4]:
                    maxy = self.miny+int(parsed[4].replace("%", ""))
                else:
                    maxy = self.maxy+int(parsed[4])
                if "%" in parsed[5]:
                    minz = self.maxz+int(parsed[5].replace("%", ""))
                else:
                    minz = self.minz+int(parsed[5])
                if "%" in parsed[6]:
                    maxz = self.minz+int(parsed[6].replace("%", ""))
                else:
                    maxz = self.maxz+int(parsed[6])
                if "permanent" not in parsed[7]:
                    spawn_platform(minx, maxx, miny, maxy, minz,
                                   maxz, parsed[7], self.id, self.map)
                else:
                    parsed[7] = parsed[7].replace("permanent", "")
                    spawn_platform(minx, maxx, miny, maxy, minz,
                                   maxz, parsed[7], 0, self.map)
            if parsed[0] == "flex_platform" and len(parsed) > 7:
                minx = 0
                maxx = 0
                miny = 0
                maxy = 0
                minz = 0
                maxz = 0
                if "%" in parsed[1]:
                    minx = self.maxx+int(parsed[1].replace("%", ""))
                else:
                    minx = self.minx+int(parsed[1])
                if "%" in parsed[2]:
                    maxx = self.minx+int(parsed[2].replace("%", ""))
                else:
                    maxx = self.maxx+int(parsed[2])
                if "%" in parsed[3]:
                    miny = self.maxy+int(parsed[3].replace("%", ""))
                else:
                    miny = self.miny+int(parsed[3])
                if "%" in parsed[4]:
                    maxy = self.miny+int(parsed[4].replace("%", ""))
                else:
                    maxy = self.maxy+int(parsed[4])
                if "%" in parsed[5]:
                    minz = self.maxz+int(parsed[5].replace("%", ""))
                else:
                    minz = self.minz+int(parsed[5])
                if "%" in parsed[6]:
                    maxz = self.minz+int(parsed[6].replace("%", ""))
                else:
                    maxz = self.maxz+int(parsed[6])
                minx, maxx, miny, maxy = self.rotate(
                    (self.dir*90)-90, minx, maxx, miny, maxy)
                spawn_platform(minx, maxx, miny, maxy, minz,
                               maxz, parsed[7], self.id, self.map)
            if parsed[0] == "flex_wall" and len(parsed) > 7:
                minx = 0
                maxx = 0
                miny = 0
                maxy = 0
                minz = 0
                maxz = 0
                if "%" in parsed[1]:
                    minx = self.maxx+int(parsed[1].replace("%", ""))
                else:
                    minx = self.minx+int(parsed[1])
                if "%" in parsed[2]:
                    maxx = self.minx+int(parsed[2].replace("%", ""))
                else:
                    maxx = self.maxx+int(parsed[2])
                if "%" in parsed[3]:
                    miny = self.maxy+int(parsed[3].replace("%", ""))
                else:
                    miny = self.miny+int(parsed[3])
                if "%" in parsed[4]:
                    maxy = self.miny+int(parsed[4].replace("%", ""))
                else:
                    maxy = self.maxy+int(parsed[4])
                if "%" in parsed[5]:
                    minz = self.maxz+int(parsed[5].replace("%", ""))
                else:
                    minz = self.minz+int(parsed[5])
                if "%" in parsed[6]:
                    maxz = self.minz+int(parsed[6].replace("%", ""))
                else:
                    maxz = self.maxz+int(parsed[6])
                minx, maxx, miny, maxy = self.rotate(
                    (self.dir*90)-90, minx, maxx, miny, maxy)
                try:
                    spawn_wall(minx, maxx, miny, maxy, minz, maxz,
                               parsed[7], int(parsed[8]), self.id, self.map)
                except:
                    spawn_wall(minx, maxx, miny, maxy, minz, maxz,
                               parsed[7], 5000, self.id, self.map)

            if parsed[0] == "flex_zone" and len(parsed) > 7:
                minx = 0
                maxx = 0
                miny = 0
                maxy = 0
                minz = 0
                maxz = 0
                if "%" in parsed[1]:
                    minx = self.maxx+int(parsed[1].replace("%", ""))
                else:
                    minx = self.minx+int(parsed[1])
                if "%" in parsed[2]:
                    maxx = self.minx+int(parsed[2].replace("%", ""))
                else:
                    maxx = self.maxx+int(parsed[2])
                if "%" in parsed[3]:
                    miny = self.maxy+int(parsed[3].replace("%", ""))
                else:
                    miny = self.miny+int(parsed[3])
                if "%" in parsed[4]:
                    maxy = self.miny+int(parsed[4].replace("%", ""))
                else:
                    maxy = self.maxy+int(parsed[4])
                if "%" in parsed[5]:
                    minz = self.maxz+int(parsed[5].replace("%", ""))
                else:
                    minz = self.minz+int(parsed[5])
                if "%" in parsed[6]:
                    maxz = self.minz+int(parsed[6].replace("%", ""))
                else:
                    maxz = self.maxz+int(parsed[6])
                minx, maxx, miny, maxy = self.rotate(
                    (self.dir*90)-90, minx, maxx, miny, maxy)
                spawn_zone(minx, maxx, miny, maxy, minz, maxz, l.replace("zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(
                    parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" ", ""), self.id, self.map)

            if parsed[0] == "wall" and len(parsed) > 7:
                minx = 0
                maxx = 0
                miny = 0
                maxy = 0
                minz = 0
                maxz = 0
                if "%" in parsed[1]:
                    minx = self.maxx+int(parsed[1].replace("%", ""))
                else:
                    minx = self.minx+int(parsed[1])
                if "%" in parsed[2]:
                    maxx = self.minx+int(parsed[2].replace("%", ""))
                else:
                    maxx = self.maxx+int(parsed[2])
                if "%" in parsed[3]:
                    miny = self.maxy+int(parsed[3].replace("%", ""))
                else:
                    miny = self.miny+int(parsed[3])
                if "%" in parsed[4]:
                    maxy = self.miny+int(parsed[4].replace("%", ""))
                else:
                    maxy = self.maxy+int(parsed[4])
                if "%" in parsed[5]:
                    minz = self.maxz+int(parsed[5].replace("%", ""))
                else:
                    minz = self.minz+int(parsed[5])
                if "%" in parsed[6]:
                    maxz = self.minz+int(parsed[6].replace("%", ""))
                else:
                    maxz = self.maxz+int(parsed[6])
                if "permanent" not in parsed[7]:
                    try:
                        spawn_wall(minx, maxx, miny, maxy, minz, maxz,
                                   parsed[7], int(parsed[8]), self.id, self.map)
                    except:
                        spawn_wall(minx, maxx, miny, maxy, minz, maxz,
                                   parsed[7], 5000, self.id, self.map)
                else:
                    parsed[7] = parsed[7].replace("permanent", "")
                    try:
                        spawn_wall(minx, maxx, miny, maxy, minz, maxz,
                                   parsed[7], int(parsed[8]), self.id, self.map)
                    except:
                        spawn_wall(minx, maxx, miny, maxy, minz, maxz,
                                   parsed[7], 5000, self.id, self.map)
            if parsed[0] == "zone" and len(parsed) > 7:
                minx = 0
                maxx = 0
                miny = 0
                maxy = 0
                minz = 0
                maxz = 0
                if "%" in parsed[1]:
                    minx = self.maxx+int(parsed[1].replace("%", ""))
                else:
                    minx = self.minx+int(parsed[1])
                if "%" in parsed[2]:
                    maxx = self.minx+int(parsed[2].replace("%", ""))
                else:
                    maxx = self.maxx+int(parsed[2])
                if "%" in parsed[3]:
                    miny = self.maxy+int(parsed[3].replace("%", ""))
                else:
                    miny = self.miny+int(parsed[3])
                if "%" in parsed[4]:
                    maxy = self.miny+int(parsed[4].replace("%", ""))
                else:
                    maxy = self.maxy+int(parsed[4])
                if "%" in parsed[5]:
                    minz = self.maxz+int(parsed[5].replace("%", ""))
                else:
                    minz = self.minz+int(parsed[5])
                if "%" in parsed[6]:
                    maxz = self.minz+int(parsed[6].replace("%", ""))
                else:
                    maxz = self.maxz+int(parsed[6])
                if "permanent" in parsed[7]:
                    spawn_zone(minx, maxx, miny, maxy, minz, maxz, l.replace("zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(
                        parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" permanent", ""), 0, self.map)
                else:
                    spawn_zone(minx, maxx, miny, maxy, minz, maxz, l.replace("zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(
                        parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" ", ""), self.id, self.map)

    def create_loot(self):
        result = {}
        for i in range(0, self.lootitems):
            item = ""
            amount = 0
            index = get_allow_zone(self.minx, self.miny, self.minz, self.map)
            if index != -1:
                what = random.randint(0, allow_zones[index].max_number)
                s = 0
                for i in allow_zones[index].items:
                    s += allow_zones[index].items[i]
                    if s >= what:
                        item = i
                        break
                if item == "nothing":
                    continue
            else:
                what = random.randint(1, 3550)
                if what in range(0, 151):
                    item = "12_gauge_ammo"
                if what in range(150, 301):
                    item = "5.56mm_ammo"
                if what in range(300, 451):
                    item = "9mm_ammo"
                if what in range(450, 551):
                    item = "4.6x30mm_ammo"
                if what in range(550, 701):
                    item = "weapon_MP7"
                if what in range(700, 751):
                    item = "weapon_hk_mg4"
                if what in range(750, 781):
                    item = "weapon_fn_f2000"
                if what in range(780, 841):
                    item = "weapon_Winchester_Model_24"
                if what in range(840, 881):
                    item = "weapon_Benelli_M4"
                if what in range(880, 1001):
                    item = "weapon_FN_509_tactical"
                if what in range(1000, 1051):
                    item = "weapon_barrett_M107A1"
                if what in range(1050, 1151):
                    item = "7.62mm_ammo"
                if what in range(1150, 1451):
                    item = "weapon_machete"
                if what in range(1450, 1501):
                    item = "bandage"
                if what in range(1500, 1551):
                    item = "Painkiller_injection"
                if what in range(1550, 1601):
                    item = "weapon_ARX160"
                if what in range(1600, 1701):
                    item = "weapon_beretta92A1"
                if what in range(1700, 1731):
                    item = "c4"
                if what in range(1730, 1851):
                    item = "grenade"
                if what in range(1850, 1901):
                    item = "weapon_fn_p90"
                if what in range(1900, 1951):
                    item = "5.7x28mm_ammo"
                if what in range(1950, 2001):
                    item = "weapon_SVD_Dragunov"
                if what in range(2000, 2051):
                    item = "weapon_ruger_redhawk"
                if what in range(2050, 2061):
                    item = "welding_machine"
                if what in range(2060, 2101):
                    item = "welding_machine_battery"
                if what in range(2100, 2151):
                    item = "weapon_mp5"
                if what in range(2150, 2181):
                    item = "first_aid_kit"
                if what in range(2180, 2221):
                    item = "weapon_remington870xs"
                if what in range(2220, 2281):
                    item = ".44_magnum_ammo"
                if what in range(2280, 2301):
                    item = "welding_machine_battery"

                if what in range(2300, 2351):
                    item = "helmet"
                if what in range(2350, 2401):
                    item = "ladder"
                if what in range(2400, 2501):
                    item = "weapon_flail"
                if what in range(2500, 2551):
                    item = "RCE_package"
                if what in range(2550, 2601):
                    item = "weapon_ak47"
                if what in range(2600, 2651):
                    item = "weapon_dsr50"
                if what in range(2650, 2751):
                    item = "metal_piece"
                if what in range(2750, 2851):
                    item = "plastic_piece"
                if what in range(2850, 2901):
                    item = "rubber_piece"
                if what in range(2900, 2931):
                    item = "tool_box"
                if what in range(2930, 3001):
                    item = "flash_grenade"
                if what in range(3000, 3101):
                    item = "metal_piece"
                if what in range(3100, 3201):
                    item = "plastic_piece"
                if what in range(3200, 3251):
                    item = "rubber_piece"
                if what in range(3250, 3301):
                    item = "tool_box"
                if what in range(3300, 3351):
                    item = "50bmg_round"
                if what in range(3350, 3401):
                    item = "weapon_AR10"
                if what in range(3400, 3451):
                    item = "weapon_smith_n_wesson_model29"
                if what in range(3450, 3551):
                    item = "glass_piece"

            if item == "50bmg_round":
                amount = 5
            elif item == "12_gauge_ammo":
                amount = 10
            elif item == "5.56mm_ammo":
                amount = 20
            elif item == "9mm_ammo" or item == "45ACP_ammo" or item==".44_magnum_ammo":
                amount = 15
            elif item == "4.6x30mm_ammo":
                amount = 30
            elif item == "5.7x28mm_ammo":
                amount = 50
            elif item == "7.62mm_ammo":
                amount = 15
            else:
                amount = 1
            if item not in self.forbiddenlist:
                old_amount = 0
                try:
                    old_amount = result[item]
                except:
                    pass
                old_amount = old_amount+amount
                result[item] = old_amount
#   else:
#    i-=1
        for r in result:
            if result[r] < 1:
                result[r] = result[r]*100
        return result

    def check_health(self, explotion=False):
        if self.health <= 0 and self.destroying == False:
            if self.name != "window":
                if explotion == False or explotion == True and self.hitsounds != "glass_showcase":
                    send_all(self.map, r"object_sound "+str(self.id)+" " +
                             self.hitsounds+"destroy"+str(random.randint(1, 3))+".ogg")
            else:
                send_all(self.map, r"object_sound "+str(self.id)+" " +
                         self.hitsounds+"destroy"+str(random.randint(1, 5))+".ogg")


            self.check_event()
            destroying_objects.append(self)
            self.destroytimer.restart()
            self.destroying = True

    def check_event(self):
            parsed = self.last_hit.split(" ")
            killer = parsed[0].replace("'s", "")
            if self.name != "window" and self.name != "ladder":
                index=get_players_index(killer)
                if index>-1:
                 event.add_score(killer, "destroy objects", 1)

    def move(self, dir):
        self.minx, self.miny = rotation.move(self.minx, self.miny, dir)
        self.maxx, self.maxy = rotation.move(self.maxx, self.maxy, dir)
        for l in objects_x:
            for m in l:
                try:
                    l[m].remove(self)
                except:
                    pass
        minx, maxx, miny, maxy = get_mmmm(self)
        for l in range(round(minx/10)-1, round(maxx/10)):
            for m in range(round(miny/10)-1, round(maxy/10)):
                objects_x[l][m].append(self)

        for p in platforms:
            if p.id == self.id:
                p.minx, p.miny = rotation.move(p.minx, p.miny, dir)
                p.maxx, p.maxy = rotation.move(p.maxx, p.maxy, dir)
                for l in platforms_x:
                    for m in l:
                        try:
                            l[m].remove(p)
                        except:
                            pass

                minx, maxx, miny, maxy = get_mmmm(p)
                for l in range(round(minx/10)-1, round(maxx/10)):
                    for m in range(round(miny/10)-1, round(maxy/10)):
                        try:
                            platforms_x[l][m].append(p)
                        except:
                            pass
        for p in walls:
            if p.id == self.id:
                p.minx, p.miny = rotation.move(p.minx, p.miny, dir)
                p.maxx, p.maxy = rotation.move(p.maxx, p.maxy, dir)
                for l in walls_x:
                    for m in l:
                        try:
                            l[m].remove(p)
                        except:
                            pass
                minx, maxx, miny, maxy = get_mmmm(p)
                for l in range(round(minx/10)-1, round(maxx/10)):
                    for m in range(round(miny/10)-1, round(maxy/10)):
                        walls_x[l][m].append(p)

        for p in zones:
            if p.id == self.id:
                p.minx, p.miny = rotation.move(p.minx, p.miny, dir)
                p.maxx, p.maxy = rotation.move(p.maxx, p.maxy, dir)
        return self.fall_check()

    def fall_check(self):
        m = get_things_in_area(self.minx, self.maxx, self.miny,
                               self.maxy, self.minz-1, self.minz-1, self.map, True, False)
        m = m.replace("|", "")
        m = m.replace("blank", "")
        if "wall" not in m:
            self.falling = True
            self.falltimer.restart()
            falling_objects.append(self)
            return 1
        else:
            return 0


def remove_object_mapdata(id):
    global platforms_x
    global platforms
    global walls_x
    global walls
    global zones
    list = []
    for _ in range(60):
        row = [[] for _ in range(60)]
        list.append(row)

    for l in range(0, 60):
        for m in range(0, 60):
            for b in platforms_x[l][m]:
                if b.id != id:
                    list[l][m].append(b)
    platforms_x = list
    list = []
    for _ in range(60):
        row = [[] for _ in range(60)]
        list.append(row)

    for l in range(0, 60):
        for m in range(0, 60):
            for b in walls_x[l][m]:
                if b.id != id:
                    list[l][m].append(b)
    walls_x = list

    list = []
    for b in platforms:
        if b.id != id:
            list.append(b)
    platforms = list
    list = []
    for b in walls:
        if b.id != id:
            list.append(b)
    walls = list
    list = []
    for b in zones:
        if b.id != id:
            list.append(b)
    zones = list


def remove_object(id):
    remove_object_mapdata(id)
    global objects_x
    objects[str(id)].actif = False
    if objects[str(id)].name == "metal_fortress" or objects[str(id)].respawn == False:
        list = []
        for _ in range(60):
            row = [[] for _ in range(60)]
            list.append(row)

        for l in range(0, 60):
            for m in range(0, 60):
                for b in objects_x[l][m]:
                    if b.id != id:
                        list[l][m].append(b)
        objects_x = list
        del objects[str(id)]


def get_objects_index(id):
    try:
        if id == -1:
            return ""
        return str(objects[str(id)].id)
    except:
        return ""


def get_objects_index_by_cords(x, y, z, map, need_be_actif=True):
    x=round(x)
    y=round(y)
    z=round(z)

    final = ""
    check_x = x
    if check_x < 0:
        check_x = 0
    if check_x > 600:
        check_x = 600
    check_x = round(check_x/10)
    check_y = y
    if check_y < 0:
        check_y = 0
    if check_y > 600:
        check_y = 600
    check_y = round(check_y/10)
    for p in reversed(objects_x[check_x-1][check_y-1]):
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz and map == p.map and p.actif == True:
            if p.actif == True or p.actif == False and need_be_actif == False:
                return str(p.id)
    return final


def get_object(x, y, z, map, need_be_actif=True):
    x=round(x)
    y=round(y)
    z=round(z)
    final = -1
    check_x = x
    if check_x < 0:
        check_x = 0
    if check_x > 600:
        check_x = 600
    check_x = round(check_x/10)
    check_y = y
    if check_y < 0:
        check_y = 0
    if check_y > 600:
        check_y = 600
    check_y = round(check_y/10)
    for p in objects_x[check_x-1][check_y-1]:
        if x >= p.minx and x <= p.maxx and y >= p.miny and y <= p.maxy and z >= p.minz and z <= p.maxz-1 and map == p.map:
            if p.actif == True or p.actif == False and need_be_actif == False:
                final = p.id
    return final


def spawn_object(minx, maxx, miny, maxy, minz, maxz, name, dir, map, respawn=True):
    f = object(minx, maxx, miny, maxy, minz, maxz, name, dir, map, 0, respawn)
    p = convert_object(f)
    objects[str(p.id)] = p
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
            objects_x[l][m].append(p)

        return p


metal_fortresss = []


class metal_fortress(object):
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, map, team):
        super().__init__(minx, maxx, miny, maxy, minz, maxz, "metal_fortress", 1, map)
        self.alarm_playingtimer = timer.timer()
        self.last_team = ""
        self.team = team
        self.max_health = 5000000
        self.alarm_players = {}
        self.data = {
            "alarm": False,
            "highest_health": self.health,
        }
        minx, maxx, miny, maxy = self.minx, self.maxx, self.miny, self.maxy
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
                objects_x[l][m].append(self)
        metal_fortresss.append(self)

    def load(self, data):
        self.health = data["health"]
        try:
            for d in data["data"]:
                self.data[d] = data["data"][d]
        except:
            pass

    def save(self):
        data = {
            "minx": self.minx,
            "maxx": self.maxx,
            "miny": self.miny,
            "maxy": self.maxy,
            "minz": self.minz,
            "maxz": self.maxz,
            "map": self.map,
            "health": self.health,
            "data": self.data,
            "team": self.team,
        }
        return data

    def check_health(self, explotion=False):
        try:
            if self.health <= 0 and self.destroying == False:
                if self.destroying == False:
                    destroying_objects.append(self)
                    self.destroytimer.restart()
                    self.destroying = True

                index = teams.get_teams_index(self.team)
                if index > -1:
                    v.teams[index].metal_fortresstimer.restart()
                    metal_fortresss.remove(self)

                if self.last_team != "" and self.last_team != self.team:
                    index = teams.get_teams_index(self.last_team)
                    if index > -1:
                        tokens = round(self.data["highest_health"]/15000)
                        v.teams[index].data["tokens"] += tokens
                        v.teams[index].send("add_buffer_item team this team has earned "+str(
                            tokens)+" tokens for destroying the metal_fortress of "+self.team+"|n|play_sound tokenget.ogg 0 0 0 1 0")

                send_all(self.map, r"object_sound "+str(self.id)+" " +
                         self.hitsounds+"destroy"+str(random.randint(1, 3))+".ogg")

                removing_objects = []
                for f in objects:
                    o = objects[f]
                    if hasattr(o, "team") and f != self.id and o.name == "locker" and o.team == self.team:
                        removing_objects.append(o)

                for o in removing_objects:
                    o.health = -1
                    o.check_health()

                import trap
                remaining_traps = []
                for t in v.traps:
                    if t.team != self.team:
                        remaining_traps.append(t)
                v.traps = remaining_traps
                trap.remake_traps_x()

        except Exception as e:
            error_message = ''.join(
                traceback.format_exception(type(e), e, e.__traceback__))
            print(error_message)

def objectloop():
        for o in falling_objects:
            if o.falltimer.elapsed() > 30:
                o.falltimer.restart()
                if "wall" not in get_things_in_area(o.minx, o.maxx, o.miny, o.maxy, o.minz-1, o.minz-1, o.map, True, False):
                    o.minz -= 1
                    o.maxz -= 1
                    for p in platforms:
                        if p.id == o.id:
                            p.minz -= 1
                            p.maxz -= 1
                    for p in walls:
                        if p.id == o.id:
                            p.minz -= 1
                            p.maxz -= 1
                    for p in zones:
                        if p.id == o.id:
                            p.minz -= 1
                            p.maxz -= 1
                    o.falldist += 1
                else:
                    send_all(o.map,"remove_object "+str(o.id)+"|n|spawn_object "+str(o.minx)+" "+str(o.maxx)+" "+str(o.miny)+" "+str(o.maxy)+" "+str(
                        o.minz)+" "+str(o.maxz)+" "+o.name+" "+str(o.dir)+" "+str(o.id)+"|n|set_object_mapdata "+str(o.id)+" "+o.mapdata+"|n|")
                    if o.falldist > 6:
                        send_all(o.map,"object_sound "+str(o.id) +
                                 " "+o.movesounds+"fall.ogg")
                        m = get_things_in_area(
                            o.minx, o.maxx, o.miny, o.maxy, o.minz, o.maxz+1, o.map, False, True, True)
                        plist = m.split("|")
                        for p in plist:
                            index = get_players_index(p)
                            if index > -1:
                                v.clients[index].data["health"] = -100
                                v.clients[index].data["last_hit"] = "a falling "+o.name
                        if o.name != "shipment":
                            send_all(o.map,"remove_object "+str(o.id))
                            remove_object(o.id)
                            o.actif = False
                        else:
                            index = get_objects_index_by_cords(
                                o.minx, o.miny, o.minz-1, o.map)
                            if index != "" and objects[index].name == "metal_fortress":
                                send_all(objects[index].map,
                                    r"object_sound "+str(objects[index].id)+" shipmentfallfortress.ogg")

                        falling_objects.remove(o)
                        break
                    else:
                        send_all(o.map,"object_sound "+str(o.id)+" "+o.movesounds +
                                 "land"+str(random.randint(1, 2))+".ogg")

                    o.falldist = 0
                    o.falling = False
                    falling_objects.remove(o)
                    break
        if len(destroying_objects) > 0:
            for item in destroying_objects:
                if item.destroytimer.elapsed() > item.destroytime and item.destroying == True:

                    send_all(item.map,"remove_object "+str(item.id))
                    item.destroying = False
                    item.actif = False
                    remove_object(item.id)
                    destroying_objects.remove(item)
                    break
        for item in alarm_vehicles:
            if item.alarm == True and item.alarmtimer.elapsed() > 6000:
                item.alarm = False
                send_all(item.map,"remove_object_sound "+str(item.id) +
                         " vehiclealarm"+str(item.alarmsort)+".ogg")
                alarm_vehicles.remove(item)
                break
        if len(corpses) > 0:
            for item in corpses:
                if item.lifetimer.elapsed() >= 300000:
                    send_all(item.map,"remove_object "+str(item.id))
                    corpses.remove(item)
                    remove_object(item.id)
                    break
        if len(examining_objects) > 0:
            for item in examining_objects:
                if item.examining == True and item.examinetimer.elapsed() >= item.examinetime:
                    item.examining = False
                    index = get_players_index(item.examiner)
                    if index > -1:
                        if v.clients[index].data["death"] == True:
                            examining_objects.remove(item)
                            break
                        item.examiner = ""
                        v.clients[index].examining = False
                        if item.quest_item != "":
                            i = 0
                            for q in v.clients[index].quests:
                                qe = quests.quest(q)
                                if qe.item == item.quest_item and v.clients[index].quests[q] == 0:
                                    cx, cy = rotation.move(
                                        v.clients[index].data["x"], v.clients[index].data["y"], v.clients[index].data["facing"])
                                    send_all(item.map,r"player_sound "+v.clients[index].data["name"]+" sounds\\"+get_quest_item(
                                        cx, cy, v.clients[index].data["z"], v.clients[index].data["map"], True)+" 0")
                                    v.clients[index].quests[q] = 1
                                    v.clients[index].get_quest_rewards(q)
                                    v.clients[index].send(
                                        "add_buffer_item misc you have completed the "+q+" quest.|n|buffer_sound misc quest_complete.ogg 0 0 0 1 0")
                                    if qe.unlock_quest != "":
                                        v.clients[index].quests[qe.unlock_quest] = 0
                                        v.clients[index].send(
                                            "add_buffer_item misc you have unlocked the "+qe.unlock_quest+" quest")
                                    i = 1
                            if i == 1:
                                break
                        final = "you found "
                        l = []
                        remaining_loot = {}
                        sounds_packet = ""
                        for f in item.loot:
                            if f == "welding_machine_battery" or f == "welding_machine":
                                if teams.get_team(v.clients[index].data["name"]) == "":
                                    f = "weapon_machete"
                            if f[0:7] == "weapon_":
                                f = f.replace("weapon_", "")
                                we = weapons.weapon(f)
                                if we.level > v.clients[index].data["level"]:
                                    continue
                                if item.name != "shipment":
                                    times = 1
                                else:
                                    times = item.loot["weapon_"+f]
                                we = weapons.weapon(f)
                                if we.melee == False and item.remove_after_examining == False:
                                    v.clients[index].give(
                                        we.needed_ammo, we.max_ammo)
                                    l.append(str(times)+" "+f+" with " +
                                             str(we.max_ammo)+" "+we.needed_ammo)
                                else:
                                    l.append(str(times)+" "+f)
                                for i in range(times):
                                    if v.clients[index].data["weapons"].count(f) < 3:
                                        v.clients[index].add_weapon(f)
                                    else:
                                        v.clients[index].send(
                                            "speak you already have 3 "+f+"s")
                                        break
                                sounds_packet = sounds_packet+"player_sound " + \
                                    v.clients[index].data["name"]+" sounds\\"+f+"get.ogg 0|n|player_sound " + \
                                    v.clients[index].data["name"] + \
                                    " sounds\\"+we.sort+"get.ogg 0|n|"
                            else:
                                rest = v.clients[index].give(f, item.loot[f])
                                if rest > 0:
                                    if item.name == "shipment":
                                        remaining_loot[f] = rest
                                sounds_packet = sounds_packet+"player_sound " + \
                                    v.clients[index].data["name"] + \
                                    " sounds\\"+f+"get.ogg 0|n|"
                                l.append(str(item.loot[f])+" "+f)

                        for w in item.weapons:
                            if w.level > v.clients[index].data["level"]:
                                continue
                            if v.clients[index].data["weapons"].count(w.name) >= 3:
                                v.clients[index].send(
                                    "speak you already have 3 "+w.name+"s")
                                continue
                            l.append("1 "+w.name)
                            v.clients[index].add_weapon_instance(w)
                            sounds_packet = sounds_packet+"player_sound " + \
                                v.clients[index].data["name"]+" sounds\\"+w.sort+"get.ogg 0|n|player_sound " + \
                                v.clients[index].data["name"] + \
                                " sounds\\"+w.sort+"get.ogg 0|n|"
                        if l == []:
                            final = final+"nothing."
                        else:
                            if remaining_loot == {}:
                                v.clients[index].change_statistic(
                                    "objects examined", 1, True)
                                event.add_score(
                                    v.clients[index].data["name"], "examine objects", 1)
                            final = final+v.get_list_in_text(l)
                            send_all(item.map,r""+sounds_packet)
                        item.loot = remaining_loot
                        v.clients[index].send(
                            "add_buffer_item misc "+final+"|n|get_weapons "+"||".join(v.clients[index].data["weapons"]))
                        if item.remove_after_examining == True and item.loot == {}:
                            send_all(item.map,"remove_object "+str(item.id))
                            if item in corpses:
                                corpses.remove(item)
                            remove_object(item.id)
                        examining_objects.remove(item)

def metal_fortressloop():
    for m in metal_fortresss:
        if m.alarm_players != {}:
            if m.alarm_playingtimer.elapsed() > 4000:
                m.alarm_playingtimer.restart()
                send_all(m.map, "object_sound "+str(m.id)+" intruderalarm.ogg")
                tindex = teams.get_teams_index(m.team)
                if tindex > -1:
                    for t in v.teams[tindex].members:
                        index = get_players_index(t)
                        if index > -1 and v.clients[index].inv_check("team_phone") >= 1:
                            send_all(
                                m.map, r"player_sound "+v.clients[index].data["name"]+" sounds\\intruderalarmphone.ogg 0")

            for p in m.alarm_players:
                if m.alarm_players[p].elapsed() > 10000:
                    index = get_players_index(p)
                    if index > -1:
                        if get_metal_fortress(v.clients[index].data["x"], v.clients[index].data["y"], v.clients[index].data["z"], v.clients[index].data["map"]) == m.id:
                            v.clients[index].data["health"] = -1
                            v.clients[index].data["last_hit"] = "the alarm system of the " + \
                                m.team+"'s metal fortress"
                            send_all(m.map, r"player_sound "+v.clients[index].data["name"]+" sounds\\electricityhit"+str(
                                random.randint(1, 3))+".ogg 0")
                    del m.alarm_players[p]
                    break


def get_metal_fortress(x, y, z, map):
    x=round(x)
    y=round(y)
    z=round(z)

    for m in metal_fortresss:
        if m.minx <= x <= m.maxx and m.miny <= y <= m.maxy and m.minz <= z <= m.maxz+6 and m.map == map:
            return m.id
    return -1


def has_metal_fortress(team_name):
    for m in metal_fortresss:
        if m.team == team_name:
            return True
    return False


class vehicle(object):
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, name, dir, map,old_id=0,send_spawn=True):
        super().__init__(minx, maxx, miny, maxy, minz, maxz,
                       name, dir, map,old_id,True,send_spawn)
        self.alarm = False
        self.alarmtimer = timer.timer()
        self.alarmsort=random.randint(1,6)
        self.alarm_pitch= random.randint(95,105)

    def check_health(self, explotion=False):
        from explosives import explode
        self.alarmtimer.restart()
        if self.alarm == False:
            self.alarm = True
            send_all(self.map,"add_object_sound "+str(self.id)+" vehiclealarm"+str(self.alarmsort)+".ogg "+str(self.alarm_pitch))
            alarm_vehicles.append(self)
        if self.health <= 0:
            self.check_event()
            send_all(self.map,"remove_object "+str(self.id))
            self.actif=False
            remove_object(self.id)
            for c in v.clients:
                if c.data["map"]==self.map:
                    x,y,z = self.calculate_closed_point(c.data["x"],c.data["y"],c.data["z"])
                    c.send("play_sound vehicleexplosiondist"+str(random.randint(1,3))+".ogg "+str(x)+" "+str(y)+" "+str(z) +
                     " 0 0|n|play_sound vehicleexplosionexplode"+str(random.randint(1,3))+".ogg "+str(x)+" "+str(y)+" "+str(z)+" 0 0")
            try:
             explode((self.minx+self.maxx)/2, (self.miny+self.maxy)/2, (self.minz+self.maxz)/2,
            self.map, "a "+self.name, 12, 300, 5, 500, "destruction",18000)
             alarm_vehicles.remove(self)
            except Exception as e:
             speak(str(e))

class locker(object):
    def __init__(self, minx, maxx, miny, maxy, minz, maxz, map, team):
        super().__init__(minx, maxx, miny, maxy, minz, maxz, "locker", 1, map)
        self.last_team = ""
        self.team = team
        self.math = 0
        self.max_math = 1
        self.max_math_numbers = 10
        self.data = {
            "maximum_health_level": 1,
            "security_level": 1,
            "storage_level": 1,
            "opened": False,
        }
        self.health_levels = [20000, 50000, 100000, 150000,
                              220000, 330000, 450000, 630000, 850000, 1000000]
        self.max_health = self.health_levels[self.data["maximum_health_level"]-1]
        minx, maxx, miny, maxy = self.minx, self.maxx, self.miny, self.maxy
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
                objects_x[l][m].append(self)

    def load(self, data):
        self.health = data["health"]
        try:
            new_weapons = data["weapons"]
            for n in new_weapons:
                new_weapon = player_weapon.player_weapon(
                    new_weapons[n]["name"])
                new_weapon.load(new_weapons[n])
                self.weapons.append(new_weapon)
        except:
            pass
        self.loot = data["loot"]
        new_loot = {}
        for l in self.loot:
            if not l.startswith("weapon_"):
                new_loot[l] = self.loot[l]
        self.loot = new_loot
        for d in data["data"]:
            self.data[d] = data["data"][d]
        self.max_health = self.health_levels[self.data["maximum_health_level"]-1]

    def save(self):
        weapons = {}
        for w in self.weapons:
            w.data["name"] = w.name
            weapons[str(self.weapons.index(w))] = w.data

        data = {
            "data": self.data,
            "minx": self.minx,
            "maxx": self.maxx,
            "miny": self.miny,
            "maxy": self.maxy,
            "minz": self.minz,
            "maxz": self.maxz,
            "map": self.map,
            "health": self.health,
            "loot": self.loot,
            "team": self.team,
            "weapons": weapons,
        }
        return data

    def check_health(self, explotion=False):
        from explosives import explode
        if self.health <= 0 and self.destroying == False:
            if self.last_team != "" and self.last_team != self.team:
                index = teams.get_teams_index(self.last_team)
                if index > -1:
                    tokens = (self.data["maximum_health_level"] +
                              self.data["security_level"]+self.data["storage_level"])*3
                    v.teams[index].data["tokens"] += tokens
                    v.teams[index].send("add_buffer_item team this team has earned "+str(
                        tokens)+" tokens for destroying the locker of "+self.team+"|n|play_sound tokenget.ogg 0 0 0 1 0")
            send_all(self.map, "remove_object "+str(self.id))
            remove_object(self.id)
            del objects[str(self.id)]
            send_all(self.map, "play_sound lockerexplodedist.ogg "+str(self.minx)+" "+str(self.miny)+" "+str(self.minz) +
                     " 0 0|n|play_sound lockerexplode.ogg "+str(self.minx)+" "+str(self.miny)+" "+str(self.minz)+" 0 0")
            explode((self.minx+self.maxx)/2, (self.miny+self.maxy)/2, (self.minz+self.maxz)/2,
                    self.map, "the locker of the "+self.team+" team", 20, 900, 30, 7000, "locker explotion")

    def create_calculation(self):
        operator = ""
        g = random.randint(1, 4)
        if g == 1:
            operator = "+"
            n1 = random.randint(self.max_math_numbers*1,
                                self.max_math_numbers*5)
            n2 = random.randint(self.max_math_numbers*1,
                                self.max_math_numbers*5)
        elif g == 2:
            operator = "-"
            n1 = random.randint(self.max_math_numbers*1,
                                self.max_math_numbers*5)
            n2 = random.randint(self.max_math_numbers*1,
                                self.max_math_numbers*5)
            if n2 > n1:
                f = n1
                n1 = n2
                n2 = f
        elif g == 3:
            operator = "*"
            n1 = round(random.randint(
                self.max_math_numbers*0.1, self.max_math_numbers*1))
            n2 = round(random.randint(
                self.max_math_numbers*0.1, self.max_math_numbers*1))
        if g == 4:
            operator = "/"
            n2 = round(random.randint(
                self.max_math_numbers*0.1, self.max_math_numbers*1))
            n1 = round(random.randint(self.max_math_numbers *
                       0.1, self.max_math_numbers*1)*n2)

        return n1, n2, operator


object_mapdata = ""
map_loading = False


def copy_map(name, new_name):
    for a in allow_zones:
        if a.map == name:
            spawn_allow_zone(a.minx, a.maxx, a.miny, a.maxy,
                             a.minz, a.maxz, a.items, new_name)
    for a in walls:
        if a.map == name and a.id == 0:
            spawn_wall(a.minx, a.maxx, a.miny, a.maxy, a.minz,
                       a.maxz, a.tile, a.strength, a.id, new_name)
    for a in platforms:
        if a.map == name and a.id == 0:
            spawn_platform(a.minx, a.maxx, a.miny, a.maxy,
                           a.minz, a.maxz, a.tile, a.id, new_name)

    for a in zones:
        if a.map == name and a.id == 0:
            spawn_zone(a.minx, a.maxx, a.miny, a.maxy,
                       a.minz, a.maxz, a.text, a.id, new_name)
    for a in regions:
        if a.map == name:
            spawn_region(a.minx, a.maxx, a.miny, a.maxy,
                         a.minz, a.maxz, a.text, a.id, new_name)

    spawn_list = []
    for o in objects:
        a = objects[o]
        if a.map == name:
            spawn_list.append(a)
    global map_loading
    map_loading = True
    global object_mapdata
    object_mapdata = ""
    for a in spawn_list:
        spawn_object(a.minx, a.maxx, a.miny, a.maxy, a.minz,
                     a.maxz, a.name, a.dir, new_name, False)
    map_loading = False
    for c in v.clients:
        if c.lobby == False and c.data["map"] == name:
            c.send(object_mapdata)


def reset_map(name):
    global loot_outs
    global allow_zones
    global objects_x
    list = []
    for _ in range(60):
        row = [[] for _ in range(60)]
        list.append(row)

    for l in range(0, 60):
        for m in range(0, 60):
            for b in objects_x[l][m]:
                if b.map != name:
                    list[l][m].append(b)
    objects_x = list

    for _ in range(60):
        row = [[] for _ in range(60)]
        objects_x.append(row)

    global objects
    global regions
    global walls
    global platforms
    global respawn_zones
    global spawn_points
    global zones
    global platforms_x
    list = []
    for _ in range(60):
        row = [[] for _ in range(60)]
        list.append(row)

    for l in range(0, 60):
        for m in range(0, 60):
            for b in platforms_x[l][m]:
                if b.map != name:
                    list[l][m].append(b)
    platforms_x = list

    global walls_x
    list = []
    for _ in range(60):
        row = [[] for _ in range(60)]
        list.append(row)

    for l in range(0, 60):
        for m in range(0, 60):
            for b in walls_x[l][m]:
                if b.map != name:
                    list[l][m].append(b)
    walls_x = list

    global alarm_vehicles
    global corpsess
    new_objects = {}
    for a in objects:
        if objects[a].map != name:
            new_objects[a] = objects[a]
    objects = new_objects

    new_platforms = []
    for p in platforms:
        if p.map != name:
            new_platforms.append(p)

    platforms = new_platforms
    new_allow_zones = []
    for p in allow_zones:
        if p.map != name:
            new_allow_zones.append(p)
    allow_zones = new_allow_zones
    new_loot_outs = []
    for p in loot_outs:
        if p.map != name:
            new_loot_outs.append(p)
    loot_outs = new_loot_outs

    global alarm_vehicles
    new_vehicles = []
    for p in alarm_vehicles:
        if p.map != name:
            new_vehicles.append(p)
    alarm_vehicles = new_vehicles


    global corpses
    new_corpses = []
    for p in corpses:
        if p.map != name:
            new_corpses.append(p)
    corpses = new_corpses

    global examining_objects
    new_examining_objects = []
    for p in examining_objects:
        if p.map != name:
            new_examining_objects.append(p)
    examining_objects = new_examining_objects

    global destroying_objects
    new_destroying_objects = []
    for p in destroying_objects:
        if p.map != name:
            new_destroying_objects.append(p)

    destroying_objects = new_destroying_objects
    global falling_objects
    new_falling_objects = []
    for p in falling_objects:
        if p.map != name:
            new_falling_objects.append(p)

    falling_objects = new_falling_objects

    global zones
    new_zones = []
    for p in zones:
        if p.map != name:
            new_zones.append(p)

    zones = new_zones
    global respawn_zones
    new_respawn_zones = []
    for p in respawn_zones:
        if p.map != name:
            new_respawn_zones.append(p)

    respawn_zones = new_respawn_zones

    global spawn_points
    new_spawn_points = []
    for p in spawn_points:
        if p.map != name:
            new_spawn_points.append(p)

    spawn_points = new_spawn_points
    global walls
    new_walls = []
    for p in walls:
        if p.map != name:
            new_walls.append(p)

    walls = new_walls
    global regions
    new_regions = []
    for p in regions:
        if p.map != name:
            new_regions.append(p)

    regions = new_regions


def load_map(name, data=""):
    global map_loading
    map_loading = True
    global object_mapdata
    object_mapdata = ""
    map_lockers = {}
    for o in objects:
        if hasattr(objects[o], "team") and objects[o].actif == True and objects[o].map == name or objects[o].name == "barricade" and objects[o].actif == True and objects[o].map == name:
            map_lockers[str(o)] = objects[o]
    reset_map(name)
    data += "\n end"
    lines = data.split("\n")
    for l in lines:
        parsed = l.split(" ")
        if parsed[0] == "platform" and len(parsed) > 7:
            try:
                spawn_platform(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(
                    parsed[4]), int(parsed[5]), int(parsed[6]), parsed[7], 0, name)
            except:
                pass
        elif parsed[0] == "object" and len(parsed) > 8:
            try:
                spawn_object(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(
                    parsed[4]), int(parsed[5]), int(parsed[6]), parsed[7], int(parsed[8]), name)
            except:
                pass
        elif parsed[0] == "wall" and len(parsed) > 8:
            try:
                spawn_wall(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(parsed[4]), int(
                    parsed[5]), int(parsed[6]), parsed[7], int(parsed[8]), 0, name)
            except:
                pass
        elif parsed[0] == "wall" and len(parsed) > 7:
            try:
                spawn_wall(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(
                    parsed[4]), int(parsed[5]), int(parsed[6]), parsed[7], 0, 0, name)
            except:
                pass
        elif parsed[0] == "spawn_point" and len(parsed) > 4:
            try:
                spawn_spawn_point(int(parsed[1]), int(
                    parsed[2]), int(parsed[3]), int(parsed[4]), name)
            except Exception as e:
                error_message = ''.join(
                    traceback.format_exception(type(e), e, e.__traceback__))
                print("error: "+error_message)

        elif parsed[0] == "staircase" and len(parsed) > 9:
            try:
                spawn_staircase(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(parsed[4]), int(
                    parsed[5]), int(parsed[6]), parsed[7], parsed[8], int(parsed[9]), name)
            except:
                pass
        elif parsed[0] == "zone" and len(parsed) > 7:
            try:
                spawn_zone(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(parsed[4]), int(parsed[5]), int(parsed[6]), l.replace(
                    "zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" ", ""), 0, name)
            except:
                pass
        elif parsed[0] == "region" and len(parsed) > 7:
            try:
                spawn_region(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(parsed[4]), int(parsed[5]), int(parsed[6]), l.replace(
                    "region "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" ", ""), 0, name)
            except:
                pass
        elif parsed[0]=="loot_out" and len(parsed)>1:
         try:
          data=l.replace(parsed[0]+" ","")
          loot={}
          for d in data.split(":"):
           amount=1
           words=d.split(";")
           loot[words[0]]=amount
           if len(words)>1:
            amount=words[1]
            loot[words[0]]=amount
          object=loot_out(name,loot)
         except:
          pass
        elif parsed[0] == "allow_zone" and len(parsed) > 7:
            try:
                data = l.replace("allow_zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(
                    parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" ", "")
                itemlist = data.split(":")
                items = {}
                for i in itemlist:
                    words = i.split(";")
                    items[words[0]] = int(words[1])
                spawn_allow_zone(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(
                    parsed[4]), int(parsed[5]), int(parsed[6]), items, name)
            except:
                pass
        elif parsed[0] == "respawn_zone" and len(parsed) > 11:
            try:
                spawn_respawn_zone(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(parsed[4]), int(parsed[5]), int(
                    parsed[6]), int(parsed[7]), int(parsed[8]), int(parsed[9]), int(parsed[10]), int(parsed[11]), int(parsed[12]), name)
            except:
                pass
        elif parsed[0] == "quest_item" and len(parsed) > 6:
            try:
                spawn_quest_item(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(
                    parsed[4]), int(parsed[5]), int(parsed[6]), parsed[7], parsed[8], name)
            except:
                pass
        elif parsed[0] == "quest_zone" and len(parsed) > 8:
            try:
                spawn_quest_zone(int(parsed[1]), int(parsed[2]), int(parsed[3]), int(parsed[4]), int(parsed[5]), int(parsed[6]), parsed[7], int(parsed[8]), l.replace(
                    "quest_zone "+str(parsed[1])+" "+str(parsed[2])+" "+str(parsed[3])+" "+str(parsed[4])+" "+str(parsed[5])+" "+str(parsed[6])+" "+str(parsed[7])+" "+str(parsed[8])+" ", ""), name)
            except:
                pass

    for o in objects:
        if not hasattr(objects[o], "team") and objects[o].map==name:
            objects[o].loot = objects[o].create_loot()

    for m in map_lockers:
        o = map_lockers[m]
        objects[m] = o
        o.load_mapdata()
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
                objects_x[l][m].append(o)

    for c in v.clients:
        if c.lobby == False and c.data["map"] == name:
            c.send(object_mapdata)
    map_loading = False


def calculate_walls(x1, y1, z1, x2, y2, z2, map, forbidid=-1, strength=7500):
    final = strength
    x=round(x1)
    y=round(y1)
    z=round(z1)
    x2=round(x2)
    y2=round(y2)
    z2=round(z2)
    while (x, y, z) != (x2, y2, z2):
        if x != x2:
            x += 1 if x2 > x1 else -1
        if y != y2:
            y += 1 if y2 > y1 else -1
        if z != z2:
            z += 1 if z2 > z1 else -1
        if get_platform(x, y, z, map) == "wall":
            index = get_walls_index(x, y, z, map)
            if index > -1:
                if walls[index].id != forbidid:
                    final -= walls[index].strength
    return final


def map_exsist(name):
    script_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(script_path, 'maps')

    for filename in os.listdir(folder_path):
        if filename == name+".txt":
            return True
    return False


def get_mmmm(p):
    minx, maxx, miny, maxy = p.minx, p.maxx, p.miny, p.maxy
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
    return minx, maxx, miny, maxy
