import v
v.get()
import random
import datetime
def get_time():
 nu = datetime.datetime.now()
 datum = nu.strftime("%d %B %Y")
 tijd = nu.strftime("%H:%M")
 return datum,tijd
def get():
 global changes
 changes= """
New in 1.55
server changes:
You no longer can accept an invite for a team when you are already in one.
Fixed a bug where you could get hit by a flash grenade on an other map.
While searching for a match, you will now get notified when someone else starts searching as well
The player menu will now show how many players there are searching for a match.
client changes:
This update introduces a new ranked mode: Last Man Standing. This will be the main mode for now, running throughout the entire week. It’s played with 4 players on 4 brand-new maps, and we’ve redesigned the rewards track accordingly. For more information, please refer to the documentation.
Along with Last Man Standing, we also added a new account item to the rewards track: the Joker Skill Point. This is an unassigned skill point that you can insert into any skill of your choice, allowing you to upgrade your skills in a more flexible way.
Added a new skill: DMR Precision. This skill lets you build up a hit streak, increasing your damage as long as you don’t miss.
Added Shift + F2 to see who is on the same map as you.
Added a setting to enable or disable using the Right Control key to shoot.
Fixed a bug where you could take a weapon from a locker while your level was too low.
Fixed a bug where vehicle alarms could be heard in the lobby.
Fixed a traceback error that occurred while updating the game.
new in 1.54.1
Server changes:
Fixed a bug where matches didn't start.
Fixed clients staying online.
Team kills will no longer coun't on the training camp.
Added an option in the death messages selector which will only show death messages on the map that you are on.
Fixed a bug where players holding a team phone couldn't enter the training_camp.
Ensured that lockers and metal fortresses can no longer be placed on the training camp.
Fixed a bug with deleting accounts.
Added a training camp map for new players to fight each other. Players below level 10 can spawn on to it if they enter the map.
Fixed bullets hitting players when they shouldn't.
Fixed a bug where you could go offline inside windows and spawn on top of roofs.
Reverded the bullets changes.
The hk_mg4's range has been increased to 40.
tried to fix some bugs related to bullets.
Added event descriptions.

client changes:
Changed to a new server.
The game will now speak the cardinal directions if you turn precizely.
Cordinates will be announced with no decimals, just as it was before version 1.54.
partially reverded the thrown knife damage reduction on longer ranges.
Tripwires will explode faster upon activating it.
Fixed a bug where locations weren't found correctly.
Fixed a bug where fortresses weren't placed correctly.
slightly adjusted some of the sounds for the AR10 and smw model 29.

New in 1.54
server changes:
Made the duration of the vehicle alarms shorter.
Vehicles will do less damage to other objects and players when they explode.
Fixed a bug where sharp shooter mastery got to much extra range.
Removed the bonus range on the smg experience skill, but increased it's bonus damage to 4.
Recoil mastery now has 20% less effect.
Fixed the server crash.
Knife throw will do less damage on longer ranges, fixing cases where you could oneshot people on 20 tiles whith it.
the AR10 will will have less rounds, but deals more damage and has more range.
client changes:
Added parked vehicles on the map. These have alarms when they get damaged, and they'll eventually explode.
We're introducing 360-degree movement. Press Shift + Q or E to turn around. You can press Shift + F to switch the key bindings for precise turning and snap turning if you wish to do so.
There are now two new weapon categories: Revolvers and Marksman Rifles. Accordingly, you will also find two new weapons: the Smith & Wesson Model 29 revolver, and the AR-10 marksman rifle.
C4s and RCEs will now deal more damage through walls.
The damage reduction of the choke tube has been removed.
Added the precision barrel for sniper rifles, which grants them 25 tiles of extra range.
Added the large scope (attachment) for marksman rifles. These will require glass pieces, which you can find on the map.
You can no longer run or jump while using the HK MG4. The movement speed is now reduced to match that of the SVD.
Fixed a game-breaking bug where attachments were applied to the wrong weapons.
Fixed ghost objects.
Solved a bug where you got teleported if you spawned on a corpse when entering the map.
Fixed the bug where grenades didn't fall correctly.
Weapons will now be loaded at the beginning of a ranked match again.
New sounds have been added for explosions on gravel.
new in 1.53.2
client changes:
fixed automatic weapons

new in 1.53.1
client changes:
fixed some bugs that came with version 1.53, including gun shots in the lobby, replying not working correctly and shotguns dealing the same damage on large ranges.

new in 1.53
client changes:
Added more stats to the profile of a player.
Pressing I will now direct you to your profile menu. This is handy if you want to see your skills for example.
Pressing Backspace on a chat will work now. It will go to the profile of a player.
You no longer can reply to an other reply.
increased the maximum amount of 7.62 bullets from 80 to 90.
Changed the firetime of the beretta from 340 to 400
The choke_tube will now decrease the damage of the shotgun by 50.
Added more sounds for bodyfall wall inpects and knife throw landings.

New in 1.52
server changes:
Increased the time before you can return to the lobby after you have been hit from 30 to 45 seconds.
There is now a minimum and maximum length for player- and team names.
As stated in the change log of version 1.5, the Benelli_m4 has it's damage reduced from 700 to 650.
Added a button in the team phone to see the status of your shipment.
Thrown knives will be doing less damage on longer ranges.
Corpse's remove time has been increased to 5 minutes.
the hk_mg4 is no longer available in ranked mode.
the weapon competition event no longer chooses the m2.
reverded the sharp shooter mastery change, but added a chanse to recoil even if you have the stock attached.
fixed food steps.

client changes:
Added a new attachment: the choke tube. This allows you to scattershot, increasing the hit radius of a shotgun.
The store on the team phone has been redesigned. Bulletproof vests now cost 1 teamtoken, and the amount of grenades and helmets has been increased.
Sharpshooter mastery now grands 2 instead of 3 extra tiles of range upon upgrading.
The Beretta’s fire time has been reduced from 440 to 340 milliseconds.
The knife throw skill now deals more damage at higher skill levels.
The distance sounds of the silenced Beretta, Colt, and DSR50 have been made slightly louder.
If a corpse is on top of an object that gets destroyed, the corpse will now fall down.
Fixed the error message bug that players experienced when the map was refreshed.


new in 1.51
client changes:
Added 50bmg_rounds to the loot pool.
fixed a bug where you could get more than 4 copies of a weapon.
lag inprovements

New in 1.5
server changes:
Flash grenades will do 10 instead of 50% damage if you're close.
client changes:
The rules of the game have been updated. We at Firegaming want you to know these rules and restrictions that you will be held to. Please review them before you continue playing.
You now have the ability to customize your weapon with attachments. These are created with materials collected on the map. Once you have a toolbox, you can choose what attachment you'd like to put on your weapon. Each weapon can have different sets of attachments. For example: the Beretta can have a small barrel and silencer, while an assault rifle could get an upgrade with an extra magazine and a stock. All these attachments will have a different effect on the weapon of choice and can be crafted with metal, plastic, or rubber.
Guns now have the ability to jam, so be patient when firing your weapon, especially while reloading. No worries though, a jammed weapon can be fixed with a toolbox.
Furthermore, guns can eventually degrade, either due to frequent jamming or when you fall from a higher position.
You can now press Shift + I in the weapon menu to receive information about the weapon you have selected, such as attachments, jam status, and percentage of degradation.
Pressing Shift + Space in the weapon menu will allow you to switch between different modeled copies of a selected weapon.
If you want to get rid of a weapon, for instance when all your three copies are degraded, you can press Backspace. Keep in mind that once you've dropped it, there is no way to get the weapon back.
We're introducing a new sniper rifle, the DSR50. This weapon is unlockable from level 35. It is a bolt-action rifle, which means it can only hold one bullet at a time, but on the other hand it's fast to reload and has a long range.
Added a new type of grenade, the flash grenade. This explosive creates a flash when it explodes, causing players to be blinded and partially deafened for a few seconds.
Chapter 6 of the game's storyline is finally done, and has been added to the quests.
Added a Vietnamese translation and updated some others as well.
Some weapons will now require other ammo types, making the game more realistic. For instance:
The Barrett_M107A1 now uses 50BMG_rounds instead of the 7.62_mm.
The Colt_M1911 and Ruger_Redhawk now use an entirely new type of ammunition: 45ACP_ammo.
Some weapons have been renamed due to realism changes.
Previously, you could have an unlimited number of the same weapon; now you're restricted to having only three of each.
It is now possible to use the number keys to switch between categories in the weapon menu.
Lowered the damage of the machete and the flail to 500 each.
Increased the damage of the Benelli_M4, previously known as the M26, from 650 to 700, allowing it to one-shot people with a headshot from a really close distance. This is because shotguns don't have an attachment yet, though they will get one soon.
Decreased the damage of the Beretta to 225.
The number of sounds you'll have to do for a Simon to break into a fortress has been increased to 35.
The maximum health of a fortress has been reduced from 10000000 to 5000000.
Lockers now have a maximum number of weapons that they can store. Now, you can store 20 weapons per level of the storage of the locker, allowing you to hold 200 weapons in total at storage_level 10.
The range within which you can detonate an RCE has been reduced from 200 to 50 meters.
Added jumping, landing, turning, and aiming movement sounds to your character to make it sound more realistic.
The main map has received several updates and/or slight adjustments. We've updated and reworked Sofia's and Tim's house, as well as the apartment above the restaurant. Maria's house got a second floor, Jack's house got an attic, and Jane's house finally got a little bathroom. The hospital also got a second entrance and a basement. A few other houses got extra windows or lootable objects. Some of these windows are higher than ground level, which means you have to jump up to reach them.
Fixed a bug where you still got healed if you respawn after you died.
If a glass display case gets destroyed, you will now hear the broken glass as you walk over it.
Removed the CPU setting that had been added in version 1.44.3, since it didn't work as expected.

New in 1.44.3
client changes:
Fixed an issue with the DDoS attack prevention system.
Added a setting to switch between the behavior introduced in versions 1.44 and 1.44.2, as some users experienced increased lag while playing on version 1.44.2. The default is set to version 1.44.

new in 1.44.2
server changes:
security fixes to the server to prevent dedos attacks
client changes:
reverded a change that caused much lag for people playing the game.

new in 1.44
client changes:
Fixed some bugs with the scope, including the issue where there was significantly more lag when looking through it.
Fixed a bug where translations didn't translate dialog texts.
instead of only doing %1, %2 edc in translation files you now also can fill in a # for the % sign to force the translator to not translate the text.
fixed a bug where you still could place a c4 after you died.
fixed a bug where you could walk with the barret.
performance updates to reduce lag.


new in 1.43
server changes:
improved the admin and moderator systems.
The improved admin and moderator systems now include a key change: moderators have the ability to ban players.
Fixed a bug where a team member's rights were not removed when they left the team.
Reduced the bonus damage on SMG streaks from 5 to 3 per streak level.
You no longer can disconnect when enemies are close.
added the moderator rank.
fixed a bug where you could loot a corpse in ranked mode.
the ruger_mark_IV_tactical got it's range back to 30 instead of 25 tiles.
the ARX160 got it's range back to 30.
the ak47 got also a range nerf, but got a damage encrease of 10 damage.
tried to implement a method to let players stay online if they disconnect during a fight.
did some changes to fortresses:
1. The m2 browning and explosives will do now twice the amount of damage to metal fortresses.
2. A metal fortress starts now with 250000 instead of 100000 health.
3. Your team now gets team tokens depending on how much health the fortress had on it highest point. A fortress that had 10000000 health gives around 300 tokens, but a small one only gives 8 tokens.

fixed bullets hitting players through walls.
added the server cleanup function for admins.
fixed a bug where you sometimes saw an item with the amount 0 in your belt.
client changes:
added a new weapon, the ak47.
you now can drop multiple weapons at once in a locker.
decreased the range of all pistols to 25 tiles.
increased the range of each assault rifle by 5.
fixed the looking by your self function on the scope of sniper rifles.

new in 1.42
server changes:
lowered the health of the bulletproof_vest from 3000 to 1500.

client changes
Fixed a bug where jumping wasn't registered by the server.
Sounds checking, which has been added in version 1.41, will work now.



new in 1.41
client changes:
Added a new item for the team fortress store. The bullet proof vest. This item will protect you to bullets that are aimed at your body. Melee weapons still do the same damage to players that are wearing a vest.
Added friendly matches which you can play during the whole week.
If a team has a metal fortress on the map, they can get an extra team member. This person will be removed if the fortress has been destroyed.
Finally fixed bullets and staircases.
Lowered the amount of kills needed to get a team token from 25 to 15.
Patched some bugs with ranked mode, including the bug where you stil could match your previous opponent and the bug where a player could appear two or more times on the leader board.
Fixed a bug where the sniper zoom sounds weren't playing.
Added the english short translation.
Did some work to moving objects. Hopefully there will be no cases where you no longer can't move an object while you are standing streight infront of it.
A security fix has been added to the game to ensure there are no sounds missing, which could people give benefits in gameplay.
throwing a grenade from an elevated spot will no longer damage you if you are throwing it streight forward.
A team leader can now remove every team note on the team phone.
You no longer can remove rights of the leader of a team.
Fixed a bug where you sometimes didn't unlocked a quest.

new in 1.4
server changes:
Tried to solve the bug where you were still being matched with your previous matched player in ranked mode.
Re -designed weapon competition to only choose weapons that are unlocked for each player.
patched a bug where your timer of the rapid fire skill was reset when you activated the skill with no pistol in your hand.
tried to fix bullets.
fixed a bug where you could give items to death players.
fixed a bug where you couldn't turn on the alarm of your fortress even if anyone wasn't inside.
decreased the damage of the m26 from 800 to 650.
decreased the range of the remington from 24 to 20, but gave it a small damage increase of 50 damage.
decreased the damage from the winchester from 950 to 850.
added builder rank.
tried to fix a bug where people could get on roofs of buildings trough exiting the game with task manager.
fixed a bug where you could place fortresses in strange places.
Recoded saving player data. If you found any bugs let us know.
A new function has been added to the team phone, team notes. With this feature you can communicate with your team members who are offline to give them information about attacks on the metal fortress, for example.
made welding_machine batterys more common to find in objects.
reverded the examining change. Now corpses wouldn't stay after looting them.
changed the view my traps button on the team phone. Now it shows all traps that are placed by your team.
fixed a bug where the object fall sounds where playing if you was moving an object.
increased the damage of large bullets to objects.
you will now get more team otkens if you destroy a locker or metal fortress.
fixed the bug where fortresses didn't remove Becuse some teams have so much team tokens there their tokens will be reset.
lowered the amount of simon sounds to 25 to break in to a fortress.
you no longer can get the m2 in ranked mode.
the flail does more damage to fortresses and lockers now.
explosives do more damage to fortresses and lockers.
client changes:
This update contains a lot of new content related to teams. For instance: You can put  a small metal fortress together, which you can build on the map to create a safe place for your locker. Along with the fortress, you will get a team telephone, which you can use to order some special items and traps to protect your hide out and the locker inside.
In the team menu, you can retreive a metal_fortress_construction_kit, which contains metal sheats. In order to create the fortress, you have to find a welding_machine, along with 2 batteries, to weld the sheats together.
Each teammember will get a team phone, giving them access to the fortress's alarmsystem, an overview of the currendly active traps, and the ordering of items.
The metal sheads found in the construction kit can also be used to add more Solidity points to your locker.
To find more information about fortress's, shipments and traps, please refer to the documentation.
---
Added a new weapon: The m2_browning. It uses a new ammo type: 50_BMG rounds. These rounds can go through some of the objects such as furniture and bushes.
We have created a new weapon category: Machine guns. We placed the hk_mg4 in here,  since it is not an actuall assault rifle. The m2_browning also belongs to this category.
as of now we count the team's total kills. This can be reviewd in the profile of a team.
Updated and adjusted the documentation a bit.
increased the flail firetime by 0.4 seconds.
Decreased the time that rapid fire will increase on higher levels. It was 1 second per level, now it is 0.3 seconds.
You can no longer jump with the SVD_Dragunov equiped.
If you examine an object and you already have the maximum of that item, then you place it back in the object. Due to potential exploits, we have decided to only give players event_points if they examine an object and they take all the items.
fixed a bug where you could press keys while loading the map. All input will be ignored while loading now.
Fixed the read_code button on the RCE_controller.
Some experimental lag improvements.
new in 1.35
server changes:
When announcing the location of a VIP, the coordinates of where he or she is are now spoken.
tried to fix the bug where player data somehow was removed.
shooting from planters should work now.
lag improvements
did some performance improvements.
If you use an item and you have that item no longer in your inventory you will lose the focus on an other item.
You no longer can send pm's to your self.

client changes:
saving settings works now. Woops

new in 1.34
client changes:
reverded some of the changes that were made in 1.32 to reduce lag, because they were increasing it.
translation fixes.

new in 1.33
client changes:
added a new mastery, SMG experience. This skill allows you to build up a kill streak with your SMG's, which gives them more damage and range.
menus now support proper first-letter navigation that matches your current language.
Did some more inprovements to the speed of translations.
Tried to fix a bug where you could get higher level weapons by canceling a match.
increased the wait time for finding a match without automatically canceling.
the time before corpses remove their self has been increased from 2 to 3 minutes.
fixed a bug where the sound of the c4 alert didn't play.
Fixed a bug where you wouldn't hear your own player's hit sounds while scoping.
stability fixes to the ingame updater.

new in 1.32
server changes:
lowered the education points of the holster augmentation skill by 5 points.
lowered the cooldown time of the infrared scanner interference skill to 2 minutes.
increased the time of the RCE explotion after the activation by 1.3 seconds.
fixed a small bug where you could stack up ladders.
Some VIP event fixes.
Did some work to the huge spikes of lag that happened sometimes.
You will no longer be matched with your previous matched player.
fixed a bug where you sometimes didn't got event points if you was a VIP.
client changes:
you no longer can shoot trough bridges.
Fixed a bug where you could hit players with a flail or machete_swing, even if they were hiding behind a object.
fixed a bug where you couldn't move some objects.
the mufling of noises has been resolved
fixed false anti-cheat warnings.

new in 1.31
server changes:
fixed the bug where a player losed ranking points, even if he won in a match.
fixed a bug where players  heard body falls in other maps.
client changes:
Some optimizations for the new lag improvements.
added a new mastery for the pistols. Rapid fire.
updated the rules a bit. Be sure to read them again so you don't miss anything.
Fixed the lag with larger translations
Fixed a bug where you wouldn't hear your your player sounds when scoping at a greater distance.
security fixes.
Did ssome improvements to the lag.

new in 1.3
server changes:
You can only place a ladder agains a wall.
Did some inprovements to ranked mode to hopefully fix the crash.
Fixed the bug where players could move themselves to places they shouldn't be. For example, Janes' house.
did some inprovements to bullets and staircases.
A helmet ping sound has been added for when you hit someone wearing a helmet.
increased the amount of ranking points you get from winning ranked matches.
Your weapons are automaticaly loaded when you start a match.
Trys to fix the bug where you losed your loot after losing a ranked match.
The player menu has been upgraded to see how many players are in a match.
Fixed a bug where you lost your items if you died in a ranked match.
Tried to fix the crash of the server.
You now longer can get event points while you are in a match.
Tried to fix the double losing of points in a ranked match.
add buffer items related to ranked mode.
client changes:
In this update, we introduce Ranked mode. This is a secondary gamemode that is available during the weekends.
Now, you can only have 1 vs 1 matches, but we have plans for extra types of matches in the future.
We also added a new chest: The diamond chest. This contains quite some more skill points then the other chests. You can get this  if you win the weekly ranked mode event. To get more specific information about how matches work, you can read the Ranked mode topic in the documentation.

Added some permanent items that are connected to your account:
- Mastery potion: This item boost your progress of your mastery's by 100% for a period of 30 minutes.
- magical_reappearance: This item lets you keep your loot the next time you die.

Added a new explosive, the remote Controlled Explosive (in short: R_C_E). This explosive can be activated by typing a code on a controller.
Chapter 4 and 5 of the story have been added to the game. Chapter 4 is unlockable from level 15 and chapter 5 from level 20.
The quarry on the main map is now available.
You have now an option in the main menu to go to the games' translations web page. You can download language packs from there, so we don't need to update the client to add new translations!
Added A Turkish an dportugese translation of the game.
The machete swing has been changed. Now when you use the swing, you have to wait 800 milliseconds before actually executing the swing.
increased the firetime of the beretta by 100 miliseconds.
the capacity of the MP5 has been increased to 30 rounds of ammunition.
decreased the lockers height so people can jump ofer it.
Fixed the sniper's scope.
You cannow zoom in with the scope if you are standing on an edge of a wall.
You can now throw a grenade streight down if you are standing on an edge of a wall.
Fixed the bug where you couldn't hit players if they were on a staircase.
translation system fixes, including a bug where the game crashed by some lines when translating.
Fixed a small bug with the walking speed of the SVD.
Fixed a bug where lockers didn't explode.
Fixed the VIP kills. It now shows the correct number of kills the VIP has made.

new in 1.22
server changes:
Made the side range of the machete swing smaller. It is now an angle of 90 instead of 180 degrees.
Lowered the amount of simon sounds to 5 per security level.
fixed a bug where you could get up to strange place on the map by using a bug with objects.
client changes:
changed translation a bit. Adds %s to skip texts. Texts are also only translated if they are complete.
Fixed a bug where some characters were not translated correctly.
patched some more bugs with the translation system.

new in 1.21
server changes:
Fixed the bug where machete swing and knife throw didn't count in the weapon competition event.
The cool down time of skills are now always 0 if you respawn.
client changes:
this is very experimental, but we have added a translation system to the game. For an example, see the dutch.txt file in the Languages ​​folder.
Fixed the issue where players couldn't startup the game.
Fixed a bug with the scope of the sniper where you didn't hert player sounds.
Fixed the bug where you would hear bird sounds when the map was done loading and you didn't take a step.
Did some inprovements to the mapload function.
Fixed a minor bug where characters wouldn't speak when you pressed Backspace if you didn't have the pronounce letters setting enabled.

new in 1.2
server changes:
Changed how the welding machine works. Every battery restores 15000 solity points.
Made the get staff members function faster.
Fixed a bug where you could place a ladder in a wall.
Did some changes to the destroy objects event. Increased the maximum score and fixed a bug where you got event points if you destroyed ladders.
Removed the helmet's mute function.
Tried to fix a bug where people couldn't leave a team.

client changes:
Added the third chapter of the story. You need to be level 10 to unlock this chapter.
Added armor. For now we only have the helmet, which prevents you from getting headshots, butwe're adding more in the future.
Added a new item, the ladder. This ladder can be placed everywhere in the map. You can use it to climb to windows or roofs of houses.
Added a new melee weapon, the flale. It is a weapon that uses the same meganic as the machete swing skill, except that it has a total of 90 degree  hitbox, where the machete_swing's hit box is 180 degrees.
Added a new event. Destroy objects.
Fixed a bug with falling damage. If you now fall from 11 tiles high you lose less health.
Fixed the bug where settings didn't save.
Fixed a bug where the game didn't say a name was already in use if you created an account.
added more sounds to the learn game sounds menu.

new in 1.13
server changes:
Team chat sounds will now be played in the lobby.
Fixed a bug where a corpse disappeared if a player that died was looting it.
Experimental lag inprovements.
Added a new skill: beeing a docter.
If you now aim completely downwards and you are standing on a ledge of an abyss, you can now shoot over the ledge. This is useful, for example, if you are standing from a window on the second floor of a house.
You can now see if a player is in the lobby or on the map in the player menu.
The server will now report to you how many bullets in your belt you have left for you gun if you press A.
Fixed a bug with the infrared scanner where members of your team were signed as enemies.

client changes:
Added a password reset system. Please note that you need to set a e-mail addres on your account to let this work.
lowered the volume of the hk_mg4 fire sounds.
jumps will reset now if you die.
Fixed a bug with capital letters in the first letter navigation in menus.
Fixed a bug where you fired a machine gun for unlimited time if you opened a menu.
fixed that some buffers muting didn't save.

new in 1.12
server changes
You no longer can place a locker that is on an unstable platform, such as a table.
Made an option in the server menu which shows all staff members.
Fixed the survive timer.
lag inprovements
experimental lag inprovements with bullets.
Tried to fix a bug where objects didn't remove it self correctly after falling.
your survive timer will pause now if you are in the lobby.
client changes:
new in 1.12
added more sounds to the learn game sounds menu.
You now hear how many sounds you have to play in a simon if it starts.
Fixed sounds not playing correctly when looking through a scope.
fixed the broken updater.
Fixed the bug where the settings didn't save after an update of the client.
Tried to fix the bug where players glidge through staircases.
lag inprovements

new in 1.11
server changes:
You can only upgrade stats of the locker when you have the placing lockers right.
You can now set your email adress in the account options. Your email adress will be used for password resetting, which will be added in the next client update.
Made a teams buffer which saves all things related to your team such as team management and notifys of getting team tokens for destroying lockers.
Your scanner mode will now be saved if you die.
Fixed a bug where people were stuck in their team.
You now get team tokens for destroying other lockers.
Made that you have to do less memories of simon to break in to a locker.
You get now an extra menu which asks if you are realy sure to delete your team.
There is now an option in the team menu which shows all teams on the server and an option which shows all teams on the server that have a locker.
You can now see in a team profile how much team tokens that team has.
added the death messages buffer.
Fixed a bug with the sharp shooter mastery skill and the range of the fm_f2000.
Fixed a bug where people didn't spawn with a full pistol clip when they respawn.

client changes:
Replaced the math calculation for a simon game by breaking the security of the locker.
Made the fire sounds of the silenced guns a little bit louder.
You can now give a weapon if you only have one of them.
Tried to fix the bug where the updater would download a corrupted setup of the game.
An error dialog has been added if there wend something wrong with the loading of musics.
new in 1.1
you can no longer put large weapons in your holster using shift + accent graf.
client changes:
Made almost every weapon available at level 1. This was done because of the following changelog entry.
Added masteries for different types of weapons. These are basically skills, but you can level them up to a maximum of level 8 and you get skill points for killing people with a mastery weapon. For example, if you have a shotgun mastery active and you make kills with a shotgun, you will get skill points for all your shotgun masteries that you have actieve in your skill set.
Added recoil for automatic weapons. The chance is greater if you keep the gun on automatic fire for a longer period of time.
Added silencers for every sub_machine_gun. You can find those on the map.
You can now press alt + accent graf to put your current weapon in your holster.
Added a learn game sounds option in the main menu to help new players become familiar with commonly used sounds in the game.
Changed the infrared scanner sound for a team member.
Fixed the spelling error bug with the colt_m1911
The W key scanner will now support the scope so you can now see who you are going to snipe.
You can now rotate while using the scope when fully zoomed out.
new in 1.0
Fixed the bug where players didn't got event points.
Fixed a bug where you couldn't unload a weapon sometimes.
Made explosives less effective on lockers.
The feature of doing math calculations for lockers is temporary disabled.
the hk_mg4 will do 120 instead of 150 damage.
machete swing's cooldown is now 25 instead of 10 secondes.
Mutes will save now.
You will now spawn with a fully loaded colt_m1911
added an option to see which kills and deaths you see. You can find it in the account options
Added an account options in the server menu which will be used for all misc options for your account. For now you can only delete your account, but more is comming.
You will now get a notify if you come online and you have 1 or more unread staff messages.
You no longer can be chosen as VIP when you're in the respawn menu.
Made leveling a little bit easyer.
Death players will no longer fire bullets.
exiting the game while your dieing wouldn't get you back in the position where you died.
You can now kick players that are offline from your team.
Implemented a small method to stop endless shooting.
VIP timer is now 5 instead of 15 minutes.
Lag inprovements for the W key scanner.
You will now get 30 instead of 20 9mm_ammo if you spawn, since the colt_m1911 does less damage.
You now get a xp bonus if you kill someone that is a higher level than you.
De colt_m1911 en ruger_mark_IV_tactical do now less damage.
Fixed grenades.
Trys to patch the bug where the scanner didn't see walls or objects.
Fixed an issue where you would not lose a grenade if you held it in your hand.
Tried to fix the bug where people can get killed in the lobby.
You no longer get reset to the English chat channel when you die.
Fixed an issue where objects would not spawn properly.
Recoded objects to inprove the speed of the code. If you find any bugs please let us know.
You will get a notify if you've got an invite for joining a team.
Added staff message buffer.
Tried to fix that everyone could hear the staff message close sound.
Tried to fix the server crash with the VIP event.
From now on you must have a high enough level to get a weapon from a locker. So you can no longer get an ARX160 from the locker at level 5.
The desk should now play the fall sounds if you push it from a staircase.
You can now go to the lobby even if a player from your team is nearby.
Fixed a bug where players could not see the weapon they took from the locker.
Serverside support for higher pitch sounds for team members by the infrared scanner.
There is now an option in your team's menu that provides information about the coordinates of your team's locker.
Teams without members are automatically deleted now.
You can't go to the lobby if someone is close to you.
the landing knowledge skill no longer makes you immune to all falling damage.
Chests will open now. Something wend wrong while I was fixing some spelling things.
staff message sounds are no longer plaid for everyone. Only the admins and the player who has created the staff message will hear it.
VIP kills should work now.
players beeing in the lobby are no longer recognized by the infrared scanner.
Players no longer have to go offline for a server update.
You will no longer spawn near the location where you died.
Adds saving of staff messages.
If you now click on the A key  you can also see which bullets the weapon that you are holding uses.
"""
class announcement():
 def __init__(self,name,text):
  self.name=name
  self.text=text.split("\n")
  self.read=[]
  list=[]
  for a in v.admin_messages:
   list.append(a.id)
  self.id=random.randint(0,100000000)
  while self.id in list:
   self.id=random.randint(0,100000000)
  self.tijd,self.datum=get_time()
  self.create_time=self.tijd+" "+self.datum
 def save(self):
  data={
"name": self.name,
"text": self.text,
"read": self.read,
"create_time": self.create_time
}
  return data
 def load(self,data):
   self.name=data["name"]
   self.text=data["text"]
   self.read=data["read"]
   self.create_time=data["create_time"]
