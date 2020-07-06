import numpy as np 
import matplotlib.pyplot as plt
from scipy.integrate import quad
#from math import *



def init_spline(X,Y, F1=0 , Fn=0):
    n = len(X)
    h=[]
    F=[]
    h.append(X[1]-X[0])
    for i in range (1,len(X)-1):
        h.append(X[i+1]-X[i])
        F.append( (Y[i+1]-Y[i])/h[i] - ((Y[i]-Y[i-1])/h[i-1]) )
    F = [F1] + F +[Fn]

    X = np.array(X)
    Y = np.array(Y)
    h = np.array(h)
    F = np.array(F)
    R = np.zeros((n,n))
    
    R[0,0],R[n-1,n-1] = 1,1

    for i in range (1,n-1):
        R[i,i] = (h[i-1]+h[i])/3 #diagonale
        R[i,i+1] = h[i]/6 #diagonale superieure
        R[i,i-1] = h[i-1]/6 #diagonale inferieure
    
    invR = np.linalg.inv(R)
    M = np.dot(invR , F)
    C,Cprime = np.zeros(n-1),np.zeros(n-1)
    for i in range(n-1):
        C[i] = (Y[i+1]-Y[i])/h[i] - h[i]/6 * (M[i+1]-M[i])
        Cprime[i] = Y[i] - M[i]*(h[i]**2)/6
    
    #print(C)
    return M,h,C,Cprime





class Spline:
    def __init__(self,X,Y):
        self.X = X
        self.Y = Y
        self.M , self.h , self.C , self.Cprime = init_spline(self.X,self.Y)

    def interpolated(self,x):
        n = len(self.X)
        if x< self.X[0]:
            return self.Y[0]
        elif x>self.X[n-1]:
            return self.Y[n-1]
        k = 0
        while not(self.X[k] <= x <= self.X[k+1]) : #inf ou egal?
            k += 1
        y = self.M[k] * (self.X[k+1]-x)**3 / (6*self.h[k]) 
        y += self.M[k+1] * (x-self.X[k])**3 / (6*self.h[k])
        y += self.C[k] * (x - self.X[k])
        y += self.Cprime[k]

        return (y)







#TEST DE LA FONCTION

#X = [0,0.5,1,1.5,2]
#Y = [0,0.4794,0.8415,0.9975,0.9093]


#X = list(np.arange(0,8.05,0.5))
#Y = list(np.sin(X))

#splinned = Spline(X,Y)


#Xtest = list(np.arange(0,8,0.01))
#Ytest = list()

#xmin = 0.0
#xmax = 2*np.pi
#def function(x): 
#    return np.abs(splinned.interpolated(x) - np.sin(x))
#res, err = quad(function, xmin, xmax)

#print("Erreur: ", res)     





#for x in Xtest:
#    if x in X:
#        y = Y.pop(0)
#        Ytest.append(y)
#    else :
#        Ytest.append(splinned.interpolated(x))
#Y = list(np.sin(X))
#plt.plot(X,Y,'b')

#plt.plot(Xtest,Ytest,'r')


##plt.show()
