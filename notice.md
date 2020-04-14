## Prise en main


# Parser:

Pour faire fonctionner le parser, vous devez placer le programme parser.py ansi que le csv dans un même dossier
Via le terminal, on se place dans ce dossier:
    cd "path"

on effectue alors la commande suivante:

    python parser.py "nom_fichier.csv" "Colonne 1" "Colonne 2" .. "Colonne n"

où "Colonne k" sont les noms des colonnes que l'on veut extraire 

Le parser crée alors un nouveau fichier csv "ancien_fichier"_extracted.csv contenant uniquement les colonnes voulues.

