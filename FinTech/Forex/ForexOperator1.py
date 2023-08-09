#Next possible dimensions implementations: 
#Trailing stop distance from current price in case of tp SURF
#Current price distance to put stop on break even
#Daily, weekly or monthly Risk Management
#dimensionsInput = [tpType, stoplossMultiplier, breakEvenDistance]
import os
import datetime

cdir = os.getcwd()
file_path = cdir + "\\FinTech\\Forex\\USDJPY_M15_2023_3Y.csv"
allResults = {}
dataArray = []
with open(file_path, "r") as file:
    for line in enumerate(file):
        dataArray.append(line[1].replace('"','').split())
targetVariable = 0 #total profit over residuals variance arround the regression line
currentEntryPoint = 0


def nextEntryPoint():
    global currentEntryPoint
    currentEntryPoint += 1
    return currentEntryPoint
nextEntryPoint()

def searchOperation():
    for i in dataArray:
        print(i)
searchOperation()