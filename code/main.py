import matplotlib.pyplot as plt
import BS
import interpolation_spline3
import csv
from math import sqrt,exp

file_name = None
#while file_name == None:  
#symbol=input("sur quel symbol on travaille? : ")
symbol ='AMZN'
file_name = "stocks-options_extracted_" + symbol + ".csv"

def Pearson(x,y): #Retourne le coefficient de correlation de Pearson
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

def rearrange(x,y): 
    n = min ( len(x),len(y))
    return x[:n],y[:n]


def study(L):
    
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
    def __init__(self,symbol):
        self.symbol = symbol
        self.S0 , self.T , self.K , self.IV , self.Volumes = recup(self.symbol)
        self.r = 0.06 #OIS/USD
        
        self.K_,self.IV_ = TRI3(self.K,self.IV)
        i = 0
        while i <= len(self.K_)-2:
            while self.K_[i] == self.K_[i+1]:
                self.K_.pop(i)
                IV.pop(i)
            i += 1
        indexes = delete_indexes(self.Volumes,0.155,False)
        self.K_ = TRI2(self.K_,indexes)
        self.IV_ = TRI2(self.IV_,indexes)

        self.sigma = interpolation_spline3.Spline(self.K_,self.IV_) #Sigma est une fonction qui s'appelle par sigma.interpolated(k)

    def plot_F(self):
        X,Y,Y2 = list() , list() ,list()
        for i in range(len(self.K)):
            X.append(self.K[i])
            Y.append(self.F(self.K[i],i))
            Y2.append(exp(-1* self.r * self.T[i])*BS.N(BS.d2(self.S0[i],self.T[i],self.K[i],self.r,self.IV[i])))
        plt.scatter(X,Y,)
        plt.scatter(X,Y2,)
        plt.title(f'P (St >K)     {self.symbol}     ( k= {round(Pearson(Y,Y2),4)} )',   )
        plt.xlabel('Strike')
        plt.ylabel('Proba de finir dans la monnaie')
        plt.legend(['Par la fonction de repartition','Par N(d2)'])
        plt.show()

    def plotting(self,color = 'r'):
        borne_inf=(self.K_[0]*10)//1 + 1
        borne_sup=(self.K_[len(self.K_)-1]*10)//1 - 1


        #plt.plot(pseudo_normalize(self.K),self.IV,color)
        #plt.plot(pseudo_normalize(self.K),self.IV_,color)


        X = [ i/10 for i in range (int(borne_inf),int(borne_sup))]
        Y = list()
        for x in X:
            Y.append( self.sigma.interpolated(x)  )
        plt.plot(pseudo_normalize(X),Y,color)
        plt.xlabel('Strike')
        plt.ylabel('IV')
        #plt.title("IV(K) "+ symbol)
        #plt.show()
    
    def F(self,k,i,s=0 ,epsilon = 10**-11): #fonction de répartition du sous jacent
        #self.rs = 0.5
        #tau = self.T[i] - t
        yk1 = BS.Call(max(s,self.S0[i]),self.T[i],k-epsilon/2,self.r,self.sigma.interpolated(k-epsilon/2))
        yk2 = BS.Call(max(s,self.S0[i]),self.T[i],k+epsilon/2,self.r,self.sigma.interpolated(k +epsilon/2 ))
        
        D = -  (yk2 - yk1)/epsilon

        if abs(D)>1 or D<0 : #petite correction
            D = 1
        return D

    def dF_dK(self,i,epsilon = 10**-10):
        F1 = self.F(self.K[i]- epsilon/2,i)
        F2 = self.F(self.K[i]+ epsilon/2,i)
        
        D = (F2 - F1 )/epsilon
        return D

    def dF_div(self,i,epsilon = 10**-10):
        k = self.K[i]
        yk1 = BS.Call(self.S0[i],self.T[i],k-epsilon/2,self.r,self.sigma.interpolated(k-epsilon/2)-epsilon/2    )
        yk2 = BS.Call(self.S0[i],self.T[i],k+epsilon/2,self.r,self.sigma.interpolated(k +epsilon/2 )-epsilon/2     )
        F1 = -  (yk2 - yk1)/epsilon
        yk3 = BS.Call(self.S0[i],self.T[i],k-epsilon/2,self.r,self.sigma.interpolated(k-epsilon/2)+epsilon/2    )
        yk4 = BS.Call(self.S0[i],self.T[i],k+epsilon/2,self.r,self.sigma.interpolated(k +epsilon/2 )+epsilon/2     )
        F2 = -  (yk4 - yk3)/epsilon
        D = (F2 - F1 )/epsilon
        return D
        
    def dF_dT(self,i,epsilon = 10**-10):
        k = self.K[i]
        yk1 = BS.Call(self.S0[i],self.T[i]+epsilon/2,k-epsilon/2,self.r,self.sigma.interpolated(k-epsilon/2))
        yk2 = BS.Call(self.S0[i],self.T[i]+epsilon/2,k+epsilon/2,self.r,self.sigma.interpolated(k +epsilon/2 )) 
        F1 = -  (yk2 - yk1)/epsilon
        yk3 = BS.Call(self.S0[i],self.T[i]-epsilon/2,k-epsilon/2,self.r,self.sigma.interpolated(k-epsilon/2))
        yk4 = BS.Call(self.S0[i],self.T[i]-epsilon/2,k+epsilon/2,self.r,self.sigma.interpolated(k +epsilon/2 ))
        F2 = -  (yk3 - yk4)/epsilon
        D =   (F2 - F1)/epsilon
        return D


