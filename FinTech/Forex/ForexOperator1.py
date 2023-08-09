#Next possible dimensions implementations: 
#Trailing stop distance from current price in case of tp SURF
#Current price distance to put stop on break even
#Daily, weekly or monthly Risk Management
#dimensionsInput = [tpType, stoplossMultiplier, breakEvenDistance]
import os
import datetime

targetVariable = 0 #total profit over residuals variance arround the regression line
stopLossMultiplier = 2.25
breakEvenDistance = 1

allResults = {}
marketInfo = []
entryPoints = []
e = 0 #current entry point index
m = 0 #curent market candle index
currentOperation = []

cdir = os.getcwd()
file_path = cdir + "\\FinTech\\Forex\\USDJPY_M15_2023_3Y.csv"
with open(file_path, "r") as file:
    for index, line in enumerate(file):
        if index > 0:
            marketInfo.append(line.replace('"','').split())
file_path = cdir + "\\FinTech\\Forex\\Forex_Entrypoints.csv"
with open(file_path, "r") as file:
    for index, line in enumerate(file):
        if index > 0:
            entryPoints.append(line.replace('\n','').replace(' ',',').split(','))        

def nextEntryPoint():
    global e
    e += 1
    return e

def searchOperation():
    global m
    while entryPoints[e][0] != marketInfo[m][0] or entryPoints[e][1].split(":")[0] > marketInfo[m][1].split(":")[0] or entryPoints[e][1].split(":")[1] >= marketInfo[m][1].split(":")[1]:
        m+=1
    enterOperation()

def enterOperation():
    currentOperation = entryPoints[e] #todo define stop and gain prices
    
    
searchOperation()