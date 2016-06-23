 #-*- coding:latin1 -*-f
from __future__ import print_function
#from HydroBonds import *
from funcoes import *
import os
import itertools
#~ from calculate_rmsd import *
import numpy as np
from subprocess import call
import re




ASU = 1
T = 1
for PDB in os.listdir(os.curdir):
    if PDB[-3:]=='pdb':
        print(PDB)
        virus = parse_PDB(PDB)
        print(len(virus))
        os.mkdir(PDB[:-4])
        os.system("cp "+PDB+" "+PDB[:-4]+"/"+PDB)
        dicionario = calculate_number_bonds(virus)
        Dicionario = open("dic_lig_"+PDB[:-4]+".txt",'w')
        for i in dicionario:
            print (i,'\t',dicionario[i], file=Dicionario)
        Dicionario.close()
