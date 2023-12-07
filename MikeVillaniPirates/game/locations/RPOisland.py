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
import game.locations.RPOPortal as keyHandling

class RPOIsland(location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "RPO"
        self.symbol = 'R'
        self.visitable = True
        self.starting_location = Dock(self)
        self.locations = {}

        self.locations["Dock"] = self.starting_location
        
        self.locations["northBeach"] = NorthBeach(self)
        self.locations["southBeach"] = SouthBeach(self)
        self.locations["eastBeach"] = EastBeach(self)
        self.locations["westBeach"] = WestBeach(self)
        self.locations["bluePortal"] = Portal(self)
        
        
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
        self.verbs['enter'] = self
        self.verbs['test'] = self


        self.verbs['portal'] = self
                
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "dock"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "east" or verb == "west" or verb == "north" or verb == "south"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Beach"]
        elif (len(cmd_list) >= 2 and cmd_list[0] == 'enter' and cmd_list[1] == 'portal'):
            config.the_player.next_loc = self.main_location.locations["bluePortal"]
            config.the_player.go = True

    
    def enter (self):
        announce ("The dock is empty, just a wooden bridge sitting still in the water and land. \n" +
                  "Looking to the island you see nothing but sand and a sign.\n" +
                  "The Sign reads as follows:\n" + 
                  "====================\n"+
                  "======Welcome to====\n"+
                  "==Ready Player One==\n"+
                  "=======Island!======\n"+
                  "====================\n"+
                  "You get a werid feeling there's something here, you sense something calling you")
        
class Portal (location.SubLocation): #player needs to be able to go to this location and play the games/challenges
    def __init__ (self,m):
        super().__init__(m)
        self.name = "bluePortal"
        self.verbs["first"] = self
        self.verbs["second"] = self
        self.verbs["third"] = self
      
    def enter (self):
        description =  ("A grand ancient wizard is draped in starlit robes, with a flowing silver beard that whispers of eons past. His eyes, pools of ancient wisdom, hold the secrets of countless realms.\n"
               "A gnarled staff, etched with cosmic runes, anchors the magic that resonates with each step."
               "Adorned in celestial symbols, he stands, a living bridge between the arcane and the timeless, a brief glimpse into the vast expanse of cosmic knowledge.\n"
               "-------------He begins to speak-------------")
        announce(description)
        
        greeting = ("Anorak, the all knowing:\n Greetings, seeker of the OASIS. I am Anorak the all-knowing. I've created a quest for those looking for a challenge, and a prize.\n"
              "Three keys lie veiled, each guarded by clever trials woven into the fabric of our digital world.\n"

    "In the dance of Rock, Paper, Scissors, discover the First Key. Unravel the secrets of language in Hangman to claim the Second Key. Embrace the intuitive dance of a guessing game for the last\n."

    "These challenges are your gateway to untold knowledge. Traverse the digital expanse, decipher the puzzles, and may the keys unveil themselves to those who tread the path of insight.\n" 
    "Commence your quest, and may the OASIS yield its treasures to the clever and the wise.\n"
    "Enter (First/Second/Third) To start a challenge:")
        print(greeting)
        
            
    def process_verb (self, verb, cmd_list, nouns):
            if (verb == "return"):
                announce ("You return to the ship.")
                config.the_player.next_loc = config.the_player.ship
                config.the_player.visiting = False
                
            if (verb == "first"):
                keyHandling.firstkey(self)
            if (verb == "second"):
                keyHandling.secondkey(self)
            if (verb == "third"):
                keyHandling.thirdkey(self)
                
            elif (verb == "unlock"):
                    for item in config.the_player.inventory:
                        if item.name == "copper_key" and "jade_key" and "crystal_key":
                            config.the_player.inventory.pop(item.name)
                            config.the_player.add_to_inventory([GoldenEgg()])
                            break
                        
            
class GoldenEgg(Item):
            def __init__ (self):
                super().__init__("Golden Egg", 10000)
                self.name = "golden_egg"
                self.description = "The Prohencies Easter Egg"

class WestBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "westBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self

    def enter (self):
        description = "You walk upon the west beach of the island.\nThere is nothing here."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["eastBeach"]
        if (verb == "west"):
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
            config.the_player.next_loc = self.main_location.locations["eastBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]
            
class NorthBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "northBeach"
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
    def enter (self):
        description = "You walk upon the north beach of the island.\nFacing opposite your ship, you hear something faintly coming from the left."
        announce(description)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["eastBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        
            
class EastBeach (location.SubLocation): #handles the scroll
    def __init__ (self, m):
        super().__init__(m)
        self.name = "eastBeach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['take'] = self
        self.verbs['west'] = self
        self.verbs["portal"] = self
        self.verbs["raise"] = self
        self.verbs["cross"] = self

    
        self.scroll_taken = False
      
    def enter(self):
        description = "*PING*PING*\nYou walk upon the east beach of the island.\nThe sand is smooth beneath your feet.\nAs you walk around, something metallic hits your foot."
        announce(description)

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "take" and not self.scroll_taken:
            print("Scroll has been added to inventory!")
            self.scroll_taken = True
            config.the_player.add_to_inventory([RPO_Scroll()])
        elif verb == "take" and self. scroll_taken:
            print("There's nothing in the sand now.")
            
        elif (verb == "raise"):
            if len(cmd_list) > 1: #storing whats after read into list
                item_name = cmd_list[1]
                item_found = None
                for item in config.the_player.inventory:
                    if item.name == item_name:
                        item_found = item
                        break
                    
                if not (item_found is None):
                    print("You raise two cutlass' pointing to the sky")
                    
        elif (verb == "cross"):
            if len(cmd_list) > 1: #storing whats after read into list
                item_name = cmd_list[1]
                item_found = None
                for item in config.the_player.inventory:
                    if item.name == item_name:
                        item_found = item
                        break
                    
                if not (item_found is None):
                    print("Crosses the blades high, just like the scroll suggests")
                    print("*A giant flash of blue light fades into existence*")
                    print("*The blue light pops, like a light bulb, disappearing... Quickly re-materializing in front of you, merely blinding you*")
                    print("It seems to resemble a portal. An egg shaped blue portal, floating in space.")
    
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["eastBeach"]
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["westBeach"]
        if (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["southBeach"]
        if (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["northBeach"]
        if (verb == "portal"):
            config.the_player.next_loc = self.main_location.locations["bluePortal"]
            config.the_player.go = True
            
class RPO_Scroll (Item):
    def __init__ (self):
        super().__init__("scroll", 200)
        self.name = "scroll"
        self.description = "An ancient scroll that has a riddle, inscribed into the pages"
        self.inscription = ("To open the portal, a pirate must be wise,\n"
"With cutlass held high, 'neath the azure skies.\n"
"*Raise thy Blade and Cross them high*,\n"
"Speak the phrases, true and sly.\n"
"\n"
"When the words echo through the salty air,\n"
"A portal to the unknown shall appear.\n"
"Step through the shimmer, ye daring soul,\n"
"To a realm where mysteries take their toll.\n"
"\n"
"Beyond the veil, a new adventure awaits,\n"
"With islands to conquer and destinies to mate.\n"
"Embrace the unknown, with courage in thy eye,\n"
"For through the portal, a pirate shall fly.\n")
        


       


            



        