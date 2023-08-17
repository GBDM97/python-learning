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

mdtype = np.dtype([
    ('datetime', np.datetime64),
    ('open', np.float32),
    ('high', np.float32),
    ('low', np.float32),
    ('close', np.float32)
])
edtype = np.dtype([
    ('datetime', np.datetime64),
    ('entryPointRef', np.float32),
    ('entryPointActual', np.float32),
    ('sl', np.float32),
    ('tp', np.float32),
    ('side', np.dtype('S10'))
])

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
    if pl[-1] != "buy" and pl[-1] != "sell":
        out=np.array([],dtype=mdtype)
        out=np.append(out, date_time)
        out=np.append(out,float(pl[2]))
        out=np.append(out,float(pl[3]))
        out=np.append(out,float(pl[4]))
        out=np.append(out,float(pl[5]))
    else:
        out=np.array([],dtype=edtype)
        out=np.append(out, date_time)
        out=np.append(out,float(pl[2]))
        out=np.append(out,float(pl[3]))
        out=np.append(out,0)
        out=np.append(out,0)
        out=np.append(out,pl[4])
    return np.array(out)

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
    currentOperation = entryPoints[e] #dateTime, entryPointRefPrice, entryPointActualPrice, SL, TP, Side
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
            xNPArray.append(np.array([m+1],dtype=np.float32))
            yNPArray.append(np.array([totalResult],dtype=np.float32))
        return
    xNPArray.append(np.array([m+1],dtype=np.float32))
    yNPArray.append(np.array([totalResult],dtype=np.float32))
    findTargetVariable()
    print(d)
    ex = True
    
def findTargetVariable():
    global targetVariable
    x = np.append(x, xNPArray).reshape((-1, 1))
    y = np.append(y, yNPArray)
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
    currentOperation = np.array([],dtype=edtype)
    if dn == 700:
        print
    stopPosition = 0
    firstCdPastLine = False
    cdPastLineIndex = None
    xNPArray = []
    yNPArray = []
    xNPArray.append(np.array([totalResult],dtype=np.float32))
    yNPArray.append(np.array([m],dtype=np.float32))
    searchOperation()
    return targetVariable

