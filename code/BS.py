
from scipy.integrate import quad
from math import sqrt,log,exp,pi



def Normale(x):
    return 1/sqrt(2*pi) * exp(-x**2/2)

def N(x):
    res = quad(Normale, -50,x)[0]    
    return res



# T = DTE / 365 
# IV est la volatility sigma (volatilité implicite)
# K = Strike
# S0 = Price valeur actuelle de l'action sous jacente
# r = 0.1 taux interet sans risque OIS/USD 


def d1(S0,T,K,r,sigma):
    return 1/(sigma*sqrt(T)) *(log(S0/K)+T*(r+sigma**2/2))


def d2(S0,T,K,r,sigma):
    return d1(S0,T,K,r,sigma) - sigma * sqrt(T)


def delta_call(S0,T,K,r,sigma):
    return N(d1(S0,T,K,r,sigma))

def delta_put(S0,T,K,r,sigma):
    return delta_call(S0,T,K,r,sigma) - 1



def gamma(S0,T,K,r,sigma):   # gamma_call = gamma_put
    return Normale(d1(S0,T,K,r,sigma)) / (S0*sigma*sqrt(T))



def theta_call(S0,T,K,r,sigma):
    theta = - S0 * sigma * Normale(d1(S0,T,K,r,sigma)) / (2*sqrt(T)) 
    
    theta = theta - r * K * N(d2(S0,T,K,r,sigma)) *exp(-r*T)
    return theta


def theta_put(S0,T,K,r,sigma):
    theta = - S0 * sigma * Normale(d1(S0,T,K,r,sigma)) / (2*sqrt(T)) 

    theta = theta + r * K * N(-d2(S0,T,K,r,sigma)) *exp(-r*T)
    return theta

def rho_call(S0,T,K,r,sigma):
    return K*T*N(d2(S0,T,K,r,sigma)) * exp(-r*T)

def rho_put(S0,T,K,r,sigma):
    return - K*T*N(-d2(S0,T,K,r,sigma)) * exp(-r*T)


def vega(S0,T,K,r,sigma): # vega_call = vega_put
    return sqrt(T) * S0 * Normale( d1(S0,T,K,r,sigma) ) 


def Put(S0,T,K,r,sigma):
    P = -S0 * N(-d1(S0,T,K,r,sigma)) + K*exp(-r*T) * N(-d2(S0,T,K,r,sigma))
    return P

def Call(S0,T,K,r,sigma):
    C = S0 * N(d1(S0,T,K,r,sigma)) - K*exp(-r*T) * N(d2(S0,T,K,r,sigma))
    return C 



def derivee(X,Y): #derive la fonction Y = f(X)
    D , X2 = list() , list()
    for i in range(len(Y)-1):
        D.append((Y[i+1]-Y[i])/(X[i+1]-X[i]))
        X2.append( (X[i+1]+X[i])     /2     )
    return X2,D


#d PrixBS / d K 
# doit tendre vers 1 en +inf et 0 en O


#print(Put(650.95 , 4/365 , 580,0,0.9725))

print(1 + (1/10)*(Call(650.95 , 4/365 , 580+5,0,0.9725)-Call(650.95 , 4/365 , 580-5,0,0.9725)))


print (N(d2(650.95 , 4/365 , 580+5,0,0.9725)))