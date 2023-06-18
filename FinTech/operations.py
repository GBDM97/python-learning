import os
import datetime

cdir = os.getcwd()
file_path = cdir + "\FinTech\HK50M1_10_01_2023.txt"
currentDate = ""
dataArray = []
with open(file_path, "r") as file:
    for line in enumerate(file):
        dataArray.append(line[1].replace('"','').split())

def fimatheChannel(day):
    averageChannel = 30
    print(day)

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
