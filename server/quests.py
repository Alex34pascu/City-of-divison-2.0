import v
v.get()

cutseens={
"cutseen_intro1.ogg": "chapter 1 intro",
"cutseen_intro2.ogg": "chapter 1 part 3",
"cutseen_The_factory1.ogg": "chapter 2 part 1",
"cutseen_The_factory2.ogg": "chapter 2 part 3",
"cutseen_The_factory3.ogg": "chapter 2 part 4",
"cutseen_jack1.ogg": "chapter 3 part 1",
"cutseen_jack2.ogg": "chapter 3 part 4",
"cutseen_the_quarry.ogg": "chapter 4 part 1",
"cutseen_jack3.ogg": "chapter 5 part 1",
"cutscene_final1.ogg": "chapter 6 part 2",
"cutscene_final2.ogg": "chapter 6 part 4",
"cutscene_final3.ogg": "chapter 6 part 5",
"cutscene_final4.ogg": "chapter 6 part 6",

}

class quest():
 def __init__(self,name):
  self.name=name
  self.item=""
  self.needed_quest=""
  if self.name=="chapter 1 intro":
   self.task="View the intro cutseen, and then go to part 1 of chapter 1 to see what you can do."
   self.item=""
   self.level=1
   self.reward={}
   self.unlock_quest="chapter 1 part 1"
   self.unlock_by_level=True
  elif self.name=="chapter 1 part 1":
   self.task="After watching the intro cutseen, find evidence of what happened to James."
   self.item="corpse_of_James"
   self.level=1
   self.reward={}
   self.unlock_quest="chapter 1 part 2"
   self.unlock_by_level=True
  elif self.name=="chapter 1 part 2":
   self.task="""After finding the corpse of James, you wonder who did this. There must have been something written about it somewhere, right?\n
   See if you can find information about the murder."""
   self.item="newspaper_article_about_the_murder_of_James"
   self.level=1
   self.reward={}
   self.unlock_quest="chapter 1 part 3"
   self.unlock_by_level=False
  elif self.name=="chapter 1 part 3":
   self.task="""In the newspaper that you found, stands the following\n
   ---\n
The main suspect in the case of James's murder is the 46-year old mister A. Smid, who had an argument with the victim the day James was murdered.\n
Many witnesses also told the police that the victim had more arguments with his neighbors, especially about the 25-year-old man's alcohol consumption and agressive behavior.\n
---\n
Find out who killed James, And find the weapon it was done with."""
   self.item="long_knife"
   self.level=1
   self.reward={"golden chest": 1}
   self.unlock_quest=""
   self.unlock_by_level=False
  elif self.name=="chapter 2 part 1":
   self.needed_quest="chapter 1 part 3"
   self.task="""To the south of the city, something happend in a large factory.\n
People say there was a shooting.\n
You wonder what happend, so you head over to the abandoned factory to look for some kind of evidence."""
   self.item="directors_ID_card"
   self.level=5
   self.reward={}
   self.unlock_quest="chapter 2 part 2"
   self.unlock_by_level=True
  elif self.name=="chapter 2 part 2":
   self.task="""On the id_card you see a picture of the director of the factory, although a few years younger
Seeing the foto, you suddenly remember he was quite a rich  citizen, living in one of the larger houses.
---
Find out where the director lives, and where he went after he survived the shooting."""
   self.item=""
   self.level=5
   self.reward={}
   self.unlock_quest="chapter 2 part 3"
   self.unlock_by_level=False
  elif self.name=="chapter 2 part 3":
   self.task="Look for evidence of what happend to the director in the manor"
   self.item="corpse_of_brown_haired_man"
   self.level=5
   self.reward={}
   self.unlock_quest="chapter 2 part 4"
   self.unlock_by_level=False
  elif self.name=="chapter 2 part 4":
   self.task="""See if you can find out if the director made it.\nProbably, he was brought to the nearest hospital.\nBut did the attackers leave it by that?"""
   self.item="corpse_of_director"
   self.level=5
   self.reward={"golden chest": 1}
   self.unlock_quest=""
   self.unlock_by_level=False
  elif self.name=="chapter 3 part 1":
   self.needed_quest="chapter 2 part 4"
   self.task="Rumors go around that Jack was about to find something out about the murderer of James. Go to his house, and see if you can find something that provides more information."
   self.item="Handwritten_map_of_Andrew's_house"
   self.level=10
   self.reward={}
   self.unlock_quest="chapter 3 part 2"
   self.unlock_by_level=True
  elif self.name=="chapter 3 part 2":
   self.task="Watch the unlocked cutcene and collect more evidence."
   self.item=""
   self.level=10
   self.reward={}
   self.unlock_quest="chapter 3 part 3"
   self.unlock_by_level=False
  elif self.name=="chapter 3 part 3":
   self.task="The body of Andrew is no where to be found, and you wonder where it went. \n People wisper that they saw Jack heading to the woods, carrying something heavy. \nHead to the woods, and find out what happend."
   self.item="corpse_of_Andrew"
   self.level=10
   self.reward={}
   self.unlock_quest="chapter 3 part 4"
   self.unlock_by_level=False
  elif self.name=="chapter 3 part 4":
   self.task="Now you found Andrew's deformed body, you wonder about all the bullet holes you saw in the trees on your way through the forest. You also remember hearing several gun shots the night before. \nLook for clues, and see if you can find the firearm that has fired the shots. \nHint, think of a good place to snipe from."
   self.item="Jeremy's_sniper_rifle"
   self.level=10
   self.reward={"golden chest": 1}
   self.unlock_quest=""
   self.unlock_by_level=False

  elif self.name=="chapter 4 part 1":
   self.needed_quest="chapter 3 part 4"
   self.task="A family has gone missing with out a trace. For all you know, a car was found in a ditch, abandoned, and with broken windows.\n Find out which family it was, and continue on from there."
   self.item=""
   self.level=15
   self.reward={}
   self.unlock_quest="chapter 4 part 2"
   self.unlock_by_level=True
  elif self.name=="chapter 4 part 2":
   self.task="Watch the cutscene related to chapter 4, and follow the Edward family to find out what happend."
   self.item=""
   self.level=15
   self.reward={"golden chest": 1}
   self.unlock_quest=""
   self.unlock_by_level=False


  elif self.name=="chapter 5 part 1":
   self.needed_quest="chapter 4 part 2"
   self.task="What happend to Jack after he after he fled? And to Jeremy? \nhead back to the woods, and look for any signs of what happend after Jack fell into the water."
   self.item="Jeremy's_headless_body"
   self.level=20
   self.reward={}
   self.unlock_quest="chapter 5 part 2"
   self.unlock_by_level=True
  elif self.name=="chapter 5 part 2":
   self.task="Who is the thirt shooter, (the blond man) that managed to escape? \nGo to the gas station, and see if you can find anything that might tell you more about the blond hitman than you would initially think."
   self.item="tool_box_with_the_figures_k.r_written_on_it"
   self.level=20
   self.reward={"golden chest": 1}
   self.unlock_quest=""
   self.unlock_by_level=False
  elif self.name=="chapter 6 part 1":
   self.needed_quest="chapter 5 part 2"
   self.task="""During the last quest, you found a toolbox with the initials K.R.\n
Find the house that belongs to a pedestrian with these initials, and investigate."""
   self.ite=""
   self.level=25
   self.reward={}
   self.unlock_quest="chapter 6 part 2"
   self.unlock_by_level=True
  elif self.name=="chapter 6 part 2":
   self.task="""Now that you found the house, you wonder what happend to the blond man, (Kevin), after he escaped out of the woods.\n
Get inside the house, and see if you can find some kind of secret hiding place where information could be gathered."""
   self.item=""
   self.level=25
   self.reward={}
   self.unlock_quest="chapter 6 part 3"
   self.unlock_by_level=False
  elif self.name=="chapter 6 part 3":
   self.task="""Watch the cutsceene that belongs to the previous part. Ones you're done, return here.
---
Jack went to the manor to investigate the shooting he read about online. Find evidence of Jack sneaking into the manor."""
   self.item="broken_tree_branch"
   self.level=25
   self.reward={}
   self.unlock_quest="chapter 6 part 4"
   self.unlock_by_level=False
  elif self.name=="chapter 6 part 4":
   self.task="""There has been a wild chase in town, and everyone is talking about it.
---
Jack went to the manor, and managed to break in.
Find out how Jack' was spotted during his search through the manor, and how his pursuers managed to trace his location."""
   self.item=""
   self.level=25
   self.reward={}
   self.unlock_quest="chapter 6 part 5"
   self.unlock_by_level=False
  elif self.name=="chapter 6 part 5":
   self.task="""Kevin and Tim had been chasing Jack through out the entire city, leaving a lot of evidence behind.
Collect signs of the desctruction."""
   self.item="crashed_motorcycle"
   self.level=25
   self.reward={}
   self.unlock_quest="chapter 6 part 6"
   self.unlock_by_level=False

  elif self.name=="chapter 6 part 6":
   self.task="""View the cutscene of chapter 6 part 5. Ones you're done, return back here.
---
John had a vivid nightmare, that turned real before he knew it.
Find the weapon John saw when Jack dropped it."""
   self.item="Busted_up_pistol"
   self.level=25
   self.reward={"diamond chest": 1}
   self.unlock_by_level=False



  else:
   self.task=""
   self.item=""
   self.level=-1
   self.reward={}
   self.unlock_quest=""
   self.unlock_by_level=False
