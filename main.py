import matplotlib.pyplot as plt
import BS
import interpolation_spline3
import csv

file_name = None
#while file_name == None:  
symbol=input("sur quel symbol on travaille? : ")
file_name = "stocks-options_extracted_" + symbol + ".csv"




def recup():

    with open(file_name, newline='') as csvfile:
        IV_index, S0s_index,Ts,Ks = 0,0,0,0
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        IVs,S0s,Ts,Ks = list(),list(),list(),list()
        for row in spamreader:
            A = list((" , ".join(row)).split(","))

            if not(IV_index == 0) :

                IVs.append(A[IV_index])
                S0s.append(A[S0s_index])
                Ts.append(A[Ts_index])
                Ks.append(A[Ks_index])

            #NE SE FAIT QU'AU HEADER ===========
            else:
                while A[S0s_index] != 'Price':
                    S0_index += 1
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


plt.plot(IV,Calls)
plt.show()
#
#Put(S0,T,K,r,sigma)
#print(BS.Put(650.95 , 4/365 , 580,0,0.9725))



