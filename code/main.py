import matplotlib.pyplot as plt
import BS
import interpolation_spline3
import csv
from math import sqrt,exp,sin
import numpy as np
from mpl_toolkits import mplot3d

file_name = None
#while file_name == None:  
#symbol=input("sur quel symbol on travaille? : ")
symbol ='AMZN'
file_name = "stocks-options_extracted_" + symbol + ".csv"




def Pearson(x,y): #Retourne le coefficient de correlation de Pearson entre les distributions x et y
    xm,sigmax = study(x)
    ym,sigmay = study(y)
    n = min(len(x),len(y))
    coef = 0.0
    for i in range(n):
        coef +=  (x[i]-xm)*(y[i]-ym)
    coef = coef/(n*sigmax*sigmay)
    return coef

def pseudo_normalize(L):
    n = len(L)
    new_L = [i/(n-1) for i in range(n)]
    return new_L

def rearrange(x,y): #retourne les listes x et y avec le meme nombre d'elements
    n = min (len(x),len(y))
    return x[:n],y[:n]

def study(L): #retoune la moyenne et l'écart type de la distribution L
    
    for i in range(len(L)): #petit test
        L[i] = abs(L[i])
    moy = sum(L) / len(L)
    M = list()
    for x in L:
        M.append((x-moy)**2)
    var = sum(M) / len(M)
    et = sqrt(var)
    return moy,et
    
def TRI(X,Y):#trie la liste L et applique les même changement à la liste M
    L,M = X[:],Y[:]
    if len(L) != len(M):
        raise("Les listes doivent être de la même taille.")
    for k in range(1,len(L)): #cette partie est simplement un tri croissant de la liste Calls
        temp=L[k]
        temp2=M[k]
        j=k
        while j>0 and temp<L[j-1]:
            L[j]=L[j-1]
            M[j]=M[j-1] #on y applique les memes changements sur la liste IV
            j-=1 
        L[j]=temp
        M[j]=temp2   
    return L,M
    
def TRI3(X,Y):#trie la liste L et applique les même changement à la liste M
    L,M = X[:],Y[:]
    if len(L) != len(M):
        raise("Les listes doivent être de la même taille.")
    for k in range(1,len(L)): #cette partie est simplement un tri croissant de la liste Calls
        temp=L[k]
        temp2=M[k]
        j=k
        while j>0 and temp<L[j-1]:
            L[j]=L[j-1]
            M[j]=M[j-1] #on y applique les memes changements sur la liste IV
            j-=1 
        L[j]=temp
        M[j]=temp2   
    return L,M

def TRI2(L,indexes): #retire les éléments d'indices dans indexes dans L
    k = 0
    for i in indexes:
        L.pop(i-k)
        k += 1
    return L

def recup(symbol):
    with open("stocks-options_extracted_" + symbol + ".csv", newline='') as csvfile:
        IV_index, S0s_index,Ts_index,Ks_index, Volume_index = 0,0,0,0,0
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        IVs,S0s,Ts,Ks,Volumes = list(),list(),list(),list(),list()
        for row in spamreader:
            A = list((",".join(row)).split(","))

            if not(IV_index == 0) :
                n = len(A[IV_index])
                sigma =float(A[IV_index][:n-1])/100  #pourcentages donc /100 
                
                IVs.append(sigma)
                S0s.append(float(A[S0s_index]))
                Ts.append(float(A[Ts_index])/365) #en annee donc /365
                Ks.append(float(A[Ks_index]))
                Volumes.append(float(A[Volume_index]))

            #NE SE FAIT QU'AU HEADER ===========
            else:
                while A[S0s_index] != 'Price':
                    S0s_index += 1
                while A[Ks_index] != 'Strike':
                    Ks_index += 1
                while A[Ts_index] != 'DTE':
                    Ts_index += 1
                while A[IV_index] != 'IV':
                    IV_index += 1
                while A[Volume_index] != 'Volume':
                    Volume_index += 1
            #NE SE FAIT QU'AU HEADER ===========
    return S0s,Ts,Ks,IVs,Volumes

def numbarize(n): #transforme le str "1.234" en l'int "1234"
    #type(n) = str
    if "." in n:
        k=0
        while n[k] != ".":
            k+=1
        return str(int(n[:k])*1000) + n[k:]
    return n

