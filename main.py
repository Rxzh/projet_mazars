import matplotlib.pyplot as plt
import BS
import interpolation_spline3
import csv

file_name = None
#while file_name == None:  
#symbol=input("sur quel symbol on travaille? : ")
symbol ='AMZN'
file_name = "stocks-options_extracted_" + symbol + ".csv"




def recup():

    with open(file_name, newline='') as csvfile:
        IV_index, S0s_index,Ts_index,Ks_index = 0,0,0,0
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        IVs,S0s,Ts,Ks = list(),list(),list(),list()
        for row in spamreader:
            A = list((",".join(row)).split(","))

            if not(IV_index == 0) :
                n = len(A[IV_index])
                sigma =float(A[IV_index][:n-1])/100  #pourcentages donc /100 
                
                IVs.append(sigma)
                S0s.append(float(A[S0s_index]))
                Ts.append(float(A[Ts_index]))
                Ks.append(float(A[Ks_index]))

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
            #NE SE FAIT QU'AU HEADER ===========
    return S0s,Ts,Ks,IVs



S0,T,K,IV = recup()
r = 0

Calls = list()

for i in range(len(S0)):
    Calls.append(BS.Call(S0[i],T[i]/365,K[i],r,IV[i]))

#on range les calls par ordre croissant
for k in range(1,len(Calls)): #cette partie est simplement un tri croissant de la liste Calls
        temp=Calls[k]
        temp2=IV[k]
        j=k
        while j>0 and temp<Calls[j-1]:
            Calls[j]=Calls[j-1]
            IV[j]=IV[j-1] #on y applique les memes changements sur la liste IV
            j-=1 
        Calls[j]=temp
        IV[j]=temp2   


plt.plot(Calls,IV,'b')


splinned = interpolation_spline3.Spline(Calls,IV)

print(Calls)
borne_inf=(Calls[0]*10)//1 + 1
borne_sup=(Calls[len(Calls)-1]*10)//1 - 1
print("===================")
print(borne_inf)
print(borne_sup)
print("===================")

X = [ i/10 for i in range (int(borne_inf),int(borne_sup))]
#print(X)
Y = list()
for x in X:
    Y.append( splinned.interpolated(x))   



plt.plot(X,Y,'r')
plt.xlabel('Prix des calls')
plt.ylabel('IV')
plt.title(symbol)
plt.show()
#
#Put(S0,T,K,r,sigma)




