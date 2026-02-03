
class weapon():
 def __init__(self,name):
  self.name=name
  if self.name=="knife":
   self.firetime=500
   self.automatic=False
  elif self.name=="machete":
   self.firetime=750
   self.automatic=False
  elif self.name=="flail":
   self.firetime=1500
   self.automatic=False

  elif self.name=="Winchester_Model_24":
   self.firetime=1500
   self.automatic=False
  elif self.name=="barrett_M107A1":
   self.firetime=3250
   self.automatic=False
  elif self.name=="dsr50":
   self.firetime=2000
   self.automatic=False

  elif self.name=="ak47":
   self.firetime=75
   self.automatic=True

  elif self.name=="SVD_Dragunov":
   self.firetime=1400
   self.automatic=False
  elif self.name=="AR10":
   self.firetime=900
   self.automatic=False

  elif self.name=="Benelli_M4":
   self.firetime=780
   self.automatic=False
  elif self.name=="remington870xs":
   self.firetime=910
   self.automatic=False
  elif self.name=="FN_509_tactical":
   self.firetime=480
   self.automatic=False
  elif self.name=="ruger_redhawk":
   self.firetime=1400
   self.automatic=False
  elif self.name=="smith_n_wesson_model29":
   self.firetime=730
   self.automatic=False

  elif self.name=="cold_m1911":
   self.firetime=470
   self.automatic=False
  elif self.name=="colt_m1911":
   self.firetime=470
   self.automatic=False

  elif self.name=="beretta92A1":
   self.firetime=400
   self.automatic=False
  elif self.name=="m2_browning":
   self.firetime=135
   self.automatic=True
  elif self.name=="hk_mg4":
   self.firetime=105
   self.automatic=True
  elif self.name=="fn_f2000":
   self.firetime=80
   self.automatic=True
  elif self.name=="fn_p90":
   self.firetime=60
   self.automatic=True
  elif self.name=="ARX160":
   self.firetime=90
   self.automatic=True
  elif self.name=="MP7":
   self.firetime=55
   self.automatic=True
  elif self.name=="mp5":
   self.firetime=75
   self.automatic=True
  else:
   self.firetime=0
   self.automatic=False
