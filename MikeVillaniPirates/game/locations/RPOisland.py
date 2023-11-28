from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

class RPOIsland(location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "RPO"
        self.symbol = 'R'
        self.visitable = True
        self.starting_location = Dock(self)
        self.locations = {}

        self.locations["Portal"] = Portal(self)
        self.locations["Dock"] = self.starting_location
        
        self.locations["northBeach"] = NorthBeach(self)
        self.locations["southBeach"] = SouthBeach(self)
        self.locations["eastBeach"] = EastBeach(self)
        self.locations["westBeach"] = WestBeach(self)
        self.locations["middle"] = Middle(self)
        
        self.locations["scroll"] = Scroll(self)
  
        
    def enter (self, ship):
        print ("You've sailed to a island that looks empty, or atleast it seems like it.")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()
        
class Dock (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Dock"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
                
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "dock"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "east" or verb == "west" or verb == "north" or verb == "south"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]
    
    def enter (self):
        announce ("The dock is empty, just a wooden bridge sitting still in the water and land. \n" +
                  "Looking to the island you see nothing, sand from edge to edge\n" +
                  "You get a werid feeling there *is* something here, you sense something calling you")
            
class WestBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "westBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self

        self.event_chance = 25
        self.events.append(seagull.Seagull())

    def enter (self):
        description = "You walk upon the west beach of the island.\nThere is nothing here."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["eastbeach"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]
            
            
class SouthBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "southBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 50
        self.events.append(seagull.Seagull())

    def enter (self):
        description = "You walk upon the south beach of the island.\nJust the dock and your ship lay still."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["eastbeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]
            
class EastBeach (location.SubLocation): #holds the scroll
    def __init__ (self, m):
        super().__init__(m)
        self.name = "eastBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['pick up'] = self
        self.verbs['west'] = self

        self.event_chance = 15
        self.events.append(seagull.Seagull())

    def enter (self):
        description = "*PING*PING*\nYou walk upon the east beach of the island.\nThe sand is smooth beneath your feet.\nAs you walk around something metallic hits your foot."

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "pick up"):
            config.the_player.next_loc = self.main_location.locations["scroll"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]
            
            
class Scroll (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "scroll"
        self.verbs['read'] = self
        self.verbs['drop'] = self
        
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "read"):
            self.ScrollRiddle()
            
    def ScrollRiddle(self):
        riddle = self.GetRiddle
        
    def GetRiddle(self):
        announce("Upon the Isle of Lost Souls, where shadows dance and legends unfold,"
"Stand ye East, gaze West, cutlass high, a tale to be told."
"In the moon's soft caress, secrets untold shall align,"
"Raise thy blade to the sky, where stars in whispers entwine."

"A portal awaits, a gateway unknown,"
"Through the mystic, the unseen, where souls find their own."
"What awaits beyond, a pirate's fate to reclaim,"
"Brave ye be, to stand true, and play in this mysterious game.")
        
class NorthBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "northBeach"
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        self.event_chance = 50
        self.events.append(seagull.Seagull())
        
    def enter (self):
        description = "You walk upon the north beach of the island.\nFacing opposite your ship, you hear something faintly coming from the left."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["eastbeach"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]
    
class Middle (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Middle"
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['north'] = self
        
class Portal (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "middle"
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['north'] = self
        self.verbs['approach'] = self
        self.verbs['enter'] = self



            



        