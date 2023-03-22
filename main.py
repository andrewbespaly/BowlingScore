import os
from tabulate import tabulate
import keyboard
import time
import math


# Callback function that gets key press information
def retrieveKey(self, latestKeyPressRetriever):
    latestKeyPressRetriever["keyPressName"] = self.name
    latestKeyPressRetriever["keyJustPressed"] = True


# Make sure input is 0-9, x, X, /, (R to restart)
def validateKeyPress(latestKeyPress):
    latestKeyPress = latestKeyPress.upper()
    if(latestKeyPress.isdigit() or 
        latestKeyPress == "X" or 
        latestKeyPress == "/" or
        latestKeyPress == "R" or
        latestKeyPress == "esc"):
        return latestKeyPress
    else: 
        return None

# Check if position of valid key press is acceptable for gameplay
def correctUseOfKey(latestKeyPress, entireScoreBoard, nextShotNumber):
    frameNumber = getFrameNumber(nextShotNumber)
    if(frameNumber != 10):
        if(nextShotNumber % 2 == 1):
            if(latestKeyPress == "X" or latestKeyPress.isdigit()):
                return True
        else:
            if(latestKeyPress == "/"):
                return True
            elif(latestKeyPress.isdigit()):
                frameFirstShot = getShotForFrame(entireScoreBoard[frameNumber], frameNumber)[0]
                if(int(latestKeyPress) + int(frameFirstShot) < 10):
                    return True
    # All possible frame 10 inputs
    else:
        lastFrameShot1, lastFrameShot2, lastFrameShot3 = getShotForFrame(entireScoreBoard[frameNumber], frameNumber)
        if(lastFrameShot1 == " "):
            if(latestKeyPress == "X" or latestKeyPress.isdigit()):
                return True
        elif(lastFrameShot2 == " "):
            if(lastFrameShot1 == "X" and latestKeyPress == "X"):
                return True
            elif(lastFrameShot1.isdigit() and latestKeyPress == "/"):
                return True
            elif(latestKeyPress.isdigit() and lastFrameShot1.isdigit()):
                if(int(latestKeyPress) + int(lastFrameShot1) < 10):
                    return True
            elif(latestKeyPress.isdigit() and lastFrameShot1 == "X"):
                return True
        elif(lastFrameShot3 == " "):
            if(lastFrameShot1 == "X" and lastFrameShot2 == "X" and latestKeyPress == "X"):
                return True
            elif(lastFrameShot2 == "/" and latestKeyPress == "X"):
                return True
            elif(lastFrameShot2.isdigit() and latestKeyPress == "/"):
                return True
            elif(latestKeyPress.isdigit()):
                return True

    if(latestKeyPress == "R" or latestKeyPress == "esc"):
        return True

    return False

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

# Gets total score from previous frame than passed in
def getPreviousTotalScore(entireScoreBoard, frameNumber):
    if(frameNumber > 1):
        return entireScoreBoard[frameNumber-1][1]
    else:
        return 0

# Return the shot values for a given frame
def getShotForFrame(frameValue, frameNumber):
    if(frameNumber != 10):
        firstShot = frameValue[0][0]
        secondShot = frameValue[0][-1]
        return firstShot, secondShot, None
    else:
        firstShot = frameValue[0][0]
        secondShot = frameValue[0][2]
        thirdShot = frameValue[0][-1]
        return firstShot, secondShot, thirdShot

# Calculates the scores for each shot taken in a frame and returns the resulting numbers
def calculateCurrentFrame(frameValue, frameNumber):
    currentFirstShot, currentSecondShot, currentThirdShot = getShotForFrame(frameValue, frameNumber)
    frameShot1Score = frameShot2Score = frameShot3Score = 0
    if(currentFirstShot != " "):
        if(currentFirstShot == "X"):
            frameShot1Score = 10
        else:
            frameShot1Score = int(currentFirstShot)

    if(currentSecondShot != " "):
        if(currentSecondShot == "/"):
            frameShot2Score = 10 - frameShot1Score
        elif(currentSecondShot == "X"):
            frameShot2Score = 10
        elif(currentSecondShot == "_"):
            frameShot2Score = 0
        else:
            frameShot2Score = int(currentSecondShot)

    if(currentThirdShot != " " and currentThirdShot != None):
        if(currentThirdShot == "/"):
            frameShot3Score = 10 - frameShot2Score
        elif(currentThirdShot == "X"):
            frameShot3Score = 10
        else:
            frameShot3Score = int(currentThirdShot)

    return frameShot1Score, frameShot2Score, frameShot3Score


