# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 14:56:36 2017

@author: louis
"""


### Question 1.1.4
import numpy as np
import matplotlib.pyplot as plt

s = [4, 2, 3, 1]
def T_old(j, L):
    """int x int -> bool
    j est l'indice de la position courante dans la ligne, l est l'indice du bloc
    retourne vrai s’il est possible de colorier les j + 1 premieres cases de la 
    ligne d'indice li avec la sous-sequence (s1, . . . , sl) des premiers blocs de la ligne li."""
                                             
    #cas 1                                      
    if (L==0):        
        return True
    #cas 2
    else:
        #cas 2a)
        if (j<s[L-1]-1):
            return False
        #cas 2b)
        elif (j==s[L-1]-1):
            if (L==1):
                return True
            else:
                return False
        #cas 2c)
        else:
            return T(j-s[L-1]-1, L-1)
 
            

### Question 1.2.6 
#"0" signifie, case pas encore remplie, 
#"N" signifie, case coloriée en noir, 
#"B" signifie, case coloriée en blanc

def T(j, L,ligne,sequence):
    """int x int x array(string) * array(int)-> bool
    j est l'indice de la position courante dans la ligne, l est l'indice du bloc
    retourne vrai s’il est possible de colorier les j + 1 premieres cases de la 
    ligne d'indice li avec la sous-sequence (s1, . . . , sl) des premiers blocs de la ligne li."""


    #cas 1                                      
    if (L==0):          
        return "N" not in ligne[:j+1]
    if(j<0):
        return False
        
    #cas 2
    else:
        s=sequence[L-1]
        #cas 2a)
        if (j<s-1):
            return False
            
        #cas 2b)
        elif (j==s-1):
            if (L==1):                              #si on veut placer le dernier bloc        
                return "B" not in ligne[:j+1]       #on verifie qu'il n'y a pas de case blanche dans la partie qu'on veux colorier en noir
            else:
                return False
                
        #cas 2c)
        else:
            if(ligne[j]=="B"):                      #si la case visitée est blanche
                return T(j-1, L,ligne,sequence)
                
            elif(ligne[j]=="N"):                    #si la case visité est noire
                # on souhaite que toutes les suivantes devant appartenir au bloc ne soient pas blanches
                if "B" in ligne[j-s+1:j+1]:
                    return False                
                if(L==1):                           #si on veut placer le dernier bloc
                    return "N" not in ligne[:j-s+1] # on verifie qu'il n'y a pas de cases noires en dehors de la zone du  bloc
                if (ligne[j-s]=="N"):               # si la case juste avant le bloc est noire 
                    return False
                return T(j-s-1, L-1,ligne,sequence)
                
            else:
                #si la case visitée n'a pas encore de couleur         
                for c in range (1,s):               #on vérifie les suivantes (devant appartenir au bloc) ne sont pas blanches
                    if (ligne[j-c]=="B"):           #si une case que l'on veut colorier est déjà assignée comme blanche
                       #on verifie qu'il n'y a pas de case noire entre la case visitée et la case blanche
                       return "N" not in ligne[j-c+1:j] and T(j-c-1, L,ligne,sequence)

                if (ligne[j-s]=="N"):               #si la case qui "sépare" les deux blocs est noire
                    return T(j-1, L,ligne,sequence)
                
                return  T(j-s-1, L-1,ligne,sequence) or T(j-1, L,ligne,sequence)
            


