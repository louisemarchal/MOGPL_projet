# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 19:51:09 2017

@author: louis
"""

import matplotlib.pyplot as plt

Data = [['N','N','N','B'],
                  ['N','N','C','B'],
                  ['N','B','N','B'],
                  ['B','N','N','B'],
                  ['N','N','N','B']]

for ligne in range(len(Data)):
    for i in range(len(Data[ligne])):
        if(Data[ligne][i]=="N"):
            Data[ligne][i]=1
        elif(Data[ligne][i]=="B"):
            Data[ligne][i]=-1
        else:
            Data[ligne][i]=0

plt.imshow(Data, cmap=plt.cm.gray, interpolation='nearest')