def recup2(csvname,DTE,S0):
    with open(csvname, newline='') as csvfile:
        IV_index,Ks_index, Volume_index,Type_index = 0,0,0,0
        spamreader = csv.reader(csvfile,delimiter=';', quotechar='|')
        IVs,S0s,Ts,Ks,Volumes = list(),list(),list(),list(),list()
        for row in spamreader:
            A = list((",".join(row)).split(","))
            if not(IV_index == 0):
                
                if A[Type_index] == "Call":
                    n = len(A[IV_index])
                    sigma =float(A[IV_index][:n-1])/100  #pourcentages donc /100 
                    IVs.append(sigma)
                    S0s.append(S0)
                    Ts.append(DTE/365)
                    Ks.append(float(A[Ks_index]))
                    Volumes.append(float(numbarize(A[Volume_index])))

            #NE SE FAIT QU'AU HEADER ===========
            else:
                while A[Type_index] != "Type":
                    Type_index += 1
                while A[Ks_index] != 'Strike':
                    Ks_index += 1
                while A[IV_index] != 'IV':
                    IV_index += 1
                while A[Volume_index] != 'Volume':
                    Volume_index += 1
            #NE SE FAIT QU'AU HEADER ===========
    return S0s,Ts,Ks,IVs,Volumes


def distrib(L):
    fig = plt.figure(figsize=(10,5))

    ax = fig.add_subplot(1, 1, (1))

    h = ax.hist(L, bins=20, edgecolor='none')

    ax.set_title('test')

    fig.tight_layout(pad=1)

def distrib2(x,t):
    hist, bin_edges = np.histogram(x, bins=20, normed=True)

    plt.bar(bin_edges[:-1], hist, width=bin_edges[1]-bin_edges[0], color='red', alpha=0.5)
    #plt.bar(([0],0.0010))
    moy,et = study(x)

    coche = moy-t*et
    plt.bar(coche, height=0.060, width=5, bottom=None, align='center', data=None)
    plt.grid()
    plt.xlim(-1,max(x))

    plt.savefig('cumulative_distribution_01.png', bbox_inches='tight')

    plt.show()


def boite(distribution):
    X = [1 for i in range(len(distribution))]
    plt.scatter(X,distribution)
    plt.boxplot(distribution)
    plt.show()


def delete_indexes(Volumes,x,option=True):
    moy,et = study(Volumes)
    indexes = list()
    for i in range(len(Volumes)):
        if option:
            if  not (  moy-x*et  < Volumes[i] < moy+x*et ): #pour la dérivée
                indexes.append(i)
        else: 
            if   (  Volumes[i] < moy - x*et ): #pour le volume
                indexes.append(i)

    return indexes

