# projet_mazars
Projet informatique pour Mazars - Mines ParisTech


Contact
Guillaume Chartier, Mazars


Il est proposé aux étudiants de développer un programme capable de calculer le prix d’un produit financier (option digitale) à partir de l’estimation de la densité de probabilité du sous-jacent.

CAHIER DES CHARGES :

    - Récupération, parsing (lecture) des quotations d’options vanilles
    - Développer un programme d’interpolation spline cubique
    - Implémenter la formule de Black-Scholes
    - Impliciter la fonction de répartition et de densité
    - Implémenter un pricer d’option digitale et de call (utilisant les fonctions de l’étape 3)
    - Mener des analyses de sensibilités et des tests(repricing des calls, rationalisation des écarts…)
    - Documentation de l’outil réaliser

BONUS :
    - Développement d’une autre méthode d’interpolation (cubique weighted).
    - Optimisation du code (qualité, performance etc…)
    - Développer en Python, un Scrapper automatique depuis la source de données


Détails des étapes techniques
1) Récupération et parsing des quotations d’options
Un jeu de données au format .csv sera fourni aux étudiants. Il contiendra des données de marché tel qu’observable sur le site https://www.barchart.com/options . Les étudiants développeront un parser, qui filtrera le fichier d’input pour en conserver seulement les données utiles. 


2) Développer un programme d’interpolation spline cubique
Les étudiants développeront une fonction capable de réaliser une interpolation spline cubique des volatilités implicites (rappel de la méthodologie voir https://fr.wikipedia.org/wiki/Spline#Spline_d%27interpolation).


3) Implémenter la formule de Black-Scholes
Les étudiants déterminent le prix des calls en implémentant la formule de Black-Scholes (fonction paramétrique de la volatilité implicite https://fr.wikipedia.org/wiki/Mod%C3%A8le_Black-Scholes#Formule_de_Black-Scholes ).


4) Impliciter la fonction de répartition
Les étudiants déterminent la fonction de répartition du sous-jacent à maturité à partir des volatilités implicites. La technique repose principalement par la discrétisation d’une dérivée partielle  (introduction à la méthode d’implicitation de la fonction de distribution d’un sous-jacent https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr677.pdf ).


5) Analyses de sensibilités et tests
Les étudiants finalisent le pricer d’option digitale à partir des développements des étapes précédentes et discutent de la qualité des résultats obtenus. En particulier, des analyses de sensibilités fournissent des ‘intervalles’ de validité des calculs (https://fr.wikipedia.org/wiki/Analyse_de_sensibilit%C3%A9#M%C3%A9thodologies ).