###Question 1.3.7
def coloration(A,sl,sc):

    lignesAVoir=set([i for i in range(len(A))])
    colonnesAVoir=set([i for i in range(len(A[0]))])
    k=0
    
    while((len(lignesAVoir)!=0 or len(colonnesAVoir)!=0) and k<33):
        
        k+=1
        nouveaux=set()
        for l in lignesAVoir:
            j=len(A[l])-1
            L=len(sl[l])
                       
            for c in range(len(A[l])):
                if not(sl[l]):
                    A[l][c]="B"
                if(A[l][c]=="0"):
                    A[l][c]="B"
                    blanc=T(j,L,A[l],sl[l])
                    A[l][c]="N"
                    noir=T(j,L,A[l],sl[l])
                    if(noir and blanc):
                        A[l][c]="0"
                    elif(noir):
                        A[l][c]="N"
                        nouveaux.add(c)
                    elif(blanc):
                        A[l][c]="B"
                        nouveaux.add(c)
                    else:
                        return False
                    nouveaux.add(c)
                    
        lignesAVoir=set()
        colonnesAVoir.update(nouveaux)

        nouveaux=set()
              
        for c in colonnesAVoir:
            nouveaux=set()
            colonne=[]
            for i in range(len(A)):
                colonne.append(A[i][c])
                
            j=len(A)-1
            L=len(sc[c])        
                    
            for l in range(len(A)):
                if not(sc[c]):
                    A[l][c]="B"
                if(A[l][c]=="0"):
                    colonne[l]="B"
                    blanc=T(j,L,colonne,sc[c])
                    colonne[l]="N"
                    noir=T(j,L,colonne,sc[c])
                    if(noir and blanc):
                        A[l][c]="0"
                        colonne[l]="0"
                    elif(noir):
                        A[l][c]="N"
                        colonne[l]="N"
                        nouveaux.add(l)
                    elif(blanc):
                        A[l][c]="B"
                        colonne[l]="B"
                        nouveaux.add(l)
                    else:
                        return False
                nouveaux.add(l)
                             
        colonnesAVoir=set()
        lignesAVoir.update(nouveaux)
        
    print("k",k)          
    return np.array(A)           
    

def propagation(fichier):
    """ fichier.txt -> array(array(string))
    fonction qui réalise la propagation permettant de remplir la grilles qui se trouve dans fichier """
    

    #lecture du fichier et création des séquences de blocks   
    with open(fichier, "r") as f:
        file = f.read()
        lines = file.split("\n")
    sep = lines.index("#")
    
    # creation des listes de sequences
    sl, sc = [], []
    for sr in lines[:sep]:
        sl.append([int(i) for i in sr.split(" ") if i])
    for slc in lines[sep + 1:-1]:
        sc.append([int(j) for j in slc.split(" ") if j])
    
    #initialisation de la grille de réponses
    A= []
    for i in range(len(sl)):
        tmp=[]
        for j in range(len(sc)):
            tmp.append("0")
        A.append(tmp)
               
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
    
    #affichage de la grille
    plt.imshow(res, cmap='Greys', interpolation='nearest')
    plt.show()
    return res

    
    
    
###Question 1.3.8    
import time
"""for i in range(0,11):
    start = time.clock()
    propagation("instances/"+str(i)+".txt")
    end = time.clock() - start
    print("instances "+str(i)+" fini, time=", end)
 
###Question 1.3.9    
start = time.clock()
propagation("instances/11.txt")
end = time.clock() - start
print("instances 11 fini, time=", end)


###Question 2.2.15
for i in range(7,9):
    start = time.clock()
    propagation("instances/"+str(i)+".txt")
    end = time.clock() - start
    print("instances "+str(i)+" fini, time=", end)
"""

