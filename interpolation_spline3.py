import numpy as np 

def inti_spline(X,Y, F1=0 , Fn=0):
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

    
    return M,h,C,Cprime





