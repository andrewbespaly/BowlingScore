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
    latestKeyPress = latestKeyPress.upper()
    if(latestKeyPress.isdigit() or 
        latestKeyPress == "X" or 
        latestKeyPress == "/" or
        latestKeyPress == "R"):
        return latestKeyPress
    else: 
        return None


# Get the frame number for the current shot
def getFrameNumber(nextShotNumber):
    if(nextShotNumber > 19):
        return 10
    else:
        return math.ceil(nextShotNumber / 2)

# Update the current shot in the current frame
def updateFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber):
    if(frameNumber == 10):
        if(nextShotNumber == 19):
            entireScoreBoard[frameNumber][0] = updateFrameString(entireScoreBoard[frameNumber][0], currentShotScore, 0)
        elif(nextShotNumber == 20):
            entireScoreBoard[frameNumber][0] = updateFrameString(entireScoreBoard[frameNumber][0], currentShotScore, 2)
        elif(nextShotNumber == 21):
            entireScoreBoard[frameNumber][0] = updateFrameString(entireScoreBoard[frameNumber][0], currentShotScore, -1)
    else:
        if(nextShotNumber % 2 == 1):
            entireScoreBoard[frameNumber][0] = updateFrameString(entireScoreBoard[frameNumber][0], currentShotScore, 0)
        else:
            entireScoreBoard[frameNumber][0] = updateFrameString(entireScoreBoard[frameNumber][0], currentShotScore, -1)


# Update the string for the score at the given index
def updateFrameString(oldScoreString, newValue, newValueIndex):
    tempString = list(oldScoreString)
    tempString[newValueIndex] = newValue
    newString = "".join(tempString)
    return newString


# Add previous frame score to current frame
def updateCurrentFrameScore(entireScoreBoard, frameNumber):
    if(frameNumber > 1):
        priorTotalScore = entireScoreBoard[frameNumber-1][1]
    else:
        priorTotalScore = 0

    currentFrameScore = evaluateFrameScore(entireScoreBoard[frameNumber][0])
    
    entireScoreBoard[frameNumber][1] = currentFrameScore + priorTotalScore


# Evaluate current frame score
def evaluateFrameScore(frameShotString):
    firstShot = frameShotString[0]
    secondShot = frameShotString[-1]
    if(firstShot == "X"):
        return 10
    elif(secondShot == "/"):
        return 10
    else:
        return int(firstShot) + int(secondShot)


# Update score after the first shot in the frame
def firstFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber):
    if(currentShotScore == "X"):
        updateFrameShot("_", entireScoreBoard, nextShotNumber+1, frameNumber)
        updateCurrentFrameScore(entireScoreBoard, frameNumber)
    

# Update score after the second shot in the frame
def secondFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber):
    updateCurrentFrameScore(entireScoreBoard, frameNumber)
    

# Update the total score
def updateTotalScore(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber):
    if(nextShotNumber % 2 == 1):
        firstFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber)
    else:
        secondFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber)


# Add next shot taken onto the scoreboard in the latest shot position
def updateScoreBoard(currentShotScore, entireScoreBoard, nextShotNumber):
    frameNumber = getFrameNumber(nextShotNumber)
    
    updateFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber)

    updateTotalScore(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber)

    
# Reset all game variables
def restartGame():
    newScoreBoard = {1: [" | ", " "], 2: [" | ", " "], 3: [" | ", " "], 4: [" | ", " "], 5: [" | ", " "], 6: [" | ", " "], 7: [" | ", " "], 8: [" | ", " "], 9: [" | ", " "], 10: [" | | ", " "]}
    newNextShotNumber = 1
    return newScoreBoard, newNextShotNumber


# Clears the previous board and displays the updated one
def displayBoard(entireScoreBoard):
    os.system('cls')
    print(tabulate(entireScoreBoard, headers="keys", tablefmt="fancy_grid", stralign="center"))
    print("\n\t'R' - Restart\t\t\t'ESC' - Quit")


def main():
    # Passing in a dict into the on_press callback function because it's a mutable object and will update in this scope
    latestKeyPressRetriever = {"keyPressName": "", "keyJustPressed": False}
    keyboard.on_press(lambda e: retrieveKey(e, latestKeyPressRetriever))

    entireScoreBoard = {1: [" | ", " "], 2: [" | ", " "], 3: [" | ", " "], 4: [" | ", " "], 5: [" | ", " "], 6: [" | ", " "], 7: [" | ", " "], 8: [" | ", " "], 9: [" | ", " "], 10: [" | | ", " "]}
    nextShotNumber = 1
    tabulate.PRESERVE_WHITESPACE = True
    displayBoard(entireScoreBoard)
    while(latestKeyPressRetriever["keyPressName"] != "esc"):

        # Check if key has been pressed, only update the board if input is valid
        if(latestKeyPressRetriever["keyJustPressed"]):
            latestKeyPress = validateKeyPress(latestKeyPressRetriever["keyPressName"])
            if(latestKeyPress != None):
                if(latestKeyPress == "R"):  # Restart the game if R is typed
                    entireScoreBoard, nextShotNumber = restartGame()
                    displayBoard(entireScoreBoard)
                else:
                    updateScoreBoard(latestKeyPress, entireScoreBoard, nextShotNumber)
                    if(latestKeyPress == "X"):    # Skip next shot if there's a strike
                        nextShotNumber+=1
                    nextShotNumber+=1
                    displayBoard(entireScoreBoard)
            
            latestKeyPressRetriever["keyJustPressed"] = False
        time.sleep(0.01) # No reason to run the while loop any faster
        
    displayBoard(entireScoreBoard)
    print("Thanks for playing!")


if __name__ == "__main__":
    main()