import weapon_attachment
import admin_message
import v
import misk
import shipment
import timer
import explosives
import match
import quests
import rotation
import map
import teams
import event
import math
import random
import sd
import os
import re
import skills
import weapons
import math

import datetime


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


misk.get()
v.get()


def read_file_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return lines
    except:
        pass


def get_players_index(name):
    for p in v.clients:
        if p.data["name"].lower() == name.lower():
            return v.clients.index(p)
    return -1


def send_all(message):
 v.send_packet_to_clients(message,v.clients, "")



def server_menu_answer(c, name, option):
    c.sended = False
    if name == "tool_box_menu":
        upgrades= c.drawn_weapon.get_upgrades()
        if option not in upgrades:
         c.send("error")
         return
        if option == "jam clear this weapon":
            c.drawn_weapon.jammed = False
            c.drawn_weapon.loaded_ammo-=1
            send_all(r"player_sound "+c.data["name"]+" sounds\\"+c.drawn_weapon.sort+"jamclear.ogg 0")
            stun_times={
                "assault_rifle": 5000,
                "machine_gun": 5000,
                "marksman_rifle": 5000,

                "pistol": 4300,
                "revolver": 4300,
                "shotgun": 3800,
                "sniper_rifle": 6300,
                "sub_machine_gun": 4400
            }
                                        
            c.send("stun "+str(stun_times[c.drawn_weapon.sort]))
        else:
            attachment=weapon_attachment.get_weapon_attachment_by_name(option.split(":")[0])
            if attachment.name in c.drawn_weapon.modifications:
                c.send("speak you already have attached this attachment on this weapon")
                return
            if len(c.drawn_weapon.modifications)>=2:
                c.send("speak this gun has already the maximum of attachments")
                return
            if attachment.has_player_enough_resources(c.inventory,c.drawn_weapon):
                c.drawn_weapon.modifications.append(attachment.name)
                attachment.remove_resources(c.inventory,c.drawn_weapon)
                inventory=c.inventory
                c.inventory={}
                for i in inventory:
                 if inventory[i] > 0:
                  c.inventory[i]=inventory[i]
                attachment.attach_to_weapon(c.drawn_weapon)
                send_all(r"player_sound "+c.data["name"]+" sounds\\"+attachment.name+"attach.ogg 0|n|set_players_silencer "+c.data["name"]+" "+str(c.has_silencer(c.data["weapon"])))
            else:
                c.send("speak you don't have enough resources for this attachment")
                
    elif name == "phone_menu":
        if option == "place a team note":
            c.send("input type_the_text_of_the_team_note ")

        if option == "remove a team note":
            tindex = teams.get_teams_index(teams.get_team(c.data["name"]))
            if tindex > -1:
                options = []
                for n in v.teams[tindex].data["notes"]:
                    if v.teams[tindex].data["notes"][n]["owner"] == c.data["name"] or v.teams[tindex].data["leader"] == c.data["name"]:
                        options.append(n)
                if len(options) > 0:
                    c.send(
                        "server_menu which_note_do_you_want_to_remove? "+"\n".join(options))
                else:
                    c.send("speak you don't have any notes")

        if option == "view team notes":
            tindex = teams.get_teams_index(teams.get_team(c.data["name"]))
            if tindex > -1:
                options = []
                for n in v.teams[tindex].data["notes"]:
                    options.append(n+": sent by "+v.teams[tindex].data["notes"][n]["owner"]+" on "+str(
                        v.teams[tindex].data["notes"][n]["date"]))
                if len(options) > 0:
                    c.send(
                        "server_menu view_here_the_notes_placed_by_your_team "+"\n".join(options))
                else:
                    c.send("speak your team doesn't have any notes")

        if option == "alarm for the metal fortress switch":
            for f in map.objects:
                o = map.objects[f]
                if o.name == "metal_fortress" and o.team == teams.get_team(c.data["name"]):
                    if o.data["alarm"] == True:
                        o.data["alarm"] = False
                        o.alarm_players = {}
                        c.send("speak alarm turned off.")
                    else:
                        for p in v.clients:
                            if map.get_metal_fortress(p.data["x"], p.data["y"], p.data["z"], p.data["map"]) == o.id and p.lobby == False and p.data["death"] == False:
                                c.send(
                                    "speak you can't turn the alarm on when someone is inside the fortress.")
                                return
                        o.data["alarm"] = True
                        c.send("speak alarm turned on.")

        if option == "my team's traps":
            options = []
            my_team = teams.get_team(c.data["name"])
            for t in v.traps:
                if t.team == my_team:
                    options.append("a "+t.name+" at "+str(round((t.minx+t.maxx)/2))+", "+str(round(
                        (t.miny+t.maxy)/2))+", "+str(round((t.minz+t.maxz)/2))+". Placed by "+t.owner)
            if len(options) > 0:
                c.send("server_menu view_your_team's_traps_here " +
                       "\n".join(options))
            else:
                c.send("speak you don't have any traps")

        if option=="view my shipment status":
            for s in v.shipments:
                if s.team==teams.get_team(c.data["name"]):
                    if s.dropping==True:
                        c.send("speak your shipment is dropping at the moment.")
                    else:
                        c.send("speak your shipment will arrive in "+str(v.get_time_in_mm(s.arrivetime-s.arrivetimer.elapsed())))
                    return
            c.send("speak your team doesn't have an incomming shipment")
                    
        if option == "place an order":
            options = []
            for s in v.store_items:
                try:
                    shopping_amount = c.shopping_cart[s]
                except:
                    shopping_amount = 0
                options.append(s+". Grab "+str(v.store_items[s]["amount"])+" for "+str(
                    v.store_items[s]["price"])+" team tokens. You currently have selected "+str(shopping_amount)+" of this item")
            options.append("order the items")
            c.send(
                "server_menu Put_your_order_together._Click_on_order_to_order. "+"\n".join(options))

    if name == "which_note_do_you_want_to_remove?":
        tindex = teams.get_teams_index(teams.get_team(c.data["name"]))
        if tindex > -1:
            try:
                del v.teams[tindex].data["notes"][option]
                c.send("speak successfully removed")
            except:
                c.send(
                    "speak something wend wrong while deleting the team note. Please try again.")

    if name == "Put_your_order_together._Click_on_order_to_order.":
        if option == "order the items":
            for s in v.shipments:
                if s.team == teams.get_team(c.data["name"]):
                    c.send("speak there is already an order going to your fortress")
                    return
            for f in map.objects:
                o = map.objects[f]
                if o.name == "shipment" and o.destination_team == teams.get_team(c.data["name"]):
                    c.send("speak there is already a shipment on your fortress.")
                    return
            shopping_total = c.calculate_shopping_cart_total(v.store_items)
            if shopping_total <= 0:
                c.send("speak you haven't selected any item.")
                return
            tindex = teams.get_teams_index(teams.get_team(c.data["name"]))
            if tindex > -1:
                if shopping_total <= v.teams[tindex].data["tokens"]:
                    for s in c.shopping_cart:
                        c.shopping_cart[s] = c.shopping_cart[s] * \
                            v.store_items[s]["amount"]
                    shipment.spawn_shipment(teams.get_team(
                        c.data["name"]), c.shopping_cart)
                    v.teams[tindex].data["tokens"] -= shopping_total
                    send_all(r"player_sound " +
                             c.data["name"]+" sounds\\phonemsg.ogg 0")
                    c.send("speak transaction has been completed.")
                    c.shopping_cart = {}
                else:
                    c.send(
                        "speak your team doesn't have enough tokens to buy these items|n|last_server_menu")

        else:
            item = option.split(".")[0]
            maximum = 0
            tindex = teams.get_teams_index(teams.get_team(c.data["name"]))
            if tindex > -1:
                try:
                    maximum = math.floor(
                        v.teams[tindex].data["tokens"]/v.store_items[item]["price"])
                    if maximum > 99:
                        maximum = 99
                except:
                    pass
            options = []
            for i in range(0, maximum+1):
                options.append(str(i))
            if len(options) <= 1:
                c.send("speak you can't buy this item|n|last_server_menu")
                return
            c.send("server_menu how_many_"+item +
                   "'s_would_you_like_to_buy? "+"\n".join(options))

    if name[0:9] == "how_many_":
        item = name.replace("how_many_", "")
        item = item.replace("'s_would_you_like_to_buy?", "")
        c.shopping_cart[item] = int(option)

        c.send("delete_server_menu|n|delete_server_menu")
        server_menu_answer(c, "phone_menu", "place an order")
    if name == "table_menu":
        try:
            we = weapons.weapon(option)
            send_all(r"player_sound " +c.data["name"]+" sounds\\"+we.sort+"get.ogg 0")
            c.add_weapon(option)
            the_weapon=c.get_weapon_in_list(option)
            the_weapon.loaded_ammo=the_weapon.max_ammo
            c.give(we.needed_ammo, we.max_ammo)
            c.send("get_weapons "+"||".join(c.data["weapons"]))
            index = match.get_matches_index(c.match_id)
            if index > -1:
                v.matches[index].weapons.remove(option)
                v.matches[index].send(
                    "add_buffer_item misc "+c.data["name"]+" took the "+option)
                if len(v.matches[index].weapons) == 0:
                    map.reset_map(c.data["map"])
                    v.matches[index].choose_map()

                    v.matches[index].status = "playing"
                    return

            mindex = v.matches[index].ranked_players.index(c)+1
            if mindex > len(v.matches[index].ranked_players)-1:
                mindex = 0
            v.matches[index].ranked_players[mindex].send(
                "table_menu "+"\n".join(v.matches[index].weapons))
        except:
            pass
    if name == "type_the_code_you_want_to_explode" and option != "":
        i = 0
        for r in v.RCEs:
            if r.code == option and get_3d_distance(r.x, r.y, r.z, c.data["x"], c.data["y"], c.data["z"]) <= 75 and r.map == c.data["map"]:
                i += 1
                send_all("play_sound RCEactivate.ogg "+str(r.x) +
                         " "+str(r.y)+" "+str(r.z)+" 0 0")
                r.explodetimer.restart()
                r.alert = True
        if i == 0:
            c.send("speak no RCEs found with that code in a range of 75 meter")
        else:
            c.send("speak "+str(i)+" RCE's detenated")
    if name == "type_the_code_for_detenating_this_R_C_E" and option != "":
        c.send("stun 8000")
        v.RCEs.append(explosives.RCE(
            c.data["x"], c.data["y"], c.data["z"], c.data["map"], c.data["name"], option))
        c.give("R_C_E", -1)
        send_all(r"player_sound "+c.data["name"]+" sounds\\RCEplace.ogg 0")
        return

    elif name == "lobby_menu._Select_an_item" and c.lobby == True:
        if option == "teams":
            options = ["your team", "create a team", "send an request for a team", "view all teams",
                       "", "view all teams that have a locker", "view all teams that have a metal fortress"]
            for t in v.teams:
                if c.data["name"] in t.data["invites"]:
                    options.append(
                        t.name+" has send you an invite to join their team. Press here to accept or decline it.")
            c.send("server_menu team_menu._Select_an_option "+"\n".join(options))

        if option == "story and quests":
            options = []
            for q in c.quests:
                if c.quests[q] == -1:
                    options.append("locked: "+q)
                elif c.quests[q] == 1:
                    options.append("completed: "+q)
                else:
                    options.append(q)
            c.send("server_menu select_a_quest "+"\n".join(options))

        if option == "view events":
            options = []
            for e in v.events:
                options.append(e.name)
            if len(options) > 0:
                c.send("server_menu select_an_event "+"\n".join(options))
            else:
                c.send("speak there are no active events.|n|last_server_menu")
        if option == "my account":
            options = ["view my account inventory", "open chests"]
            c.send("server_menu select_an_option_for_your_account " +
                   "\n".join(options))

        if option == "manage skills":
            options = ["manage skill set", "view unlocked skills"]
            c.send("server_menu select_an_option_for_your_skills " +
                   "\n".join(options))
        if option == "visit the event shop":
            options = []
            for p in v.prices:
                options.append(p+" for "+str(v.prices[p])+" event points. You can currently buy "+str(
                    math.floor(c.data["event_points"]/v.prices[p])))
            c.send("server_menu select_an_item_to_buy_in_the_event_shop._You_have_" +
                   str(c.data["event_points"])+"_event_points. "+"\n".join(options))
        if option == "ranked mode":
            c.send("speak ranked mode is disabled|n|last_server_menu")
            return
            options = ["search for a match", "view your rank", "view rewards track",
                       "view leader board", "find a friendly match", "create a friendly match"]
            c.send("server_menu select_an_option_for_ranked_mode " +
                   "\n".join(options))
        if option == "enter the map":
            if c.match_id > -1 and c.data["map"] == "main":
                c.send("speak can't enter the map while you are in a match.")
                return

            if map.map_exsist(c.data["map"]) == False and c.match_id <= -1:
                c.data["map"] = "main"

            if c.data["level"]<10 and c.starter_weapons==c.data["weapons"] and c.inventory_is_starter_inventory:
             options=["main","training_camp"]
             c.send("server_menu which_map_do_you_want_to_spawn_at? "+"\n".join(options))
             return

            c.data["chosen_map"]="main"
            c.enter_map()
    if name=="which_map_do_you_want_to_spawn_at?":
     c.data["chosen_map"]=option
     c.data["map"]=option
     c.spawn()
     c.enter_map()


    if name[0:39] == "select_an_item_to_buy_in_the_event_shop":
        p = option.split(" for ")
        option = p[0]
        if c.data["event_points"] < v.prices[option]:
            c.send("speak you don't have enough event points to buy this item.")
        else:
            c.data["event_points"] -= v.prices[option]
            if " chest" in option:
                option = option.replace(" chest", "")
                c.data["chests"][option] += 1
                c.send("play_sound chestget.ogg 0 0 0 1 0")
            c.send(
                "speak purchase has been done.|n|play_sound eventshopbuy.ogg 0 0 0 1 0")
        c.send("last_server_menu")

    if name == "select_an_option_for_your_account":
        if option == "view my account inventory":
            options = list(c.account_inventory.keys())
            for o in options:
                options[options.index(o)] = o+": you have " + \
                    str(c.account_inventory[o])
            if len(options) == 0:
                c.send("speak you have no items on your account|n|last_server_menu")
            else:
                c.send(
                    "server_menu select_an_item_from_your_account_inventory "+"\n".join(options))

        if option == "open chests":
            options = []
            for p in c.data["chests"]:
                if c.data["chests"][p] > 0:
                    options.append("a "+p+" chest. You currently have " +
                                   str(c.data["chests"][p])+" on your account")
            if len(options) > 0:
                c.send("server_menu choose_the_chest_you_want_to_open " +
                       "\n".join(options))
            else:
                c.send(
                    "speak you don't have any chests on your account.|n|last_server_menu")

    if name == "select_an_item_from_your_account_inventory":
        words = option.split(":")
        option = words[0]
        options = ["description: "+v.get_description(option), "use this item"]
        c.send("server_menu select_an_option_for_the_item_" +
               option+" "+"\n".join(options))

    if name[0:30] == "select_an_option_for_the_item_":
        item = name.replace("select_an_option_for_the_item_", "")
        if option == "use this item":
            if item == "mastery_potion":
                if c.is_potion_used(item) == True:
                    c.send(
                        "speak you are already using this potion|n|last_server_menu")
                    return
                else:
                    c.using_potions[item] = {
                        "max_time": 1800000,
                        "timer": timer.timer(),
                    }
                    c.give_account("mastery_potion", -1)
                    c.send(r"play_sound_dlg sounds\\potionuse.ogg 8000")
            elif item == "magical_reappearance":
                c.send("speak this item is temporary disabled")
                return
                if c.losing_loot == True:
                    c.losing_loot = False
                    c.send("speak you apply the magical reappearance. The next time you die you will keep your loot. If you wish to disable it, just use this item again. The effects of the magical reappearance will end after you died once")
                else:
                    c.losing_loot = True
                    c.send("speak you disable the "+item)
            elif item=="joker_skill_point":
             options=[]
             for s in c.skill_data:
              sk=skills.skill(s)
              if c.skill_data[s]["unlocked"] and c.skill_data[s]["level"]<sk.max_level:
               options.append(s)
             if len(options)<=0:
              c.send("speak you don't have any skill to use the joker skill points on|n|last_server_menu")
             else:
              c.send("server_menu select_the_skill_you_want_to_use_the_joker_skill_points_on "+"\n".join(options))

        else:
            c.send("last_server_menu")
    if name=="select_the_skill_you_want_to_use_the_joker_skill_points_on":
     if option in c.skill_data:
      c.send("input how_many_skill_points_do_you_want_to_invest_in_to_the_"+option.replace(" ","_")+"_skill? ")
    if name == "select_an_option_for_ranked_mode":
        if option == "view rewards track":
            options = []
            index = event.get_ranked_events_index("last_man_standing")
            if index == -1:
                c.send("speak ranked mode isn't active at the moment")
                return
            for i in v.ranked_events[index].rewards:
                options.append(str(v.ranked_events[index].rewards[i]["amount"])+" x "+v.ranked_events[index].rewards[i]
                               ["name"]+": requires "+str(v.ranked_events[index].rewards[i]["points"])+" ranking points")
            if len(options) > 0:
                c.send("server_menu view_here_the_rewards_track " +
                       "\n".join(options))
            else:
                c.send("speak this mode hasn't a rewards track|n|last_server_menu")
        if option == "create a friendly match":
            c.send(
                "input what_should_be_the_password_for_this_match_to_allow_players_to_join? ")
        if option == "find a friendly match":
            c.send("input type_the_password_of_the_match_you_would_like_to_join ")

        if option == "search for a match" and c.match_id == -1:
            if v.is_weekend() == False:
                c.send(
                    "speak you can only play ranked mode during the weekends|n|last_server_menu")
                return
            if c.losing_loot == False:
                c.send(
                    "speak can't go in a match with a magical_reappearance in use|n|last_server_menu")
                return
            m = match.match("last_man_standing", c.data["name"])
            v.matches.append(m)

            c.send("start_match")
        if option == "view leader board":
            index = event.get_ranked_events_index("last_man_standing")
            if index == -1:
                c.send("speak ranked mode isn't active at the moment")
                return
            options = []
            sorted_keys = sorted(
                v.ranked_events[index].scores, key=lambda x: v.ranked_events[index].scores[x], reverse=True)
            i = 1
            for p in sorted_keys:
                options.append(
                    str(i)+": "+p+" with "+str(v.ranked_events[index].scores[p])+" ranking points.")
                i += 1
            if len(options) > 0:
                c.send("server_menu view_here_the_leader_board " +
                       "\n".join(options))
            else:
                c.send("speak there are no scores|n|last_server_menu")
        if option == "view your rank":
            c.send("speak you have currently a rank of " +
                   str(round(c.data["ranked_points"]))+" ranking points|n|last_server_menu")
    if name == "view_here_the_rewards_track":
        words = option.split(" ")
        amount = int(words[len(words)-3])
        if c.data["ranked_points"] < amount:
            c.send(
                "speak you don't have enough ranking points to claim this reward|n|last_server_menu")
            return
        index = event.get_ranked_events_index("last_man_standing")
        if index == -1:
            return
        for i in v.ranked_events[index].rewards:
            if v.ranked_events[index].rewards[i]["points"] == amount:
                if c.data["name"] in v.ranked_events[index].rewards[i]["players"]:
                    c.send(
                        "speak you already claimed this reward.|n|last_server_menu")
                    return

                v.ranked_events[index].rewards[i]["players"].append(
                    c.data["name"])
                c.give_account(
                    v.ranked_events[index].rewards[i]["name"], v.ranked_events[index].rewards[i]["amount"])
                c.send(
                    "speak reward claimed successfully|n|play_sound eventshopbuy.ogg 0 0 0 1 0")

    if name == "select_a_quest":
        quest_name = option.replace("locked: ", "")
        if quest_name != option:
            qe = quests.quest(quest_name)
            if qe.unlock_by_level == True:
                c.send("speak you haven't unlocked this quest. You need to be level " +
                       str(qe.level)+" to unlock this quest|n|last_server_menu")
            else:
                c.send("speak you haven't yet unlocked this quest. You need to complete an other one in order to unlock this quest.|n|last_server_menu")
            return
        quest_name = quest_name.replace("completed: ", "")
        qe = quests.quest(quest_name)
        options = [qe.name, qe.task]
        for cs in quests.cutseens:
            if quests.cutseens[cs] == quest_name:
                options.append(
                    "view the cutsene that is related to this quest.")

        c.send("server_menu view_here_the_quest_information_of_the_" +
               qe.name.replace(" ", "_")+"_quest "+"\n".join(options))
    if name[0:39] == "view_here_the_quest_information_of_the_":
        quest_name = name.replace(
            "view_here_the_quest_information_of_the_", "")
        quest_name = quest_name.replace("_quest", "")
        quest_name = quest_name.replace("_", " ")
        if option == "view the cutsene that is related to this quest.":
            if c.quests[quest_name] != 1:
                c.send(
                    "speak you have to complete the quest before you can watch the cutsene|n|last_server_menu")
                return

            sound_name = ""
            for key, cs in quests.cutseens.items():
                if cs == quest_name:
                    sound_name = str(key)
            c.send("audio_player "+sound_name)
        else:
            c.send("last_server_menu")
    if name == "this_metal_fortress_belongs_to_a_team_that_you_aren't_a_member_of._Would_you_like_to_turn_off_the_alarm_by_doing_a_simon_game?":
        if option == "yes":
            cx, cy = rotation.move(c.data["x"], c.data["y"], c.data["facing"])
            id = map.get_object(cx, cy, c.data["z"], c.data["map"])
            o = map.get_objects_index(id)
            if o == "" or c.data["z"] >= map.objects[o].maxz or map.objects[o].actif == False and map.objects[o].name != "locker":
                c.send("speak you aren't standing in front of a metal fortress.")
                return
            c.data["calculation_locker"] = map.objects[o].id
            c.send("locker_simon 35")

    if name == "this_locker_belongs_to_a_team_that_you_aren't_a_member_of._Would_you_like_to_break_the_security_by_doing_a_simon_game?":
        if option == "yes":
            cx, cy = rotation.move(c.data["x"], c.data["y"], c.data["facing"])
            id = map.get_object(cx, cy, c.data["z"], c.data["map"])
            o = map.get_objects_index(id)
            if o == "" or c.data["z"] >= map.objects[o].maxz or map.objects[o].actif == False and map.objects[o].name != "locker":
                c.send("speak you aren't standing in front of a locker.")
                return
            c.data["calculation_locker"] = map.objects[o].id
            c.send("locker_simon " +
                   str(map.objects[o].data["security_level"]*5))

    if name == "locker_menu":
        cx, cy = rotation.move(c.data["x"], c.data["y"], c.data["facing"])
        id = map.get_object(cx, cy, c.data["z"], c.data["map"])
        o = map.get_objects_index(id)
        if o == "" or c.data["z"] >= map.objects[o].maxz or map.objects[o].actif == False and map.objects[o].name != "locker":
         c.send("speak you aren't standing in front of a locker.")
         return
        if map.objects[o].data["opened"] == False:
         c.send(
                    "speak the door of your locker is closed")
         return
        if option == "view upgrades":
            options = []
            for d in map.objects[o].data:
                if d[len(d)-6:len(d)] == "_level":
                    options.append(d.replace(
                        d[len(d)-6:len(d)], "")+": upgrade level "+str(map.objects[o].data[d]))
            c.send("server_menu view_the_upgrade_levels_of_the_locker " +
                   "\n".join(options))
        else:
            the_item = option.split(": ")[0]
            if the_item in list(map.objects[o].loot.keys()):
             c.data["take_item"] = the_item
             c.send("input how_many_"+the_item+"s_do_you_want_to_take? ")
            else:
                options=[]
                for w in map.objects[o].weapons:
                    if w.name==the_item:
                        options.append(the_item+"#"+str(len(options)+1)+": "+w.get_info())
                if len(options)<=0:
                    c.send("speak no weapon found")
                else:
                    c.send("server_menu select_a_spesific_weapon_of_the_"+the_item+" "+"\n".join(options))
    if name.startswith("select_a_spesific_weapon_of_the_"):
        the_weapon_name=name.replace("select_a_spesific_weapon_of_the_","")
        cx, cy = rotation.move(c.data["x"], c.data["y"], c.data["facing"])
        id = map.get_object(cx, cy, c.data["z"], c.data["map"])
        o = map.get_objects_index(id)
        if o == "" or c.data["z"] >= map.objects[o].maxz or map.objects[o].actif == False and map.objects[o].name != "locker":
         c.send("speak you aren't standing in front of a locker.")
         return
        if map.objects[o].data["opened"] == False:
         c.send(
                    "speak the door of the locker is closed")
         return
        index=int(option.split('#')[1].split(':')[0])
        i=0
        if c.data["weapons"].count(the_weapon_name)>=3:
         c.send("speak you already have 3 copies of this weapon.")
         return
        if weapons.weapon(the_weapon_name).level>c.data["level"]:
         c.send("speak your level is to low to get this weapon")
         return
        for w in map.objects[o].weapons:
            if w.name==the_weapon_name:
                i+=1
            if i>=index:
                map.objects[o].weapons.remove(w)
                c.add_weapon_instance(w)
                c.send("get_weapons "+"||".join(c.data["weapons"]))
                send_all(r"player_sound "+c.data["name"]+" sounds\\lockertakeweapon.ogg 0|n|player_sound "+c.data["name"] +
                     " sounds\\"+w.sort+"get.ogg 0|n|player_sound "+c.data["name"]+" sounds\\"+the_weapon_name+"get.ogg 0")
                return
        c.send("speak         this weapon is no longer in the locker")
                
        
    if name == "view_the_upgrade_levels_of_the_locker":
        c.data["current_locker_upgrade"] = option.split(": ")[0]
        cx, cy = rotation.move(c.data["x"], c.data["y"], c.data["facing"])
        id = map.get_object(cx, cy, c.data["z"], c.data["map"])
        o = map.get_objects_index(id)
        if o == "" or c.data["z"] >= map.objects[o].maxz or map.objects[o].actif == False and map.objects[o].name != "locker":
            c.send("speak you aren't standing in front of a locker.")
            return
        if map.objects[o].data["opened"] == False:
            c.send(
                "speak the door of the locker is closed, so you can't see the upgrades.")
            return
        options = ["name: "+c.data["current_locker_upgrade"], "upgrade level: " +
                   str(map.objects[o].data[c.data["current_locker_upgrade"]+"_level"])]
        if map.objects[o].data[c.data["current_locker_upgrade"]+"_level"] < 10:
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                options.append("To upgrade this stat of the locker you need "+str(
                    map.objects[o].data[c.data["current_locker_upgrade"]+"_level"]*2)+"  team tokens. Your team has currently "+str(v.teams[index].data["tokens"])+" team tokens")
                if v.teams[index].data["tokens"] >= (map.objects[o].data[c.data["current_locker_upgrade"]+"_level"]*2) and c.data["name"] in v.teams[index].rights["can place lockers"]:
                    options.append("upgrade")
        c.send(
            "server_menu view_here_the_information_of_this_locker_upgrade "+"\n".join(options))

    if name == "view_here_the_information_of_this_locker_upgrade":
        if option == "upgrade":
            cx, cy = rotation.move(c.data["x"], c.data["y"], c.data["facing"])
            id = map.get_object(cx, cy, c.data["z"], c.data["map"])
            o = map.get_objects_index(id)
            if o == "" or c.data["z"] >= map.objects[o].maxz or map.objects[o].actif == False and map.objects[o].name != "locker":
                c.send("speak you aren't standing in front of a locker.")
                return
            if map.objects[o].data["opened"] == False:
                c.send(
                    "speak the door of the locker is closed, so you can't see the upgrades.")
                return
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                if v.teams[index].data["tokens"] >= (map.objects[o].data[c.data["current_locker_upgrade"]+"_level"]*2):
                    v.teams[index].data["tokens"] -= (
                        map.objects[o].data[c.data["current_locker_upgrade"]+"_level"]*2)
                    map.objects[o].data[c.data["current_locker_upgrade"]+"_level"] += 1
                    map.objects[o].max_health = map.objects[o].health_levels[map.objects[o].data["maximum_health_level"]-1]
                    send_all(
                        r"player_sound "+c.data["name"]+" sounds\\lockerupgrade"+c.data["current_locker_upgrade"]+".ogg 0")
                    c.send("stun 2000")

        else:
            c.send("last_server_menu")

    if name == "team_menu._Select_an_option":
        if " has send you an invite to join their team. Press here to accept or decline it." in option:
            team_name = option.replace(
                " has send you an invite to join their team. Press here to accept or decline it.", "")
            options = ["accept", "decline"]
            c.send("server_menu would_you_like_to_accept_or_decline_the_invitation_of_the_" +
                   team_name+"_team? "+"\n".join(options))
        if option == "send an request for a team":
            if teams.get_team(c.data["name"]) != "":
                c.send("speak you are already in a team|n|last_server_menu")
                return
            options = []
            for t in v.teams:
                options.append(t.name)
            if len(options) > 0:
                c.send(
                    "server_menu select_a_team_to_send_an_request_to "+"\n".join(options))
            else:
                c.send("speak there are no teams on the server.|n|last_server_menu")

        if option == "create a team":
            if teams.get_team(c.data["name"]) == "":
                c.send("input type_the_name_of_your_new_team ")
            else:
                c.send("speak you are already in a team|n|last_server_menu")

        if option == "view all teams that have a locker":
            options = []
            for o in map.objects:
                if map.objects[o].name == "locker":
                    options.append(map.objects[o].team)
            if len(options) > 0:
                c.send("server_menu select_a_team "+"\n".join(options))
            else:
                c.send("speak there are no lockers on the server|n|last_server_menu")
        if option == "view all teams that have a metal fortress":
            options = []
            for o in map.objects:
                if map.objects[o].name == "metal_fortress":
                    options.append(map.objects[o].team)
            if len(options) > 0:
                c.send("server_menu select_a_team "+"\n".join(options))
            else:
                c.send(
                    "speak there are no metal fortresses on the server|n|last_server_menu")

        if option == "view all teams":
            options = []
            for t in v.teams:
                options.append(t.name)
            if len(options) > 0:
                c.send("server_menu select_a_team "+"\n".join(options))
            else:
                c.send("speak there are no teams on the server|n|last_server_menu")
        if option == "your team":
            if teams.get_team(c.data["name"]) != "":
                options = ["team profile", "view invites and requests"]
                index = teams.get_teams_index(teams.get_team(c.data["name"]))
                if index > -1:
                    if c.data["name"] in v.teams[index].rights["can place lockers"]:
                        options.append("take a locker to place on the map")
                        options.append(
                            "take a metal fortress construction kit, costs 10 team tokens")
                    if c.data["name"] in v.teams[index].rights["can kick players"]:
                        options.append("kick someone out of your team.")
                    if v.teams[index].data["leader"].lower() == c.data["name"].lower():
                        options.append("change the leader of your team.")
                options.append("view the location of the locker of your team")
                options.append(
                    "view the location of the metal fortress of your team")
                options.append("progress for killing players, reward 1 team token: "+str(
                    v.teams[index].data["kills"] % v.teams[index].token_kills)+" of "+str(v.teams[index].token_kills)+" kills")
                options.append("leave the team")
                if v.teams[index].data["leader"].lower() == c.data["name"].lower():
                    options.append("cancel your team.")
                c.send("server_menu select_an_option_for_your_team " +
                       "\n".join(options))
            else:
                c.send("speak you aren't in a team|n|last_server_menu")

    if name[0:58] == "would_you_like_to_accept_or_decline_the_invitation_of_the_":
        team_name = name.replace(
            "would_you_like_to_accept_or_decline_the_invitation_of_the_", "")
        team_name = team_name.replace("_team?", "")
        if option == "accept":
            if teams.get_team(c.data["name"]) != "":
               c.send("speak can't accept an invite for a team when you are already in one")
               return
            for t in v.teams:
                try:
                    t.members.remove(c.data["name"])
                    t.send("speak "+c.data["name"]+" has left the team.")
                except:
                    pass
            index = teams.get_teams_index(team_name)
            if index > -1:
                v.teams[index].data["invites"].remove(c.data["name"])
                if len(v.teams[index].members) < v.teams[index].data["max_members"]:
                    v.teams[index].members.append(c.data["name"])
                else:
                    c.send("speak this team is full.")
                    return
                v.teams[index].send("add_buffer_item team "+c.data["name"] +
                                    " has joined the team.|n|play_sound teamnotifymisc1.ogg 0 0 0 1 0")

        else:
            index = teams.get_teams_index(team_name)
            if index > -1:
                try:
                    v.teams[index].data["invites"].remove(c.data["name"])
                    v.teams[index].send(
                        "add_buffer_item team "+c.data["name"]+" declined the invitation")
                except:
                    pass

    if name == "select_a_team":
        index = teams.get_teams_index(option)
        if index > -1:
            c.send("server_menu this_is_the_profile_of_the_" +
                   v.teams[index].name+"_team "+"\n".join(v.teams[index].profile_menu()))

    if name == "select_a_team_to_send_an_request_to":
        if teams.get_team(c.data["name"]) != "":
            c.send("speak you are already in a team|n|last_server_menu")
            return
        index = teams.get_teams_index(option)
        if index > -1:
            if c.data["name"] in v.teams[index].data["requests"]:
                c.send(
                    "speak you already have send a request to this team.|n|last_server_menu")
            elif c.data["name"] in v.teams[index].data["invites"]:
                c.send(
                    "speak you already have an invite from this team.|n|last_server_menu")
            else:
                for te in v.teams:
                    try:
                        te.data["requests"].remove(c.data["name"])
                    except:
                        pass
                v.teams[index].data["requests"].append(c.data["name"])
                v.teams[index].send("add_buffer_item team "+c.data["name"] +
                                    " has send a request.|n|play_sound teamnotifymisc1.ogg 0 0 0 1 0")
                c.send("speak request send successfully")

    if name == "select_an_option_for_your_team":
        if option.startswith("progress for killing players, reward 1 team token: "):
            c.send("last_server_menu")
            return
        if option == "team profile":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                c.send("server_menu this_is_the_profile_of_the_" +
                       v.teams[index].name+"_team "+"\n".join(v.teams[index].profile_menu()))
        elif option == "view invites and requests":
            options = []
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                for i in v.teams[index].data["invites"]:
                    options.append("an invite has been sent to "+i)
                for i in v.teams[index].data["requests"]:
                    options.append(
                        i+" has send a request. Press here to accept it.")
            if len(options) > 0:
                c.send(
                    "server_menu view_the_requests_and_invites_for_your_team "+"\n".join(options))
            else:
                c.send(
                    "speak There are currently no pending invites or requests for your team.|n|last_server_menu")
        if option == "kick someone out of your team.":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index == -1:
                return
            if len(v.teams[index].members) <= 1:
                c.send("speak you're the only one in your team|n|last_server_menu")
                return
            options = []
            for t in v.teams[index].members:
                if t != v.teams[index].data["leader"]:
                    options.append(t)
            c.send(
                "server_menu who_do_you_want_to_kick_out_of_your_team? "+"\n".join(options))

        if option == "change the leader of your team.":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                options = []
                for m in v.teams[index].members:
                    options.append(m)
                c.send(
                    "server_menu select_the_new_leader_of_your_team "+"\n".join(options))

        elif option == "cancel your team.":
            c.send("server_mega_menu are_you_sure_you_want_to_delete_your_team? dlg:Are you sure you want to delete your team? This can't be undone by the staff.\ncheck_box:0:Yes. I am sure\nbutton:delete my team")
        elif option == "take a locker to place on the map":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                if v.teams[index].lockertimer.elapsed() >= 3600000:
                    c.give("locker", 1)
                    v.teams[index].lockertimer.restart()
                    v.teams[index].send(
                        "add_buffer_item team "+c.data["name"]+" has taken a locker")

                else:
                    c.send("speak you can't take a locker at the moment. You have to wait "+str(
                        v.get_time_in_mm(3600000-v.teams[index].lockertimer.elapsed()))+"|n|last_server_menu")
        elif option == "take a metal fortress construction kit, costs 10 team tokens":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                if v.teams[index].metal_fortresstimer.elapsed() >= 21600000:
                    if v.teams[index].data["tokens"] < 10:
                        c.send(
                            "speak you need to have 10 team tokens to take this package.")
                        return
                    v.teams[index].data["tokens"] -= 10
                    c.give("metal_fortress_construction_kit", 1)
                    c.send(
                        "play_sound metal_fortress_construction_kitget.ogg 0 0 0 1 0")
                    v.teams[index].metal_fortresstimer.restart()
                    v.teams[index].send("add_buffer_item team "+c.data["name"] +
                                        " has taken a metal fortress construction kit. The team lost 10 team tokens")
                else:
                    c.send("speak you can't take a metal fortress construction kit at the moment. You have to wait "+str(
                        v.get_time_in_mm(21600000-v.teams[index].metal_fortresstimer.elapsed()))+"|n|last_server_menu")

        elif option == "view the location of the locker of your team":
            cords = ""
            for f in map.objects:
                o = map.objects[f]
                if o.name == "locker" and o.team == teams.get_team(c.data["name"]):
                    cords = str(round((o.minx+o.maxx)/2))+", " + \
                        str(round((o.miny+o.maxy)/2))+", "+str(o.minz)
            if cords == "":
                c.send("speak your team doesn't have a locker|n|last_server_menu")
            else:
                c.send("speak your team's locker is at " +
                       cords+"|n|last_server_menu")
        elif option == "view the location of the metal fortress of your team":
            cords = ""
            for f in map.objects:
                o = map.objects[f]
                if o.name == "metal_fortress" and o.team == teams.get_team(c.data["name"]):
                    cords = str(round((o.minx+o.maxx)/2))+", " + \
                        str(round((o.miny+o.maxy)/2))+", "+str(o.minz)
            if cords == "":
                c.send(
                    "speak your team doesn't have a metal_fortress|n|last_server_menu")
            else:
                c.send("speak your team's metal_fortress is at " +
                       cords+"|n|last_server_menu")

        elif option == "leave the team":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                if v.teams[index].data["leader"].lower() == c.data["name"].lower():
                    c.send(
                        "speak you can't leave the team if you are the leader of it.|n|last_server_menu")
                    return
                v.teams[index].send("add_buffer_item team "+c.data["name"] +
                                    " has left the team.|n|play_sound teamnotifymisc2.ogg 0 0 0 1 0")
                v.teams[index].remove_members_rights(c.data["name"])
                for t in v.teams[index].members:
                    if t.lower() == c.data["name"].lower():
                        v.teams[index].members.remove(t)
                if len(v.teams[index].members) < 1:
                    v.teams.remove(v.teams[index])

    if name == "who_do_you_want_to_kick_out_of_your_team?":
        index = teams.get_teams_index(teams.get_team(c.data["name"]))
        if index > -1:
            try:
                v.teams[index].remove_members_rights(option)
                v.teams[index].members.remove(option)
                v.teams[index].send("add_buffer_item team "+option+" was kicked off the team by " +
                                    c.data["name"]+"|n|play_sound teamnotifymisc2.ogg 0 0 0 1 0")
            except:
                c.send("speak something wend wrong with remove " +
                       option+" from your team.")

    if name == "select_the_new_leader_of_your_team":
        if teams.get_team(c.data["name"]) == teams.get_team(option) and teams.get_team(c.data["name"]) != "":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                for r in v.teams[index].rights:
                    v.teams[index].rights[r].append(option)
                v.teams[index].data["leader"] = option
                v.teams[index].send("add_buffer_item team "+option +
                                    " is now the leader of the team.|n|play_sound teamnotifymisc2.ogg 0 0 0 1 0")
    if name == "view_the_requests_and_invites_for_your_team":
        index = teams.get_teams_index(teams.get_team(c.data["name"]))
        if index > -1:
            if "has send a request. Press here to accept it." in option:
                if len(v.teams[index].members) < v.teams[index].data["max_members"]:
                    if c.data["name"] not in v.teams[index].rights["can accept players"]:
                        c.send(
                            "speak you don't have the rights to accept new players|n|last_server_menu")
                        return
                    option = option.replace(
                        " has send a request. Press here to accept it.", "")
                    if len(v.teams[index].members) < v.teams[index].data["max_members"]:
                        v.teams[index].members.append(option)
                    else:
                        c.send("speak the team is full.")
                        return
                    v.teams[index].data["requests"].remove(option)
                    v.teams[index].send(
                        "add_buffer_item team "+option+" has joined the team.|n|play_sound teamnotifymisc2.ogg 0 0 0 1 0")
                    return
                else:
                    c.send("speak your team is full|n|last_server_menu")
            else:
                v.teams[index].data["invites"].remove(
                    option.replace("an invite has been sent to ", ""))
                v.teams[index].send("add_buffer_item team the invite of "+option.replace(
                    "an invite has been sent to ", "")+" has been withdrawn")

    if name[0:27] == "this_is_the_profile_of_the_":
        if option == "members":
            options = []
            team_name = name.replace("this_is_the_profile_of_the_", "")
            team_name = team_name.replace("_team", "")
            index = teams.get_teams_index(team_name)
            if index > -1:
                for t in v.teams[index].members:
                    options.append(t)
                c.send("server_menu view_here_the_members_of_the_" +
                       team_name+"_team "+"\n".join(options))

        else:
            c.send("last_server_menu")

    if name[0:29] == "view_here_the_members_of_the_":
        server_menu_answer(c, "player_menu", option)
    if name == "select_an_event":
        options = []
        for e in v.events:
            if e.name == option:
                options.append("name: "+e.name)
                options.append(v.get_description(e.name))
                options.append("remaining time for this event: " +
                               v.get_time_in_mm(e.max_time-e.timer.elapsed()))
                if e.name == "kill the VIP":
                    vip = e.information["vip"]
                    if vip == "":
                        vip = "no one"
                    if 300000-e.information["new_viptimer"].elapsed() > 0:
                        options.append("the current VIP is "+vip+". The next VIP will be chosen in " +
                                       v.get_time_in_mm(300000-e.information["new_viptimer"].elapsed()))
                    else:
                        options.append(
                            "there are not enough players to chose a new vip.")
                if e.name == "weapons competition":
                    weapon = e.information["weapon"]
                    if weapon == "":
                        weapon = "nothing"
                    if 900000-e.information["new_weapontimer"].elapsed() > 0:
                        options.append("the current weapon is "+weapon+". The next weapon will be chosen in " +
                                       v.get_time_in_mm(900000-e.information["new_weapontimer"].elapsed()))

                options.append(
                    "Required score to get 100 event points: "+str(e.max_score))
                try:
                    progress = math.floor(
                        e.scores[c.data["name"].lower()]/e.max_score*100)
                    if progress < 100:
                        options.append(
                            "your progress in this event: "+str(progress)+"%")
                    else:
                        options.append(
                            "You have completed this event and collected all the event points.")
                except:
                    pass
                options.append("view the leader board of this event.")
        c.send("server_menu view_the_"+option.replace(" ", "_") +
               "_event "+"\n".join(options))
    if name[0:9] == "view_the_" and "event" in name:
        if option == "view the leader board of this event.":
            name = name.replace("view_the_", "")
            name = name.replace("_event", "")
            name = name.replace("_", " ")
            options = []
            for e in v.events:
                if e.name == name:
                    sorted_keys = sorted(
                        e.scores, key=lambda x: e.scores[x], reverse=True)
                    i = 1
                    for p in sorted_keys:
                        options.append(str(i)+": "+p+" with " +
                                       str(e.scores[p])+" score points.")
                        i += 1
            c.send("server_menu view_here_the_leader_board "+"\n".join(options))
        else:
            c.send("last_server_menu")
    if name == "choose_the_chest_you_want_to_open":
        if c.data["level"] < 5:
            c.send("speak you have to be level 5 to open chests.")
            return
        parsed = option.split(" ")
        if parsed[1] not in c.data["chests"] or c.data["chests"][parsed[1]] <= 0:
            c.send("speak you don't have this chest")
        else:
            amounts = {
                "bronze": 15,
                "silver": 30,
                "golden": 70,
                "platinum": 150,
                "diamond": 500,
            }
        final = {}
        maximum = 0
        i = 0
        can = 0
        for s in c.skill_data:
            sk = skills.skill(s)
            if c.skill_data[s]["unlocked"] == True and c.skill_data[s]["level"] < sk.max_level:
                can = 1
        if can == 0:
            c.send("speak you already have all your skills maximum level.")
            return
        while i < maximum+amounts[parsed[1]]:
            skill_list = list(c.skill_data.keys())
            number = random.randint(0, len(skill_list)-1)
            name = skill_list[number]
            sk = skills.skill(name)
            if c.skill_data[name]["unlocked"] == False or c.skill_data[name]["level"] >= sk.max_level:
                maximum += 1
            else:
                try:
                    old_amount = final[name]
                except:
                    old_amount = 0
                final[name] = old_amount+1
            i += 1
        if teams.get_team(c.data["name"]) != "":
            r = random.randint(1, 3)
            final["team_token"] = r
        for f in final:
            if f != "team_token":
                c.skill_data[f]["skill_points"] += final[f]
            else:
                index = teams.get_teams_index(teams.get_team(c.data["name"]))
                if index > -1:
                    v.teams[index].data["tokens"] += final[f]
        c.send("open_chest "+parsed[1]+" "+str(final))
        c.data["chests"][parsed[1]] -= 1
    if name == "select_an_option_for_your_skills":
        if c.data["level"] < 5:
            c.send("speak skills are available at level 5 or higher.")
            return
        if option == "view unlocked skills":
            options = []
            for s in c.skill_data:
                if c.skill_data[s]["unlocked"] == True:
                    sk = skills.skill(s)
                    if c.skill_data[s]["level"] < 5 and c.skill_data[s]["skill_points"] >= sk.needed_skill_points[c.skill_data[s]["level"]-1]:
                        options.append(s+". Upgrade available.")
                    else:
                        options.append(s)
            c.send(
                "server_menu select_a_skill_to_get_more_information_about_it "+"\n".join(options))
        if option == "manage skill set":
            c.data["edit_skills"] = []
            options = skill_set(c)
            c.send(
                "server_menu select_which_skill_you_want_to_activate "+"\n".join(options))

    if name == "select_a_skill_to_get_more_information_about_it":
        option = option.replace(". Upgrade available.", "")
        sk = skills.skill(option)
        options = ["name: "+option, "description: "+sk.get_description()]
        if sk.permanent == False:
            options.append(
                "this skill can be used using either the g or shift + g key.")
        else:
            options.append(
                "this skill's effects will always be active if you have this skill in use.")

        options.append(
            "level: "+sk.level_names[c.skill_data[option]["level"]-1])
        if c.skill_data[option]["level"] >= sk.max_level:
            options.append("this skill is maximum level")
        else:
            options.append("collected Skill points to upgrade this skill to the "+sk.level_names[c.skill_data[option]["level"]]+" level: "+str(
                c.skill_data[option]["skill_points"])+" / "+str(sk.needed_skill_points[c.skill_data[option]["level"]-1]))
            if c.skill_data[option]["skill_points"] >= sk.needed_skill_points[c.skill_data[option]["level"]-1]:
                options.append("upgrade")
        c.send("server_menu view_here_the_information_of_the_" +
               option.replace(" ", "_")+"_skill "+"\n".join(options))
    if name[0:33] == "view_here_the_information_of_the_":
        s = name.replace("view_here_the_information_of_the_", "")
        s = s.replace("_skill", "")
        sk = skills.skill(s)
        if option == "upgrade":
            s = s.replace("_", " ")
            c.skill_data[s]["skill_points"] -= sk.needed_skill_points[c.skill_data[s]["level"]-1]
            c.skill_data[s]["level"] += 1
            c.send(
                "speak upgraded successfully|n|play_sound skillupgrade.ogg 0 0 0 1 0|n|server_menu_reset")

        else:
            c.send("last_server_menu")
    if name == "select_which_skill_you_want_to_activate":
        if option == "reset all your education points":
            c.data["edit_skills"] = []
            for s in c.skill_data:
                if c.skill_data[s]["active"] == True:
                    c.data["edit_skills"].append(s)
            c.send("speak done|n|play_sound skillset.ogg 0 0 0 1 0")
        if option[0:13] == "you will use ":
            c.send("last_server_menu")
        if option == "done":
            if len(c.data["edit_skills"]) > 0:
                c.store_data()
                skill_data = change_skills(c, c.skill_data)
                weapon_type = ""
                i = 0
                for s in skill_data:
                    if skill_data[s]["active"] == True:
                        sk = skills.skill(s)
                        i += sk.education_points
                        if sk.weapon_sort != "":
                            if weapon_type == "":
                                weapon_type = sk.weapon_sort
                            else:
                                if sk.weapon_sort != weapon_type:
                                    c.send(
                                        "speak error: your skill set uses more than one weapon category.")
                                    c.get_data()
                                    return
                if i > c.data["level"]:
                    c.send(
                        "speak you don't have enough education points to use all these skills")
                    c.get_data()
                    return
                else:
                    c.skill_data = skill_data
                    c.send("speak done")
                    c.send("|n|play_sound skillset.ogg 0 0 0 1 0")
        else:
            parsed = option.split(":")
            if parsed[0] not in c.data["edit_skills"]:
                c.data["edit_skills"].append(parsed[0])
            else:
                c.data["edit_skills"].remove(parsed[0])
        options = skill_set(c)
        if option != "done" and "you will use " not in option:
            c.send(
                "delete_server_menu|n|server_menu select_which_skill_you_want_to_activate "+"\n".join(options))

    if name == "View_all_levels_with_the_associated_weapons_here" or name == "view_the_changes" or name == "view_the_profile_of_"+c.data["selected_player"] or name == "view_your_profile" or name == "read_the_announcement" or name == "view_the_messages_here" or name == "view_here_the_leader_board" or name == "read_the_article_here" or name == "view_all_the_staff_members_here" or name == "read_the_file_here" or name == "view_your_team's_traps_here" or name == "view_here_the_notes_placed_by_your_team" or name == "view_this_player's_warningss":
        c.send("last_server_menu")
    if name == "server_menu._Select_an_item":
        if option == "account settings":
            options = ["set email address, currently it is "+c.data["mail"],
                       "set which death messages you see", "delete account"]
            c.send("server_menu account_menu._Select_an_option "+"\n".join(options))

        if option == "view active events":
            options = []
            for e in v.events:
                options.append(e.name)
            if len(options) > 0:
                c.send("server_menu select_an_event "+"\n".join(options))
            else:
                c.send("speak there are no active events.|n|last_server_menu")

        if option == "view documentation":
            c.data["documentation_path"] = "documentation"
            options = c.get_documentation_files()
            folders = c.data["documentation_path"].split("/")
            last_folder = folders[len(folders)-1]
            if len(options) > 0:
                c.send("server_menu select_an_article "+"\n".join(options))
            else:
                c.send("speak this_folder_or_article_is_empty|n|last_server_menu")

        if option == "view staff members":
            options = []
            for f in v.admin_list:
                index = get_players_index(f)
                if index > -1:
                    status = "online"
                else:
                    status = "offline"
                options.append(f+": "+v.admin_list[f]+": "+status)
            c.send("server_menu view_all_the_staff_members_here " +
                   "\n".join(options))

        if option == "contact staff":
            options = ["support", "report", "bug_report", "feedback"]
            c.send(
                "server_menu Please_select_one_of_the_options_for_contacting_the_staff. "+"\n".join(options))
        if option == "announcements":
            options = []
            for a in v.announcements:
                l = ""
                if c.data["name"] not in a.read:
                    l = "unread, "
                options.append(l+"subject: "+a.name +
                               ". Created on "+a.create_time+". Id: "+str(a.id))
            if len(options) == 0:
                c.send("speak there are no announcements.|n|last_server_menu")
            else:
                c.send("server_menu select_an_announcement "+"\n".join(options))
        if option == "unmute someone":
            options = []
            for m in c.data["mutelist"]:
                options.append(m)
            c.send("server_menu who_do_you_want_to_unmute? "+"\n".join(options))
        if option == "view levels":
            skilllist = list(c.skill_data)
            data = []
            for i in range(1, v.max_level+1):
                l = "level "+str(i)+" unlocks "
                unlock = []
                for f in v.weapon_names:
                    weapon = weapons.weapon(f)
                    if weapon.level == i:
                        unlock.append("the "+f)
                for f in skilllist:
                    skill = skills.skill(f)
                    if skill.unlocklevel == i:
                        unlock.append("the "+f+" skill")
                if unlock == []:
                    result = "nothing"
                else:
                    result = v.get_list_in_text(unlock)
                data.append(l+result)
            c.send(
                "server_menu View_all_levels_with_the_associated_weapons_here "+"\n".join(data))
        if option == "set chat channel":
            c.send("server_menu select_a_chat_channel "+"\n".join(v.languages))
        if option == "changes":
            c.send("server_menu view_the_changes "+misk.changes)
        if option == "your current_ staff messages":
            options=[]
            messages = admin_message.select_admin_messages("",c.data["name"])
            for a in messages:
                    l = ""
                    if c.data["name"] not in a.read:
                        l = "unread, "
                    options.append(
                        l+"subject: "+a.name+". Created on "+a.create_time+". Id: "+str(a.id))
            if len(options) == 0:
                c.send("speak you haven't any open staff messages.|n|last_server_menu")
            else:
                c.send("server_menu select_a_staff_message "+"\n".join(options))
        if option == "options that belong to your rank":
            if c.data["admin"] == 1:
                options = ["view staffmessages.", "logs", "post an announcement", "remove an announcement",
                           "ban someone", "unban someone", "enable someone's chat", "send a notification to the hole server"]
                if v.freeze == False:
                    options.append("freeze all players on the server")
                else:
                    options.append("unfreeze all players on the server")
                options.append("create an event")
                if c.lobby == True:
                    options.append("change map")
                options.append("create a new map")
                options.append("cleanup the server. This will remove all spam team- and players")
                options.append("view server stats.")
                options.append("restart the server")
            if c.data["moderator"] == 1:
                options = ["view staffmessages.", "logs", "enable someone's chat",
                           "send a notification to the hole server"]
            if c.data["builder"] == 1:
                options = []
                options.append("move your self")
                if c.lobby == True:
                    options.append("change map")
                options.append("create a new map")

            c.send("server_menu rank_menu "+"\n".join(options))

    if name[0:17] == "select_an_article":
        chosen_path = os.path.join(c.data["documentation_path"], option)
        folders = c.data["documentation_path"].split("/")
        am = folders.count(option)
        if am > 0:
            folders.pop()

            chosen_path = r"/".join(folders)
        c.data["documentation_path"] = chosen_path
        if os.path.isdir(chosen_path):
            options = c.get_documentation_files()

            folders = c.data["documentation_path"].split(r"/")
            last_folder = folders[len(folders)-1]
            if len(options) > 0:
                c.send("server_menu select_an_article "+"\n".join(options))
            else:
                folders = c.data["documentation_path"].split(r"/")
                last_folder = folders[len(folders)-1]
                folders.remove(last_folder)
                if len(folders) > 0:
                    c.data["documentation_path"] = "/".join(folders)
                else:
                    c.data["documentation_path"] = "documentation"
                c.send("speak this_folder_is_empty|n|last_server_menu")
        else:
            options = read_file_lines(chosen_path)
            if len(options) > 0:
                c.send("server_menu read_the_article_here "+"\n".join(options))
            else:
                folders = c.data["documentation_path"].split(r"/")
                last_folder = folders[len(folders)-1]
                folders.remove(last_folder)
                if len(folders) > 0:
                    c.data["documentation_path"] = "/".join(folders)
                else:
                    c.data["documentation_path"] = "documentation"
                c.send("speak this_article_is_empty|n|last_server_menu")

    if name == "account_menu._Select_an_option":
        if option[0:17] == "set email address":
            c.send("input type_your_new_email_address ")

        if option == "set which death messages you see":
            options = ["only your self", "only your team members", "only people on your map","everyone"]
            c.send(
                "server_menu select_which_death_messages_you_will_see "+"\n".join(options))

        if option == "delete account":
            c.send("server_mega_menu are_you_sure_you_want_to_delete_your_account? dlg:Are you sure you want to delete your account? This can't be undone by the staff.\ncheck_box:0:Yes. I am sure\nbutton:delete my account")
    if name == "select_which_death_messages_you_will_see":
        c.send("speak set to "+option)
        c.data["death_messages"] = option

    if name == "select_a_chat_channel":
        if option != c.data["language"]:
            c.data["language"] = option
            if option != "disable chat":
                c.send("speak your chat channel has been set to "+option)
            else:
                c.send("speak your chat has been disabled")
        else:
            c.send("speak you are already in this channel")
    if name == "who_do_you_want_to_unmute?":
        if option in c.data["mutelist"]:
            c.data["mutelist"].remove(option)
            c.send("speak "+option+" has been unmuted.")
    if name == "which_announcement_do_you_want_to_remove?":
        if option != "":
            parsed = option.split(" ")
            index = misk.get_announcements_index(int(parsed[len(parsed)-1]))
            if index > -1:
                send_all("speak  the announcement " +
                         v.announcements[index].name+" has been removed")
                del v.announcements[index]
                c.send("done")

    if name == "select_an_announcement":
        if option != "":
            parsed = option.split(" ")
            index = misk.get_announcements_index(int(parsed[len(parsed)-1]))
            if index > -1:
                v.announcements[index].read.append(c.data["name"])
                c.send("server_menu read_the_announcement " +
                       "\n".join(v.announcements[index].text))
    if name == "whose_chat_do_you_want_to_enable?":
        if option in v.mute_players:
            v.mute_players.remove(option)
        index = get_players_index(option)
        if index > -1:
            v.clients[index].data["org_mutetime"] = 0
        else:
            data = sd.get("data", option+".plr", {}, "players")
            data["org_mutetime"] = 0
            sd.save("data", data, option+".plr", "players")
        c.send("speak "+option+"'s chat has been enabled")

    if name == "rank_menu":
        if option == "logs":
            c.data["logs_path"] = "logs"
            options = c.get_log_files()
            folders = c.data["logs_path"].split("/")
            last_folder = folders[len(folders)-1]
            if len(options) > 0:
                c.send("server_menu select_a_folder_or_file "+"\n".join(options))
            else:
                c.send("speak this_folder_or_file_is_empty|n|last_server_menu")

        if option == "create a new map":
            c.send("input type_the_map_name_for_your_new_map ")
        if option == "move your self":
            if c.data["map"] == "main":
                c.send("speak can't move your self on the main map")
                return
            c.send("input type_the_cordinates_you_want_to_move_to._Press_a_period_to_split_it._An_example_could_be_0.0.0_to_move_your_self_to0,_0,_0 ")
        if option == "change map":
            options = []
            script_path = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.join(script_path, 'maps')
            for filename in os.listdir(folder_path):
                options.append(filename.replace(".txt", ""))
            if len(options) > 0:
                c.send(
                    "server_menu which_map_do_you_want_to_change_to? "+"\n".join(options))

        if option == "create an event":
            c.send("server_menu select_the_type_event " +
                   "\n".join(v.event_types))
        if option == "freeze all players on the server":
            v.freeze = True
            send_all(
                "buffer_sound important alert.ogg 0 0 0 1 0|n|add_buffer_item important alert: all players have been frozen.")
        elif option == "unfreeze all players on the server":
            v.freeze = False
            send_all("buffer_sound important alert.ogg 0 0 0 1 0|n|add_buffer_item important alert: all players are no longer frozen.|n|stun_reset")
        if option == "enable someone's chat":
            options=v.mute_players
            if len(options) > 0:
                c.send("server_menu whose_chat_do_you_want_to_enable? " +
                       "\n".join(options))
            else:
                c.send(
                    "speak there are no players with their chat disabled.|n|last_server_menu")
        if option == "send a notification to the hole server":
            c.send("input type_the_text_of_your_notify ")
        if option=="view server stats.":
            c.send("speak platforms "+str(len(map.platforms))+". Objects "+str(len(map.objects))+". Corpses "+str(len(map.corpses))+". Players "+str(len(v.clients))+". Bullets "+str(len(v.bullets))+". Matches "+str(len(v.matches)))
        if option == "cleanup the server. This will remove all spam team- and players":
            send_all("buffer_sound important alert.ogg 0 0 0 1 0|n|add_buffer_item important the server is cleaning up. This may lag the server for a while...")
            new_teams = []
            for t in v.teams:
                if t.data["kills"] > 19:
                    new_teams.append(t)
            c.send("speak "+str(len(v.teams)-len(new_teams))+" teams deleted")
            v.teams = new_teams
            removed_accounts = 0
            script_path = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.join(script_path, 'players')
            for filename in os.listdir(folder_path):
                try:
                    file_path = os.path.join(folder_path, filename)
                    data = sd.get("data", file_path, {})
                    if data["playtime"] < 3600000:
                        os.remove(file_path)
                        removed_accounts += 1
                except:
                    pass
            c.send("speak "+str(removed_accounts)+" accounts deleted")
            send_all("add_buffer_item important cleanup done")

        if option == "restart the server":
            if v.restarting == False:
                send_all(
                    "buffer_sound important alert.ogg 0 0 0 1 0|n|add_buffer_item important the server is restarting in 15 seconds")
                v.restarttimer.restart()
                v.restarting = True
            else:
                c.send("speak the server is already going to restart.")
        if option == "ban someone":
            script_pad = os.path.dirname(os.path.abspath(__file__))
            players_map_pad = os.path.join(script_pad, 'players')
            files = os.listdir(players_map_pad)
            options = []
            for f in files:
                f = f.replace(".plr", "")
                options.append(f)
            c.send("server_menu who_do_you_want_to_ban? "+"\n".join(options))
        if option == "unban someone":
            options = []
            for b in v.banlist:
                options.append(b)
            if len(options) == 0:
                c.send("speak there are no banned players.|n|last_server_menu")
            else:
                c.send("server_menu who_do_you_want_to_unban? "+"\n".join(options))

        if option == "remove an announcement":
            options = []
            for a in v.announcements:
                options.append("subject: "+a.name+". Created on " +
                               a.create_time+". Id: "+str(a.id))
            if len(options) == 0:
                c.send("speak there are no announcements.|n|last_server_menu")
            else:
                c.send(
                    "server_menu which_announcement_do_you_want_to_remove? "+"\n".join(options))
        if option == "post an announcement":
            c.data["input"] = ""
            c.send("input type_the_subject_of_the_announcement ")
        if option == "view staffmessages.":
            sorts = ["support", "report", "bug_report", "feedback", "marked"]
            options = []
            for s in sorts:
                i = 0
                for a in v.admin_messages:
                    if a.sort == s and c.data["name"] not in a.read and s != "marked":
                        i += 1
                    if len(a.marked_by) > 0 and c.data["name"] not in a.read and s == "marked":
                        i += 1

                if i == 0:
                    options.append(s)
                else:
                    options.append(s+": "+str(i)+" unread")
            options.append("mark every message as read.")
            c.send("server_menu select_the_category "+"\n".join(options))
    if name == "select_a_folder_or_file":
        chosen_path = os.path.join(c.data["logs_path"], option)
        folders = c.data["logs_path"].split("/")
        am = folders.count(option)
        if am > 0:
            folders.pop()

            chosen_path = r"/".join(folders)
        c.data["logs_path"] = chosen_path
        if os.path.isdir(chosen_path):
            options = c.get_log_files()

            folders = c.data["logs_path"].split(r"/")
            last_folder = folders[len(folders)-1]
            if len(options) > 0:
                c.send("server_menu select_a_folder_or_file "+"\n".join(options))
            else:
                folders = c.data["logs_path"].split(r"/")
                last_folder = folders[len(folders)-1]
                folders.remove(last_folder)
                if len(folders) > 0:
                    c.data["logs_path"] = "/".join(folders)
                else:
                    c.data["logs_path"] = "logs"
                c.send("speak this_folder_is_empty|n|last_server_menu")
        else:
            key = b"0010011001001010"
            options = v.read_log_file(chosen_path, key)
            if len(options) > 0:
                c.send("server_menu read_the_file_here "+"\n".join(options))
            else:
                folders = c.data["logs_path"].split(r"")
                last_folder = folders[len(folders)-1]
                folders.remove(last_folder)
                if len(folders) > 0:
                    c.data["logs_path"] = "/".join(folders)
                else:
                    c.data["logs_path"] = "logs"
                c.send("speak this_file_is_empty|n|last_server_menu")

    if name == "which_map_do_you_want_to_change_to?":
        c.data["map"] = option
        c.send("speak map changed to "+option)

    if name == "select_the_type_event":
        c.send("input select_the_time_for_the_" +
               option.replace(" ", "_")+"_event._86400000_is_1_day ")

    if name == "who_do_you_want_to_ban?":
        # lekker bannen
        data = sd.get("data", option+".plr", {}, "players")
        v.banlist[option] = data["comp_id"]
        index = get_players_index(option)
        if index > -1:
            send_all("add_buffer_item misc " +
                     v.clients[index].data["name"]+" has been banned from the server")
            v.clients[index].send("ban")
            v.clients[index].disconnect(True)
        else:
            send_all("speak "+option+" has been banned")
    if name == "who_do_you_want_to_unban?":
        del v.banlist[option]
        c.send("speak "+option+" has been unbanned.")
    if name == "select_the_category":
        if option == "mark every message as read.":
            for a in v.admin_messages:
                if c.data["name"] not in a.read:
                    a.read.append(c.data["name"])
            c.send("speak done")
            return

        try:
            words = option.split(": ")
            option = option.replace(": "+words[1], "")
        except:
            pass
        options = []
        for a in v.admin_messages:
            if a.sort == option and option != "marked" or option == "marked" and len(a.marked_by) > 0:
                l = ""
                if c.data["name"] not in a.read:
                    l = "unread, "
                options.append(l+"subject: "+a.name+". Created by " +
                               a.owner+" on "+a.create_time+". Id: "+str(a.id))
        if len(options) > 0:
            c.send("server_menu select_a_staff_message "+"\n".join(options))
        else:
            c.send("speak no staff messages in this category|n|last_server_menu")
    if name == "Please_select_one_of_the_options_for_contacting_the_staff.":
        if option != "":
            c.send(
                "input Type_the_subject_of_the_staff_message_in_the_category_"+option+" ")
    if name == "select_a_staff_message":
        if option != "":
            parsed = option.split(" ")
            index = admin_message.get_admin_messages_index(
                int(parsed[len(parsed)-1]))
            if index > -1:
                v.admin_messages[index].read.append(c.data["name"])
                options = ["view messages in this staff chat",
                           "send a message in this staff chat"]
                if c.data["name"] != v.admin_messages[index].owner:
                    if v.admin_messages[index].owner in v.admin_messages[index].read:
                        options.append(
                            v.admin_messages[index].owner+" has read the staff message")
                    else:
                        options.append(
                            v.admin_messages[index].owner+" hasn't read the staff message")
                if v.admin_messages[index].owner != c.data["name"]:
                    if c.data["name"] in v.admin_messages[index].marked_by:
                        options.append("unmark this staff message")
                    else:
                        options.append("mark this staff message")
                options.append("close this staff chat")

                c.send("server_menu select_an_option_for_staff_message_" +
                       str(v.admin_messages[index].id)+" "+"\n".join(options))
    if name[0:35] == "select_an_option_for_staff_message_":
        parsed = name.split("_")
        index = admin_message.get_admin_messages_index(
            int(parsed[len(parsed)-1]))
        if index > -1:
            if option == "mark this staff message":
                v.admin_messages[index].marked_by.append(c.data["name"])
                c.send("speak done")
            elif option == "unmark this staff message":
                v.admin_messages[index].marked_by.remove(c.data["name"])
                c.send("speak done")
            elif option == "close this staff chat":
                if c.data["name"] == v.admin_messages[index].owner and len(v.admin_messages[index].marked_by) > 0:
                    c.send(
                        "speak the admins have marked this staff message, so it can't be closed")
                    return
                v.admin_messages[index].send("add_buffer_item staff_messages the staff message "+str(
                    v.admin_messages[index].name)+" has been closed.")
                v.admin_messages[index].send(
                    "play_sound staffmsgclosed.ogg 0 0 0 1 0")
                del v.admin_messages[index]

            elif option == "view messages in this staff chat":
                c.send("server_menu view_the_messages_here " +
                       "\n".join(v.admin_messages[index].messages))
            elif option == "send a message in this staff chat":
                c.send("input type_your_message_to_be_send_in_staff_chat_" +
                       str(v.admin_messages[index].id)+" ")
            else:
                c.send("last_server_menu")
