import sd
import combine_sounds as cs
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 speatch.output(text)
list=["abandoned_place2","birds1","birds2","birds3","birds4","birds5","birds6","birds7","birds8","birds9","birds10","birds11","birds12","building","buzzy_parkingstructure","calm1","calm2","calm3","canal1","forest1","forest2","landscape1","landscape2","landscape3","smallpark","stream","stream1","stream2","stream3","waves","building2","water_under_bridge","fountain","abandoned_place","birds13","road","menumusic","c4dist","c4explode","concrete7step1","death","fountaindestroy","grenadedist","grenadeexplode1","grenadeexplode2","grenadeexplode3","Smallpark","treedestroy2","treedestroy3","waterexplode1","waterexplode2","waterexplode3","wallmetal3","underwateramb","printer","monitor1","updatefound","menumusicintro","lobbymusic","lobbymusicintro","miscmusic1","miscmusic1intro","skillunlockchest","menuclick","menuopen","menuclose","menuenter","menuedge","ditch","lockerupgradesecurity","lockerrepair","lockerexplodedist","lockerexplode","bridgedestroy3","bridgedestroy2","bridgedestroy1","first_aid_kituse","AD_cutseen_intro1","AD_cutseen_intro2","AD_cutseen_jack1","AD_cutseen_jack2","cutseen_jack2","AD_cutseen_The_factory1","AD_cutseen_The_factory2","cutseen_intro1","cutseen_intro2","cutseen_jack1","cutseen_The_factory1","cutseen_The_factory2","spin wheel_of_fortune","cutseen_the_factory3","AD_cutseen_The_factory3","srvrestart","wheel_of_fortunespin","AD_cutseen_jack3","AD_cutseen_the_quarry","cutseen_jack3","cutseen_the_quarry","matchfound","matchnotfound","matchsearch","matchwin","weaponroommusic","weaponroommusicintro","rmstart","rmstart_clock","rmstart_hearbeat","abandoned_place3","abandoned_place4","city1","city2","countdown","metal_fortressbuild","intruderalarm","intruderalarmphone","shipmentdropdist","flash_grenadeimpact","AD_cutscene_final1","AD_cutscene_final2","AD_cutscene_final3","AD_cutscene_final4","cutscene_final1","cutscene_final2","cutscene_final3","cutscene_final4","vehiclealarm1","vehiclealarm2","vehiclealarm3","vehiclealarm4","vehiclealarm5","vehiclealarm6","vehicleexplosiondist","vehicleexplosionexplode2","vehicleexplosionexplode3","watertankdestroy","headbudimpact","birds14","bunker","calm4","canyion","rockscanyon","rockscanyon1","rockscanyon2","rocksquarry","rocksquarry1","rocksquarry2","watertankloop","wind","vehicleexplosiondist1","vehicleexplosiondist2","vehicleexplosiondist3","waterfallloop","waterfallloop2","waves2","gravelexplode1","gravelexplode2","gravelexplode3","vehicleexplosionexplode1","vehicleexplosionexplode2","vehicleexplosionexplode3","dripping_water1","dripping_water2","dripping_water3","sewer","smallpipe","largepipe","bleeding"]
looplist=[]
for l in list:
 looplist.append(l+".ogg")
from Cryptodome.Cipher import AES
import os
key = b"001003001%%.1001"  # Hier wordt een willekeurige 32-byte sleutel gegenereerd

total_list=[]

def encrypt_file(input_file, output_file, key):
    chunk_size = 64 * 1024  
    cipher = AES.new(key, AES.MODE_ECB)
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        while True:
            chunk = infile.read(chunk_size)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += b' ' * (16 - len(chunk) % 16)  
            outfile.write(cipher.encrypt(chunk))

def encrypt_audio(input_file, output_file, key):
    chunk_size = 64 * 1024  
    cipher = AES.new(key, AES.MODE_ECB)

    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        while True:
            chunk = infile.read(chunk_size)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += b' ' * (16 - len(chunk) % 16)  
            outfile.write(cipher.encrypt(chunk))


mapnaam = "audio"  

if os.path.exists(mapnaam):
    bestanden_in_map = os.listdir(mapnaam)

    bestanden = [bestand for bestand in bestanden_in_map if os.path.isfile(os.path.join(mapnaam, bestand))]

    for bestand in bestanden:
        speak(bestand)
        if bestand in looplist:
         encrypt_audio(r"audio\\"+bestand,r"sounds\\"+bestand.replace(".ogg",".bin"), key)
         total_list.append(bestand)
        else:
         try:
          f=cs.add_silence(r"audio\\"+bestand,"nsound.ogg")
          if f==True:
           encrypt_audio("nsound.ogg",r"sounds\\"+bestand.replace(".ogg",".bin"), key)
           total_list.append(bestand)
          else:
           encrypt_audio(r"audio\\"+bestand,r"sounds\\"+bestand.replace(".ogg",".bin"), key)
           total_list.append(bestand)

         except:
          encrypt_audio(r"audio\\"+bestand,r"sounds\\"+bestand.replace(".ogg",".bin"), key)
         total_list.append(bestand)
else:
    print(f"De map '{mapnaam}' bestaat niet.")

sd.save("sound_list",total_list,"list.dat")
encrypt_file("list.dat", "sounds\sound_list.dat", key)
os.remove("list.dat")
