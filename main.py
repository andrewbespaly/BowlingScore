import os
from tabulate import tabulate
import keyboard
import time
import math


# Callback function that runs whenever a key is pressed down
def retrieveKey(self, latestKeyPressRetriever):
    latestKeyPressRetriever["keyPressName"] = self.name
    latestKeyPressRetriever["keyJustPressed"] = True


# Make sure input is 0-9, x, X, /, (R to restart)
def validateKeyPress(latestKeyPress):
    if(latestKeyPress.isdigit() or 
       latestKeyPress == "X" or 
       latestKeyPress == "x" or 
       latestKeyPress == "/" or
       latestKeyPress == "r"):
        return True
    else: 
        return False


# Get the frame number for the current shot
def getFrameNumber(nextShotNumber):
    if(nextShotNumber > 19):
        return 10
    else:
        return math.ceil(nextShotNumber / 2)

# Update the current shot in the current frame
def updateFrameShot(currentShotScore, entireScoreBoard, nextShotNumber):
    frameNumber = getFrameNumber(nextShotNumber)
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
    tempString = list(oldScoreString)
    tempString[newValueIndex] = newValue
    newString = "".join(tempString)
    return newString


# Update the total score
def updateTotalScore(currentShotScore, entireScoreBoard, nextShotNumber):
    frameNumber = getFrameNumber(nextShotNumber)
    if(frameNumber > 1):
        priorTotalScore = entireScoreBoard[str(frameNumber-1)][1]
    else:
        priorTotalScore = 0

    currentTotalScore = int(currentShotScore) + int(priorTotalScore)
    
    entireScoreBoard[str(frameNumber)][1] = currentTotalScore


# Add next shot taken onto the scoreboard in the latest shot position
def updateScoreBoard(currentShotScore, entireScoreBoard, nextShotNumber):
    
    updateFrameShot(currentShotScore, entireScoreBoard, nextShotNumber)

    updateTotalScore(currentShotScore, entireScoreBoard, nextShotNumber)

# Check if the game should be restarted
def shouldRestart(lastKeyPress):
    if(lastKeyPress == "r"):
        return True
    else:
        return False
    
# Reset all game variables
def restartGame():
    newScoreBoard = {"1": [" | ", " "], "2": [" | ", " "], "3": [" | ", " "], "4": [" | ", " "], "5": [" | ", " "], "6": [" | ", " "], "7": [" | ", " "], "8": [" | ", " "], "9": [" | ", " "], "10": [" | | ", " "]}
    newNextShotNumber = 1
    newCurrentTotalScore = 0
    return newScoreBoard, newNextShotNumber, newCurrentTotalScore


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
                if(shouldRestart(latestKeyPressRetriever["keyPressName"])):
                    entireScoreBoard, nextShotNumber, currentTotalScore = restartGame()
                    displayBoard(entireScoreBoard)
                else:
                    updateScoreBoard(latestKeyPressRetriever["keyPressName"], entireScoreBoard, nextShotNumber)
                    nextShotNumber+=1
                    displayBoard(entireScoreBoard)
            
            latestKeyPressRetriever["keyJustPressed"] = False
        time.sleep(0.01) # No reason to run the while loop as fast as possible
        
    displayBoard(entireScoreBoard)
    print("Thanks for playing!")


if __name__ == "__main__":
    main()