# if c.sended==False:
#  c.send("|n|server_menu_reset")
    if name[0:11] == "player_menu":
        names = option.split(": ")
        option = names[0]
        index = get_players_index(names[0])
        if index == -1:
            c.send("speak this player is offline|n|last_server_menu")
            return
        c.data["selected_player"] = option
        options = ["view the profile of this player", "send a private message"]
        if option in c.data["mutelist"] or c.data["name"] == option:
            options.remove("send a private message")
        if teams.get_team(c.data["name"]) != "" and teams.get_team(c.data["name"]) != teams.get_team(option):
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                if c.data["name"] in v.teams[index].rights["can invite players"]:
                    if option in v.teams[index].data["invites"]:

                        options.append(
                            "withdraw the invitation to join your team for this player.")
                    else:
                        options.append(
                            "send an invite for joining your team to this player.")

        if teams.get_team(c.data["name"]) != "" and teams.get_team(c.data["name"]) == teams.get_team(option) and c.data["name"] != option:
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                if c.data["name"] in v.teams[index].rights["can kick players"]:
                    options.append("kick this player from your team")
        if teams.get_team(c.data["name"]) != "" and teams.get_team(c.data["name"]) == teams.get_team(option) and c.data["name"] != option:
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                if c.data["name"] in v.teams[index].rights["can change rights"]:
                    if option in v.teams[index].rights["can change rights"] and v.teams[index].data["leader"] == c.data["name"] or option not in v.teams[index].rights["can change rights"]:
                        options.append(
                            "change this player's rights in your team.")

        if option != c.data["name"]:
            if option in c.data["mutelist"]:
                options.append("unmute this player")
            else:
                options.append("mute this player")
        options.append("copy the player name to your clipboard")
        index = get_players_index(option)
        if index > -1:
            if c.data["moderator"] == 1 and v.clients[index].data["admin"] == 0 and v.clients[index].data["moderator"] == 0 or c.data["admin"] == 1:
                options.append("ranked options for this player")
        c.send("server_menu select_an_option_for_" +
               c.data["selected_player"]+" "+"\n".join(options))
    if name == "select_an_option_for_"+c.data["selected_player"]+"":
        if option == "withdraw the invitation to join your team for this player.":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                v.teams[index].data["invites"].remove(
                    c.data["selected_player"])
                c.send("speak the invite has been withdrawn.")

        if option == "change this player's rights in your team.":
            text = ""
            items = []
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                for t in v.teams[index].rights:
                    if c.data["selected_player"] in v.teams[index].rights[t]:
                        items.append("check_box:1:"+t)
                    else:
                        items.append("check_box:0:"+t)
                text = "\n".join(items)
            c.send("server_mega_menu select_the_rights_for_" +
                   c.data["selected_player"]+" dlg:press tap and shift tap and select the check boxes for the rights that this player should have\n"+text+"\nbutton:finish")
        if option == "kick this player from your team":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                if v.teams[index].data["leader"] == c.data["selected_player"]:
                    c.send(
                        "speak you can't kick the leader of your team out of the team.|n|last_server_menu")
                    return
                cindex = get_players_index(c.data["selected_player"])
                if cindex > -1:
                    v.clients[cindex].send(
                        "speak you have been kicked out of your team.")
                v.teams[index].remove_members_rights(c.data["selected_player"])
                v.teams[index].members.remove(c.data["selected_player"])
                v.teams[index].send("add_buffer_item team "+c.data["selected_player"] +
                                    " has been kicked out of the team by "+c.data["name|n|play_sound teamnotifymisc2.ogg 0 0 0 1 0"])

        if option == "send an invite for joining your team to this player.":
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                index2 = teams.get_teams_index(
                    teams.get_team(c.data["selected_player"]))
                if index2 > -1:
                    if v.teams[index2].data["leader"] == c.data["selected_player"]:
                        c.send(
                            "speak this player is the leader of an other team.|n|last_server_menu")
                        return
                if c.data["selected_player"] in v.teams[index].data["requests"]:
                    c.send(
                        "speak this player has already send an request for joining your team.|n|last_server_menu")
                else:
                    v.teams[index].data["invites"].append(
                        c.data["selected_player"])
                    c.send("speak the invite has been sent.")
                    pindex = get_players_index(c.data["selected_player"])
                    if pindex > -1:
                        v.clients[pindex].send(
                            "play_sound teamnotifymisc1.ogg 0 0 0 1 0|n|speak You've got an invite for joining a team. See it in the team menu.")

        if option == "view the profile of this player":
            index = get_players_index(c.data["selected_player"])
            if index > -1:
                options = ["name: "+v.clients[index].data["name"]]
                options.append("level: "+str(v.clients[index].data["level"]))
                if v.clients[index].data["name"]==c.data["name"] and v.clients[index].data["level"]<v.max_level:
                 percent = 0
                 percent = c.data["xp"]/c.data["needed_xp"]
                 percent = math.floor(percent*100)
                 options.append("progression to the next level: "+str(percent)+"%")
                for p in c.using_potions:
                 options.append("remaining time of the "+p+": "+v.get_time_in_mm(
                c.using_potions[p]["max_time"]-c.using_potions[p]["timer"].elapsed()))


                if teams.get_team(v.clients[index].data["name"]) != "":
                    tindex = teams.get_teams_index(
                        teams.get_team(v.clients[index].data["name"]))
                    if tindex > -1:
                        rights = []
                        if c.data["selected_player"] == v.teams[tindex].data["leader"]:
                            text = v.clients[index].data["name"]+" is the leader of the " + \
                                teams.get_team(
                                    v.clients[index].data["name"])+" team"
                        else:
                            text = v.clients[index].data["name"]+" is part of the " + \
                                teams.get_team(
                                    v.clients[index].data["name"])+" team"
                        for t in v.teams[tindex].rights:
                            if v.clients[index].data["name"] in v.teams[tindex].rights[t]:
                                rights.append(t)
                        if len(rights) == 0:
                            text = text+" and has no rights"
                        else:
                            text = text+" and "+v.get_list_in_text(rights)
                        options.append(text)
                options.append("chat channel: " +
                               v.clients[index].data["language"])
                options.append(
                    "total playing time: "+v.get_time_in_mm(v.clients[index].playtimer.elapsed()))
                options.extend(v.clients[index].show_statistics())
                options.append("this player is already surviving "+v.get_time_in_mm(v.clients[index].survivetimer.elapsed(
                ))+" and has made "+str(v.clients[index].data["kills"])+" kills in this time.")
                final = v.clients[index].data["name"]+" has "
                skill_text = []
                for i in v.clients[index].skill_data:
                    if v.clients[index].skill_data[i]["active"] == True:
                        sk = skills.skill(i)
                        skill_text.append(
                            "a "+sk.level_names[v.clients[index].skill_data[i]["level"]-1]+" "+i)
                final = final+v.get_list_in_text(skill_text)
                if skill_text != []:
                    final = final+" skill in use."
                else:
                    final = final+" no skills in use."
                options.append(final)
                c.send("server_menu view_the_profile_of_" +
                       v.clients[index].data["name"]+" "+"\n".join(options))
        if option == "send a private message":
            c.send("input type_your_message_to_"+c.data["selected_player"]+" ")
        if option == "copy the player name to your clipboard":
            c.send("copie "+c.data["selected_player"]+"|n|speak " +
                   c.data["selected_player"]+" has been copied to your clipboard.")
        if option == "ranked options for this player":
            options = ["warn this player", "view this player's warnings",
                       "disable this player's chat"]
            if c.data["admin"] == 1:
                options.append("move this player")
                options.append("kick this player")
                options.append("ban this player")
            c.send("server_menu select_an_ranked_option "+"\n".join(options))

        if option == "admin options for this player":
            c.send("admin_player_menu "+c.data["selected_player"])
        if option == "mute this player":
            c.data["mutelist"].append(c.data["selected_player"])
            c.send("speak "+c.data["selected_player"]+" has been muted")
        if option == "unmute this player":
            c.data["mutelist"].remove(c.data["selected_player"])
            c.send("speak "+c.data["selected_player"]+" has been unmuted")
    if name == "select_an_ranked_option":
        if option == "view this player's warnings":
            index = get_players_index(c.data["selected_player"])
            if index == -1:
                c.send("speak this player isn't online")
                return
            if len(v.clients[index].data["warnings"]) <= 0:
                c.send("speak this player doesn't have any warnings")
                return
            c.send("server_menu view_this_player's_warningss " +
                   "\n".join(v.clients[index].data["warnings"]))

        if option == "warn this player":
            c.send("input type_the_warning_text ")
        if option == "disable this player's chat":
            c.send(
                "input how_many_minutes_should_this_player_be_restricted_from_chatting? ")

        if option == "move this player":
            c.send(
                "input type_the_cordinates_where_this_player_should_move_to._Press_._to_split ")
        if option == "ban this player":
            index = get_players_index(c.data["selected_player"])
            if index == -1:
                c.send("speak this player isn't online")
                return
            send_all("add_buffer_item misc " +
                     v.clients[index].data["name"]+" has been banned from the server")
            v.clients[index].send("ban")
            v.banlist[v.clients[index].data["name"]] = v.clients[index].comp_id
            v.clients[index].disconnect(True)

        if option == "kick this player":
            index = get_players_index(c.data["selected_player"])
            if index == -1:
                c.send("speak this player isn't online")
                return
            send_all("add_buffer_item misc " +
                     v.clients[index].data["name"]+" has been kicked from the server")
            v.clients[index].send("kick")
            v.clients[index].disconnect(True)

    if name[0:35] == "who_do_you_want_to_give_the_weapon_":
        the_weapon = name.replace("who_do_you_want_to_give_the_weapon_", "")
        the_weapon = the_weapon.replace("?", "")
        index = get_players_index(option)
        if index == -1:
            c.send("speak this player isn'tonline at the moment.")
            return
        if get_3d_distance(c.data["x"], c.data["y"], c.data["z"], v.clients[index].data["x"], v.clients[index].data["y"], v.clients[index].data["z"]) > 4 or c.data["map"] != v.clients[index].data["map"]:
            c.send("speak this player is no longer in your range.")
            return
        we =c.get_weapon_in_list(the_weapon)
        if we.level > v.clients[index].data["level"]:
            c.send("speak "+v.clients[index].data["name"] +
                   " can't get this weapon, because their level is to low.")
            return
        if v.clients[index].data["weapons"].count(the_weapon)>=3:
            c.send("speak this player has already the maximum of "+the_weapon+"s")
            return
        c.remove_weapon_instance(we)
        v.clients[index].add_weapon_instance(we)
        if c.data["holster"] == the_weapon:
            c.data["holster"] = ""
        if c.data["weapon"] == the_weapon:
            c.change_weapon(None)

        c.send("get_weapons "+"||".join(c.data["weapons"]) +
               "|n|speak you give "+v.clients[index].data["name"]+" a "+the_weapon)
        v.clients[index].send("get_weapons "+"||".join(v.clients[index].data["weapons"]) +
                              "|n|speak "+c.data["name"]+" just gave you a "+the_weapon)
        send_all(r"player_sound "+v.clients[index].data["name"]+" sounds\\"+we.name+"get.ogg 0|n|player_sound " +
                 v.clients[index].data["name"]+" sounds\\"+we.sort+"get.ogg 0|n|player_sound "+c.data["name"]+" sounds\\give.ogg 0")

    dic = list(c.inventory.keys())
    if len(dic) == 0:
        return
    try:
        iname = dic[c.invpos]
    except:
        return
    if name == "who_do_you_want_to_give_"+iname+"?":
        index = get_players_index(option)
        if index == -1:
            c.send("speak this player isn'tonline at the moment.")
            return
        c.send("input how_many_"+iname+"_would_you_like_to_give_to_"+option+" ")


