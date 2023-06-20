import os
import datetime

cdir = os.getcwd()
file_path = cdir + "\FinTech\HK50M1_10_01_2023.txt"
allResults = {}
dataArray = []
dayInitIndex = None
with open(file_path, "r") as file:
    for line in enumerate(file):
        dataArray.append(line[1].replace('"','').split())
currentDate = None
currentCdIndex = 0

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

def operateSpecificDay(firstRefChannel):

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
        spread = 10
        while int(dataArray[currentCdIndex][5]) <= currentRefChannel[0] and int(dataArray[currentCdIndex][5]) >= currentRefChannel[1]:
            currentCdIndex = currentCdIndex+1
        if int(dataArray[currentCdIndex][5]) > currentRefChannel[0]:
            return ['Buy', currentCdIndex, int(dataArray[currentCdIndex][5])+spread,
            currentRefChannel[0]-round(currentRefChannel[2]*2.25),currentRefChannel]
        elif int(dataArray[currentCdIndex][5]) < currentRefChannel[1]:
            return ['Sell', currentCdIndex, int(dataArray[currentCdIndex][5])-spread,
            currentRefChannel[1]+round(currentRefChannel[2]*2.25),currentRefChannel]
        #operation request information: buy or sell, current cd index, entry price, stop, current ref channel

    def startOperation(operationRequest):
        def registerDayOperation(result):
            global allResults
            global currentDate
            if currentDate in allResults:
                newEntry = allResults[currentDate]
                newEntry.append(result)
                allResults.update({currentDate:newEntry})
            else:
                allResults.update({currentDate:[result]})

        def decideDayOperations(req, index):
            currResults = allResults[currentDate]
            # we will build another operation req
            # in case there will be another operation
            
            # ===========
            # Here are the daily rules of operation:
            # Deu o take vaza! :
            if len(currResults) == 1 and currResults[0] > 0:
                return currentCdIndex
            # Primeiro stop, ou zero a zero? tenta de novo vai :
            if len(currResults) == 1  and currResults[0] <= 0:
                updatedReq = updateReferences(req, index)
                startOperation(searchOpr(updatedReq[1], updatedReq[4]))
            # Duas operações? vaza meo :
            if len(currResults) == 2:
                return currentCdIndex
            # Next possible daily rules:
            # Operar antes das 8 somente
            # Operar mais ou menos
            # Depois de um loss e um zero a zero, ou dois zero a zero, opera? 

        def updateReferences(req, index):
            def returnValue(i):
                while req[4][0] > int(dataArray[i][5]) and int(dataArray[i][5]) > req[4][1]:
                    i -= 1
                if int(dataArray[i][5]) > req[4][0]:
                    req[4][0] += req[4][2]
                if int(dataArray[i][5]) < req[4][1]:
                    req[4][1] -= req[4][2]
                return req

            req[1] = index
            i = index
            if int(dataArray[i][5]) > req[4][0]:
                while int(dataArray[i][5]) > req[4][0]:
                    req[4][0] += req[4][2]
                    i += 1
                req[4][1] = req[4][0]-req[4][2]
                return returnValue(i)
            elif int(dataArray[i][5]) < req[4][1]:
                while int(dataArray[i][5]) < req[4][1]:
                    req[4][1] -= req[4][2]
                    i+=1
                req[4][0] = req[4][1]+req[4][2]
                return returnValue(i)
            else:
                while int(dataArray[i][5]) < req[4][0]:
                    req[4][0] -= req[4][2]
                    i+=1
                req[4][0] += req[4][2]
                req[4][1] = req[4][0]-req[4][2]
                return returnValue(i)
                
        side = operationRequest[0]
        global currentCdIndex
        currentCdIndex = operationRequest[1]
        entryPrice = operationRequest[2]
        stop = operationRequest[3]
        stopPosition = 0
        firstCdPastLine = False
        operationResult = None
        cdPastLineIndex = None

        if side == "Buy":
            while int(dataArray[currentCdIndex][4]) > stop:
                currentCdIndex = currentCdIndex+1
                if int(dataArray[currentCdIndex][5]) > entryPrice + (operationRequest[4][2]) and stopPosition == 0:
                    if firstCdPastLine == True:
                        if int(dataArray[currentCdIndex][5]) > int(dataArray[cdPastLineIndex][5]):
                            stopPosition = 1
                            stop = entryPrice
                    else:
                        firstCdPastLine = True
                        cdPastLineIndex = currentCdIndex
                if int(dataArray[currentCdIndex][5]) > operationRequest[4][0] + (operationRequest[4][2]*2) and stopPosition == 1:
                    stopPosition = 2
                    stop = round(0.75*operationRequest[4][2] + operationRequest[4][0])
                    operationRequest[4] = [operationRequest[4][0]+operationRequest[4][2]*3, operationRequest[4][0]+operationRequest[4][2], operationRequest[4][2]]
                    #the channel is retracted
                if int(dataArray[currentCdIndex][5]) > operationRequest[4][0] and stopPosition == 2:
                    operationRequest[4][0] = operationRequest[4][0]+operationRequest[4][2]
                    operationRequest[4][1] = operationRequest[4][1]+operationRequest[4][2]
                    stop = operationRequest[4][1]-round(0.25*operationRequest[4][2])
            operationResult = stop - entryPrice
            

        if side == "Sell":
            while int(dataArray[currentCdIndex][4]) < stop:
                currentCdIndex = currentCdIndex+1
                if int(dataArray[currentCdIndex][5]) < entryPrice - (operationRequest[4][2]) and stopPosition == 0:
                    if firstCdPastLine == True:
                        if int(dataArray[currentCdIndex][5]) < int(dataArray[cdPastLineIndex][5]):
                            stopPosition = 1
                            stop = entryPrice
                    else: 
                        firstCdPastLine = True
                        cdPastLineIndex = currentCdIndex
                if int(dataArray[currentCdIndex][5]) < operationRequest[4][1] - (operationRequest[4][2]*2) and stopPosition == 1:
                    stopPosition = 2
                    stop = round(operationRequest[4][1] - 0.75*operationRequest[4][2])
                    operationRequest[4] = [operationRequest[4][1]-operationRequest[4][2]*3, operationRequest[4][1]-operationRequest[4][2], operationRequest[4][2]]
                    #the channel is retracted
                if int(dataArray[currentCdIndex][5]) < operationRequest[4][1] and stopPosition == 2:
                    operationRequest[4][1] = operationRequest[4][1]-operationRequest[4][2]
                    operationRequest[4][0] = operationRequest[4][0]-operationRequest[4][2]
                    stop = operationRequest[4][0]+round(0.25*operationRequest[4][2])
            operationResult = entryPrice - stop
        registerDayOperation(operationResult)
        return decideDayOperations(operationRequest, currentCdIndex)
        

    currentCdIndex = dayInitIndex + 4
    return startOperation(searchOpr(currentCdIndex, applySecurityExtension(firstRefChannel)))

def selectDaysAndOperate():
    # The days are Brazil operation days:
    
    global currentDate

    SUNDAY = True
    MONDAY = True
    TUESDAY = False
    WEDNESDAY = False
    THURSDAY = False

    operationDaysArray = []
    i = 0

    def transformToWeekDay(d):
        d = d.split(".")
        # print(d)
        return datetime.date(int(d[0]), int(d[1]), int(d[2])).strftime("%A")
    def isDateWeekDayPresent(date, array):
        try:
            array.index(transformToWeekDay(date))
            return True
        except:
            return False

    if SUNDAY:
        operationDaysArray.append("Monday")
    if MONDAY:
        operationDaysArray.append("Tuesday")
    if TUESDAY:
        operationDaysArray.append("Wednesday")
    if WEDNESDAY:
        operationDaysArray.append("Thursday")
    if THURSDAY:
        operationDaysArray.append("Friday")

    while i < len(dataArray):
        currentDate = dataArray[i][0]
        if isDateWeekDayPresent(dataArray[i][0], operationDaysArray):
            i = operateSpecificDay(initialFimatheChannel(i))
        while currentDate == dataArray[i][0]:
            i+=1
            
            
    return allResults

print(selectDaysAndOperate())

