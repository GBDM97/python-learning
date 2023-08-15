import ForexOperator1
import time

start_time = time.time()

X = []
Y = []
Z = []

X_RANGE = [0.01,4.25]
Y_RANGE = [0.01,4.25]

DEFINITION = 100

DEFINITION = int(DEFINITION/10)
for l in range(1, DEFINITION):
    for ll in range(1, DEFINITION):
        X.append(((X_RANGE[1]-X_RANGE[0])/DEFINITION)*l)
        Y.append(((Y_RANGE[1]-Y_RANGE[0])/DEFINITION)*ll)
dn=0
for c in range(0, len(X)):
    dn+=1
    Z.append(ForexOperator1.operate(X[c],Y[c],dn))

print("X = ")
print(X)
print("Y = ")
print(Y)
print("Z = ")
print(Z)
print(time.time()-start_time)

