import menus
import pygame.locals as pl
import pygame
import accessible_output2.outputs.auto
import net
import key_constants as kc
import map
import sound_pool
import v
v.get()
pygame.init()
speatch = accessible_output2.outputs.auto.Auto()


def speak(text):
 text = v.vertaal_tekst(text, "nl")
 speatch.output(text)


def weapon_menu():
 x = 0
 y = 0
 v.msp.play_stationary("sounds\wpnmenuopen.ogg")
 flag = True
 speak("weapon menu: "+position(x, y))
 while flag:
  m = net.mainloop()
  if m == 1:
   return
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
     if event.unicode.isdigit():
      number = int(event.unicode)
      if number <= len(v.sorts) and number>0:
       x = number-1
       y = 0
       v.msp.play_stationary("sounds\wpnmenuclick.ogg")
       speak(position(x, y))

     if event.scancode == kc.K_a and y > 0:
      net.send("weapon_menu_ammo_check "+position(x, y))
      v.msp.play_stationary("sounds\wpnmenuinfo.ogg")
     if event.scancode == kc.K_s and y > 0:
      net.send("weapon_store "+position(x, y))
      return
     if event.scancode == kc.K_g and y > 0:
      v.new_sm = 1
      v.first_sm = ""
      net.send("give_weapon "+position(x, y))
      return
     if event.scancode == kc.K_i and y > 0:
      if v.shift==False:
       net.send("weapon_info "+position(x, y))
      else:
       net.send("weapon_spesific_info "+position(x, y))
      v.msp.play_stationary("sounds\wpnmenuinfo.ogg")
     if event.scancode == kc.K_BACKSPACE and y > 0:
      sure=menus.yesno("are you sure you want to remove this weapon? This can't be undone.")
      if sure==1:
        net.send("delete_weapon "+position(x,y))
        return
     if event.scancode == kc.K_SPACE and y > 0:
      if v.shift == False:
       net.send("weapon_amount "+position(x, y))
       v.msp.play_stationary("sounds\wpnmenuinfo.ogg")
      if v.shift==True:
       net.send("rotate_weapon "+position(x, y))
       v.msp.play_stationary("sounds\wpnmenuclick.ogg")
     if event.scancode==kc.K_RETURN and y>0 and v.stunned==False:
      if v.shift==False:
       v.scoping=False
       net.send("draw_weapon "+position(x,y))
      else:
       list=v.sorts[x]
       if position(x,y)!="flale":
        if list[0]=="pistols" or list[0]=="revolvers" or list[0]=="sub_machine_guns" or list[0]=="melee" or v.skill_data["holster augmentation"]["active"]==True and list[0]=="shotguns" and v.skill_data["holster augmentation"]["level"]>=1 or list[0]=="assault_rifles" and v.skill_data["holster augmentation"]["level"]>=2 and v.skill_data["holster augmentation"]["active"]==True or list[0]=="sniper_rifles" and v.skill_data["holster augmentation"]["level"]>=3 and v.skill_data["holster augmentation"]["active"]==True:
         net.send("holster_put "+position(x,y))
        else:
         speak("this weapon doesn't fit in your holster")
       else:
        speak("this weapon doesn't fit in your holster")
     if event.scancode==kc.K_DOWN and x<len(v.sorts)-1:
      if v.shift==False:
       x+=1
       y=0
       v.msp.play_stationary("sounds\wpnmenuclick.ogg")
       speak(position(x,y))
#      else:
       #implementation for weapon switching
     if event.scancode==kc.K_UP and x>0:
      if v.shift==False:
       x-=1
       y=0
       v.msp.play_stationary("sounds\wpnmenuclick.ogg")
       speak(position(x,y))
#      else:
       #implementation for weapon switching
     if event.scancode==kc.K_LEFT and y>0:
      y-=1
      v.msp.play_stationary("sounds\wpnmenuclick.ogg")
      speak(position(x,y))
     list=v.sorts[x]
     if event.scancode==kc.K_RIGHT and y<len(list)-1:
      y+=1
      v.msp.play_stationary("sounds\wpnmenuclick.ogg")
      speak(position(x,y))
     if event.scancode==kc.K_ESCAPE:
      flag=False
 v.msp.play_stationary("sounds\wpnmenuclose.ogg")

def position(x,y):
 list=[]
 list=v.sorts[x]
 data=list[y]
 return data