import os
import datetime

cdir = os.getcwd()
file_path = cdir + "\FinTech\HK50M1_10_01_2023.txt"
currentDate = ""
dataArray = []
dayInitIndex = None
with open(file_path, "r") as file:
    for line in enumerate(file):
        dataArray.append(line[1].replace('"','').split())

def initialFimatheChannel(d):
    global dayInitIndex
    dayInitIndex = d
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
    for i in cdsData:
        firstComparedElement = int(i)
        for ii in range(1, len(cdsData)):
            secondComparedElement = int(cdsData[ii])
            currentAnalyzedChannelSize = abs(firstComparedElement-secondComparedElement)
            if bestChannelFound is None:
                bestChannelFound = sorted([firstComparedElement, secondComparedElement], reverse=True)
                bestChannelFound.append(bestChannelFound[0]-bestChannelFound[1])
                continue
            if abs(currentAnalyzedChannelSize - averageChannel) < abs(bestChannelFound[2]-averageChannel):
                bestChannelFound = sorted([firstComparedElement, secondComparedElement], reverse=True)
                bestChannelFound.append(bestChannelFound[0]-bestChannelFound[1])
    #finding the first reference channel:
    firstRefChannel = None
    closeOfCd4 = int(dataArray[dayInitIndex+3][5])
    if closeOfCd4 > bestChannelFound[0]:
        currentChannel = bestChannelFound
        while closeOfCd4 > currentChannel[0]:
            currentChannel[0] = currentChannel[0]+currentChannel[2]
            currentChannel[1] = currentChannel[1]+currentChannel[2]
        firstRefChannel = currentChannel
    if closeOfCd4 < bestChannelFound[1]:
        currentChannel = bestChannelFound
        while closeOfCd4 < currentChannel[1]:
            currentChannel[0] = currentChannel[0]-currentChannel[2]
            currentChannel[1] = currentChannel[1]-currentChannel[2]
        firstRefChannel = currentChannel
    else:
        firstRefChannel = bestChannelFound
    #adapt channel for operations use
    reversedCdsData = cdsData[::-1]
    i = 0
    currentClose = int(reversedCdsData[i])
    currentOpen = int(reversedCdsData[i+3])
    while currentOpen <= firstRefChannel[0] and currentOpen >= firstRefChannel[1] and currentClose <= firstRefChannel[0] and currentClose >= firstRefChannel[1]:
        i = i + 4
        if i+3 > 16:
            print("First reference channel not found for the date: "+ dataArray[dayInitIndex][0])
            return
        currentClose = int(reversedCdsData[i])
        currentOpen = int(reversedCdsData[i+3])
    if currentOpen < firstRefChannel[1] or currentClose < firstRefChannel[1]:
        firstRefChannel[1] = firstRefChannel[1]-firstRefChannel[2]
        return firstRefChannel
    if currentOpen > firstRefChannel[0] or currentClose > firstRefChannel[0]:
        firstRefChannel[0] = firstRefChannel[0]+firstRefChannel[2]
        return firstRefChannel

def getDay():
    global currentDate
    for index, data in enumerate(dataArray):
        if data[0] != currentDate:
            currentDate = data[0]
            return index

def operate(firstRefChannel):

    #Apply security Extension
    def applySecurityExtension(firstRefChannel):
        securityExtension = 1
        if firstRefChannel is None:
            return
        firstRefChannel = [
            firstRefChannel[0]+(securityExtension*firstRefChannel[2]),
            firstRefChannel[1]-(securityExtension*firstRefChannel[2]), 
            firstRefChannel[2]
        ]
        currentRefChannel = firstRefChannel
        currentRefChannel.append("Extended")
        return currentRefChannel

    #search for operation opportunity:
    def searchOpr(currentCdIndex, currentRefChannel):
        operationRequest = []
        spread = 10
        while int(dataArray[currentCdIndex][5]) <= currentRefChannel[0] and int(dataArray[currentCdIndex][5]) >= currentRefChannel[1]:
            currentCdIndex = currentCdIndex+1
        if int(dataArray[currentCdIndex][5]) > currentRefChannel[0]:
            return ['Buy', currentCdIndex, int(dataArray[currentCdIndex][5])+spread,
            currentRefChannel[0]-round(currentRefChannel[2]*2,25),currentRefChannel]
        elif int(dataArray[currentCdIndex][5]) < currentRefChannel[1]:
            return ['Sell', currentCdIndex, int(dataArray[currentCdIndex][5])-spread,
            currentRefChannel[1]+round(currentRefChannel[2]*2,25),currentRefChannel]
        #operation request information: buy or sell, current cd index, entry price, stop, current ref channel

    def startOperations(operationRequest):
        def decide():
            print("decide function executed")
        side = operationRequest[0]
        currentCdIndex = operationRequest[1]
        entryPrice = operationRequest[2]
        stop = operationRequest[3]
        noLoss = False #akas zero a zero

        if side == "Buy":
            while dataArray[currentCdIndex][5] > stop:
                currentCdIndex = currentCdIndex+1
                if dataArray[currentCdIndex][5] > entryPrice + (operationRequest[4][2]*2) and noLoss == False:
                    noLoss = True
                    stop = entryPrice
                elif dataArray[currentCdIndex[5]] > stop + (operationRequest[4][2]*2):
            
        if side == "Sell":
            while dataArray[currentCdIndex][5] < stop:
                currentCdIndex = currentCdIndex+1
            
        decide()

    currentCdIndex = dayInitIndex + 4
    startOperations(searchOpr(currentCdIndex, applySecurityExtension(firstRefChannel)) )


operate(initialFimatheChannel(33519))

    #pegar a abertura/max/min/fechamento dos primeiros 4 cds e encontrar os dois niveis de preço que formariam um canal
    #com a maior proximidade de averageChannel
