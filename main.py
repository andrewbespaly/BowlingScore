import os
from tabulate import tabulate
import keyboard
import time
import math


# Callback function that runs whenever a key is pressed down
def retrieveKey(self, latestKeyPressRetriever):
    latestKeyPressRetriever["keyPressName"] = self.name
    latestKeyPressRetriever["keyJustPressed"] = True


# Make sure input is 0-9, x, X, /, (R to reset)
def validateKeyPress(latestKeyPress):
    if(latestKeyPress.isdigit() or 
       latestKeyPress == "X" or 
       latestKeyPress == "x" or 
       latestKeyPress == "/" or
       latestKeyPress == "R"):
        return True
    else: 
        return False


# Update the current shot in the current frame
def updateFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber):
    if(frameNumber == 10):
        if(nextShotNumber == 19):
            entireScoreBoard[str(frameNumber)][0] = updateFrameString(entireScoreBoard[str(frameNumber)][0], currentShotScore, 0)
        elif(nextShotNumber == 20):
            entireScoreBoard[str(frameNumber)][0] = updateFrameString(entireScoreBoard[str(frameNumber)][0], currentShotScore, 2)
        elif(nextShotNumber == 21):
            entireScoreBoard[str(frameNumber)][0] = updateFrameString(entireScoreBoard[str(frameNumber)][0], currentShotScore, -1)
    else:
        if(nextShotNumber % 2 == 1):
            entireScoreBoard[str(frameNumber)][0] = updateFrameString(entireScoreBoard[str(frameNumber)][0], currentShotScore, 0)
        else:
            entireScoreBoard[str(frameNumber)][0] = updateFrameString(entireScoreBoard[str(frameNumber)][0], currentShotScore, -1)


# Update the string for the score at the given index
def updateFrameString(oldScoreString, newValue, newValueIndex):
    print(oldScoreString)
    tempString = list(oldScoreString)
    tempString[newValueIndex] = newValue
    newString = "".join(tempString)
    print(newString)
    return newString


# Add next shot taken onto the scoreboard in the latest shot position
def updateScoreBoard(currentShotScore, entireScoreBoard, nextShotNumber):
    if(nextShotNumber > 19):
        frameNumber = 10
    else:
        frameNumber = math.ceil(nextShotNumber / 2)
    
    updateFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber)

    #calculate new score




# Clears the previous board and displays the updated one
def displayBoard(entireScoreBoard):
    os.system('cls')
    print(tabulate(entireScoreBoard, headers="keys", tablefmt="fancy_grid", stralign="center"))
    print("\n\t'r' - restart\t\t\t'esc' - quit")


def main():
    # Passing in a dict into the on_press callback function because it's a mutable object and will update in this scope
    latestKeyPressRetriever = {"keyPressName": "", "keyJustPressed": False}
    keyboard.on_press(lambda e: retrieveKey(e, latestKeyPressRetriever))

    entireScoreBoard = {"1": [" | ", " "], "2": [" | ", " "], "3": [" | ", " "], "4": [" | ", " "], "5": [" | ", " "], "6": [" | ", " "], "7": [" | ", " "], "8": [" | ", " "], "9": [" | ", " "], "10": [" | | ", " "]}
    nextShotNumber = 1
    currentTotalScore = 0
    tabulate.PRESERVE_WHITESPACE = True
    displayBoard(entireScoreBoard)
    while(latestKeyPressRetriever["keyPressName"] != "esc"):

        # Check if key has been pressed, only update the board if input is valid
        if(latestKeyPressRetriever["keyJustPressed"]):
            if(validateKeyPress(latestKeyPressRetriever["keyPressName"])):
                updateScoreBoard(latestKeyPressRetriever["keyPressName"], entireScoreBoard, nextShotNumber)
                nextShotNumber+=1
                displayBoard(entireScoreBoard)
            
            latestKeyPressRetriever["keyJustPressed"] = False
        time.sleep(0.01) # No reason to run the while loop as fast as possible
        
    displayBoard(entireScoreBoard)
    print("Thanks for playing!")


if __name__ == "__main__":
    main()