start = time.clock()
propagation("instances/cloche.txt")
end = time.clock() - start
print("cloche.txt fini, time=", end)
    
    
###Question 1.2.6
###Tests de la fonction T()    
"""s = [4, 2, 3, 1]            
ligne1=["0","0","0","0","0","N","0"]
print("T(6, 2,ligne1,s) true",T(6, 2,ligne1,s))
ligne2=["0","0","0","0","N","0","0"]
print("T(6, 2,ligne2,s) false",T(6, 2,ligne2,s))
ligne3=["0","0","N","0","0","0","0"]
print("T(6, 2,ligne3,s) true",T(6, 2,ligne3,s))  
ligne4=["0","B","0","0","0","N","0"]
print("T(6, 2,ligne4,s) false",T(6, 2,ligne4,s))            
ligne5=["0","0","0","0","0","0","0","0","0","0","0","0","0"]
print("T(6, 2,ligne5,s) true",T(12, 4,ligne5,s))         
ligne6=["0","0","0","0","0","0","0","0","0","0","0","0","N"]
print("T(12, 4,ligne6,s) true",T(12, 4,ligne6,s))           
ligne7=["0","0","0","0","0","0","0","0","0","0","0","0","0","B","0","N"]
print("T(15, 4,ligne7,s) true",T(15, 4,ligne7,s)) 
ligne8=["0","0","0","0","0","0","0","0","0","0","0","0","B","B","0","N"]
print("T(15, 4,ligne8,s) true",T(15, 4,ligne8,s))
ligne9=["0","0","0","0","0","0","0","0","0","0","0","0","B","B","N","N"]
print("T(15, 4,ligne9,s) false",T(15, 4,ligne9,s))
s2=[3,1]
ligne10=["N","0","N","0","N"]
print("T(4, 1,lign10,s2) false",T(4, 1,ligne10,s2))
ligne11=["N","0","0","0","0"]
print("T(4, 1,lign11,s2) true",T(4, 1,ligne11,s2))
s3=[1,1]
ligne12=["B","B","0","0"]
print("T(3, 2,lign12,s3) false",T(3, 2,ligne12,s3))
s4=[2]
ligne13=["N","B","N","N"]
print("T(3, 1,ligne13,s3) false",T(3, 1,ligne13,s4))
s5=[3]
ligne14=["N","N","N","N","B"]
print("T(3, 1,ligne14,s3) false",T(4, 1,ligne14,s5))
s6=[1]
ligne15=["B","B","B","B"]
print("T(3, 1,ligne14,s3) false",T(3, 1,ligne15,s6))
ligne=['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'N', '0', '0', '0', 'N', 'N', 'N', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
s=[3, 3, 3, 1]
print("T(",len(ligne)-1,", ",len(s),",ligne,s) true",T(len(ligne)-1, len(s),ligne,s))
l=['0', 'N', 'N', 'N', 'N', 'N', 'N', '0', '0', 'N', 'N', 'N', '0', '0', '0', 'N', 'B', '0', '0', 'B']
s=[7, 4, 4]
print("T(",len(l)-1,", ",len(s),",ligne,s) true",T(len(l)-1, len(s),l,s))
l=['0', '0', '0', 'B', '0', '0', 'N', 'N', 'N', 'N', '0', '0', '0', 'N', '0', '0', 'B', 'N', 'N', 'B']
s=[1, 6, 3, 2]
print("T(",len(l)-1,", ",len(s),",ligne,s) true",T(len(l)-1, len(s),l,s))
l=["N","N","0","0","0","0","0"]
s=[1,2,1]
print("T(",len(l)-1,", ",len(s),",ligne,s) false",T(len(l)-1, len(s),l,s))
l=["N","0","0","0","0","0","0","N","0","N","0","0","N"]
s=[1,3,1]
print("T(",len(l)-1,", ",len(s),",ligne,s) true ",T(len(l)-1, len(s),l,s))
l=["B","N","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","N"]
s=[2,4]
print("T(",len(l)-1,", ",len(s),",ligne,s) true ",T(len(l)-1, len(s),l,s))
l=["N","0","0","0","0"]
s=[3]
print("T(",len(l)-1,", ",len(s),",ligne,s) true ",T(len(l)-1, len(s),l,s))
l=['B', '0', '0', '0', '0', 'N', '0', 'B', '0', '0', '0', '0', 'N', '0', '0', '0', '0', 'B', '0', '0']
s=[5, 1, 2]
print("T(",len(l)-1,", ",len(s),",ligne,s) true ",T(len(l)-1, len(s),l,s))"""