class SYMBOL:
    def __init__(self,symbol,version,csvname=None,dte=None,S0=None, r=0.0006):
        self.symbol = symbol
        if version == 'v1':
            self.S0 , self.T , self.K , self.IV , self.Volumes = recup(self.symbol)
        else:
            self.S0 , self.T , self.K , self.IV , self.Volumes = recup2(csvname,dte,S0)
        self.r = r  #OIS/USD
        
        self.K_,self.IV_ = TRI3(self.K,self.IV)
        i = 0
        while i <= len(self.K_)-2:
            while self.K_[i] == self.K_[i+1]:
                self.K_.pop(i)
                self.IV.pop(i)
            i += 1
        t = 0.2
        indexes = delete_indexes(self.Volumes,t,False)
        print(f"points supprimés car trop peu liquides pour {self.symbol} : ",len(indexes))
        self.K_ = TRI2(self.K_,indexes)
        self.IV_ = TRI2(self.IV_,indexes)
        self.Volumes_ = TRI2(self.Volumes,indexes)
        self.T_ = TRI2(self.T,indexes)
        self.S0_ = TRI2(self.S0,indexes)
        self.sigma = interpolation_spline3.Spline(self.K_,self.IV_) #Sigma est une fonction qui s'appelle par sigma.interpolated(k)
        
        #recherche atm:
        self.atm_index = 0
        dist = abs(self.K_[self.atm_index] - self.S0_[self.atm_index])
        for j in range(len(self.K_)):
            if abs(self.K_[j] - self.S0_[j]) < dist:
                dist = abs(self.K_[self.atm_index] - self.S0_[self.atm_index])
                self.atm_index = j
        #fin recherche

    def test_sensibilite_F(self):
        
        
        E , proba = list(),list()
    
        for epsilon in range(-10,100):
            E.append(epsilon/100)
            proba.append(self.F(self.atm_index,iv=epsilon/100+self.IV_[self.atm_index]))
        plt.plot(E,proba)
        plt.xlabel("epsilon")
        plt.ylabel("P(St > K)")
        plt.title("Probabilite de finir dans la monnaie avec S0 = K et IV = IV[atm] + epsilon")
        axes = plt.gca()
        #axes.set_xlim([0,1])
        axes.set_ylim([0,1])
        plt.show()


    def test_sensi_Call(self):
        E , prix = list(),list()
        print(self.IV_[self.atm_index])
        for epsilon in range(-10,100):
            E.append(epsilon/1000)
            
            prix.append(BS.Call(self.S0_[self.atm_index],self.T_[self.atm_index],self.K_[self.atm_index],self.r,self.IV_[self.atm_index]+epsilon/1000))


        plt.plot(E,prix)
        plt.xlabel("epsilon")
        plt.ylabel("C(S0,T,K,r,sigma+epsilon)")
        plt.title("Prix du sous jacent à S0 = K et IV = IV[atm] + epsilon")

        plt.show()



    def plot_F(self):
        X,Y,Y2 = list() , list() ,list()
        for i in range(len(self.K_)):
            X.append(self.K_[i])
            Y.append(self.F(i))
            Y2.append(exp(-1* self.r * self.T_[i])*BS.N(BS.d2(self.S0_[i],self.T_[i],self.K_[i],self.r,self.IV_[i])))
        plt.scatter(X,Y,)
        plt.scatter(X,Y2,)
        plt.title(f'P (St >K| S0 = {self.S0_[0]})     {self.symbol}     ( k= {round(Pearson(Y,Y2),4)} )',   )
        plt.xlabel('Strike')
        plt.ylabel('Proba de finir dans la monnaie')
        plt.legend(['Par la fonction de repartition','Par N(d2)'])
        plt.show()

    def plotting(self,color = 'r'):
        
        borne_inf=(self.K_[0]*10)//1 + 1
        borne_sup=(self.K_[len(self.K_)-1]*10)//1 - 1

        #plt.plot(pseudo_normalize(self.K),self.IV,color)
        #plt.plot(pseudo_normalize(self.K),self.IV_,color)
        plt.plot(self.K,self.IV)
        plt.plot(self.K_,self.IV_)
        X = [ i/10 for i in range (int(borne_inf),int(borne_sup))]
        Y = list()
        for x in X:
            Y.append( self.sigma.interpolated(x)  )
        plt.plot(X,Y,color)
        plt.xlabel('Strike')
        plt.ylabel('IV')
        plt.legend(['Avant traitement','Après traitement'])
        #plt.title("IV(K) "+ symbol)
        plt.show()
    
    def F(self,i,s=None,k=None,t=None,iv=None ,epsilon = 10**-11): #fonction de répartition du sous jacent
        if s == None:
            s = self.S0_[i]
        if t == None:
            t = self.T_[i]
        if k == None:
            k = self.K_[i]
        if iv == None:
            iv1 = self.sigma.interpolated(k-epsilon/2)
            iv2 = self.sigma.interpolated(k+epsilon/2)
        else:
            iv1,iv2 = iv,iv
        yk1 = BS.Call(s,t,k-epsilon/2,self.r,iv1)
        yk2 = BS.Call(s,t,k+epsilon/2,self.r,iv2)
        
        D = -  (yk2 - yk1)/epsilon

        if abs(D)>1 or D<0 : #petite correction
            D = 1
        return D






    def F_IV(self,s=0 ,epsilon = 10**-11): 
        i = 0
        while abs(self.S0_[i] - self.K_[i]) > 1:
            print(i)
            i+=1 
        D =  list()
        k = self.K[i]
        X = [self.sigma.interpolated(k)+i for i in range(0,100)]
        
        for x in X:
       
            yk1 = BS.Call(max(s,self.S0[i]),self.T[i],k-epsilon/2,self.r,self.sigma.interpolated(k-epsilon/2)+x)
            yk2 = BS.Call(max(s,self.S0[i]),self.T[i],k+epsilon/2,self.r,self.sigma.interpolated(k +epsilon/2)+x)
            D.append( - (yk2 - yk1)/epsilon )

        plt.scatter(X,D)
        plt.show()

    def dF_dK(self,i,epsilon = 10**-10):
        F1 = self.F(self.K[i]- epsilon/2,i)
        F2 = self.F(self.K[i]+ epsilon/2,i)
        
        D = (F2 - F1 )/epsilon
        return D



#AAPL = SYMBOL("AAPL")
AAPL = SYMBOL("AAPL",'v2',"aapl-options-4.csv",4,358.87)
#MSFT = SYMBOL("MSFT","msft-options-3.csv",3,202.98)
#TSLA.F_IV()
#AAPL.test_sensi_Call()
#AAPL.test_sensibilite_F()
#AAPL.plot_F()
#MSFT.plotting()

AAPL.plotting()