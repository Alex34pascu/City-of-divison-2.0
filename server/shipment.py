
import map
import v
v.get()
import timer

def send_all(message,map=""):
 v.send_packet_to_clients(message,v.clients,map)

class shipment():
 def __init__(self,team,items):
  self.team=team
  self.items=items
  self.arrivetimer=timer.timer()
  self.arrivetime=180000
  self.dropping=False
  self.x,self.y,self.z=0,0,0
  self.map=""
  if map.has_metal_fortress(self.team):
   for f in map.objects:
    o=map.objects[f]
    if o.name=="metal_fortress" and o.team==self.team:
     self.x=round((o.minx+o.maxx)/2)
     self.y=round((o.miny+o.maxy)/2)
     self.z=o.maxz+50
     self.map=o.map

 def loop(self):
  if self.dropping==False and self.arrivetimer.elapsed()>self.arrivetime:
   self.dropping=True
   self.arrivetimer.restart()
   send_all("play_sound shipmentdropdist.ogg "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" 0 0",self.map)
  if self.dropping==True:
   if self.arrivetimer.elapsed()>30000:
    o=map.spawn_object(self.x-1,self.x+1,self.y-1,self.y+1,self.z,self.z+3,"shipment",1,self.map,False)
    o.destination_team=self.team
    o.loot=self.items
    v.shipments.remove(self)
    return
def spawn_shipment(team,items):
 s=shipment(team,items)
 v.shipments.append(s)


def shipmentloop():
 for s in v.shipments:
  s.loop()