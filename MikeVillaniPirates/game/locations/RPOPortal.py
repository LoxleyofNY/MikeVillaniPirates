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

# "A missing link, a game not finished.\n"

# "Retrace your steps, unveil the hidden.\n"

# "And the secret of the maze will be yours at last.\n")
            
class Rock_Paper_Scissors:
    
        def __init__(self):
            #consists unchangable
            self.WIN = "Winner!"
            self.LOSE = "Loser!"
            self.DRAW = "Stalemate!"
            self.player_score = 0
            self.computer_score = 0
            self.round_number = 1

        def getRules(self):
            #Dictionary of rules in which one results an outcome
            self.rules = {
                "Rock": {"Rock": self.DRAW, "Paper": self.LOSE, "Scissors": self.WIN},
                "Paper": {"Rock": self.WIN, "Paper": self.DRAW, "Scissors": self.LOSE},
                "Scissors": {"Rock": self.LOSE, "Paper": self.WIN, "Scissors": self.DRAW}}
            return self.rules
        

        def roundGame(self):
            self.rpc = True

            while self.rpc is True:

                print(f"\nRound {self.round_number}")

                self.player_choice = input("Enter your choice (Rock/Paper/Scissors): ").capitalize()

                if self.player_choice not in self.rules:
                    print("Please enter Rock, Paper, or Scissors")
                    continue

                self.computer_choice = random.choice(["Rock", "Paper", "Scissors"])
                print(f"Computer chose {self.computer_choice}")

                result = self.rules[self.player_choice][self.computer_choice]
                print(result)

                if result == self.WIN:
                    self.player_score += 1
                elif result == self.LOSE:
                    self.computer_score += 1
                    self.player_score == 0

                print(f"\nScores - Players: {self.player_score}, Computer: {self.computer_score}")

                if self.player_score == 3:
                    self.rpcwin()
                    self.rpc = False

                play_again = input("Do you want to play again? (yes/no): ")
                if play_again != 'yes':
                    break

                self.round_number += 1

        def rpcwin(self):
            print(
                "Hail, triumphant one! Thrice victorious in the mystical game of rock, paper, scissors - a magic trinity! \n"
                "Remember, the number three holds a secret enchantment. As you journey forth, await its unexpected power. Three is the key to a destiny woven in magic!")
            config.the_player.add_to_inventory([self.CopperKey()])
            print("Copper Key has been added to inventory!")
            print("Token: 01110110 01101001 01101100 001101100 01100001 01101110 01101001")
            #Return to portal with wizard

            
        def playGame(self):
            self.__init__()
            self.getRules()
            self.roundGame()

class Hangman:
        def __init__(self):
            """Set up the hangman game by getting the word to guess and initializing the game's state"""
            self.setWord(self.getWord())
            self.gameWon = False
            self.gameWon2 = False
            self.gameLost = False
            self.errorCount = 0
            self.GUESS_LIMIT = 6
            self.ALPHABET = "abcdefghijklmnopqrstuvwxyz"

        def setWord(self, word):
            """Sets the given word as the word to guess, updating the working word and the list of already guessed letters as well."""
            self.wordToGuess = self.getWord().lower()
            self.workingWord = ["" if char == " " else "-" for char in self.wordToGuess]
            self.guessedAlready = []


    #The functions above this point are "given," you don't need to modify them.
        
        def getWord(self):
            """Returns a word to be guessed."""
            return "The Shinning Directed by Stanley Kubrick"
        
        def getTextPerson(self, stage):
            """Returns a single string, suitable to be printed, depicting the person at the given stage of the game."""
            if stage == 0:
                return " +---+\n  |   |\n      |\n      |\n      |\n      |\n========="
            if stage == 1:
                return "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n========="
            if stage == 2:
                return "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n========="
            if stage == 3:
                return "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n========="
            if stage == 4:
                return "  +---+\n  |   |\n  O   |\n /|\  |\n      |\n      |\n========="
            if stage == 5:
                return "  +---+\n  |   |\n  O   |\n /|\  |\n /    |\n      |\n========="
            if stage == 6:
                return "  +---+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n========="
            
        def allowableGuess(self, guess):
            """Returns true if guess is a single letter string that does not appear in guessedAlready. Assumes guess is a string."""
            if guess not in self.ALPHABET: #if the guess isn't in Alphabet List, return false
                return False

            if guess in self.guessedAlready: #if guess is IN guessedAlready list, return false
                return False

            guess_len = len(guess)

            if guess_len != 1: #if length isn't single char
                return False

            return True #if guess passes top 3 parameters return True

        def updateGame(self, guess):
            """Updates the game's state in response to the provided guess. Updates workingWord, guessedAlready, errorCount, and whether the game is won or lost."""

            if self.allowableGuess(guess):
                for i, g in enumerate(self.wordToGuess): # Iterate  the elements of wordToGuess with both index i and character g
                    if g == guess:
                        # Check if the character is not a space
                        if g != ' ':
                            self.guessedAlready.append(g)
                            self.workingWord[i] = guess
                        continue

                    if g != guess:
                        self.errorCount += 1

            if self.errorCount == self.GUESS_LIMIT:
                self.gameLost = True
            
            if self.workingWord == self.wordToGuess:
                self.gameWon = True
                if self.wordToGuess == "Stephen King":
                    self.gameWon2 = True


    ###Functions below this point assume that the game is being played on the terminal, and can use print and input.
        def showInTerminal(self):
            """Prints the current state of the game to the terminal (the ASCII graphic of the person, the working state of the word, and the letters guessed so far)."""
            print(self.getTextPerson(self.errorCount))
            print("Current Word: ", self.workingWord)
            print("Guess List: ", self.guessedAlready)
            
            if self.gameWon == True:
                print("Impressive progress, seeker! The second stanza's secrets are yours, but the creator's discontent in the first line still eludes thy grasp. Illuminate that shadowed path, and the revelation awaits.")
                print("A creator who hates his own creation")
                self.setWord = "Stephen King"
                self.gameLost = True

            if self.gameWon2 == True:
                print("Well done, astute seeker! The riddles have yielded to your wizardry. Remember the author's discontent for future endeavors, and may your journey be ever enchanted.")
                #config.the_player.add_to_inventory([JadeKey()])
                print("Jade Key has been added to inventory!")
                print("Author: Stephen King")
                #Return to portal with wizard


        def getGuessFromTerminal(self):
            """Gets the next guess from the user.
                Returns the user's guess if and only if the guess is allowable
                Repeats until the user enters an allowable guess.
            """
            player_guess = input("Guess a Letter: ") #gets guess from the user
            allow_guess = self.allowableGuess(player_guess.lower())

            if player_guess.lower() == "exit": #if exit is given, code stops
                exit()

            if allow_guess == True: #while the allowableGuess function outputs True with player_guess fed in
                return player_guess #return the players guess

            elif not allow_guess:
                print("Not Acceptable Guess")
                return self.getGuessFromTerminal()


        def playGame(self):
            """Instructs the game to play itself with the user in the terminal."""
            self.__init__()
            self.setWord(self.getWord())
            while not (self.gameWon or self.gameWon2 or self.gameLost):
                self.showInTerminal()
                print("Hint: genre defining horror movie")
                self.updateGame(self.getGuessFromTerminal())
            
