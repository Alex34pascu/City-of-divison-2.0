import numpy as np
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 speatch.output(text)
from sound_pool import Rotation_Matrix_Function as rf
#99.9% of this was not done by me, Amerikranian.
#The functions and formulas for the sounds were written by Carter Tem to the best of my knowledge
#The only thing I, Amerikranian added is keeping the sound's pitch, because I thought it would be useful.
import math
def get_platform(x,y,z,filterlist):
 final=""
 for p in filterlist:
  if x>=p.minx and x<=p.maxx and y>=p.miny and y<=p.maxy and z>=p.minz and z<=p.maxz and p.id==0:
   final=p.tile
 return final
def crieer_formule(ox,oy,nx,ny):
 delta_x=0
 delta_y=0
 a=0
 delta_x=nx-ox
 delta_y=ny-oy
 try:
  a=delta_y/delta_x
 except:
  pass
 b=ox*a
 b=oy-b
 return a,b
def position_sound_1d(handle, listener_x, source_x, pan_step, volume_step):
 position_sound_custom_1d(handle, listener_x, source_x, pan_step, volume_step, 0.0, 0.0)

def position_sound_custom_1d(handle, listener_x, source_x, pan_step, volume_step, start_pan, start_volume):
 delta=0
 final_pan=start_pan
 final_volume=start_volume
 #First, we calculate the delta between the listener and the source.
 if source_x<listener_x:
  delta=listener_x-source_x
  final_pan-=(delta*pan_step)
  final_volume-=(delta*volume_step)
 if source_x>listener_x:
  delta=source_x-listener_x
  final_pan+=(delta*pan_step)
  final_volume-=(delta*volume_step)
 #Then we check if the calculated values are out of range, and fix them if that's the case.
 if final_pan<-100:   final_pan=-100
 if final_pan>100: final_pan=100
 if final_volume<-100: final_volume=-100
 #Now we set the properties on the sound, provided that they are not already correct.
 if handle.pan!=final_pan:
  handle.pan=final_pan
 if handle.volume!=final_volume:
  handle.volume=final_volume

def position_sound_3d(handle, listener_x, listener_y, listener_z, source_x, source_y, source_z, theta, pan_step, volume_step, behind_pitch_decrease,keep_pitch,filterlist=[]):
 position_sound_custom_3d(handle, listener_x, listener_y, listener_z, source_x, source_y, source_z, theta, pan_step, volume_step, behind_pitch_decrease, 0.0, 0.0, 100.0,keep_pitch,filterlist)
def position_sound_custom_3d(handle, listener_x, listener_y, listener_z, source_x, source_y, source_z, theta, pan_step, volume_step, behind_pitch_decrease, start_pan, start_volume, start_pitch,keep_pitch,filterlist):
 orginal_source_x=source_x
 orginal_source_y=source_y
 orginal_source_z=source_z
 delta_x=0
 delta_y=0
 delta_z=0
 final_pan=start_pan
 final_volume=start_volume
 final_pitch=start_pitch
 orginal_source_x=source_x
 orginal_source_y=source_y
 #First, we calculate the x and y based on the theta the listener is facing. 
 """
    # Convert the angle from degrees to radians
 theta_radians = math.radians(theta)
    
    # Compute the cosine and sine of the angle
 cosine_theta = math.cos(theta_radians)
 sine_theta = math.sin(theta_radians)
    
    # Shift the points so that the listener point becomes the origin
 relative_x = source_x - listener_x
 relative_y = source_y - listener_y
    
    # Perform the rotational transformation
 source_x = (cosine_theta * relative_x) - (sine_theta * relative_y)
 source_y = (sine_theta * relative_x) + (cosine_theta * relative_y)
    
    # Shift the points back to their original position
 source_x += listener_x
 source_y += listener_y
 """    
 theta_radians = np.radians(theta)
    
    # Shift the points so that the listener point becomes the origin
 relative_x = source_x - listener_x
 relative_y = source_y - listener_y
    
    # Perform the rotational transformation
 rotation_matrix = np.array([[np.cos(theta_radians), -np.sin(theta_radians)],
 [np.sin(theta_radians), np.cos(theta_radians)]])
    
 rotated_point = np.dot(rotation_matrix, [relative_x, relative_y])
    
    # Shift the points back to their original position
 rotated_x = rotated_point[0] + listener_x
 rotated_y = rotated_point[1] + listener_y
 source_x=rotated_x
 source_y=rotated_y

   
# source_x,source_y=rf.rotate_matrix(source_x,source_y,theta,listener_x,listener_y) 
    
 if handle.three_d==True:
  handle.handle.set_x(((listener_x-source_x)*-1)*1)
  handle.handle.set_y(((listener_y-source_y)*-1)*1)
  handle.handle.set_z(((listener_z-source_z)*-1)*1)
  handle.handle.set_3d_position(None,theta)
 else:
  if source_x<listener_x:
   delta_x=listener_x-source_x
   final_pan-=(delta_x*pan_step)
   final_volume-=(delta_x*volume_step)
  if source_x>listener_x:
   delta_x=source_x-listener_x
   final_pan+=(delta_x*pan_step)
   final_volume-=(delta_x*volume_step)
  if source_y<listener_y:
   final_pitch-=abs(behind_pitch_decrease)
   delta_y=listener_y-source_y
   final_volume-=(delta_y*volume_step)
  if source_y>listener_y:
   delta_y=source_y-listener_y
   final_volume-=(delta_y*volume_step)
  if source_z<listener_z:
   final_pitch-=abs(behind_pitch_decrease)
   delta_z=listener_z-source_z
   final_volume-=(delta_z*volume_step)
  if source_z>listener_z:
   delta_z=source_z-listener_z
   final_volume-=(delta_z*volume_step)
 if final_pan<-100: final_pan=-100
 if final_pan>100: final_pan=100
 if final_volume<-100: final_volume=-100
 if final_pitch<0: final_pitch=0
 if handle.pan!=final_pan: handle.pan=final_pan
 if handle.volume!=final_volume: handle.volume=final_volume
 if not keep_pitch:
  if handle.pitch!=final_pitch: handle.pitch=final_pitch
