import csv
import sys


#print(sys.argv)
try:
    sys.argv.pop(0)
    nom_fichier = sys.argv.pop(0)

except:
    nom_fichier = None
    print("précisez un csv à lire")



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


def ligne():
    with open(nom_fichier, newline='') as csvfile:
        symbol = sys.argv.pop(0)
        with open(nom_fichier[:len(nom_fichier)-4] +"_extracted_"+symbol+".csv", 'w', newline='') as newfile:

            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            B = list()
            for row in spamreader:
                A = list((" , ".join(row)).split(","))


                #NE SE FAIT QU'AU HEADER ===========
                if B == []:
                    B = A
                    writer = csv.DictWriter(newfile, fieldnames=B)
                    writer.writeheader()
                #NE SE FAIT QU'AU HEADER ===========


                if A[0] == symbol:
                    d=dict()
                    for j in range (len(A)):
                        d[B[j]] = A[j] 
                    writer.writerow(d)



if choix == '-c':
    colonne()
elif choix == '-symbol':
    ligne()
else:
    print("Veuillez choisir -c ou -symbol selon ce que vous voulez garder")
