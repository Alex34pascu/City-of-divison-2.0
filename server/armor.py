armor_types=["helmet","bulletproof_vest"]

class armor():
 def __init__(self,name):
  self.name=name
  if self.name=="helmet":
   self.type="head"
   self.melee_damage=1.0
   self.small_damage=0.1
   self.large_damage=0.1
   self.health=1000
  elif self.name=="bulletproof_vest":
   self.type="body"
   self.melee_damage=1.0
   self.small_damage=0.4
   self.large_damage=0.7
   self.health=1500
