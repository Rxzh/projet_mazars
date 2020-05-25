import csv
import sys


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
def colonne():
    with open(nom_fichier, newline='') as csvfile:
        with open(nom_fichier[:len(nom_fichier)-4] + "_extracted.csv", 'w', newline='') as newfile:
            fieldnames = sys.argv
            writer = csv.DictWriter(newfile, fieldnames=fieldnames)
            writer.writeheader()
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                A = list((" , ".join(row)).split(","))
                #NE SE FAIT QU'AU HEADER ===========
                if indices == []:
                    B = A 
                    for i in range (len(A)-1,-1,-1):
                        if A[i] in sys.argv:
                            indices =  [i] + indices
                #NE SE FAIT QU'AU HEADER ===========
                else:
                    d = dict()
                    for j in indices:
                        d[B[j]] = A[j]
                    writer.writerow(d)


def ligne(symbol, choix = "both"):
    with open(nom_fichier, newline='') as csvfile:

        print(type(symbol))
        with open(nom_fichier[:len(nom_fichier)-4] +"_extracted_"+symbol+".csv", 'w', newline='') as newfile:

            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

            B = list()
            for row in spamreader:
                A = list((",".join(row)).split(","))
                
                
                #NE SE FAIT QU'AU HEADER ===========
                
                if B == []:
                    B = A
                    writer = csv.DictWriter(newfile, fieldnames=B)
                    writer.writeheader()
                #NE SE FAIT QU'AU HEADER ===========
                if choix == 'both':
                    if A[0] == symbol  and A[5] == str(DTE) :
        
                        d=dict()
                        for j in range (len(A)):
                            d[B[j]] = A[j] 
                        writer.writerow(d)
                else :

                    if A[0] == symbol  and A[5] == str(DTE) and (A[2] == choix) :
            
                        d=dict()
                        for j in range (len(A)):
                            d[B[j]] = A[j] 
                        writer.writerow(d)



DTE = input('choisir la valeur du DTE: ')



if choix in {"Call",'Put','Both'}:
    ligne(symbol,choix)
else:
    print("Pas de type de produit précisé, par défaut : Both")
    ligne(symbol)
    

