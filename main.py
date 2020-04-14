from scipy.integrate import quad
from math import sqrt,log,exp,pi
import matplotlib.pyplot as plt

def Normale(x):
    return 1/sqrt(2*pi) * exp(-x**2/2)

def N(x):
    res = quad(Normale, -50,x)[0]    
    return res



# T = DTE / 365 
# IV est la volatility sigma (volatilité implicite)
# K = Strike
# S0 = Price valeur actuelle de l'action sous jacente
# r = 0 ?????? taux interet sans risque


def Put(S0,T,K,r,sigma):
    d1 = 1/(sigma*sqrt(T)) *(log(S0/K)+T*(r+sigma**2/2))
    d2 = d1 - sigma * sqrt(T)

    P = -S0 * N(-d1) + K*exp(-r*T) * N(-d2)
    return P




def Call(S0,T,K,r,sigma):
    d1 = 1/(sigma*sqrt(T)) *(log(S0/K)+T*(r+sigma**2/2))
    d2 = d1 - sigma * sqrt(T)

    C = S0 * N(d1) - K*exp(-r*T) * N(d2)
    
    return C 

print(Put(650.95 , 4/365 , 580,0,0.9725))

X,Y = [] , []

for i in range (0, 1000):
    X.append(i)
    Y.append(Call(5.96 , 25/365 , 6,i/1000,0.8784))

plt.plot(X,Y)
plt.show()


