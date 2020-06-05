import csv
import sys
import BS

#print(sys.argv)
try:
    sys.argv.pop(0)
    nom_fichier = sys.argv.pop(0)

except:
    nom_fichier = None
    print("précisez un csv à lire")


symbol = sys.argv.pop(0)
choix = sys.argv.pop(0)




#a ce stade sys.argv est la liste des noms des elnts à extraire du csv. (1 symbole ou des colonnes)
indices = []



def ligne(symbol, choix = "both"):
    with open(nom_fichier, newline='') as csvfile:
        with open(nom_fichier[:len(nom_fichier)-4] +"_extracted_"+symbol+".csv", 'w', newline='') as newfile:

            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

            B = list()
            for row in spamreader:
                A = list((",".join(row)).split(","))
                
                
                #NE SE FAIT QU'AU HEADER ===========
                
                if B == []:
                    B = A + ["Delta","Gamma","Theta","Vega"] ############################
                    writer = csv.DictWriter(newfile, fieldnames=B)
                    writer.writeheader()
                #NE SE FAIT QU'AU HEADER ===========


                if choix == 'Both':
                    if A[0] == symbol  and A[5] == str(DTE) :
        
                        d=dict()
                        for j in range (len(A)):
                            d[B[j]] = A[j] 

                        n = len(A[13])
                        sigma =float(A[13][:n-1])/100

                        S0,T,K,r = float(A[1]) , float(A[5])/365 , float(A[3]) , 0 


                        if A[2] == "Call":
                            d[B[len(A)]]   = BS.delta_call(S0,T,K,r,sigma)    #
                            d[B[len(A)+2]] = BS.theta_call(S0,T,K,r,sigma)    #
                        else :
                            d[B[len(A)]]   = BS.delta_put(S0,T,K,r,sigma)    #
                            d[B[len(A)+2]] = BS.theta_put(S0,T,K,r,sigma) 
                        
                        d[B[len(A)+1]] = BS.gamma(S0,T,K,r,sigma)
                    
                        d[B[len(A)+3]] = BS.vega(S0,T,K,r,sigma)

                        writer.writerow(d)
                else :

                    if A[0] == symbol  and A[5] == str(DTE) and (A[2] == choix) :
            
                        d=dict()
                        for j in range (len(A)):
                            d[B[j]] = A[j] 





                            
                        #TOUT CA POUR RAJOUTER LES GREEKS
                        n = len(A[13])
                        sigma =float(A[13][:n-1])/100
                        S0,T,K,r = float(A[1]) , float(A[5])/365 , float(A[3]) , 0 
                        if A[2] == "Call":
                            d[B[len(A)]]   = BS.delta_call(S0,T,K,r,sigma)    #
                            d[B[len(A)+2]] = BS.theta_call(S0,T,K,r,sigma)    #
                        else :
                            d[B[len(A)]]   = BS.delta_put(S0,T,K,r,sigma)    #
                            d[B[len(A)+2]] = BS.theta_put(S0,T,K,r,sigma) 
                        d[B[len(A)+1]] = BS.gamma(S0,T,K,r,sigma)
                        d[B[len(A)+3]] = BS.vega(S0,T,K,r,sigma)



                        writer.writerow(d)



DTE = input('choisir la valeur du DTE: ')



if choix in {"Call",'Put','Both'}:
    ligne(symbol,choix)
else:
    print("Pas de type de produit précisé, par défaut : Both")
    ligne(symbol)
    

