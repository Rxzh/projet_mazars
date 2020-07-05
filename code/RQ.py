def TRI4(X,Y): #trie la liste X et applique les meme changements a toutes les listes de la liste Y
    L,M = X[:],Y[:]
    n = len(M)
    for k in range(1,len(L)): #cette partie est simplement un tri croissant de la liste Calls
        temp=L[k]
        temp2 = [M[i][k] for i in range(n)]
        j=k
        while j>0 and temp<L[j-1]:
            L[j]=L[j-1]
            for i in range(n):
                M[i][j]=M[i][j-1] #on y applique les memes changements sur la liste IV
            j-=1 
        L[j]=temp
        for i in range(n):
            M[i][j]=temp2[i]   
    return L,M


X = [ 0-i for i in range(10)]
a,b,c,d = X[:],X[:],X[:],X[:]
Y = [a,b,c,d]

L,M = TRI4(X,Y)

print(L)
print(M)