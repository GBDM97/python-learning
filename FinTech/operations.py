import os
import datetime

cdir = os.getcwd()
file_path = cdir + "\FinTech\HK50M1_10_01_2023.txt"
currentDate = ""
dataArray = []
with open(file_path, "r") as file:
    for line in enumerate(file):
        dataArray.append(line[1].replace('"','').split())

def fimatheChannel(dayInitIndex):
    
    #getting the four cds all values:
    cdsData = [dataArray[dayInitIndex][2],dataArray[dayInitIndex][3],dataArray[dayInitIndex][4],
    dataArray[dayInitIndex][5],
    dataArray[dayInitIndex+1][2],dataArray[dayInitIndex+1][3],dataArray[dayInitIndex+1][4],
    dataArray[dayInitIndex+1][5],
    dataArray[dayInitIndex+2][2],dataArray[dayInitIndex+2][3],dataArray[dayInitIndex+2][4],
    dataArray[dayInitIndex+2][5],
    dataArray[dayInitIndex+3][2],dataArray[dayInitIndex+3][3],dataArray[dayInitIndex+3][4],
    dataArray[dayInitIndex+3][5]]

    #finding refs and size of the best channel:
    bestChannelFound = None
    averageChannel = 30
    for i in len(cdsData):
        firstComparedElement = cdsData[i]
        for ii in range(1, len(cdsData)):
            secondComparedElement = cdsData[ii]
            currentAnalyzedChannelSize = abs(firstComparedElement-secondComparedElement)
            if abs(currentAnalyzedChannelSize - averageChannel) < bestChannelFound:
                bestChannelFound = sorted([firstComparedElement, secondComparedElement], reverse=True)
                bestChannelFound.append(bestChannelFound[0]-bestChannelFound[1])
    #finding the first reference channel:
    closeOfCd4 = dataArray[dayInitIndex+3][5]
    

    print(cdsData)

def getDay():
    global currentDate
    for index, data in enumerate(dataArray):
        if data[0] != currentDate:
            currentDate = data[0]
            return index

def operator():
    fimatheChannel(getDay())
    fimatheChannel(getDay())


operator()

    #pegar a abertura/max/min/fechamento dos primeiros 4 cds e encontrar os dois niveis de preço que formariam um canal
    #com a maior proximidade de averageChannel
