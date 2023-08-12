#Next possible dimensions implementations: 
#Trailing stop distance from current price in case of tp SURF
#Current price distance to put stop on break even
#Daily, weekly or monthly Risk Management
#dimensionsInput = [tpType, stoplossMultiplier, minBreakEvenDistance]
import os
import math
import time
from datetime import datetime

targetVariable = 0 #total profit over residuals variance arround the regression line
stopLossMultiplier = 2.25
minBreakEvenDistance = 1

results = []
marketInfo = []
entryPoints = []
e = 0 #current entry point index
m = 0 #curent market candle index
currentOperation = []
miSize = 0
stopPosition = 0
firstCdPastLine = False
cdPastLineIndex = None
start_time = time.time()

def appendInfo(pl):
    out = []
    date_time = datetime(
        int(pl[0].split(".")[0]),
        int(pl[0].split(".")[1]),
        int(pl[0].split(".")[2]),
        int(pl[1].split(":")[0]),
        int(pl[1].split(":")[1]),
        int(pl[1].split(":")[2])
    )
    out.append(date_time)
    if pl[-1] != "buy" and pl[-1] != "sell":
        out.append(float(pl[2]))
        out.append(float(pl[3]))
        out.append(float(pl[4]))
        out.append(float(pl[5]))
    else:
        out.append(float(pl[2]))
        out.append(float(pl[3]))
        out.append(None)
        out.append(None)
        out.append(pl[4])
    return out

cdir = os.getcwd()
file_path = cdir + "\\FinTech\\Forex\\USDJPY_M15_2023_3Y.csv"
with open(file_path, "r") as file:
    for index, line in enumerate(file):
        if index > 0:
            pl = line.replace('"','').split()
            marketInfo.append(appendInfo(pl))
file_path = cdir + "\\FinTech\\Forex\\Forex_Entrypoints.csv"
with open(file_path, "r") as file:
    for index, line in enumerate(file):
        if index == 0:
            miSize = float(line.split("=")[1])
        if index > 0:
            pl = line.replace('\n','').replace(' ',',').split(',')
            entryPoints.append(appendInfo(pl))

def nextEntryPoint():
    global e
    e += 1
    verifyEndPoint()
    return e

def searchOperation():
    global m
    global stopPosition
    global cdPastLineIndex
    global firstCdPastLine
    stopPosition = 0
    cdPastLineIndex = 0
    firstCdPastLine = False
    while entryPoints[e][0] > marketInfo[m][0]:
        m+=1
        verifyEndPoint()
    enterOperation()

def enterOperation():
    global currentOperation
    currentOperation = entryPoints[e] #dateTime, entryPointRefPrice, entryPointActualPrice, SL, TP, Side
    if currentOperation[-1] == 'buy':
        slippage = math.floor(currentOperation[2] - currentOperation[1])
        sl = currentOperation[1] - miSize*stopLossMultiplier + slippage
        currentOperation[3] = sl
        currentOperation[1] += slippage
            
    if currentOperation[-1] == 'sell':
        slippage = math.floor(currentOperation[1] - currentOperation[2])
        sl = currentOperation[1] + miSize*stopLossMultiplier - slippage
        currentOperation[3] = sl
        currentOperation[1] -= slippage
    waitForPositionClose()

def waitForPositionClose():
    global m
    
    m+=1
    verifyEndPoint()
    if currentOperation[-1] == "buy":
        while marketInfo[m][-1] > currentOperation[3]: #implement different logic when having more tp types
            m+=1
            manageTrailingStop()
            verifyEndPoint()
        closePosition()
    if currentOperation[-1] == "sell":
        while marketInfo[m][-1] < currentOperation[3]:
            m+=1
            manageTrailingStop()
            verifyEndPoint()
        closePosition()

def manageTrailingStop():
    global minBreakEvenDistance
    global stopPosition
    global cdPastLineIndex
    global firstCdPastLine

    if currentOperation[-1] == "buy":
        currentCandle = marketInfo[m]
        if marketInfo[m][-1] > currentOperation[2] + miSize*minBreakEvenDistance and stopPosition == 0:
            if firstCdPastLine == True:
                if marketInfo[m][-1] > marketInfo[cdPastLineIndex][-1]:
                    stopPosition = 1
                    currentOperation[3] = currentOperation[2]
            else:
                firstCdPastLine = True
                cdPastLineIndex = m
        if marketInfo[m][-1] > currentOperation[1] + (2*minBreakEvenDistance*miSize) and stopPosition == 1:
            stopPosition = 2
            currentOperation[3] = (miSize*minBreakEvenDistance) - (0.25*miSize) + currentOperation[1]
        if marketInfo[m][-1] > currentOperation[3] + (miSize*0.25) + (2*miSize*minBreakEvenDistance) and stopPosition == 2:
            currentOperation[3] += minBreakEvenDistance*miSize

    if currentOperation[-1] == "sell":
        currentCandle = marketInfo[m]
        if marketInfo[m][-1] < currentOperation[2] - miSize*minBreakEvenDistance and stopPosition == 0:
            if firstCdPastLine == True:
                if marketInfo[m][-1] < marketInfo[cdPastLineIndex][-1]:
                    stopPosition = 1
                    currentOperation[3] = currentOperation[2]
            else:
                firstCdPastLine = True
                cdPastLineIndex = m
        if marketInfo[m][-1] < currentOperation[1] - (2*minBreakEvenDistance*miSize) and stopPosition == 1:
            stopPosition = 2
            currentOperation[3] = currentOperation[1] - (miSize*minBreakEvenDistance) + (0.25*miSize)
        if marketInfo[m][-1] < currentOperation[3] - (miSize*0.25) - (2*miSize*minBreakEvenDistance) and stopPosition == 2:
            currentOperation[3] -= minBreakEvenDistance*miSize

def registerResults():
    if currentOperation[-1] == "buy":
        results.append({currentOperation[0]:currentOperation[3]-currentOperation[2]}) #change here when implementing new operation types
        printRes()
    if currentOperation[-1] == "sell":
        results.append({currentOperation[0]:currentOperation[2]-currentOperation[3]}) #change here when implementing new operation types
        printRes()

def closePosition():
    registerResults()
    nextEntryPoint()
    searchOperation()

def verifyEndPoint():
    if m != len(marketInfo) and e != len(entryPoints):
        return
    print(len(results))
    end_time = time.time()
    print(end_time-start_time)
    exit()

def printRes():
    print(currentOperation[0].strftime("%Y-%m-%d %H:%M:%S") +" ======> "+ marketInfo[m][0].strftime("%Y-%m-%d %H:%M:%S") +" = "+ str(results[e][currentOperation[0]]))

searchOperation()

