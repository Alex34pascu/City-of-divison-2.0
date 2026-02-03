import numpy as np
import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def clip(value, min_value, max_value):
    return max(min(value, max_value), min_value)
def speak(text):
 speatch.output(text)
from sound_pool import Rotation_Matrix_Function as rf
#99.9% of this was not done by me, Amerikranian.
#The functions and formulas for the sounds were written by Carter Tem to the best of my knowledge
#The only thing I, Amerikranian added is keeping the sound's pitch, because I thought it would be useful.
from math import radians, cos, sin, copysign
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
def position_sound_custom_3d(handle, listener_x, listener_y, listener_z, source_x, source_y, source_z, theta, pan_step, volume_step, behind_pitch_decrease, start_pan, start_volume, start_pitch, keep_pitch, filterlist):
    # Shift the points so that the listener point becomes the origin
    relative_x = source_x - listener_x
    relative_y = source_y - listener_y
    relative_z = source_y - listener_z

    if relative_x==0 and relative_y==0 and relative_z==0 or handle.muted==True:
         return
    theta_radians = radians(theta)
    cos_theta = cos(theta_radians)
    sin_theta = sin(theta_radians)
    rotated_x = relative_x * cos_theta - relative_y * sin_theta + listener_x
    rotated_y = relative_x * sin_theta + relative_y * cos_theta + listener_y    
    # Initialize pan, volume, and pitch with the starting values
    final_pan = start_pan
    final_volume = start_volume
    final_pitch = start_pitch
    
    # Compute pan and volume based on x position
    if rotated_x < listener_x:
        delta_x = listener_x - rotated_x
        final_pan -= delta_x * pan_step
        final_volume -= delta_x * volume_step
    elif rotated_x > listener_x:
        delta_x = rotated_x - listener_x
        final_pan += delta_x * pan_step
        final_volume -= delta_x * volume_step

    # Compute volume and pitch adjustments based on y and z positions
    if rotated_y < listener_y:
        final_pitch -= abs(behind_pitch_decrease)
        delta_y = listener_y - rotated_y
        final_volume -= delta_y * volume_step
    elif rotated_y > listener_y:
        delta_y = rotated_y - listener_y
        final_volume -= delta_y * volume_step
    
    if source_z < listener_z:
        final_pitch -= abs(behind_pitch_decrease)
        delta_z = listener_z - source_z
        final_volume -= delta_z * volume_step
    elif source_z > listener_z:
        delta_z = source_z - listener_z
        final_volume -= delta_z * volume_step

    # Clamp pan, volume, and pitch values to appropriate ranges
    if handle.pan != final_pan:
        final_pan = clip(final_pan, -100, 100)
        handle.pan = final_pan
    if handle.volume != final_volume:
        final_volume = clip(final_volume, -100, 100)
        handle.volume = final_volume
    if not keep_pitch and handle.pitch != final_pitch:
        final_pitch = max(final_pitch, 0)  # pitch should never be less than 0
        handle.pitch = final_pitch

    """
    # If the sound is in 3D, update the 3D position
    if handle.three_d:
        handle.handle.set_x((listener_x - rotated_x) * -1)
        handle.handle.set_y((listener_y - rotated_y) * -1)
        handle.handle.set_z((listener_z - source_z) * -1)
#        handle.handle.set_3d_position(None, theta)
    """