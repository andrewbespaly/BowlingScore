import os
from tabulate import tabulate
import keyboard
import time


# Callback function that runs whenever a key is pressed down
def retrieveKey(self, latestKeyPressRetriever):
    #print(self.name)
    latestKeyPressRetriever[0] = self.name
    latestKeyPressRetriever[1] = True

    #print(keyToSet)
    # print(keyboard.read_key())


# Make sure input is 0-9, x, X, /, (R to reset)
def validateKeyPress(latestKeyPress):
    #print('not yet implemented')
    return True


# Add next shot taken onto the scoreboard in the latest shot position
def addToScoreBoard(currentShot, entireScoreBoard):
    entireScoreBoard["1"][1] = currentShot


# Clears the previous board and displays the updated one
def displayBoard(entireScoreBoard):
    os.system('cls')
    print(tabulate(entireScoreBoard, headers="keys", tablefmt="fancy_grid", stralign="center"))


def main():
    # Passing in a list into the on_press callback function because it's a mutable object and will change in this scope
    latestKeyPressRetriever = ["", False]
    keyJustPressed = False
    keyboard.on_press(lambda e: retrieveKey(e, latestKeyPressRetriever))
    latestKeyPress = latestKeyPressRetriever[0]
    # keyJustPressed = latestKeyPressRetriever[1]

    entireScoreBoard = {"1": ["1 | 2", 0], "2": ["3 | 4", 10], "3": ["5 | 6", 20], "4": ["7 | 8", 40], "5": ["9 | X", 50]}
    print(tabulate(entireScoreBoard, headers="keys", tablefmt="fancy_grid", stralign="center"))
    while(latestKeyPress != "esc"):
        latestKeyPress = latestKeyPressRetriever[0]
        keyJustPressed = latestKeyPressRetriever[1]
        if(validateKeyPress(latestKeyPress) and keyJustPressed):
            
            addToScoreBoard(latestKeyPress, entireScoreBoard)
            displayBoard(entireScoreBoard)
           
            latestKeyPressRetriever[1] = False # Set key press value to False in the retriever for it to stay upto date

        time.sleep(0.01)
    
    displayBoard(entireScoreBoard)
    print("Thanks for playing!")


if __name__ == "__main__":
    main()