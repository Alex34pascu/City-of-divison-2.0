
from __future__ import absolute_import
from Cryptodome.Cipher import AES
import os
import time
from sound_lib.effects.bass import Reverb
from sound_lib.external import pybass
from sound_lib.effects import effect, bass as effects
import timer

import accessible_output2.outputs.auto
speatch = accessible_output2.outputs.auto.Auto()
def speak(text):
 speatch.output(text)
from sound_lib import main as sm
#Written By Carter Tem
#No part of this class was done by me, Amerikranian. This is Carter's work alone.
import math
import sound_lib
from sound_lib import output
from sound_lib import stream
o=output.ThreeDOutput()

def decrypt_audio(input_file, output_file, key):
    chunk_size = 64 * 1024  
    cipher = AES.new(key, AES.MODE_ECB)
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        while True:
            chunk = infile.read(chunk_size)
            if len(chunk) == 0:
                break
            outfile.write(cipher.decrypt(chunk))

key = b"001003001%%.1001"
class sound():
 def __init__(self):
  self.three_d=True
  self.silence=None
  self.handle=None
  self.handle_backup=None
  self.effect=None
  self.freq=34100
  self.muted=False
  self.volume=0
  self.name=""
 def add_reverb(self,mix=-25,time=500):
  reverb=Reverb(self.handle)
  param={
"fInGain":0.0,
"fReverbMix":mix,
"fReverbTime":time,
"fHighFreqRTRatio":0.86
}
  reverb.set_parameters(param)
 def set_filter(self,filter):
  self.effect=effects.ParamEq(self.handle)
  test={
'fCenter': filter, 
'fBandwidth': 30, 
'fGain': -15
}
  self.effect.set_parameters(test)

 def load(self,filename="",encripted=False,three_d=False):
  self.name=filename
  if encripted==True:
   decrypt_audio(filename.replace(".ogg",".bin"), os.path.expanduser('~')+"\sound.ogg", key)
   filename=os.path.expanduser('~')+"\sound.ogg"
  self.three_d=three_d
  if self.three_d==True:
   self.handle =stream.FileStream(False,filename)
   self.handle.set_3d_attributes(1,0.0,10000000.0,180,180,-10.0)
  else:
   self.handle =stream.FileStream(False,filename,0,0,0,False,False)

  if os.path.exists(os.path.expanduser('~')+"\sound.ogg"):
    os.remove(os.path.expanduser('~')+"\sound.ogg")
  self.freq=self.handle.get_frequency()
 def play(self):
  self.handle.looping=False
  self.handle.play()
 def play_wait(self):
  self.handle.looping=False
  self.handle.play_blocking()
 def play_looped(self):
  self.handle.looping=True
  self.looping=True
  self.handle.play()
 def stop(self):
  if self.handle and self.handle.is_playing:
   self.handle.stop()
   self.handle.set_position(0)
 @property
 def volume(self):
  if hasattr(self, "handle_volume"):
   return self.handle_volume
  else:
   return False

 @volume.setter
 def volume(self,value):
  if hasattr(self, "handle_volume") and value==self.handle_volume:
   return
  self.handle_volume=value
  if not self.handle:
   return False
  self.handle.set_volume(10**(float(value)/20))
 @property
 def pitch(self):
  if hasattr(self, "handle_pitch"):
   return self.handle_pitch
  else:
   return False
 @pitch.setter
 def pitch(self, value):
  if hasattr(self, "handle_pitch") and value==self.pitch_handle:
   return
  self.pitch_handle=value
  if not self.handle:
   return False
  self.handle.set_frequency((float(value)/100)*self.freq)
 @property
 def pan(self):
  if hasattr(self, "handle_pan"):
   return self.handle_pan
  else:
   return False

 @pan.setter
 def pan(self, value):
  if hasattr(self, "handle_pan") and value==self.handle_pan:
   return
  self.handle_pan=value
  if not self.handle:
   return False
  self.handle.set_pan(float(value)/100)
 def close(self):
  if self.handle:
   self.handle.free()
   self.__init__()
