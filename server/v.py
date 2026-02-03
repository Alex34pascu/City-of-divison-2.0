import queue
import pygame

import time
import select
import zlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

def compress_data(data):
    """Comprimeert de data met zlib."""
    return zlib.compress(data.encode())

def decompress_data(data):
    """Probeer de data te decomprimeren. Als het geen gecomprimeerde data is, retourneer dan de originele data."""
    try:
        # Probeer de data te decomprimeren
        decompressed_data = zlib.decompress(data)
        return decompressed_data.decode()  # Return de gedecomprimeerde string
    except zlib.error:
        # Als decompressie niet werkt, geef dan de originele data terug
        return data

def aes_cipher(text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(text.encode(), AES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return encrypted_text

def aes_decipher(encrypted_text, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = cipher.decrypt(encrypted_text)
    unpadded_text = unpad(decrypted_text, AES.block_size)
    return unpadded_text.decode()



import sd
import os
import math
import timer
import numpy as np
import socket
def get():
 global packet_printing
 packet_printing=False
 global weapon_names
 weapon_names=["knife","machete","flail","SVD_Dragunov","barrett_M107A1","FN_509_tactical","beretta92A1","colt_m1911","ruger_redhawk","ARX160","ak47","fn_p90","fn_f2000","mp5","MP7","m2_browning","hk_mg4","Winchester_Model_24","remington870xs","Benelli_M4","dsr50","AR10","smith_n_wesson_model29"]

 global store_items
 store_items={
"weapon_m2_browning": {
"amount": 1,
"price": 3,
},
"50bmg_round": {
"amount": 50,
"price": 1,
},
"spike_trap": {
"amount": 1,
"price": 3,
},
"tripwire": {
"amount": 1,
"price": 2,
},
"barricade": {
"amount": 1,
"price": 1,
},
"grenade": {
"amount": 4,
"price": 1,
},
"bulletproof_vest": {
"amount": 1,
"price": 1,
},
"helmet": {
"amount": 2,
"price": 1,
},
}

 global packet_key
 packet_key=b"hallo goars jaja"
 global matches
 matches=[]
 global all_quests
 all_quests=["chapter 1 part 1","chapter 1 part 2","chapter 1 part 3","chapter 2 part 1","chapter 2 part 2","chapter 2 part 3","chapter 2 part 4","chapter 3 part 1","chapter 3 part 2","chapter 3 part 3","chapter 3 part 4","chapter 4 part 1","chapter 4 part 2","chapter 5 part 1","chapter 5 part 2","chapter 6 part 1","chapter 6 part 2","chapter 6 part 3","chapter 6 part 4","chapter 6 part 5","chapter 6 part 6"]
 global password_resets
 password_resets={}

 global max_level
 max_level=50
 global freeze
 freeze=False
 global min_version
 min_version="1.55"
 global event_types
 event_types=["examine objects","kill players","making head shots","kill the VIP","weapons competition","destroy objects"]
 global mute_players
 mute_players=[]
 global admin_list
 admin_list={}
 global betalist
 betalist=["032E02B4-0499-0559-0406-E20700080009","34444335-3830-4A36-474A-4A4A38304435","013761D4-7772-2320-1106-233845000000","035E02D8-04D3-0595-E806-CC0700080009","25F0E8A9-CA10-394B-A9C3-68CBC660008C","C249F6F9-7E85-ED11-8C90-7C5758D41FAC","153A85D4-0712-6BB5-F69C-E89C250CCADD"]
 global developerlist
 developerlist=["DA89B1AC-339E-4BD5-83C4-3EC06987D504","35AC7051-A435-11EC-80F1-88A4C2F727F9","32444335-3830-5738-4B31-315738304435","4C4C4544-0044-3310-8058-B8C04F524C33"]
 global release
 release="d"
 global restarting
 restarting=False
 global restarttimer
 restarttimer=timer.timer()

 global ranked_events
 ranked_events=[]
 global events
 events=[]
 global clients
 clients=[]
 global teams
 teams=[]
 global object_presets
 object_presets=[]

 global packet_queue
 packet_queue= queue.Queue()

 global s
 s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

 global traps
 traps=[]
 global shipments
 shipments=[]
 global bullets
 bullets=[] 
 global bodyfalls
 bodyfalls=[] 
 global c4s
 c4s=[]
 global RCEs
 RCEs=[]

 global grenades
 grenades=[]

 global heals
 heals=[]
 global banlist
 banlist={}
 global announcements
 announcements=[]
 global admin_messages
 admin_messages=[]
 global prices
 prices={
"bronze chest": 75,
"silver chest": 100,
"golden chest": 150,
"platinum chest": 250,
}
 global max_items
 max_items={
"9mm_ammo": 150,
"50bmg_round": 250,
"12_gauge_ammo": 80,
"5.7x28mm_ammo": 250,
"5.56mm_ammo": 200,
"4.6x30mm_ammo": 200,
"7.62mm_ammo": 90,
"45ACP_ammo": 100,
".44_magnum_ammo": 90,
"flash_grenade": 3,
"grenade": 4,
"sub_machine_gun_silencer": 5,
"locker": 1,
"spike_trap": 5,
"tripwire": 5,
"barricade": 5,

"metal_fortress_construction_kit": 1,
"metal_sheat": 6,
"metal_fortress": 1,
"team_phone": 1,
"first_aid_kit": 1,
"RCE_package": 1,
"R_C_E": 2,
"RCE_controller": 1,

"bulletproof_vest": 1,
"helmet": 2,
"ladder": 1,
"c4": 2,
"bandage": 3,
"welding_machine_battery": 5,
"welding_machine": 1,
"Painkiller_injection": 4,
"tool_box": 1,
"metal_piece": 10,
"plastic_piece": 10,
"rubber_piece": 10,
"glass_piece": 10
}
 global item_categorys
 item_categorys={
"9mm_ammo": "ammo",
"50bmg_round": "ammo",
"45ACP_ammo": "ammo",
".44_magnum_ammo": "ammo",
"12_gauge_ammo": "ammo",
"5.7x28mm_ammo": "ammo",
"5.56mm_ammo": "ammo",
"4.6x30mm_ammo": "ammo",
"7.62mm_ammo": "ammo",
"flash_grenade": "explosives",
"grenade": "explosives",
"locker": "misc",
"barricade": "misc",
"spike_trap": "misc",
"tripwire": "misc",

"metal_fortress_construction_kit": "misc",
"metal_sheat": "misc",
"metal_fortress": "misc",
"team_phone": "misc",

"RCE_package": "explosives",
"R_C_E": "explosives",
"RCE_controller": "explosives",

"helmet": "misc",
"bulletproof_vest": "misc",
"ladder": "misc",
"sub_machine_gun_silencer": "misc",
"first_aid_kit": "medical",
"c4": "explosives",
"bandage": "medical",
"welding_machine_battery": "misc",
"welding_machine": "misc",
"tool_box": "attachments",
"metal_piece": "attachments",
"plastic_piece": "attachments",
"rubber_piece": "attachments",
"Painkiller_injection": "medical", 
"glass_piece": "attachments",
}

 global languages
 languages=["English","Dutch","German","French","Spanish","Arabick","Turkish","Italian","Portuguese","Persian","Hindi","Polish","Romanian","Mandarin (Chinese)","Russian","Ukrainian","Thai","Vietnamese","Urdu"]
 languages.sort()
 languages.insert(0,"free channel")
 languages.insert(0,"disable chat")

 global weekend
 weekend=is_weekend()

def get_tile_type(name,tiles=[]):
 if name=="":
     return ""
 i=""
 if name.startswith("dirt") or name.startswith("sand"):
  i="dirt"
 elif name.startswith("grass") or name.startswith("tree"):
  i="grass"
 elif name.startswith("gravel")  or name.startswith("rocks"):
  i="gravel"
 elif name=="swim" or name=="shallow" or name.startswith("water"):
  i="water"
 elif name[0:5]=="metal" or name[0:6]=="ladder"  or name=="beam":
  i="metal"
 else:
  i="generic"
 if i in tiles:
  return i
 else:
  return "generic"


def get_wall_tile_type(name,tiles=[]):
 i=""
 if name[0:9]=="wallmetal" or name=="wallrail" or name=="wallfence":
  i="metal"
 elif name[0:9]=="wallbrush":
  i="bush"
 elif name=="wallfurniture":
  i="furniture"
 elif name=="wallstone2" or name.startswith("wallrock"):
  i="stone2"
 elif name=="wallcabinet":
  i="cabinet"
 elif name[0:8]=="wallwood" or name=="wallbuilding":
  i="wood"
 else:
  i="generic"
 if i in tiles:
  return i
 else:
  return "generic"

def get_description(name):
 final=""
 with open("descriptions.txt", 'r') as f:
  items=f.read().split("\n")
  for i in items:
   if i[0:len(name)+1]==name+":":
    return i.replace(name+":","")
 return final

def get_list_in_text(list):
 if len(list)==0:
  return ""
 if len(list)==1:
  return list[0]
 final=""
 for l in list:
  if list.index(l)==len(list)-1:
   final=final+"and "+l
  elif list.index(l)==0:
   final=final+l+" "
  else:
   final=final+", "+l+" "
 return final


def get_time_in_mm(mm):
 final={
"second": 0,
"minute": 0,
"hour": 0,
"day": 0,
"week": 0,
"month": 0,
}
 final["second"]=math.floor(mm/1000)
 final["minute"]=math.floor(final["second"]/60)
 final["second"]-=final["minute"]*60
 final["hour"]=math.floor(final["minute"]/60)
 final["minute"]-=final["hour"]*60
 final["day"]=math.floor(final["hour"]/24)
 final["hour"]-=final["day"]*24
 final["week"]=math.floor(final["day"]/7)
 final["day"]-=final["week"]*7
 final["month"]=math.floor(final["week"]/4)
 final["week"]-=final["month"]*4
 good={}
 for f in final:
  if final[f]!=0:
   good[f]=final[f]
 final=good
 end=""
 text_list=[]
 for f in reversed(final):
  i=f
  if final[f]>1:
   i=i+"s"
  text_list.append(str(final[f])+" "+i)
 end=get_list_in_text(text_list)
 if end=="":
  end="no time at all"
 return end

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP-server configuratie
smtp_server = "fire-gaming.eu"
smtp_port = 465  # Voor TLS, gebruik 465 voor SSL
smtp_user = "noreply@fire-gaming.eu"
smtp_password = "Jekuntnietreagerenbitch!"

def mail(to_email,subject,body):
 from_email = "noreply@fire-gaming.eu"

 msg = MIMEMultipart()
 msg['From'] = from_email
 msg['To'] = to_email
 msg['Subject'] = subject

 msg.attach(MIMEText(body, 'plain'))

 try:
     server = smtplib.SMTP_SSL(smtp_server, smtp_port)
     server.login(smtp_user, smtp_password)
     text = msg.as_string()
     server.sendmail(from_email, to_email, text)
     return "succes"
 except Exception as e:
     return e
 finally:
     server.quit()

import datetime

def is_weekend():
    return True
    today = datetime.datetime.today().weekday()
    if today in [4, 5, 6]:
        return True
    return False


def calculate_sum(list):
 total = sum(list)
 try:
  return total / len(list)
 except:
  return 0

def add_log_file(path, text):
    key = b"0010011001001010"
    # Voeg een newline toe aan de tekst voordat deze wordt versleuteld
    text_with_newline = text + "\n"
    encrypted_text = aes_cipher(text_with_newline, key)

    dir_name = os.path.dirname(path)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)  # Maak ontbrekende map(pen) aan
    
    with open(path, "ab") as file:  # Open het bestand in 'append binary'-modus
        file.write(encrypted_text)

def read_log_file(file_path, key):
    """
    Leest een logfile, decodeert de inhoud en retourneert de normale tekst.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Bestand niet gevonden: {file_path}")

    with open(file_path, "rb") as file:  # Lees in binaire modus
        encrypted_data = file.read()  # Lees alle gegevens in één keer

    # Controleer dat de gegevens een veelvoud van de blokgrootte zijn
    if len(encrypted_data) % AES.block_size != 0:
        raise ValueError("Versleutelde gegevens zijn corrupt of onvolledig.")

    # Decodeer de volledige gegevens
    decrypted_data = aes_decipher(encrypted_data, key)

    # Gebruik splitlines om regels te splitsen (ondersteunt ook \r\n en \n)
    return decrypted_data.splitlines()


def send_packet_to_clients(message,send_clients,map=""):
 org_message=message
 for c in send_clients:
  if org_message[0:10]=="play_sound" and map==c.data["map"] or org_message[0:10]!="play_sound" or map=="":
   try:
    c.send(message)
   except:
    c.disconnect()

client_send_clock = pygame.time.Clock()
def send_packetloop():
  while not packet_queue.empty():
   client, message = packet_queue.get()
   if message[0:11]=="server_menu" or message[0:16]=="last_server_menu":
    client.sended=True
   else:
    client.sended=False
   if message!="":
    message=message+"|n|"
#   message=v.compress_data(message).hex()
    message=aes_cipher(message,client.key).hex()

    message=message+"|end|"
    message=message.encode()
    try:

     if client.writable:
      if client.s and not client.s._closed:
       client.s.sendall(message)
    except:
     try:
      client.disconnect()
     except:
      clients.remove(client)



def projectilesloop():
 while 1:
  for b in bullets:
   b.run()
