import matplotlib.pyplot as plt
import math



X,Y,D = list(), list(),list()
def derivee(X,Y):
    D , X2 = list() , list()
    for i in range(len(Y)-1):
        D.append((Y[i+1]-Y[i])/(X[i+1]-X[i]))
        X2.append( (X[i+1]+X[i])     /2     )
    return X2,D


for x in range(600):
    X.append(x/100)
    Y.append(math.sin(x/100))
    D.append(math.cos(x/100))
Yprime = list()

for i in range(len(Y)-1):
    Yprime.append((Y[i+1]-Y[i])/(X[i+1]-X[i]))

X2,D2 = derivee(X,Y)

plt.plot(X,Y,"r")
#plt.plot(X[:len(X)-1],Yprime,"b")
#plt.plot(X[1:],Yprime,"g")
plt.plot(X,D,"b")
plt.plot(X2,D2,"g")
plt.show()