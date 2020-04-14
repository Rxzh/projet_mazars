import csv
import sys



try:
    sys.argv.pop(0)
    nom_fichier = sys.argv.pop(0)

except:
    nom_fichier = None
    print("précisez un csv à lire")




#a ce stade sys.argv est la liste des noms des elnts à extraire du csv.
indices = []


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