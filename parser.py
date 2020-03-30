import csv
import sys



try:
    nom_fichier = sys.argv[1]

except:
    nom_fichier = None
    print("précisez un csv à lire")

nom_fichier = "Appearances.csv"


with open(nom_fichier, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    print(spamreader)
    for row in spamreader:
        print(list((" , ".join(row)).split(",")))



