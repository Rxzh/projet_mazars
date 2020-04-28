import csv


nom_fichier = "stocks-options.csv"
k = 0
with open(nom_fichier, 'r', newline='') as newfile:
        spamreader = csv.reader(newfile, delimiter=',', quotechar='|')
        print(spamreader)
        for row in spamreader:
            
            A = list((" , ".join(row)).split(","))
            if k==0:
                print(A)
                k+=1