# Calculate scores for frames that are pending later shots, as well as the current frame
def evaluatePastFrameScore(entireScoreBoard, frameNumber):

    # Go back two frames and fill in score information if two strikes occurred
    if(frameNumber-2 > 0):
        twoPrevFramesFirstShot = getShotForFrame(entireScoreBoard[frameNumber-2], frameNumber-2)[0]
        if(twoPrevFramesFirstShot == "X"):
            prevFirstShot = getShotForFrame(entireScoreBoard[frameNumber-1], frameNumber-1)[0]
            if(prevFirstShot == "X"):
                currentFirstShot, currentSecondShot, currentThirdShot = getShotForFrame(entireScoreBoard[frameNumber], frameNumber)
                frameShot1Score = calculateCurrentFrame(entireScoreBoard[frameNumber], frameNumber)[0]
                # if(currentFirstShot == "X" and currentSecondShot != "X"):
                #     totalFrameShot = frameShot1Score + frameShot2Score
                # else:
                #     totalFrameShot = frameShot1Score

                entireScoreBoard[frameNumber-2][1] = 20 + frameShot1Score + getPreviousTotalScore(entireScoreBoard, frameNumber-2)

    # Go back one frame and fill in score information if a strike or spare occurred
    if(frameNumber-1 > 0):
        prevFirstShot, prevSecondShot, prevThirdShot = getShotForFrame(entireScoreBoard[frameNumber-1], frameNumber-1)
        if(prevFirstShot == "X" or prevSecondShot == "/"):
            frameShot1Score, frameShot2Score, frameShot3Score = calculateCurrentFrame(entireScoreBoard[frameNumber], frameNumber)
            if(prevFirstShot == "X"):
                totalFrameShot = frameShot1Score + frameShot2Score
            else:
                totalFrameShot = frameShot1Score

            entireScoreBoard[frameNumber-1][1] = 10 + totalFrameShot + getPreviousTotalScore(entireScoreBoard, frameNumber-1)

    # Fill in current frame score information
    frameShot1Score, frameShot2Score, frameShot3Score = calculateCurrentFrame(entireScoreBoard[frameNumber], frameNumber)
    entireScoreBoard[frameNumber][1] = frameShot1Score + frameShot2Score + frameShot3Score + getPreviousTotalScore(entireScoreBoard, frameNumber)


# Change the frame shot string if a strike was made
def checkForStrike(entireScoreBoard, nextShotNumber, frameNumber):
    firstShot, secondShot, thirdShot = getShotForFrame(entireScoreBoard[frameNumber], frameNumber)
    if(firstShot == "X" and frameNumber != 10):
        updateFrameShot("_", entireScoreBoard, nextShotNumber+1, frameNumber)

# Update the total score
def updateTotalScore(entireScoreBoard, nextShotNumber, frameNumber):
    if(nextShotNumber % 2 == 1):
        checkForStrike(entireScoreBoard, nextShotNumber, frameNumber)        
    
    evaluatePastFrameScore(entireScoreBoard, frameNumber)
        

# Add next shot taken onto the scoreboard in the latest shot position
def updateScoreBoard(currentShotScore, entireScoreBoard, nextShotNumber):
    frameNumber = getFrameNumber(nextShotNumber)
    
    updateFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber)

    updateTotalScore(entireScoreBoard, nextShotNumber, frameNumber)

    
# Reset all game variables
def restartGame():
    newScoreBoard = {1: [" | ", " "], 2: [" | ", " "], 3: [" | ", " "], 4: [" | ", " "], 5: [" | ", " "], 6: [" | ", " "], 7: [" | ", " "], 8: [" | ", " "], 9: [" | ", " "], 10: [" | | ", " "]}
    newNextShotNumber = 1
    return newScoreBoard, newNextShotNumber

# Check final frame box for score
def isGameOver(entireScoreBoard):
    firstShot, secondShot, thirdShot = getShotForFrame(entireScoreBoard[10], 10)
    if((secondShot.isdigit() and firstShot != "X") or thirdShot != " "):
        return True
    else:
        return False


# Clears the previous board and displays the updated one
def displayBoard(entireScoreBoard):
    os.system('cls')
    print(tabulate(entireScoreBoard, headers="keys", tablefmt="fancy_grid", stralign="center"))
    print("\n\t'R' - Restart\t\t\t'ESC' - Quit")


def main():
    # Passing in a dict into the on_press callback function because it's a mutable object and will update in this scope
    latestKeyPressRetriever = {"keyPressName": "", "keyJustPressed": False}
    keyboard.on_press(lambda e: retrieveKey(e, latestKeyPressRetriever))

    entireScoreBoard, nextShotNumber = restartGame()

    tabulate.PRESERVE_WHITESPACE = True
    displayBoard(entireScoreBoard)
    while(latestKeyPressRetriever["keyPressName"] != "esc" and not isGameOver(entireScoreBoard)):

        # Check if key has been pressed, only update the board if input is valid
        if(latestKeyPressRetriever["keyJustPressed"]):
            latestKeyPress = validateKeyPress(latestKeyPressRetriever["keyPressName"])
            keyAcceptable = False
            if(latestKeyPress != None):
                keyAcceptable = correctUseOfKey(latestKeyPress, entireScoreBoard, nextShotNumber)
            if(keyAcceptable == True):
                if(latestKeyPress == "R"):  # Restart the game if R is typed
                    entireScoreBoard, nextShotNumber = restartGame()
                    displayBoard(entireScoreBoard)
                else:
                    updateScoreBoard(latestKeyPress, entireScoreBoard, nextShotNumber)
                    if(latestKeyPress == "X"):    # Skip next shot if there's a strike
                        frameNumber = getFrameNumber(nextShotNumber)
                        if(frameNumber != 10):
                            nextShotNumber+=1
                    nextShotNumber+=1
                    displayBoard(entireScoreBoard)
            
            latestKeyPressRetriever["keyJustPressed"] = False
        time.sleep(0.01) # No reason to run the while loop any faster
        
    displayBoard(entireScoreBoard)
    print("Thanks for playing!")
    keyboard.send("esc") # esc clears the text written in command line

if __name__ == "__main__":
    main()