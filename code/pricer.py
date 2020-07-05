import sys
from main import SYMBOL




try:
    sys.argv.pop(0)
    symbol = sys.argv.pop(0)
    nom_fichier = sys.argv.pop(0)
    DTE = int(input('choisir la valeur du DTE (en jour): '))
    S0 = float(input('choisir la valeur actuelle du sous-jacent: '))
    #IV = float(input('choisir la valeur de la volatilité implicite: '))
    K = float(input('choisir la valeur du strike: '))


    Pricer = SYMBOL(symbol,'v2',nom_fichier,DTE,S0)
    proba=round(Pricer.F(s=S0,k=K,t=DTE/365),4)

    print(f'La probabilité que le sous-jacent dépasse le strike à maturité est : {proba}')

except:
    print("Entrez les paramètres suivants: 'SYMBOL' 'fichier.csv' ")









