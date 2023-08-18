#Next possible dimensions implementations: 
#Trailing stop distance from current price in case of tp SURF
#Current price distance to put stop on break even
#Daily, weekly or monthly Risk Management
#dimensionsInput = [tpType, stoplossMultiplier, minBreakEvenDistance]
import os
import math
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

marketInfo = []
entryPoints = []
miSize = 0

def appendInfo(pl):
    date_time = datetime(
        int(pl[0].split(".")[0]),
        int(pl[0].split(".")[1]),
        int(pl[0].split(".")[2]),
        int(pl[1].split(":")[0]),
        int(pl[1].split(":")[1]),
        int(pl[1].split(":")[2])
    )
    out = []
    if pl[-1] != "buy" and pl[-1] != "sell":
        out.append(date_time)
        out.append(float(pl[2]))
        out.append(float(pl[3]))
        out.append(float(pl[4]))
        out.append(float(pl[5]))
    else:
        out.append(date_time)
        out.append(float(pl[2]))
        out.append(float(pl[3]))
        out.append(0)
        out.append(0)
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
    while entryPoints[e][0] < marketInfo[m][0]:
        e += 1
        verifyEndPointAndAddToNpArrays()
        if ex:
            return
    return

def searchOperation():
    global m
    global stopPosition
    global cdPastLineIndex
    global firstCdPastLine
    stopPosition = 0
    cdPastLineIndex = 0
    firstCdPastLine = False
    if ex:
        return
    while entryPoints[e][0] > marketInfo[m][0]:
        m+=1
        verifyEndPointAndAddToNpArrays()
        if ex:
            return
    enterOperation()

def enterOperation():
    global currentOperation
    currentOperation = list(entryPoints[e]) #dateTime, entryPointRefPrice, entryPointActualPrice, SL, TP, Side
    if currentOperation[-1] == 'buy':
        slippage = math.floor((currentOperation[2] - currentOperation[1])/miSize)
        currentOperation[1] += slippage*miSize 
        sl = currentOperation[1] - miSize*stopLossMultiplier
        currentOperation[3] = sl
        currentOperation[1] += slippage
            
    if currentOperation[-1] == 'sell':
        slippage = math.floor((currentOperation[1] - currentOperation[2])/miSize)
        currentOperation[1] -= slippage*miSize 
        sl = currentOperation[1] + miSize*stopLossMultiplier
        currentOperation[3] = sl
        currentOperation[1] -= slippage
    waitForPositionClose()

def waitForPositionClose():
    global m
    
    m+=1
    verifyEndPointAndAddToNpArrays()
    if currentOperation[-1] == "buy":
        if ex:
            return
        while marketInfo[m][-1] > currentOperation[3]: #implement different logic when having more tp types
            m+=1
            verifyEndPointAndAddToNpArrays()
            if ex:
                return
            manageTrailingStop()
        closePosition()
    if currentOperation[-1] == "sell":
        if ex:
            return
        while marketInfo[m][-1] < currentOperation[3]:
            m+=1
            verifyEndPointAndAddToNpArrays()
            if ex:
                return
            manageTrailingStop()
        closePosition()

def manageTrailingStop():
    global stopPosition
    global cdPastLineIndex
    global firstCdPastLine

    if currentOperation[-1] == "buy":
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
    global totalResult
    if currentOperation[-1] == "buy":
        totalResult += currentOperation[3]-currentOperation[2] #change here when implementing new operation types
    if currentOperation[-1] == "sell":
        totalResult += currentOperation[2]-currentOperation[3] #change here when implementing new operation types

def closePosition():
    registerResults()
    nextEntryPoint()
    searchOperation()

def verifyEndPointAndAddToNpArrays():
    global xNPArray
    global yNPArray
    global ex
    if m != len(marketInfo) and e != len(entryPoints):
        if m != yNPArray[-1]:
            xNPArray.append(m+1)
            yNPArray.append(totalResult)
        return
    xNPArray.append(m+1)
    yNPArray.append(totalResult)
    findTargetVariable()
    print(d)
    ex = True
    
def findTargetVariable():
    global targetVariable
    global x
    x = np.array(xNPArray).reshape((-1, 1))
    y = np.array(yNPArray)
    model = LinearRegression().fit(x,y)
    y_prediction = model.predict(x)
    residuals = y - y_prediction
    residuals_variance = np.var(residuals)
    targetVariable = residuals_variance#/yNPArray[-1]

def operate(slm, mbd, dn):
    global stopLossMultiplier
    global minBreakEvenDistance
    global currentOperation
    global firstCdPastLine
    global cdPastLineIndex
    global stopPosition
    global targetVariable
    global totalResult
    global xNPArray
    global yNPArray
    global ex
    global d
    global e
    global m
    stopLossMultiplier = slm
    minBreakEvenDistance = mbd
    targetVariable = 0 #total profit over residuals variance arround the regression line
    totalResult = 0
    e = 0 #current entry point index
    m = 0 #curent market candle index
    d = dn #definition number
    ex = False
    currentOperation = []
    stopPosition = 0
    firstCdPastLine = False
    cdPastLineIndex = None
    xNPArray = []
    yNPArray = []
    xNPArray.append(totalResult)
    yNPArray.append(m)
    searchOperation()
    del currentOperation
    del xNPArray
    del yNPArray
    return targetVariable

