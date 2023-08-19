import ForexOperator1
import time
import math

start_time = time.time()

X = []
Y = []
Z = []
minZ = 1000
aspectRatioX = 0.1
aspectRatioY = 0.1
aspectRatioZ = 5
bestOperation = []

X_RANGE = [0.01,4.25]
Y_RANGE = [0.01,4.25]

DEFINITION = 10000 #insert here how many pixels of definition do you want for the 3d graph

DEFINITION = int(math.sqrt(DEFINITION))
for l in range(1, DEFINITION+1):
    for ll in range(1, DEFINITION+1):
        X.append((((X_RANGE[1]-X_RANGE[0])/DEFINITION)*l))
        Y.append((((Y_RANGE[1]-Y_RANGE[0])/DEFINITION)*ll))
dn=0
for c in range(0, len(X)):
    dn+=1
    fx = ForexOperator1.operate(X[c],Y[c],dn)
    if fx < minZ:
        minZ = fx
        bestOperation = [X[c],Y[c],minZ]
    Z.append(fx)

for i, element in enumerate(X):
    X[i] = element*aspectRatioX
for i, element in enumerate(Y):
    Y[i] = element*aspectRatioY
for i, element in enumerate(Z):
    Z[i] = element*aspectRatioZ

with open('FinTech\\Forex\\Output_Files\\3D.txt', 'w') as file:
    file.write("X = "+ str(X)+"\n")
    file.write("Y = "+ str(Y)+"\n")
    file.write("Z = "+ str(Z)+"\n")
print(bestOperation)

print(time.time()-start_time)

