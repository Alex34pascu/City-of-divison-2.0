import traceback
from threading import Thread
import sound_pool
import dlg
musics=[]

class music():
 def __init__(self,name,start_volume):
  try:
   self.name=name
   self.handle=sound_pool.sound.sound()
   self.handle.load(r"sounds\\"+name+"intro.ogg",True)
   self.handle.volume=start_volume
   self.handle.play()
   self.nhandle=sound_pool.sound.sound()
   self.nhandle.load(r"sounds\\"+self.name+".ogg",True)
   thread = Thread(target=self.check_intro)
   thread.start()
   musics.append(self)
  except Exception as e:
    error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
    dlg.dlg("error: "+error_message)

 def check_intro(self):
  while 1:
   if self.handle.handle.is_playing:
    pass
   else:
    self.nhandle.volume=self.handle.volume
    self.nhandle.play_looped()
    self.handle=self.nhandle
    break
 def stop(self):
  try:
   musics.remove(self)
  except:
   pass
  try:
   self.nhandle.stop()
   self.nhandle=None
   self.handle.stop()
   self.handle=None
  except:
   pass
def pause_all_musics():
 for m in musics:
  try:
   m.nhandle.handle.pause()
   m.handle.handle.pause()
  except:
   pass
def resume_all_musics():
 for m in musics:
  m.nhandle.handle.play()
  m.handle.handle.play()
