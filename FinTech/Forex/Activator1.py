import ForexOperator1

X = []
Y = []
Z = []

X_RANGE = [0.01,4.25]
Y_RANGE = [0.01,4.25]

DEFINITION = 10

for c in range(1, DEFINITION):
    X.append(((X_RANGE[1]-X_RANGE[0])/DEFINITION)*c)
    Y.append(((Y_RANGE[1]-Y_RANGE[0])/DEFINITION)*c)

for xVal in X:
    for yVal in Y:
        Z.append(ForexOperator1.operate(xVal,yVal))

print("X = ")
print(X)
print("Y = ")
print(Y)
print("Z = ")
print(Z)
