import v
v.get()

class skill():
 def __init__(self,name):
  self.name=name
  self.needed_skill_points=[50,200,500,1000,1800,3000,5000]
  self.level_names=["bronze","silver","gold","platinum","diamond","master 1","master 2","master 3"]
  self.cool_downtime=0
  if self.name=="jump endurance":
   self.permanent=True
   self.max_level=5	
   self.unlocklevel=23
   self.education_points=15
  self.weapon_sort=""
  if self.name=="Eyes training":
   self.permanent=True
   self.max_level=5
   self.unlocklevel=10
   self.education_points=5
  if self.name=="Learn how to swim":
   self.permanent=True
   self.max_level=5
   self.unlocklevel=5
   self.education_points=1
  if self.name=="beeing a docter":
   self.permanent=True
   self.max_level=5
   self.unlocklevel=43
   self.education_points=15
  if self.name=="Learn how to climb":
   self.permanent=True
   self.max_level=5
   self.unlocklevel=7
   self.education_points=2
  if self.name=="landing knowledge":
   self.permanent=True
   self.max_level=5
   self.unlocklevel=13
   self.education_points=10
  if self.name=="knife throw":
   self.cool_downtime=10000
   self.permanent=False
   self.max_level=8
   self.unlocklevel=20
   self.education_points=5
   self.weapon_sort="melee"

  if self.name=="machete swing":
   self.cool_downtime=25000
   self.permanent=False
   self.max_level=8
   self.unlocklevel=16
   self.education_points=15
   self.weapon_sort="melee"

  if self.name=="sprint":
   self.cool_downtime=60000
   self.permanent=False
   self.max_level=5
   self.unlocklevel=25
   self.education_points=20
  if self.name=="careful aiming":
   self.cool_downtime=60000
   self.permanent=False
   self.max_level=5
   self.unlocklevel=47
   self.education_points=15
  if self.name=="infrared scanner interference":
   self.cool_downtime=120000
   self.permanent=False
   self.max_level=5
   self.unlocklevel=35
   self.education_points=25
  if self.name=="grenade knowledge":
   self.cool_downtime=5000
   self.permanent=False
   self.max_level=5
   self.unlocklevel=8
   self.education_points=5

  if self.name=="extended pistol clip":
   self.permanent=True
   self.max_level=8
   self.unlocklevel=6
   self.education_points=4
   self.weapon_sort="pistol"
  if self.name=="rapid fire":
   self.permanent=False
   self.max_level=8
   self.unlocklevel=33
   self.education_points=10
   self.weapon_sort="pistol"
   self.cool_downtime=60000

  if self.name=="steady aim":
   self.permanent=True
   self.max_level=8
   self.unlocklevel=5
   self.education_points=5
   self.weapon_sort="shotgun"
  if self.name=="DMR precision":
   self.permanent=True
   self.max_level=8
   self.unlocklevel=28
   self.education_points=15
   self.weapon_sort="marksman_rifle"

  if self.name=="recoil mastery":
   self.permanent=True
   self.max_level=8
   self.unlocklevel=11
   self.education_points=10
   self.weapon_sort="sub_machine_gun"
  if self.name=="SMG experience":
   self.permanent=True
   self.max_level=8
   self.unlocklevel=38
   self.education_points=20
   self.weapon_sort="sub_machine_gun"

  if self.name=="sniper mastery":
   self.permanent=True
   self.max_level=8
   self.unlocklevel=15
   self.education_points=10
   self.weapon_sort="sniper_rifle"
  if self.name=="holster augmentation":
   self.permanent=True
   self.max_level=3
   self.unlocklevel=45
   self.education_points=20
  if self.name=="sharpshooter mastery":
   self.permanent=True
   self.max_level=8
   self.unlocklevel=17
   self.education_points=15
   self.weapon_sort="assault_rifle"

 def get_description(self):
  final="no description found"
  with open("descriptions.txt", 'r') as f:
   items=f.read().split("\n")
   for i in items:
    if i[0:len(self.name)]==self.name:
     final=i.replace(self.name+":","")
  return final

