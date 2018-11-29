# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 16:29:20 2017

@author: louis
"""

from gurobipy import *
import time
import matplotlib.pyplot as plt

def main(fichier):
    start = time.clock()
    for i in range(11):
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
    #print("sl",sl)
    #print("sc",sc)
    
    #initialisation de notre grille de réponses
    
    A= []
    for i in range(len(sl)):
        tmp=[]
        for j in range(len(sc)):
            tmp.append("0")
        A.append(tmp)
   
    gurobi(A, sl, sc, start, fichier)  
    
def affichage(tab_gu, N, M):
    res = []
    for i in range(N):
        tmp = []
        for j in range(M):
            tmp.append(tab_gu[i][j].x)
        res.append(tmp)
    plt.imshow(res, cmap='Greys', interpolation='nearest')
    plt.show()
    return 0

def gurobi(A, seqligne, seqcol, start, fichier):
   
    """
    A = [['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0']]
    seqligne = [[3], [], [1, 1, 1], [3]]
    seqcol = [[1, 1], [1], [1, 2], [1], [2]]
    """
    N = len(A)
    M = len(A[0])
    nbcont=(N+M)*3 
    nbvar=N*M
    #ligne
    for colonne in seqligne:
        nbvar += len(colonne)*M
    #colonne
    for ligne in seqcol:
        nbvar += len(ligne)*N
    
    # Matrice des contraintes
    a = []
    
    # Second membre
    b = []
    
    # Coefficients de la fonction objectif
    c = []
    
    m = Model("mogplex")     
            
    # declaration variables de decision
    x = []
    y = []
    z = []
    
    ###variables xij
    for i in range(N):
        tmp = []
        for j in range(M):
            tmp.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x[%d][%d]" % (i,j)))
            #x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x[%d,%d]" % (i,j)))
        x.append(tmp)
        
    ###variables yij^t
    for l in range(len(seqligne)):
        tmp1 = []
        for k in range(len(seqligne[l])):
            tmp2 = []  
            for j in range(M):
                tmp2.append(m.addVar(vtype=GRB.BINARY, lb=0, name="y[%d][%d][%d]" % (k,l,j) ))
                #y.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="y[%d,%d,%d]" % (l,j,k) ))
            tmp1.append(tmp2)
        y.append(tmp1)
        
    ###variables zij^t
    for c in range(len(seqcol)):
        tmp1 = []
        for k in range(len(seqcol[c])):
            tmp2 = []
            for i in range(N):
                tmp2.append(m.addVar(vtype=GRB.BINARY, lb=0, name="z[%d][%d][%d]" % (k,i,c) ))
            tmp1.append(tmp2)
        z.append(tmp1)
            
            
    # maj du modele pour integrer les nouvelles variables
    # fonction objectif, inutile ici
    m.update()
    
    obj = LinExpr();
    obj =0
    for i in range(N):
        for j in range(M):
            #print("x[i][j]",x[i][j])
            obj += x[i][j]
            
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    
    # Definition des contraintes  
    #si le t-ieme bloc de la ligne li commence `à la case (i, j), alors le (t + 1)ieme ne peut pas commencer avant la case (i, j + st + 1)
    compt=0
    for i in range(N) :
        for j in range(M):
            for t in range(0,len(seqligne[i])-1):
                #for k in range(j, j+seqligne[t]): # ou range( j, j+seqligne[t]-1)
                m.addConstr(y[i][t][j] + quicksum([y[i][t+1][k] for k in range(0, min(j+seqligne[i][t]+1,M))]) <= 1, "Contrainte%d" % compt)
                compt+=1
        #La somme de y[i][t] vaut 1 ou 0
        for t in range(len(seqligne[i])):
            m.addConstr(quicksum([y[i][t][k] for k in range(M)]) == 1)
            #Pour chaque ligne, le lième blocs ne peut pas commencer hors de l'intervalle Ligne[0 : sum(s[ 0 : l]) + l] ∪ ligne[sum(s[l : k]) + (k-l) : ]
            if j<(sum(seqligne[i][0:t])+t-seqligne[i][t]):
                m.addConstr(y[i][t][j]==0)
            if j>M-(sum(seqligne[i][t:len(seqligne[i])])-len(seqligne[i])+1+t):
                m.addConstr(y[i][t][j]==0)
            # si le t-ieme bloc de la ligne li commence `à la case (i, j), alors les cases (i, j) `à (i, j + st − 1) sont noires
            for j in range(M):
                m.addConstr(quicksum([x[i][k] for k in range(j, min(j+seqligne[i][t],M))]) >= (seqligne[i][t] * y[i][t][j]), "Contrainte%d" % compt)
                compt+=1
        #La somme des colonnes des x[i] vaut la somme des seqligne[i]
        m.addConstr(quicksum([x[i][j] for j in range(M)]) - quicksum(seqligne[i]) == 0)
                
    #si le t-ieme bloc de la colonne cj commence `à la case (i, j), alors le (t + 1)ieme ne peut pas commencer avant la case (i+ st + 1, j)
    compt=0
    for j in range(M) :
        for i in range(N):
            for t in range(0,len(seqcol[j])-1):
                #for k in range(j, j+seqligne[t]): # ou range( j, j+seqligne[t]-1)
                m.addConstr(z[j][t][i] + quicksum([z[j][t+1][k] for k in range(0, min(i+seqcol[j][t]+1,N))]) <= 1, "Contrainte%d" % compt)
                compt+=1
        #La somme des z[j][t] vaut 1 ou 0
        for t in range(len(seqcol[j])):
            m.addConstr(quicksum([z[j][t][k] for k in range(N)]) == 1)
            #Pour chaque colonne, le lième clocs ne peut pas commencer hors de l'intervalle Colonne[0 : sum(s[ 0 : l]) + l] ∪ Colonne[sum(s[l : k]) + (k-l) : ]                
            if i<sum(seqcol[j][0:t])+t-seqcol[j][t]:
                m.addConstr(z[j][t][i]==0)
            if i>N-sum(seqcol[j][t:len(seqcol[j])])-len(seqcol[j])+t+1: 
                m.addConstr(z[j][t][i]==0)
            # si le t-ieme bloc de la colonne cj commence `à la case (i, j), alors les cases (i, j) `à (i+ st − 1 , j) sont noires            
            for i in range(N):
                m.addConstr(quicksum([x[k][j] for k in range(i, min( i+seqcol[j][t], N))]) >= (seqcol[j][t] * z[j][t][i]), "Contrainte%d" % compt)
                compt+=1
        #La somme des ligne des x[:][j] vaut la somme des seqcol[j]
        m.addConstr(quicksum([x[i][j] for i in range(N)]) - quicksum(seqcol[j]) == 0)
                
    # Resolution
    m.optimize()
    
    end = time.clock() - start
    print(fichier+" fini, time=", end)  
    affichage(x, N, M)
    return x


for i in range(1,10):
    main("instances/"+str(i)+".txt")
#main("instances/13.txt")
    