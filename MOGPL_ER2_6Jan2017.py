import matplotlib.pyplot as plt
import numpy as np

def T(j, L,ligne,sequence):
    """int x int x array(string) * array(int)-> bool
    j est l'indice de la position courante dans la ligne, l est l'indice du bloc
    retourne vrai s’il est possible de colorier les j + 1 premieres cases de la 
    ligne d'indice li avec la sous-sequence (s1, . . . , sl) des premiers blocs de la ligne li."""

    #cas 1                                      
    if (L==0):
        return "N" not in ligne[:j+1] 
        
    #if(j<0):
    #    return False
    #cas 2
    else:
        s=sequence[L-1]
        #cas 2a)
        if (j<s-1):
            return False
        #cas 2b)
        elif (j==s-1):
            if (L==1):
                return "B" not in ligne[:j+1]
            return False
        #cas 2c)
        else:
            
            if(ligne[j]=="B"): #si la case visitée est blanche
                return T(j-1, L,ligne,sequence)
            
            elif(ligne[j]=="N"): #si la case visité est noire
                # on souhaite que toutes les suivantes qui doivent appartenir au bloc ne soient pas blanche
                if "B" in ligne[j-s+1:j]:
                    return False
                   
                if (ligne[j-s]=="N"): 
                    return False
                return T(j-s-1, L-1,ligne,sequence)
            else:
                #si la case visitée n'a pas encore de couleur         
                for c in range (1,s): #on vérifie les suivantes (devant appartenir au bloc) ne sont pas blanche
                    if (ligne[j-c]=="B"): #si une case que l'on veut colorier est déjà assignée comme blanche
                        return "N" not in ligne[j-c+1:j]\
                        and T(j-c-1, L,ligne,sequence) #si une case es blanche on essaye de mettre le bloc plus loin
                if (ligne[j-s]=="N"):
                    return T(j-1, L,ligne,sequence)
                return T(j-s-1, L-1,ligne,sequence) or T(j-1, L,ligne,sequence)
           
# print(T(19, 1, \
#    ['N', '0', '0', '0', '0', '0', '0', '0', 'B', 'B', 'B', '0', '0', '0', '0', '0', 'B', 'B', 'B', 'B'],\
#    [2]))

BLACK, WHITE, IND = "N", "B", "0"

def coloration(A,sl,sc):

    lignesAVoir=set([i for i in range(len(A))])
    colonnesAVoir=set([i for i in range(len(A[0]))])
    while(len(lignesAVoir)!=0 or len(colonnesAVoir)!=0):
        print(A)
        nouveaux=set()
        j=len(A[0])-1
        for l in lignesAVoir:
            L=len(sl[l])       
            for c in range(len(A[l])):
                #if not(sl[l]):
                #    A[l][c]="B"
                if(A[l][c]=="0"):
                    A[l][c]="B"
                    blanc=T(j,L,A[l],sl[l])
                    A[l][c]="N"
                    noir=T(j,L,A[l],sl[l])
                    if(noir and blanc):
                        A[l][c]="0"
                    elif(blanc):
                        A[l][c]="B"
                    elif(noir):
                        A[l][c]="N"
                    else:
                        return False
                    nouveaux.add(c)
        lignesAVoir=set()
        colonnesAVoir.update(nouveaux)
        nouveaux=set()
        j=len(A)-1
        for c in colonnesAVoir:
            nouveaux=set()
            colonne=[]
            for i in range(len(A)):
                colonne.append(A[i][c])
            
            L=len(sc[c])
            for l in range(len(A)):
                #if not(sc[c]):
                #    A[l][c]="B"
                if(A[l][c]=="0"):
                    colonne[l]="B"
                    blanc=T(j,L,colonne,sc[c])
                    colonne[l]="N"
                    noir=T(j,L,colonne,sc[c])
                    if(noir and blanc):
                        A[l][c]="0"
                        colonne[l]="0"
                    elif(blanc):
                        A[l][c]="B"
                        colonne[l]="B"
                    elif(noir):
                        A[l][c]="N"
                        colonne[l]="N"
                    else:
                        print(colonne, sc[l], c, l)
                        return False
                nouveaux.add(l)
        colonnesAVoir=set()
        lignesAVoir.update(nouveaux)
    return np.array(A)