TSLA = SYMBOL("TSLA")
AMZN = SYMBOL("AMZN")
AAPL = SYMBOL("AAPL")



X,Y = list(), list()
for i in range(len(TSLA.K)):
    X.append(TSLA.K[i])
    Y.append(TSLA.dF_dT(i))

plt.scatter(X,Y)
plt.show()



print("=======================")


i = 5
print( AMZN.F(AMZN.K[i],i) )
#print(BS.Call(TSLA.S0[i],TSLA.T[i],TSLA.K[i],TSLA.r,TSLA.IV[i]))
print(exp(-1* AMZN.r * AMZN.T[i])*BS.N(BS.d2(AMZN.S0[i],AMZN.T[i],AMZN.K[i],AMZN.r,AMZN.IV[i]))) #P (St >K) = N(d2) probabilite de finir dans la monnaie
#print(exp(-1* AMZN.r * AMZN.T[i])*BS.N(BS.d1(AMZN.S0[i],AMZN.T[i],AMZN.K[i],AMZN.r,AMZN.IV[i])))
print("=======================")


#AMZN.plotting("r")
#TSLA.plotting("b")
#AAPL.plotting("g")
#plt.show()


    

S0,T,K,IV,Volumes = recup(symbol) 

###########################

indexes1 = delete_indexes(Volumes,0.155,False)

#K = TRI2(K,indexes1)
#IV = TRI2(IV,indexes1)
####################################




#####################################################
r = 0




K,IV = TRI(K,IV)

i = 0
while i <= len(K)-2:
    while K[i] == K[i+1]:
        K.pop(i)
        IV.pop(i)
    i += 1






plt.plot(K,IV,'b')
#plt.show()


############################################# Effectue la linéarisation par la dérivée.
X2,D = BS.derivee(K,IV)

indexes_a_supprimer = delete_indexes(D,1.6,True)


Liste_indexes = [i for i in range(len(D))]
Global_indexes = list()

for i in range (len(indexes_a_supprimer)):
    Global_indexes.append(Liste_indexes.pop(indexes_a_supprimer[i]-i))





while indexes_a_supprimer != []:

    K = TRI2(K,indexes_a_supprimer)
    IV = TRI2(IV,indexes_a_supprimer)
    D = TRI2(D,indexes_a_supprimer)
    indexes_a_supprimer = delete_indexes(D,1.6,True)

    for i in range (len(indexes_a_supprimer)):
        Global_indexes.append(Liste_indexes.pop(indexes_a_supprimer[i]-i))



###############################################
Global_indexes.sort()

Global_indexes , indexes1 = rearrange(Global_indexes,indexes1)





coef = Pearson(Global_indexes,indexes1)

#plt.scatter(Global_indexes,indexes1)
#plt.title("Coefficient de corrélation : r = " + str(coef))

#plt.show()

