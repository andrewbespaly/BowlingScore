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

# Gets total score from previous frame than passed in
def getPreviousTotalScore(entireScoreBoard, frameNumber):
    if(frameNumber > 1):
        return entireScoreBoard[frameNumber-1][1]
    else:
        return 0


# Add previous frame score to current frame
def updateCurrentFrameScore(entireScoreBoard, frameNumber):
    if(frameNumber > 1):
        priorTotalScore = entireScoreBoard[frameNumber-1][1]
    else:
        priorTotalScore = 0
    # priorTotalScore = 0

    currentFrameScore = evaluateFrameScore(entireScoreBoard, frameNumber)
    # if(currentFrameScore != " " and priorTotalScore != " "):
    #     entireScoreBoard[frameNumber][1] = currentFrameScore + priorTotalScore

def getShotForFrame(entireScoreBoard, frameNumber):
    if(frameNumber != 10):
        firstShot = entireScoreBoard[frameNumber][0][0]
        secondShot = entireScoreBoard[frameNumber][0][-1]
        return firstShot, secondShot, None
    else:
        firstShot = entireScoreBoard[frameNumber][0][0]
        secondShot = entireScoreBoard[frameNumber][0][2]
        thirdShot = entireScoreBoard[frameNumber][0][-1]
        return firstShot, secondShot, thirdShot


# Calculate scores for frames that are pending later shots, as well as current frame
def evaluatePastFrameScore(entireScoreBoard, frameNumber):

    if(frameNumber-2 > 0):
        # if(entireScoreBoard[frameNumber-2][1] == " "):
        if(entireScoreBoard[frameNumber-2][0][0] == "X"):
                if(entireScoreBoard[frameNumber-1][0][0] == "X"): #strike on first hit after getting a strike, get second shot from current frame
                    firstShotCurrentFrame = entireScoreBoard[frameNumber][0][0]
                    if(firstShotCurrentFrame == "X"):
                        entireScoreBoard[frameNumber-2][1] = 30 + getPreviousTotalScore(entireScoreBoard, frameNumber-2)
                    else:
                        entireScoreBoard[frameNumber-2][1] = 20 + int(firstShotCurrentFrame) + getPreviousTotalScore(entireScoreBoard, frameNumber-2)

    if(frameNumber-1 > 0):
        if(entireScoreBoard[frameNumber-1][0][-1] == "/" or entireScoreBoard[frameNumber-1][0][0] == "X"):
            # evaluatePastFrameScore(entireScoreBoard, frameNumber-1)
            if(entireScoreBoard[frameNumber-1][0][0] == "X"):
                # firstShot = entireScoreBoard[frameNumber][0][0]
                # secondShot = entireScoreBoard[frameNumber][0][-1]
                firstShot, secondShot, thirdShot = getShotForFrame(entireScoreBoard, frameNumber)
                if(frameNumber != 10):
                    if(firstShot != "X"):
                        if(secondShot == "/"):
                            entireScoreBoard[frameNumber-1][1] = 20 + getPreviousTotalScore(entireScoreBoard, frameNumber-1)
                        elif(secondShot != " "):
                            entireScoreBoard[frameNumber-1][1] = 10 + int(firstShot) + int(secondShot) + getPreviousTotalScore(entireScoreBoard, frameNumber-1)
                        else:
                            entireScoreBoard[frameNumber-1][1] = 10 + int(firstShot) + getPreviousTotalScore(entireScoreBoard, frameNumber-1)
                    else:
                        entireScoreBoard[frameNumber-1][1] = 20 + getPreviousTotalScore(entireScoreBoard, frameNumber-1)
                else: # frame 9 when scoring on frame 10
                    if(firstShot != "X"):
                        if(secondShot == "/"):
                            entireScoreBoard[frameNumber-1][1] = 20 + getPreviousTotalScore(entireScoreBoard, frameNumber-1)
                        else:
                            entireScoreBoard[frameNumber-1][1] = 10 + int(firstShot) + int(secondShot) + getPreviousTotalScore(entireScoreBoard, frameNumber-1)
                    else:
                        if(secondShot == "X"):
                            entireScoreBoard[frameNumber-1][1] = 30 + getPreviousTotalScore(entireScoreBoard, frameNumber-1)
                        else:
                            entireScoreBoard[frameNumber-1][1] = 20 + getPreviousTotalScore(entireScoreBoard, frameNumber-1)

            if(entireScoreBoard[frameNumber-1][0][-1] == "/"):
                firstShot = entireScoreBoard[frameNumber][0][0]
                # secondShot = entireScoreBoard[frameNumber][0][-1]
                if(firstShot == "X"):
                    entireScoreBoard[frameNumber-1][1] = 20 + getPreviousTotalScore(entireScoreBoard, frameNumber-1)
                else:
                    entireScoreBoard[frameNumber-1][1] = 10 + int(firstShot) + getPreviousTotalScore(entireScoreBoard, frameNumber-1)

    if(getPreviousTotalScore(entireScoreBoard, frameNumber) != " "):
        if(frameNumber > 1):
            priorTotalScore = entireScoreBoard[frameNumber-1][1]
        else:
            priorTotalScore = 0
        # currentFrameScore = evaluateFrameScore(entireScoreBoard, frameNumber)
        # firstShot = entireScoreBoard[frameNumber][0][0]
        # secondShot = entireScoreBoard[frameNumber][0][-1]
        firstShot, secondShot, thirdShot = getShotForFrame(entireScoreBoard, frameNumber)
        if(frameNumber != 10):
            if(firstShot != "X" and secondShot != "/"):
                if(secondShot != " "):
                    entireScoreBoard[frameNumber][1] = int(firstShot) + int(secondShot) + priorTotalScore
                else:
                    entireScoreBoard[frameNumber][1] = int(firstShot) + priorTotalScore
            else: # strike of spare occurred before frame 10
                entireScoreBoard[frameNumber][1] = 10 + priorTotalScore
            
        else: # update score on frame 10
            firstShot, secondShot, thirdShot = getShotForFrame(entireScoreBoard, frameNumber)
            frameShot1 = frameShot2 = frameShot3 = 0
            
            if(firstShot != " "):
                if(firstShot == "X"):
                    frameShot1 = 10
                else:
                    frameShot1 = int(firstShot)

            if(secondShot != " "):
                if(secondShot == "/"):
                    frameShot2 = 10 - frameShot1
                if(secondShot == "X"):
                    frameShot2 = 10
                else:
                    frameShot2 = int(secondShot)

            if(thirdShot != " "):
                if(thirdShot == "/"):
                    frameShot3 = 10 - frameShot2
                if(thirdShot == "X"):
                    frameShot3 = 10
                else:
                    frameShot3 = int(thirdShot)

            totalFrameShot = frameShot1 + frameShot2 + frameShot3
            entireScoreBoard[frameNumber][1] = totalFrameShot + getPreviousTotalScore(entireScoreBoard, frameNumber)



            # if(firstShot != "X" and secondShot != "/"):
            #     if(secondShot != " "):
            #         entireScoreBoard[frameNumber][1] = int(firstShot) + int(secondShot) + getPreviousTotalScore(entireScoreBoard, frameNumber)
            #     else:
            #         entireScoreBoard[frameNumber][1] = int(firstShot) + getPreviousTotalScore(entireScoreBoard, frameNumber)

            # if(thirdShot != " "):
            #     if(secondShot == "/"):
            #         if(thirdShot != "X"):
            #             entireScoreBoard[frameNumber][1] = 10 + int(thirdShot) + getPreviousTotalScore(entireScoreBoard, frameNumber)
            #         else:
            #             entireScoreBoard[frameNumber][1] = 20 + getPreviousTotalScore(entireScoreBoard, frameNumber)
            #     if(firstShot == "X"):
            #         if(secondShot != "X"):
            #             if(thirdShot != "/"):
            #                 entireScoreBoard[frameNumber][1] = 10 + int(secondShot) + int(thirdShot) + getPreviousTotalScore(entireScoreBoard, frameNumber)
            #             else:
            #                 entireScoreBoard[frameNumber][1] = 20 + getPreviousTotalScore(entireScoreBoard, frameNumber)
            #         else:
            #             if(thirdShot != "X"):
            #                 entireScoreBoard[frameNumber][1] = 20 + int(thirdShot) + getPreviousTotalScore(entireScoreBoard, frameNumber)
            #             else:
            #                 entireScoreBoard[frameNumber][1] = 30 + getPreviousTotalScore(entireScoreBoard, frameNumber)