def get_announcements_index(id):
 for p in v.announcements:
  if p.id==id:
   return v.announcements.index(p)

class object_preset():
 def __init__(self,name,**kwargbs):
  self.name=name
  self.upper_class=kwargbs.get("upper_class", "" )
  self.hitsounds=kwargbs.get("hitsounds", "" )
  self.health=kwargbs.get("health", 0)
  self.moveable=kwargbs.get("moveable", False )
  self.movetime=kwargbs.get("movetime", 0)
  self.movesounds=kwargbs.get("movesounds", "" )
  self.examinable=kwargbs.get("examinable", False )
  self.examinesounds=kwargbs.get("examinesounds", "" )
  self.lootitems=kwargbs.get("lootitems", 0 )
  self.mapdata=kwargbs.get("mapdata", "" )
def load_object_preset(data):
 upper_class=""
 name=""
 examinesounds=""
 lootitems=0
 hitsounds=""
 health=0
 moveable=False
 movetime=0
 movesounds=""
 examinable=False
 mapdatalines=[]
 lines=data.split("\n")
 for l in lines:
  if l=="@vehicle":
   upper_class="vehicle"
  parsed=l.split(": ")
  if parsed[0]=="name":
   name=l.replace("name: ","")
  elif parsed[0]=="movesounds":
   movesounds=l.replace("movesounds: ","")
  elif parsed[0]=="hitsounds":
   hitsounds=l.replace("hitsounds: ","")
  elif parsed[0]=="examinesounds":
   examinesounds=l.replace("examinesounds: ","")
  elif parsed[0]=="health":
   try:
    health=int(l.replace("health: ",""))
   except ValueError:
    pass
  elif parsed[0]=="movetime":
   try:
    movetime=int(l.replace("movetime: ",""))
   except ValueError:
    pass
  elif parsed[0]=="lootitems":
   try:
    lootitems=int(l.replace("lootitems: ",""))
   except ValueError:
    pass
  elif parsed[0]=="moveable":
   if parsed[1]=="yes":
    moveable=True
  elif parsed[0]=="examinable":
   if parsed[1]=="yes":
    examinable=True
  else:
   mapdatalines.append(l)
 mapdata="\n".join(mapdatalines)
 name=name.replace(" ","_")
 o=object_preset(name,health=health,hitsounds=hitsounds,movesounds=movesounds,movetime=movetime,moveable=moveable,examinable=examinable,mapdata=mapdata,lootitems=lootitems,examinesounds=examinesounds, upper_class = upper_class)
 v.object_presets.append(o)
