#Next possible dimensions implementations: 
#Trailing stop distance from current price in case of tp SURF
#Current price distance to put stop on break even
#Daily, weekly or monthly Risk Management
#dimensionsInput = [tpType, stoplossMultiplier, breakEvenDistance]
import os
import math
from datetime import datetime, timedelta

targetVariable = 0 #total profit over residuals variance arround the regression line
stopLossMultiplier = 2.25
breakEvenDistance = 1

allResults = {}
marketInfo = []
entryPoints = []
e = 0 #current entry point index
m = 0 #curent market candle index
currentOperation = []
microChannelSize = 0

def appendOHLCAndDatetime(pl):
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
            marketInfo.append(appendOHLCAndDatetime(pl))
file_path = cdir + "\\FinTech\\Forex\\Forex_Entrypoints.csv"
with open(file_path, "r") as file:
    for index, line in enumerate(file):
        if index == 0:
            microChannelSize = float(line.split("=")[1])
        if index > 0:
            pl = line.replace('\n','').replace(' ',',').split(',')
            entryPoints.append(appendOHLCAndDatetime(pl))

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
        sl = currentOperation[1] - microChannelSize*stopLossMultiplier + slippage
        currentOperation[3] = sl
            
    if currentOperation[-1] == 'sell':
        slippage = math.floor(currentOperation[1] - currentOperation[2])
        sl = currentOperation[1] + microChannelSize*stopLossMultiplier - slippage
        currentOperation[3] = sl
        
    print(currentOperation)
    print(marketInfo[m])
    
searchOperation()