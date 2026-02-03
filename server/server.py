import time
import client
import explosives
import os
import multiprocessing
import shipment
import trap
import zlib
import match
import traceback
import pyperclip as pc
import cProfile
import pstats
import io
import datetime
import subprocess
import sys
import math
import admin_message
import time
import select
import sd
import rotation
import v
v.get()
import socket
import timer
import weapons
import map
from threading import Thread
import scanner
import misk
import teams
import event
import random
import quests
script_dir = os.path.dirname(os.path.abspath(__file__))

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


def send_all(message, map=""):
    v.send_packet_to_clients(message, v.clients, map)


def get_current_time():
    nu = datetime.datetime.now()
    tijd = nu.strftime("%H:%M:%S")
    return tijd


def get_current_date():
    nu = datetime.datetime.now()
    datum = nu.strftime("%Y %m %d")

    return datum


def get_3d_distance(x1, y1, z1, x2, y2, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx*dx + dy*dy + dz*dz)


os.chdir(script_dir)


def get_players_index(name):
    for p in v.clients:
        if p.data["name"].lower() == name.lower():
            return v.clients.index(p)
    return -1


def send_all(message, map=""):
    v.send_packet_to_clients(message, v.clients, map)


class server():
    def __init__(self):
        self.profiler = cProfile.Profile()
        self.profiler.enable()
        admin_thread = Thread(target=self.get_all_player_data)
        admin_thread.start()
        self.current_time = get_current_time()
        self.newtimetimer = timer.timer()
        self.objectrespawntimer = timer.timer()
        self.timeouttimer = timer.timer()
        self.savetimer = timer.timer()
        self.freezetimer = timer.timer()
        self.timetimer = timer.timer()
        self.load()
        self.run()

    def load(self):
        script_path = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(script_path, 'object_presets')
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                misk.load_object_preset(content)

        folder_path = os.path.join(script_path, 'maps')
        for filename in os.listdir(folder_path):
            f = open("maps/"+filename, "r")
            data = f.readlines()
            map.load_map(filename.replace(".txt", ""), "".join(data))
            f.close()
        v.banlist = sd.get("banlist", "data.dat", {})
        announcements = sd.get("announcements", "data.dat", [])
        for a in announcements:
            an = misk.announcement("", "")
            an.load(announcements[a])
            v.announcements.append(an)
        admin_messages = sd.get("admin_messages", "data.dat", [])
        for a in admin_messages:
            an = admin_message.admin_message("", "", "", "")
            an.load(admin_messages[a])
            v.admin_messages.append(an)
        events = sd.get("events", "data.dat", [])
        for a in events:
            an = event.event("", 0)
            an.load(events[a])
            an.get_max_score()
            v.events.append(an)
        ranked_events = sd.get("ranked_events", "data.dat", [])
        for a in ranked_events:
            an = event.ranked_event("")
            an.load(ranked_events[a])
            v.ranked_events.append(an)
        new_teams = sd.get("teams", "teams.dat", [])
        for a in new_teams:
            t = teams.team(a)
            t.load(new_teams[a])
            v.teams.append(t)
        new_metal_fortresss = sd.get(
            "metal_fortresss", "metal_fortresss.dat", [])
        for a in new_metal_fortresss:
            t = map.metal_fortress(new_metal_fortresss[a]["minx"], new_metal_fortresss[a]["maxx"], new_metal_fortresss[a]["miny"], new_metal_fortresss[a]
                                   ["maxy"], new_metal_fortresss[a]["minz"], new_metal_fortresss[a]["maxz"], new_metal_fortresss[a]["map"], new_metal_fortresss[a]["team"])
            t.load(new_metal_fortresss[a])
            map.objects[str(t.id)] = t
        new_lockers = sd.get("lockers", "lockers.dat", [])
        for a in new_lockers:
            t = map.locker(new_lockers[a]["minx"], new_lockers[a]["maxx"], new_lockers[a]["miny"], new_lockers[a]
                           ["maxy"], new_lockers[a]["minz"], new_lockers[a]["maxz"], new_lockers[a]["map"], new_lockers[a]["team"])
            t.load(new_lockers[a])
            map.objects[str(t.id)] = t
        new_barricades = sd.get("barricades", "barricades.dat", [])
        for a in new_barricades:
            t = map.object(new_barricades[a]["minx"], new_barricades[a]["maxx"], new_barricades[a]["miny"], new_barricades[a]
                           ["maxy"], new_barricades[a]["minz"], new_barricades[a]["maxz"], "barricade", 1, new_barricades[a]["map"], 0, False)
            t.load(new_barricades[a])
            map.objects[str(t.id)] = t
        new_traps = sd.get("traps", "traps.dat", [])
        for a in new_traps:
            t = trap.trap(new_traps[a]["minx"], new_traps[a]["maxx"], new_traps[a]["miny"], new_traps[a]["maxy"], new_traps[a]["minz"],
                          new_traps[a]["maxz"], new_traps[a]["map"], new_traps[a]["name"], new_traps[a]["owner"], new_traps[a]["team"])
            v.traps.append(t)
        f = open("release.txt", "r")
        v.release = f.read()
        f.close()
        if v.release != "d" and v.release != "b" and v.release != "r":
            v.release = "d"
        text = ""
        if v.release == "r":
            text = "public release"
        if v.release == "b":
            text = "beta"
        if v.release == "d":
            text = "developer build"
        print("running the server in"+text)
        try:
            if os.path.isfile("server.bin") and os.path.isfile("updated_server.bin"):
                os.remove("server.bin")
                os.rename("updated_server.bin", "server.bin")
        except:
            pass
        if v.release == "r":
            v.s.bind(("", 3030))
        else:
            v.s.bind(("", 3031))
        v.s.listen()
        index = event.get_ranked_events_index("last_man_standing")
        if index == -1:
           v.ranked_events.append(event.ranked_event("last_man_standing"))


    def report_traceback(self, e):
                error_message = ''.join(
                    traceback.format_exception(type(e), e, e.__traceback__))
                with open("error_log.log", "w") as f:
                 f.write(get_current_date()+" "+get_current_time()+"\n"+error_message)

    def add_client(self, conn, addr):
        c = client.client(conn, addr)
        v.clients.append(c)

    def save_server(self):
        for c in v.clients:
            c.store_data()
        announcements = {}
        for an in v.announcements:
            announcements[str(an.id)] = an.save()
        sd.save("announcements", announcements, "data.dat")
        print(str(v.teams))
        new_teams = {}
        for an in v.teams:
            new_teams[an.name] = an.save()
        sd.save("teams", new_teams, "teams.dat")

        new_metal_fortresss = {}
        new_lockers = {}
        new_barricades = {}
        for o in map.objects:
            an = map.objects[o]
            if an.name == "locker":
                new_lockers[an.id] = an.save()
            if an.name == "metal_fortress":
                new_metal_fortresss[an.id] = an.save()
            if an.name == "barricade":
                new_barricades[an.id] = an.save()
        sd.save("barricades", new_barricades, "barricades.dat")
        sd.save("lockers", new_lockers, "lockers.dat")
        sd.save("metal_fortresss", new_metal_fortresss, "metal_fortresss.dat")

        new_traps = {}
        for t in v.traps:
            new_traps[str(t.id)] = t.save()
        sd.save("traps", new_traps, "traps.dat")

        admin_messages = {}
        for an in v.admin_messages:
            admin_messages[str(an.id)] = an.save()
        sd.save("admin_messages", admin_messages, "data.dat")
        events = {}
        for an in v.events:
            events[str(an.id)] = an.save()
        sd.save("events", events, "data.dat")
        ranked_events = {}
        for an in v.ranked_events:
            ranked_events[str(an.id)] = an.save()
        sd.save("ranked_events", ranked_events, "data.dat")

        sd.save("banlist", v.banlist, "data.dat")

    def get_all_player_data(self):
        script_pad = os.path.dirname(os.path.abspath(__file__))
        players_map_pad = os.path.join(script_pad, 'players')
        files = os.listdir(players_map_pad)
        for f in files:
            f = f.replace(".plr", "")
            data = sd.get("data", f+".plr", {}, "players")
            try:
                if data["org_mutetime"] > 0:
                    v.mute_players.append(f)
                if data["admin"] == 1:
                    v.admin_list[f] = "admin"
                elif data["builder"] == 1:
                    v.admin_list[f] = "builder"
                if data["moderator"] == 1:
                    v.admin_list[f] = "moderator"
            except:
                continue

    def check_connections(self):
     try:
        readable, _, _ = select.select([v.s], [], [], 0)
        if v.s in readable:
            conn, addr = v.s.accept()
            ip = addr[0]
            ip_count = sum(1 for c in v.clients if c.addr[0] == ip)
            if ip_count < 5:
                self.add_client(conn, addr)
     except:
      pass

    def run(self):
        while 1:
            try:
                time.sleep(0.001)
                self.check_connections()
                self.updateloop()
                if v.restarting == True and v.restarttimer.elapsed() > 15000:
                 self.save_server()
                 send_all("restart")
                 v.send_packetloop()
                 break
                v.send_packetloop()

            except Exception as e:
                     self.report_traceback(e)
        print("exiting")
        self.profiler.disable()
        result_buffer = io.StringIO()
        stats = pstats.Stats(self.profiler, stream=result_buffer)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.print_stats()
        profile_results = result_buffer.getvalue()
        if profile_results.strip():
            pc.copy(profile_results)
        else:
            print("No profiling data collected.")
            v.s.close()
            script_path = sys.argv[0]
            is_exe = os.path.splitext(script_path)[1].lower() == '.bin'
            if is_exe:
                if os.path.isfile("updated_server.bin"):
                    subprocess.Popen(["updated_server.bin"])
                else:
                    subprocess.Popen([script_path])
            else:
                subprocess.Popen([sys.bincutable, script_path])


    def updateloop(self):
        if self.objectrespawntimer.elapsed() >= 300000:
            self.objectrespawntimer.restart()
            for p in map.objects:
                o = map.objects[p]
                if o.actif == False:
                    f = map.get_things_in_area(
                        o.ominx, o.omaxx, o.ominy, o.omaxy, o.ominz, o.omaxz, o.map, False, True)
                    if f.replace("|", "") == "":
                        o.__init__(o.ominx, o.omaxx, o.ominy, o.omaxy,
                                   o.ominz, o.omaxz, o.name, o.dir, o.map, o.id)
                if o.name != "locker" and o.remove_after_examining == False:
                    o.loot = o.create_loot()


        if self.newtimetimer.elapsed() > 990:
            self.newtimetimer.restart()
            map.metal_fortressloop()
            for t in v.teams:
                has_forttress = map.has_metal_fortress(t.name)
                if has_forttress and t.data["max_members"] == 6:
                    t.data["max_members"] += 1
                elif has_forttress == False and t.data["max_members"] == 7:
                    t.data["max_members"] -= 1
                    if len(t.members) > 6:
                        if t.data["leader"] != t.members[6]:
                            t.send(
                                "speak "+t.members[6]+" has been removed from the team due to the destruction of the fortress.")
                            del t.members[6]
                        else:
                            t.send(
                                "speak "+t.members[0]+" has been removed from the team due to the destruction of the fortress.")
                            del t.members[0]

                if len(t.members) <= 0:
                    send_all("the team "+t.name +
                             " has no members and has been removed.")
                    t.remove()
                    v.teams.remove(t)
                    break

            weekend = v.is_weekend()
            if v.weekend != weekend:
                v.weekend = weekend
                if v.weekend == False:
                    index = event.get_ranked_events_index("last_man_standing")
                    if index > -1:
                        sorted_keys = list(sorted(
                            v.ranked_events[index].scores, key=lambda x: v.ranked_events[index].scores[x], reverse=True))
                        if len(sorted_keys) > 0:
                            winner = sorted_keys[0]
                            pindex = get_players_index(winner)
                            if pindex > -1:
                                v.clients[pindex].give_account(
                                    "diamond_chest", 1)
                                v.clients[pindex].send(
                                    "add_buffer_item misc Congratulations, you are the winner of this weekend's ranked mode match. You earned 1 diamond chest.")
                            else:
                                try:
                                    data = sd.get(
                                        "data", winner+".plr", {}, "players")
                                    data["chests"]["diamond"] += 1
                                    sd.save("data", data, winner +
                                            ".plr", "players")
                                except:
                                    pass
                    send_all("speak the last week's last man standing has ended")

                    for c in v.clients:
                        c.store_data()
                    script_path = os.path.dirname(os.path.abspath(__file__))
                    folder_path = os.path.join(script_path, 'players')
                    for filename in os.listdir(folder_path):
                        try:
                            data = sd.get("data", filename, {}, "players")
                            data["ranked_points"] = 0
                            sd.save("data", data, filename, "players")
                        except:
                            pass
                    for c in v.clients:
                        c.get_data()
                    index = event.get_ranked_events_index("last_man_standing")
                    if index > -1:
                        v.ranked_events[index].__init__(
                            v.ranked_events[index].name)
                    else:
                        v.ranked_events.append(event.ranked_event("last_man_standing"))
                    send_all("speak ranked mode has started")
            match.matchloop()
            self.current_time = get_current_time()
        if self.current_time == "12:00:00" and self.timetimer.elapsed() > 1100:
            self.timetimer.restart()
            event.start_event(v.event_types[random.randint(
                0, len(v.event_types)-1)], 86400000)
        event.eventloop()
        trap.activated_traploop()
        shipment.shipmentloop()
        [item.update() for item in scanner.scanners]
        [item.run() for item in v.bullets]
        [item.run() for item in v.clients]
        [item.loop() for item in v.heals]
        [item.fall()

         for item in v.bodyfalls if item.falltimer.elapsed() > item.falltime]
        [item.stop() for item in v.events if item.timer.elapsed() > item.max_time]
        explosives.explosivesloop()
        map.objectloop()
        if v.freeze == True and self.freezetimer.elapsed() > 500:
            self.freezetimer.restart()
            send_all("stun 10000")
        if self.savetimer.elapsed() > 900000:
            self.savetimer.restart()
            self.save_server()

        if self.timeouttimer.elapsed() > 2000:
            self.timeouttimer.restart()
            names = []
            text = ""
            for p in v.clients:
                if p.lobby == False and p.data["death"] == False:
                    names.append(p.data["name"])
                    text = text+"move_player " + \
                        p.data["name"]+" "+str(p.data["x"])+" " + \
                        str(p.data["y"])+" "+str(p.data["z"])+"|n|"
                    if p.data["shooting"] == 0:
                        text = text+"set_shooting "+p.data["name"]+" 0 1|n|"
            send_all("players_check "+"\n".join(names)+"|n|"+text)



s=server()