def input_answer(c, name, input):
    if name.startswith("how_many_skill_points_do_you_want_to_invest_in_to_the_"):
     skill_name=name.replace("how_many_skill_points_do_you_want_to_invest_in_to_the_","")
     skill_name = skill_name.removesuffix("_skill?")
     skill_name=skill_name.replace("_"," ")
     if not skill_name in c.skill_data:
      return
     amount=-1
     try:
      amount=int(input)
     except:
      c.send("speak input isn't valid")
      return
     if amount<1 or amount>c.account_inv_check("joker_skill_point"):
      c.send("speak input isn't valid")
      return
     c.skill_data[skill_name]["skill_points"]+=amount
     c.give_account("joker_skill_point",amount*-1)
     c.send("play_sound jokerpoint.ogg 0 0 0 1 0")

    if name == "type_the_cordinates_where_this_player_should_move_to._Press_._to_split":
        cordinates_text = input.split(".")
        if len(cordinates_text) < 3:
            c.send("speak you haven't fill in all cordinates. ")
            return
        cordinates = []
        try:
            for i in cordinates_text:
                cordinates.append(int(i))
        except:
            c.send("speak input isn't valid")
            return
        index = get_players_index(c.data["selected_player"])
        if index == -1:
            c.send("speak this player isn't online")
            return
        v.clients[index].data["x"] = cordinates[0]
        v.clients[index].data["y"] = cordinates[1]
        v.clients[index].data["z"] = cordinates[2]
        v.clients[index].send("go "+str(v.clients[index].data["x"])+" "+str(
            v.clients[index].data["y"])+" "+str(v.clients[index].data["z"]))
        send_all("move_player "+v.clients[index].data["name"]+" "+str(v.clients[index].data["x"])+" "+str(
            v.clients[index].data["y"])+" "+str(v.clients[index].data["z"]))
        c.send("speak moved")
        log_file_path = os.path.join(
        "logs", "admin actions", "moves.log")
        v.add_log_file(log_file_path, c.data["name"]+" moved "+v.clients[index].data["name"]+" to "+str(cordinates[0])+", "+str(cordinates[1])+", "+str(cordinates[2])+" on map "+v.clients[index].data["map"]+" on "+get_current_date()+" "+get_current_time())

    if name == "type_the_cordinates_you_want_to_move_to._Press_a_period_to_split_it._An_example_could_be_0.0.0_to_move_your_self_to0,_0,_0":
        cordinates_text = input.split(".")
        if len(cordinates_text) < 3:
            c.send("speak you haven't fill in all cordinates. ")
            return
        cordinates = []
        try:
            for i in cordinates_text:
                cordinates.append(int(i))
        except:
            c.send("speak input isn't valid")
            return
        c.data["x"] = cordinates[0]
        c.data["y"] = cordinates[1]
        c.data["z"] = cordinates[2]
        c.send("go "+str(c.data["x"])+" " +
               str(c.data["y"])+" "+str(c.data["z"]))
        send_all("move_player "+c.data["name"]+" "+str(c.data["x"]
                                                       )+" "+str(c.data["y"])+" "+str(c.data["z"]))
        c.send("speak moved")

    if name == "how_many_minutes_should_this_player_be_restricted_from_chatting?":
        try:
            minutes = int(input)
            if minutes <= 0:
                c.send("speak invalid input")
                return
        except:
            c.send("speak input isn't valid")
            return
        if  c.data["selected_player"] not in v.mute_players:
            v.mute_players.append(c.data["selected_player"])
        index = get_players_index(c.data["selected_player"])
        if index > -1:
            v.clients[index].data["org_mutetime"] = minutes*60000
            v.clients[index].mutetimer.restart()
            c.send("speak succesfully muted")

    if name == "type_the_warning_text":
        player_name = c.data["selected_player"]
        index = get_players_index(player_name)
        if index == -1:
            c.send("speak this player isn't online")
            return
        v.clients[index].data["warnings"].append(
            c.data["name"]+" gave this player a warning: "+input+": send on "+str(get_current_date())+" "+str(get_current_time()))
        v.clients[index].send("add_buffer_item important this is an official warning from the staff: " +
                              input+"|n|buffer_sound important warn.ogg 0 0 0 1 0")
        c.send("speak your warning has been sent")

    if name == "type_the_password_of_the_match_you_would_like_to_join":
        if c.losing_loot == False:
            c.send(
                "speak can't go in a match with a magical_reappearance in use|n|last_server_menu")
            return
        exsists = match.exsist_match(input)
        if exsists:
            exsists.players.append(c.data["name"])
            c.store_data()
            c.match_id = exsists.id
            if exsists.status == "waiting" and len(exsists.players) >= exsists.needed_players:
                exsists.start()

        else:
            c.send("speak no match found")
    if name == "what_should_be_the_password_for_this_match_to_allow_players_to_join?":
        if c.losing_loot == False:
            c.send(
                "speak can't go in a match with a magical_reappearance in use|n|last_server_menu")
            return
        exsists = match.exsist_match(input)
        if exsists:
            c.send("speak there is already a match with this password")
            return
        m = match.match("1v1_match", c.data["name"])
        m.friendly = True
        m.password = input
        v.matches.append(m)
        c.send("start_match")

    if name == "type_the_map_name_for_your_new_map":
        try:
            mapdata = """
platform -10000 10000 -10000 10000 0 0 concrete1
"""
            f = open("maps/"+input.replace(" ", "_")+".txt", "w")
            f.write(mapdata)
            f.close()
            c.send("speak the map "+input+" has been created")

        except:
            c.send(" speak error with creating the map")

    if name == "type_the_text_of_the_team_note":
        tindex = teams.get_teams_index(teams.get_team(c.data["name"]))
        if tindex > -1:
            v.teams[tindex].data["notes"][input] = {
                "owner": c.data["name"],
                "date": admin_message.get_time()
            }
            v.teams[tindex].send(
                "speak a team note has been placed by "+c.data["name"])
    if name == "type_your_new_email_address":
        c.data["mail"] = input
        c.send("speak email address has been changed to "+input)

    if name == "how_many_"+c.data["take_item"]+"s_do_you_want_to_take?":
        try:
            extra = int(input)
            if extra <= 0:
                c.send("speak invalid input")
                return
        except:
            c.send("speak input isn't valid")
            return
        cx, cy = rotation.move(c.data["x"], c.data["y"], c.data["facing"])
        id = map.get_object(cx, cy, c.data["z"], c.data["map"])
        o = map.get_objects_index(id)
        if o == "" or map.objects[o].actif == False and map.objects[o].name != "locker":
            c.send("speak you aren't standing in front of a locker.")
            return
        if map.objects[o].data["opened"] == False:
            c.send(
                "speak the door of the locker is closed, so you can't take items out of it.")
            return
        old_amount = 0
        try:
            old_amount = map.objects[o].loot[c.data["take_item"]]
        except:
            pass
        if old_amount < extra:
            c.send("speak there isn't that much in the locker of that item.")
            return
        if c.data["take_item"][0:7] != "weapon_":
            try:
                my_amount = c.inventory[c.data["take_item"]]
            except:
                my_amount = 0
            if extra+my_amount > v.max_items[c.data["take_item"]]:
                c.send("speak you can't have so much of that item in your belt.")
                return
        map.objects[o].loot[c.data["take_item"]] = old_amount-extra
        if c.data["take_item"][0:7] != "weapon_":
            send_all(r"player_sound "+c.data["name"]+" sounds\\lockertakeitem.ogg 0|n|player_sound " +
                     c.data["name"]+" sounds\\"+c.data["take_item"]+"get.ogg 0")
            c.give(c.data["take_item"], extra)
        else:
            the_weapon = c.data["take_item"].replace("weapon_", "")
            we = weapons.weapon(the_weapon)
            if we.level > c.data["level"]:
                c.send("speak your level is to low to take this weapon.")
                map.objects[o].loot[c.data["take_item"]] = old_amount
                return
            for i in range(1, extra+1):
                c.data["weapons"].append(the_weapon)
            send_all(r"player_sound "+c.data["name"]+" sounds\\lockertakeweapon.ogg 0|n|player_sound "+c.data["name"] +
                     " sounds\\"+we.sort+"get.ogg 0|n|player_sound "+c.data["name"]+" sounds\\"+the_weapon+"get.ogg 0")
            c.send("get_weapons "+"||".join(c.data["weapons"]))
        for l in map.objects[o].loot:
            if map.objects[o].loot[l] <= 0:
                del map.objects[o].loot[l]
                break
        return
    if name == "type_your_team_chat":
        tindex = teams.get_teams_index(teams.get_team(c.data["name"]))
        if tindex > -1:
            v.teams[tindex].send(
                "add_buffer_item team_chats "+c.data["name"]+" says in the team chat: "+input)
            for cl in v.clients:
                if teams.get_team(c.data["name"]) == teams.get_team(cl.data["name"]):
                    if cl.lobby == True:
                        cl.send("play_sound teamchat" +
                                str(random.randint(1, 3))+".ogg 0 0 0 1 0")
                    send_all(
                        r"player_sound "+cl.data["name"]+" sounds\\teamchat"+str(random.randint(1, 3))+".ogg 0|n|")
    if name == "type_the_name_of_your_new_team":
        team_name = input.replace(" ", "_")
        if len(team_name)<3:
            c.send("speak this team name is to short")
            return
        if len(team_name)>25:
                c.send("speak this team name is to long")
                return
        for f in v.teams:
            if f.name == team_name:
                c.send("speak this name is already in use for an other team.")
                return
        t = teams.team(team_name)
        t.members.append(c.data["name"])
        t.data["leader"] = c.data["name"]
        for r in t.rights:
            t.rights[r].append(c.data["name"])
        v.teams.append(t)
        send_all("add_buffer_item misc the team "+input+" has been created.")
    if name == "how_many_"+c.data["store_item"]+"_do_you_want_to_store_in_the_locker?":
        try:
            extra = int(input)
            if extra <= 0:
                c.send("speak invalid input")
                return
        except:
            c.send("speak input isn't valid")
            return
        cx, cy = rotation.move(c.data["x"], c.data["y"], c.data["facing"])
        id = map.get_object(cx, cy, c.data["z"], c.data["map"])
        o = map.get_objects_index(id)
        if o == "" or c.data["z"] >= map.objects[o].maxz or map.objects[o].actif == False and map.objects[o].name != "locker":
            c.send("speak you aren't standing in front of a locker.")
            return
        if map.objects[o].data["opened"] == False:
            c.send(
                "speak the door of the locker is closed, so you can't store items in it. ")
            return
        old_amount = 0
        try:
            old_amount = map.objects[o].loot[c.data["store_item"]]
        except:
            pass
        if not c.data["store_item"].startswith("weapon_"):
            if c.inventory[c.data["store_item"]] < extra:
                c.send("speak you don'thave enough of that item.")
                return
            if old_amount+extra > v.max_items[c.data["store_item"]]*map.objects[o].data["storage_level"]*2:
                c.send(
                    "speak The locker can't store so many of that item. You have to upgrade the storage capacity to store more items.")
                return
            map.objects[o].loot[c.data["store_item"]] = old_amount+extra
            c.give(c.data["store_item"], extra*-1)
            send_all(r"player_sound " +
                     c.data["name"]+" sounds\\lockerplaceitem.ogg 0")
        else:
            the_weapon = c.data["store_item"].replace("weapon_", "")
            if c.data["weapons"].count(the_weapon) < extra:
                c.send("speak you don't have enough of this weapon.")
                return
            for _ in range(extra):
                c.data["weapons"].remove(the_weapon)
            map.objects[o].loot["weapon_"+the_weapon] = old_amount+extra
            we = weapons.weapon(the_weapon)
            send_all(r"player_sound "+c.data["name"]+" sounds\\lockerplaceweapon.ogg 0|n|player_sound "+c.data["name"] +
                     " sounds\\"+the_weapon+"place.ogg 0|n|player_sound "+c.data["name"]+" sounds\\"+we.sort+"place.ogg 0")
            c.send("get_weapons "+"||".join(c.data["weapons"]))
            if the_weapon == c.data["holster"]:
                c.data["holster"] = ""

            if the_weapon == c.data["weapon"]:
                c.change_weapon(None)

                c.send("set_weapon "+the_weapon)
                send_all("set_player_weapon "+c.data["name"]+" "+c.data["weapon"] +
                         "|n|set_players_silencer "+c.data["name"]+" "+str(c.has_silencer(c.data["weapon"])))

    if name[0:24] == "select_the_time_for_the_":
        option = name.replace("select_the_time_for_the_", "")
        option = option.replace("_event._86400000_is_1_day", "")
        option = option.replace("_", " ")
        try:
            time = int(input)
            event.start_event(option, time)
        except:
            c.send("speak this input isn't legal.")
    if name == "type_your_message_to_"+c.data["selected_player"]:

        playername = c.data["selected_player"]
        index = get_players_index(playername)
        if index == -1:
            c.send("speak this player isn't online")
            return
        if c.data["name"] in v.clients[index].data["mutelist"]:
            c.send("speak "+playername+" has muted you")
            return

        if v.clients[index].data["name"] in c.data["mutelist"]:
            c.send("speak you have muted "+playername)
            return
        message = input.replace("pm "+playername+" ", "")
        v.clients[index].send("add_buffer_item pm private message from " +
                              c.data["name"]+": "+message+"|n|buffer_sound pm pm.ogg 0 0 0 1 0")
        c.send("add_buffer_item pm private message to " +
               v.clients[index].data["name"]+": "+message+"|n|buffer_sound pm pm.ogg 0 0 0 1 0")
        c.data["last_pm"] = v.clients[index].data["name"]
        v.clients[index].data["last_pm"] = c.data["name"]
    if name[0:36] == "type_the_subject_of_the_announcement":
        c.send("input Type_your_message_for_the_announcement_" +
               input.replace(" ", "_")+"._Type_end_in_the_input_box_when_you_are_done. ")
    if name[0:39] == "Type_your_message_for_the_announcement_":
        if input == "end":
            text = name.replace("Type_your_message_for_the_announcement_", "")
            text = text.replace(
                "._Type_end_in_the_input_box_when_you_are_done.", "")
            a = misk.announcement(text, c.data["input"])
            v.announcements.insert(0, a)
            c.data["input"] = ""
            send_all("play_sound announcement.ogg 0 0 0 1 0")
        else:
            name = name.replace("Type_your_message_for_the_announcement_", "")
            c.send("input Type_your_message_for_the_announcement_" +
                   name.replace(" ", "_")+" ")
            try:
                c.data["input"] = c.data["input"]+"\n"+input
            except:
                pass
    if name[0:54] == "Type_the_subject_of_the_staff_message_in_the_category_":
        subject = name.replace(name[0:54], "")
        c.data["smsubject"] = input
        c.send("input Type_your_message_in_the_category_"+subject +
               "._Make_sure_that_you_describe_as_detailed_as_possible_so_that_the_staff_can_help_you_the_best ")
    if name[0:43] == "type_your_message_to_be_send_in_staff_chat_":
        parsed = name.split("_")
        index = admin_message.get_admin_messages_index(
            int(parsed[len(parsed)-1]))
        if index > -1:
            my_name = c.data["name"]
            if v.admin_messages[index].owner != c.data["name"]:
                my_name = "admin"
            v.admin_messages[index].send(
                "add_buffer_item staff_messages a new message has been sent in staff message "+str(v.admin_messages[index].name))
            v.admin_messages[index].add_message(my_name, input)
            if c.data["name"] == v.admin_messages[index].owner:
                v.admin_messages[index].play_sound("send", "owner")
                v.admin_messages[index].play_sound("receive", "admin")
            else:
                v.admin_messages[index].play_sound("send", "admin")
                v.admin_messages[index].play_sound("receive", "owner")
            v.admin_messages[index].read = []
            v.admin_messages[index].read.append(c.data["name"])
            element = v.admin_messages.pop(index)
            v.admin_messages.insert(0, element)
    if name[0:34] == "Type_your_message_in_the_category_":
        name = name.replace("Type_your_message_in_the_category_", "")
        name = name.replace(
            "._Make_sure_that_you_describe_as_detailed_as_possible_so_that_the_staff_can_help_you_the_best", "")
        a = admin_message.admin_message(
            c.data["smsubject"], input, c.data["name"], name)
        v.admin_messages.insert(0, a)
        a.read.append(c.data["name"])
        a.play_sound("create", "admin")
        a.play_sound("send", "owner")
        c.send("speak a message with the subject " +
               c.data["smsubject"]+" has been send to the staff.")
    if "_give_to_" in name:
        dic = list(c.inventory.keys())
        iname = dic[c.invpos]
        playername = name.replace(
            "how_many_"+iname+"_would_you_like_to_give_to_", "")
        index = get_players_index(playername)
        if index < -1:
            c.send("speak this player isn't online at the moment.")
            return
        if get_3d_distance(c.data["x"], c.data["y"], c.data["z"], v.clients[index].data["x"], v.clients[index].data["y"], v.clients[index].data["z"]) > 4 or c.data["map"] != v.clients[index].data["map"]:
            c.send("speak this player is no longer in your range.")
            return
        try:
            amount = int(input)
        except:
            c.send("speak input isn't valid")
            return
        if amount <= 0:
            c.send("speak you can't give 0 or less items to someone")
            return

        if c.inventory[iname] < amount:
            c.send("speak you haven't enough of this item.")
            return
        v.clients[index].give(iname, amount)
        c.give(iname, amount*-1)
        send_all(r"player_sound "+v.clients[index].data["name"]+" sounds\\" +
                 iname+"get.ogg 0|n|player_sound "+c.data["name"]+" sounds\\give.ogg 0")
        c.send("add_buffer_item misc you give " +
               str(amount)+" "+iname+" to "+playername)
        f = 0
        if iname == "grenade":
            for g in v.grenades:
                if g.owner == c.data["name"]:
                    g.owner = v.clients[index].data["name"]
                    f = 1
        if f == 0:
            v.clients[index].send(
                "add_buffer_item misc "+c.data["name"]+" just gave you "+str(amount)+" "+iname)
        else:
            v.clients[index].send(
                "add_buffer_item misc watch out! "+c.data["name"]+" just gave you an active "+iname)
    if name == "type_the_text_of_your_notify":
        send_all(
            "buffer_sound important alert.ogg 0 0 0 1 0|n|add_buffer_item important "+input)
    if name == "type_your_staff_chat._Press_enter_when_you_are_done.":
        for f in v.clients:
            if f.data["admin"] == 1 or f.data["moderator"] == 1 or f.data["builder"] == 1:
                f.send("add_buffer_item staff_chats " +
                       c.data["name"]+" says in the staff chat: "+input+"|n|buffer_sound staff_chats staffchat.ogg")
        log_file_path = os.path.join(
            "logs", "staff chats", str(get_current_date())+".log")
        v.add_log_file(
            log_file_path, c.data["name"]+" says in the staff chat: "+input+": send on "+str(get_current_time()))


