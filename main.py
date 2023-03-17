import os
from tabulate import tabulate
import keyboard
import time
import math

# Callback function that runs whenever a key is pressed down
def retrieveKey(self, latestKeyPressRetriever):
    #print(self.name)
    latestKeyPressRetriever["keyPressName"] = self.name
    latestKeyPressRetriever["keyJustPressed"] = True

    #print(keyToSet)
    # print(keyboard.read_key())


# Make sure input is 0-9, x, X, /, (R to reset)
def validateKeyPress(latestKeyPress):
    #print('not yet implemented')
    return True


# Update the string for the score at the given index
def updateFrameString(oldScoreString, newValue, newValueIndex):
    print(oldScoreString)
    tempString = list(oldScoreString)
    tempString[newValueIndex] = newValue
    newString = "".join(tempString)
    print(newString)
    return newString

# Add next shot taken onto the scoreboard in the latest shot position
def addToScoreBoard(currentShotScore, entireScoreBoard, nextShotNumber):
    frameNumber = math.ceil(nextShotNumber / 2)
    if(nextShotNumber % 2 == 1):

        entireScoreBoard[str(frameNumber)][0] = updateFrameString(entireScoreBoard[str(frameNumber)][0], currentShotScore, 0)
    else:
        entireScoreBoard[str(frameNumber)][0] = updateFrameString(entireScoreBoard[str(frameNumber)][0], currentShotScore, -1)


    #entireScoreBoard["1"][1] = currentShotScore


# Clears the previous board and displays the updated one
def displayBoard(entireScoreBoard):
    os.system('cls')
    print(tabulate(entireScoreBoard, headers="keys", tablefmt="fancy_grid", stralign="center"))

def main():
    # Passing in a dict into the on_press callback function because it's a mutable object and will update in this scope
    latestKeyPressRetriever = {"keyPressName": "", "keyJustPressed": False}
    keyboard.on_press(lambda e: retrieveKey(e, latestKeyPressRetriever))

    entireScoreBoard = {"1": ["  |  ", 0], "2": ["  |  ", 10], "3": ["4 | 5", 20], "4": ["6 | 7", 40], "5": ["8 | 9", 50]}
    nextShotNumber = 1

    tabulate.PRESERVE_WHITESPACE = True
    displayBoard(entireScoreBoard)
    while(latestKeyPressRetriever["keyPressName"] != "esc"):

        # Update the board if input is valid and has just been received
        if(validateKeyPress(latestKeyPressRetriever["keyPressName"]) and latestKeyPressRetriever["keyJustPressed"]):
            
            addToScoreBoard(latestKeyPressRetriever["keyPressName"], entireScoreBoard, nextShotNumber)
            nextShotNumber+=1
            displayBoard(entireScoreBoard)
           
            latestKeyPressRetriever["keyJustPressed"] = False # Set key press value to False in the retriever for it to stay upto date
    
    displayBoard(entireScoreBoard)
    print("Thanks for playing!")


if __name__ == "__main__":
    main()