class GuessingGame:
        def __init__(self):
            self.num = 42 
            self.user_number = 0
            self.done = False
            
        def getRules(self):
            return ("Whats the meaning of life? Whats the answer ultimate? Pick a number 1 - 100")

        def checkGameDone(self):
            if self.done == True:
                return True
            else:
                return False

        def markGameDone(self):
            if self.user_number == self.num:
                self.done = True
                print("Huzzah, clever seeker! The cosmic truth unfolds before thee - the meaning of life is 42!\n "
                      "Now, in the spirit of jest, divide this cosmic wisdom by the magic number, and unveil the true magic that lies within the galaxy")
                config.the_player.add_to_inventory([CrystalKey()])
                print("Crystal Key has been added to inventory!")
                print("Sector: 14")
                #Return to portal with wizard

                

        def wrongGuess(self):
            if self.user_number != self.num:
                self.done = False
                
        def checkGuess(self, guess):
            if guess > self.num:
                    return 1
            elif guess < self.num:
                    return -1
            elif guess == self.num:
                    return 0

        def guessNoHints(self, output):
            if output == 1 or output == -1:
                print("Sorry Try Again")
                self.wrongGuess()
            elif output == 0:
                self.markGameDone()


        def playGame(self):
            self.__init__()
            print(self.getRules())
            
            while not self.checkGameDone():
                self.user_number = int(input("\n------->"))
                result = self.checkGuess(self.user_number)
                self.guessNoHints(result)    

def FirstKey(self): #RPC to Binary Win 3x in row     
    class CopperKey (Item):
        def __init__ (self):
            super().__init__("Copper Key", 333)
            self.name = "copper_key"
            self.description = "The worn, ancient copper key, bearing the scars of countless adventures, whispers tales of bygone eras and long-lost secrets."
            self.inscription = ("A creator who hates his own creation.\n")

    if __name__ == "__main__":
        game = Rock_Paper_Scissors()
        game.playGame()
     
def SecondKey(self): #hangman for Shining
    class JadeKey (Item):
            def __init__ (self):
                super().__init__("Jade Key", 237)
                self.name = "jade_key"
                self.description = "A serene jade key, gracefully carved, exudes tranquility and guards secrets within its vibrant essence."
                self.inscription = ("If you know the answer ultimate,\n"

"divide it by the number magic\n"

"and what you, need, want and desire will be found in the fortress tragic.\n")
    #Should create a Hangman instance, play it, and then give the player the key if they win.
    if __name__ == "__main__":
        game = Hangman()
        game.playGame()
     
def ThirdKey(self):#Guessing Game answer ultimate
    class CrystalKey (Item):
            def __init__ (self):
                super().__init__("Crystal Key", 42)
                self.name = "crystal_key"
                self.description = "A key of pure crystal, crystal clear and refracting light, possesses an ethereal beauty, its pristine facets concealing the mystic echoes of untold enchantments."
                self.inscription = ("In realms entwined with magic's grace,\n"
"Gather keys of jade, crystal, and copper's embrace.\n"
"Three truths unveiled, let wisdom shine,\n"
"Return to me, seeker, with treasures thine.\n"
"With keys and knowledge, a convergence divine,\n"
"Unlock the hidden, where secrets intertwine.\n"
"And, seeker, as jest and wisdom align,\n"
"I hope thou hast been paying attention fine!")
                
    if __name__ == "__main__":
        game = GuessingGame() #makes a new game
        game.playGame() #words containing (dot) . a reading right to left, and . is read "this part"
 
    
    
    