def skill_set(c):
    options = []
    i = 0
    for s in c.skill_data:
        sk = skills.skill(s)
        if c.skill_data[s]["unlocked"] == False:
            continue
        if c.skill_data[s]["active"] == True and s not in c.data["edit_skills"] or c.skill_data[s]["active"] == False and s in c.data["edit_skills"]:
            i += sk.education_points
            if sk.weapon_sort == "":
                options.append(s+": active.  This skill requires " +
                               str(sk.education_points)+" education points.")
            else:
                options.append(s+": active.  This mastery requires "+str(sk.education_points) +
                               " education points and it belongs to the "+sk.weapon_sort+" weapon category.")
        else:
            if sk.weapon_sort == "":
                options.insert(0, s+": inactive. This skill requires " +
                               str(sk.education_points)+" education points.")
            else:
                options.insert(0, s+": inactive.  This mastery requires "+str(sk.education_points) +
                               " education points and it belongs to the "+sk.weapon_sort+" weapon category.")

    if i > 0:
        options.append("reset all your education points")
    options.append("you will use "+str(i)+" out of the " +
                   str(c.data["level"])+" education points when confirming the selected skills.")
    options.append("done")
    return options


def change_skills(c, skill_data):
    for s in skill_data:
        if s in c.data["edit_skills"]:
            if skill_data[s]["active"] == True:
                skill_data[s]["active"] = False
            else:
                skill_data[s]["active"] = True
    return skill_data


