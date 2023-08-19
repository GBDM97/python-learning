import ForexOperator1

operationRequest = [4.24, 4.24, 1]

out = ForexOperator1.operateOneTime(operationRequest[0],operationRequest[1],operationRequest[2])

with open('FinTech\\Forex\\Output_Files\\out1.csv', 'w') as file:
    for i in out:
        w = str(i)
        w = w.replace(".",",")
        file.write(w+"\n")