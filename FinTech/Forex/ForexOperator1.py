#Next possible dimensions implementations: 
#Trailing stop distance from current price in case of tp SURF
#Current price distance to put stop on break even
#Daily, weekly or monthly Risk Management
#dimensionsInput = [tpType, stoplossMultiplier, minBreakEvenDistance]
import os
import math
from datetime import datetime, timedelta

targetVariable = 0 #total profit over residuals variance arround the regression line
stopLossMultiplier = 2.25
minBreakEvenDistance = 1

allResults = {}
marketInfo = []
entryPoints = []
e = 0 #current entry point index
m = 0 #curent market candle index
currentOperation = []
miSize = 0
stopPosition = 0

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
    return e

def searchOperation():
    global m
    while entryPoints[e][0] >= marketInfo[m][0]:
        m+=1
    enterOperation()

def enterOperation():
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
    global stopPosition
    if currentOperation[-1] == "buy":
        while marketInfo[m][-1] > currentOperation[3]: #implement different logic when having more tp types
            m+=1
            manageTrailingStop()
    if currentOperation[-1] == "sell":
        while marketInfo[m][-1] < currentOperation[3]:
            m+=1
            manageTrailingStop()

def manageTrailingStop():
    firstCdPastLine = False
    cdPastLineIndex = None
    if currentOperation[-1] == "buy":
        if int(marketInfo[m][-1]) > currentOperation[2] + miSize*minBreakEvenDistance and stopPosition == 0:
            if firstCdPastLine == True:
                if int(marketInfo[m][-1]) > int(marketInfo[cdPastLineIndex][-1]):
                    stopPosition = 1
                    currentOperation[3] = currentOperation[2]
            else:
                firstCdPastLine = True
                cdPastLineIndex = m
        if int(marketInfo[m][-1]) > currentOperation[1] + (miSize*2*minBreakEvenDistance) and stopPosition == 1:
            stopPosition = 2
            currentOperation[3] += (miSize*minBreakEvenDistance) - 0.25*miSize
        if int(marketInfo[m][-1]) > currentOperation[3] + (miSize*0.25) + (miSize*minBreakEvenDistance) and stopPosition == 2:
            currentOperation[3] += miSize*minBreakEvenDistance
    if currentOperation[-1] == "sell":
        if int(marketInfo[m][-1]) < currentOperation[2] - miSize*minBreakEvenDistance and stopPosition == 0:
            if firstCdPastLine == True:
                if int(marketInfo[m][-1]) < int(marketInfo[cdPastLineIndex][-1]):
                    stopPosition = 1
                    currentOperation[3] = currentOperation[2]
            else:
                firstCdPastLine = True
                cdPastLineIndex = m

    
    
searchOperation()