# Evaluate current frame score
def evaluateFrameScore(entireScoreBoard, frameNumber):
    firstShot = entireScoreBoard[frameNumber][0][0]
    secondShot = entireScoreBoard[frameNumber][0][-1]
    evaluatePastFrameScore(entireScoreBoard, frameNumber)
    # if(secondShot != " "):
    #     if(firstShot == "X"):
    #         return " "
    #     elif(secondShot == "/"):
    #         return " "
    #     else:
    #         return int(firstShot) + int(secondShot)


# Update score after the first shot in the frame
def firstFrameShot(currentShotScore, entireScoreBoard, nextShotNumber, frameNumber):
    if(currentShotScore == "X"):
        if(frameNumber != 10):
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

# Check final frame box for score
def isGameOver(entireScoreBoard):
    firstShot, secondShot, thirdShot = getShotForFrame(entireScoreBoard, 10)
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

    # entireScoreBoard = {1: [" | ", " "], 2: [" | ", " "], 3: [" | ", " "], 4: [" | ", " "], 5: [" | ", " "], 6: [" | ", " "], 7: [" | ", " "], 8: [" | ", " "], 9: [" | ", " "], 10: [" | | ", " "]}
    # nextShotNumber = 1
    entireScoreBoard, nextShotNumber = restartGame()

    tabulate.PRESERVE_WHITESPACE = True
    displayBoard(entireScoreBoard)
    while(latestKeyPressRetriever["keyPressName"] != "esc" and not isGameOver(entireScoreBoard)):

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