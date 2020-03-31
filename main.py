from scipy.integrate import quad
from math import *


def Normale(x):
    return 1/sqrt(2*pi) * exp(-x**2/2)

def N(x):
    res = quad(Normale, -50,x)[0]    
    return res






def BlackScholes(S0,T,K,r,sigma):
    d1 = 1/(sigma*sqrt(T)) *(log(S0/K)+T*(r+sigma**2/2))
    d2 = d1 - sigma * sqrt(T)

    C = S0 * N(d1) - K*exp(-r*T) * N(d2)
    
    return C 

def payoff (S0,K,r,T,sigma):
    d1 = 1/(sigma*sqrt(T)) *(log(S0/K)+T*(r+sigma**2/2))
    d2 = d1 - sigma * sqrt(T)

    P = -S0 * N(-d1) + K*exp(-r*T) * N(-d2)
    return P