def server_mega_menu_answer(c, name, option, given_data):
    data = {}
    if given_data != "":
        lines = given_data.split("\n")
        for l in lines:
            f = l.split(":")
            try:
                data[f[0].replace("_", " ")] = f[1]
            except:
                pass
    if name == "are_you_sure_you_want_to_delete_your_account?":
        result = int(data["Yes. I am sure"])
        if result == 1:
            c.send("kick")
            send_all(
                "add_buffer_item important "+c.data["name"]+" has deleted their account.|n|buffer_sound important offline_special.ogg 0 0 0 1 0")
            v.clients.remove(c)
            os.remove("players/"+c.data["name"]+".plr")

        else:
            c.send("server_mega_menu are_you_sure_you_want_to_delete_your_account? dlg:Are you sure you want to delete your account? This can't be undone by the staff.\ncheck_box:0:Yes. I am sure\nbutton:delete my account")
    if name == "are_you_sure_you_want_to_delete_your_team?":
        result = int(data["Yes. I am sure"])
        if result == 1:
            index = teams.get_teams_index(teams.get_team(c.data["name"]))
            if index > -1:
                v.teams[index].remove()
                v.teams.remove(v.teams[index])

                c.send("speak the team has been canceled.")
        else:
            c.send("server_mega_menu are_you_sure_you_want_to_delete_your_team? dlg:Are you sure you want to delete your team? This can't be undone by the staff.\ncheck_box:0:Yes. I am sure\nbutton:delete my team")

    if name[0:22] == "select_the_rights_for_":
        player_name = name.replace("select_the_rights_for_", "")
        change = 0
        index = teams.get_teams_index(teams.get_team(player_name))
        if index > -1:
            for t in v.teams[index].rights:
                for d in data:
                    if t == d:
                        result = int(data[d])
                        if result == 0:
                            if player_name in v.teams[index].rights[t]:
                                change = 1
                                v.teams[index].rights[t].remove(player_name)
                        else:
                            if player_name not in v.teams[index].rights[t]:
                                change = 1
                                v.teams[index].rights[t].append(player_name)
            if change == 1:
                v.teams[index].send("add_buffer_item team the rights of "+player_name +
                                    " have been changed|n|play_sound teamnotifymisc2.ogg 0 0 0 1 0")
