import numpy as np 

def calcul_spline(X,Y, F1=0 , Fn=0):
    n = len(X)
    h=[]
    F=[]
    h.append(X[1]-X[0])
    for i in range (1,len(x)-1):
        h.append(X[i+1]-X[i])
        F.append( (Y[i+1]-Y[i]/h[i]) - ((Y[i]-Y[i-1])/h[i-1]) )
    F = [F1] + F +[Fn]

    X = np.array(X)
    Y = np.array(Y)
    h = np.array(h)
    F = np.array(F)

    


