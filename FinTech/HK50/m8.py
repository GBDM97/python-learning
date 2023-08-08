import os
import datetime

cdir = os.getcwd()
print(cdir)
file_path = cdir + "\FinTech\data.txt"

def formatline(s):
   return s[1].replace('"','').split()

def findWeekDay(d):
    d = d.split(".")
    # print(d)
    return datetime.date(int(d[0]), int(d[1]), int(d[2])).strftime("%A")
    
dict1 = {}

with open(file_path, "r") as file:
    for line in enumerate(file):
        lineARR = formatline(line)
        dict1.update({lineARR[0]+"-"+lineARR[1] : int(lineARR[3])-int(lineARR[4])})

dict2 = dict(sorted(dict1.items(), key=lambda x: x[1], reverse=True))

p0 = 0
p4 = 0
p8 = 0
p12 = 0
p16 = 0
p20 = 0
itemsAnalyzed = 346

# for i in list(dict2.items())[:itemsAnalyzed]:
#     if i[0].split("-")[1] == "04:00:00":
#         p4 = p4 + 1
#     if i[0].split("-")[1] == "08:00:00":
#         p8 = p8 + 1
#     if i[0].split("-")[1] == "12:00:00":
#         p12 = p12 + 1
#     if i[0].split("-")[1] == "16:00:00":
#         p16 = p16 + 1
#     if i[0].split("-")[1] == "20:00:00":
#         p20 = p20 + 1
#     if i[0].split("-")[1] == "00:00:00":
#         p0 = p0 + 1

# print(str(p0/itemsAnalyzed*100)+"====>00")
# print(str(p4/itemsAnalyzed*100)+"====>04")
# print(str(p8/itemsAnalyzed*100)+"====>08")
# print(str(p12/itemsAnalyzed*100)+"====>12")
# print(str(p16/itemsAnalyzed*100)+"====>16")
# print(str(p20/itemsAnalyzed*100)+"====>20")

for i in list(dict2.items())[:itemsAnalyzed]:
    
    if findWeekDay(i[0].split("-")[0]) == "Friday":
        p0 = p0 + 1
    if findWeekDay(i[0].split("-")[0]) == "Monday":
        p4 = p4 + 1
    if findWeekDay(i[0].split("-")[0]) == "Tuesday":
        p8 = p8 + 1
    if findWeekDay(i[0].split("-")[0]) == "Wednesday":
        p12 = p12 + 1
    if findWeekDay(i[0].split("-")[0]) == "Thursday":
        p16 = p16 + 1
    print(i)
    
print(str(p4/itemsAnalyzed*100)+"====>Domingo")
print(str(p8/itemsAnalyzed*100)+"====>Segunda")
print(str(p12/itemsAnalyzed*100)+"====>Terça")
print(str(p16/itemsAnalyzed*100)+"====>Quarta")
print(str(p0/itemsAnalyzed*100)+"====>Quinta")


        



