from __future__ import print_function
from graph_path import *
from igraph import *
import os
from ast import literal_eval
import pickle

import itertools

os.chdir('EstruturasT1Modelo2')

"""
Lista = []
os.chdir('1a34pdbx')
#print(direct)
append = Lista.append
for i in range(1,5):
    D = {}
    F = open('1a34_energy_gsym_'+str(i)+'.txt', 'r')
    for line in F.readlines():
        line = literal_eval(line.strip())
        if line[-1]!='X':
            deletedlist = protein_deleted(line[-1])
        else:
            deletedlist = protein_deleted(line[-2])
        D[tuple(deletedlist)]=0
    F.close()
    append(D)

S= dlig_creator(Lista)
print (S)
exit()
with open('../dlig2.pickle', 'w') as Files:
    pickle.dump([S], Files)

os.chdir('..')

with open('dlig.pickle') as Files:
    dlig = pickle.load(Files)
direct = '1a34pdb'
os.chdir('1a34pdbx')
D ={}
for i in range(1,6):
    F = open(direct[:-3]+'_energy_gsym_'+str(i)+'.txt', 'r')
    for line in F.readlines():
        line = literal_eval(line.strip())
        if line[-1]!='X':
            deletedlist = protein_deleted(line[-1])
        else:
            deletedlist = protein_deleted(line[-2])
        D[tuple(deletedlist)]=line[2]
    F.close()

new_dlig={}
for i in dlig[0]:
    interm_list=[]
    append = interm_list.append
    for lig in dlig[0][i]:
        append((lig[0],D[lig[0]]))
    new_dlig[(i[0],D[i[0]])]=interm_list

G = graph_creator(new_dlig)

plot(G)
print(len(G.vs['label']))

G.write_pickle(fname='../Graph.pickle')


Gr = Graph.Read_Pickle(fname='Graph.pickle')
Gr.to_directed(mutual=False)

Dic = graph_dic_index(Gr)


with open('Index.pickle', 'w') as Files:
    pickle.dump([Dic], Files)


"""


for direct in os.listdir(os.curdir):
    Lista = []
    if direct[-4]!='.' and direct[-3:]=='pdb':
        os.chdir(direct)
        print(direct)
        D ={}
        for i in range(1,6):
            F = open(direct[:-3]+'_energy_gsym_'+str(i)+'.txt', 'r')
            for line in F.readlines():
                line = literal_eval(line.strip())
                if line[-1]!='X':
                    deletedlist = protein_deleted(line[-1])
                else:
                    deletedlist = protein_deleted(line[-2])
                D[tuple(deletedlist)]=line[2]
            F.close()



        with open('../dlig.pickle') as Files:
            dlig = pickle.load(Files)

        with open('../Index.pickle') as Files:
            IndexDic = pickle.load(Files)

        print ('Now here')
        Gr = Graph.Read_Pickle(fname='../Graph.pickle')
        Gr.to_directed(mutual=False)
        G = graph_w_energy(Gr, connections(dlig,D) , IndexDic[0])

        print ('And now here')
        F = open('graph_path_dEdN.txt','w')
        for size in range(2,6):
            target_list = [i for i in range(len(G.vs['label'])) if len(G.vs['label'][i])==size]
            target_list_items = [i for i in G.vs['label'] if len(i)==size]
            SP = G.shortest_paths(source=[0],target=target_list, weights=G.es['weight'], mode=OUT)[0]
            sortedSP = sorted(SP)[:5]
            print(sortedSP, file=F)
            minindexes=list(set([i for i,e in enumerate(SP) if e in sortedSP]))
            for ind in minindexes:
                print(target_list_items[ind],SP[ind],sep='\t',file=F)
        F.close()
        os.chdir('..')
        os.system('mv '+direct+' '+direct+'x')
