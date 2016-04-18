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
        os.rename("dic_lig_"+PDB[:-4]+".txt",PDB[:-4]+"/"+"dic_lig_"+PDB[:-4]+".txt")
        os.chdir(str(PDB[:-4]))
        L = model(PDB)
        for d in range(60*T/2):
            del_and_compare(d+1,L,ASU)
            os.chdir('Del'+str(d+1))
            for struct in os.listdir(os.curdir):
                s = 0
                h = 0
                p = 0
                modelsout = re.findall(r'\d+',struct)
                modelsout2 = []
                for element in modelsout:
                    modelsout2.append(int(element))
                for (i,j) in dicionario:
                    if i not in modelsout2 and j not in modelsout2:
                        s += dicionario[(i,j)][0]
                        p += dicionario[(i,j)][1]
                        h += dicionario[(i,j)][2]
                sasa = SASA(struct)
                Fich = open("Data"+struct[9:-4]+'.txt','w')
                print ("Salt Bridges:\t"+str(s),"Phobic Contacts:\t "+str(p),"HydrogenBonds:\t"+str(h), sep='\n' , file = Fich)
                for lines in sasa:
                    print (lines.strip(), file = Fich)
                Fich.close()
            os.system("rm Estrutura*")
            os.chdir('../Del'+str(60-d-1))
            for struct in os.listdir(os.curdir):
                s = 0
                h = 0
                p = 0
                modelsout = re.findall(r'\d+',struct)
                modelsout2 = []
                for element in modelsout:
                    modelsout2.append(int(element))
                for (i,j) in dicionario:
                    if i in modelsout2 and j in modelsout2:
                        s += dicionario[(i,j)][0]
                        p += dicionario[(i,j)][1]
                        h += dicionario[(i,j)][2]
                sasa = SASA(struct)
                Fich = open("Data"+struct[9:-4]+'.txt','w')
                print ("Salt Bridges:\t"+str(s),"Phobic Contacts:\t "+str(p),"HydrogenBonds:\t"+str(h), sep='\n' , file = Fich)
                for lines in sasa:
                    print (lines.strip(), file = Fich)
                Fich.close()
            os.system("rm Estrutura*")
            os.chdir('..')
        os.chdir('..')
