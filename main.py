import matplotlib.pyplot as plt
import BS
import interpolation_spline3
import csv
from math import sqrt

file_name = None
#while file_name == None:  
#symbol=input("sur quel symbol on travaille? : ")
symbol ='AMZN'
file_name = "stocks-options_extracted_" + symbol + ".csv"



def derivee(X,Y): #derive la fonction Y = f(X)
    D , X2 = list() , list()
    for i in range(len(Y)-1):
        D.append((Y[i+1]-Y[i])/(X[i+1]-X[i]))
        X2.append( (X[i+1]+X[i])     /2     )
    return X2,D

def calcul_grecs(): #va appeler derivee et créant systématiquement des jeux de données en fct des gdeurs et en fixant les autres
    return None #attention a bien regarder toutes les combinaisons


def study(L):
    moy = sum(L) / len(L)

    M = list()
    for x in L:
        M.append((x-moy)**2)
    var = sum(M) / len(M)
    et = sqrt(var)
    return moy,et
    

def TRI(L,M):#trie la liste L et applique les même changement à la liste M
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
    



def TRI2(L,indexes): #retire les éléments d'indice dans indexes dans L
    k = 0
    for i in indexes:
        L.pop(i-k)
        k += 1
    return L






def recup():
    with open(file_name, newline='') as csvfile:
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
                Ts.append(float(A[Ts_index]))
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




    

S0,T,K,IV,Volumes = recup()

print(Volumes)




def delete_indexes(Volumes):
    moy,et = study(Volumes)
    indexes = list()
    for i in range(len(Volumes)):
        if not (    moy-et <  Volumes[i] < moy+et    ):
            indexes.append(i)

    return indexes


indexes = delete_indexes(Volumes)

K = TRI2(K,indexes)
IV = TRI2(IV,indexes)
            




r = 0
Calls = list()

for i in range(len(K)):
    Calls.append(BS.Call(S0[0],T[0]/365,K[i],r,IV[i]))

K,IV = TRI(K,IV)
i = 0
while i <= len(K)-2:
    while K[i] == K[i+1]:
        K.pop(i)
        IV.pop(i)
    i += 1


plt.plot(K,IV,'b')


splinned = interpolation_spline3.Spline(K,IV)

#print(Calls)
borne_inf=(K[0]*10)//1 + 1
borne_sup=(K[len(K)-1]*10)//1 - 1
#print("===================")
#print(borne_inf)
#print(borne_sup)
#print("===================")

X = [ i/10 for i in range (int(borne_inf),int(borne_sup))]
#print(X)
Y = list()
for x in X:
    Y.append( splinned.interpolated(x))   



plt.plot(X,Y,'r')
plt.xlabel('Strike')
plt.ylabel('IV')
plt.title("IV(K) "+ symbol)
plt.show()
#
#Put(S0,T,K,r,sigma)