"""
BLACK, WHITE, IND = "N", "B", "0"
def coloration(A, seq_r, seq_c):
    grille = np.array(A)
    len_r, len_c = len(A), len(A[0])
    rows, cols = set(range(len_r)), set(range(len_c))
    while rows or cols:
        o = len(A[0])-1
        for i in rows:
            l = len(seq_r[i])
            tmp = list(grille[i])
            for j in range(len_c):
                if tmp[j] == IND:
                    tmp[j] = WHITE
                    blanc = T(o, l,tmp, seq_r[i])
                    tmp[j] = BLACK
                    noir = T(o, l,tmp, seq_r[i])
                    if blanc and noir:
                        tmp[j] = IND
                    else:
                        if blanc:
                            tmp[j] = WHITE
                        elif noir:
                            tmp[j] = BLACK
                        else:
                            return False
                    cols.add(j)
                    grille[i][j] = tmp[j]
        rows = set()
        o = len(A)-1
        for j in cols:
            l = len(seq_c[j])
            tmp = [grille[i][j] for i in range(len_r)]
            for i in range(len_r):

                if tmp[i] == IND:
                    tmp[i] = WHITE
                    blanc = T(o, l,tmp, seq_c[j])
                    tmp[i] = BLACK
                    noir = T(o, l,tmp, seq_c[j])
                    if blanc and noir:
                        tmp[i] = IND
                    else:
                        if blanc:
                            tmp[i] = WHITE
                        elif noir:
                            tmp[i] = BLACK
                        else:
                            return False
                    rows.add(i)
                    grille[i][j] = tmp[i]
        cols = set()
    return grille

"""
def propagation(fichier):
    """ fichier.txt -> array(array(string))
    fonction qui réalise la propagation permettant de remplir la grilles qui se trouve dans fichier """
    
    """    global table
    table = []
    #lecture du fichier et création des séquences de blocks
    f=open(fichier,'r')
    contenu=f.readlines()
    
    l=True
    sl=[] #séquence de block pour les lignes
    sc=[] #séquence de block pour les colonnes
    non_diese=True
    for ligne in contenu:
        tmp=[]
        non_diese=True
        for c in ligne:
            if(c=="#"):
                l=False
                non_diese=False
            elif( c!="\n" and c!=" " and c!="0"):
                tmp.append(int(c))
        if(l and non_diese):
            sl.append(tmp)
        elif(non_diese):
            sc.append(tmp)"""
    
    #initialisation de notre grille de réponses
    
    with open("instances/9.txt", "r") as f:
        file = f.read()
        lines = file.split("\n")
    sep = lines.index("#")
    # creation des listes de sequences
    sl, sc = [], []
    for sr in lines[:sep]:
        sl.append([int(i) for i in sr.split(" ") if i])
    for slc in lines[sep + 1:-1]:
        sc.append([int(j) for j in slc.split(" ") if j])

    A= []
    for i in range(len(sl)):
        tmp=[]
        for j in range(len(sc)):
            tmp.append("0")
        A.append(tmp)
    #print(A)
               
    #coloration de A            
    res2 = coloration(A,sl,sc)
    res = np.zeros(res2.shape)
    for i in range(len(res)):
        for j in range(len(res[1])):
            if res2[i][j] == "B":
                res[i][j] = -1
            elif res2[i][j] == "N":
                res[i][j] = 1
            else:
                res[i][j] = 0

    print(res)
    plt.imshow(res,interpolation='nearest')
    plt.show()

    return res

def affichage(Data):
    """affichage de la table"""
    for ligne in range(len(Data)):
        for i in range(len(Data[ligne])):
            if(Data[ligne][i]=="N"):
                Data[ligne][i]=-1
            elif(Data[ligne][i]=="B"):
                Data[ligne][i]=1
            else:
                Data[ligne][i]=0

    # plt.imshow(Data, cmap=plt.cm.gray, interpolation='nearest')
    plt.xticks(range(len(Data[0])),range(len(Data[0])))
    plt.yticks(range(len(Data))[::-1], range(len(Data))[::-1])

    return Data

print(propagation("instances/2.txt"))

# affichage(table)