from __future__ import print_function
from ast import literal_eval
import os
from graph_path import *
import pickle
from igraph import *
import subgroups as sbg
from datetime import datetime
os.chdir('DadosNovoArtigo')




Lista = []
append = Lista.append

for i in range(1,6):
    D = []
    F = open('1a34pdb_energy_gsym_'+str(i)+'.txt', 'r')
    for line in F.readlines():
        line = literal_eval(line.strip())
        if line[-1]!='X':
            deletedlist = protein_deleted(line[-1])
        else:
            deletedlist = protein_deleted(line[-2])
        D.append([tuple(deletedlist),line[3]])
    F.close()
    append(D)

dlig = new_dlig_creator(Lista)

with open('../dlig.pickle', 'w') as Files:
    pickle.dump([dlig], Files)

#exit()

with open('../dlig.pickle') as Files:
    dlig = pickle.load(Files)

G = graph_creator_new(dlig[0])

G.write_pickle(fname='../Graph.pickle')

#exit()


Gr = Graph.Read_Pickle(fname='../Graph.pickle')
Gr.to_directed(mutual=False)

Dic = graph_dic_index(Gr)


with open('../Index.pickle', 'w') as Files:
    pickle.dump([Dic], Files)

#exit()

with open('../dlig.pickle') as Files:
    dlig = pickle.load(Files)

with open('../Index.pickle') as Files:
    indexes = pickle.load(Files)

num = 0
size = len(dlig[0])
List_of_connections = []
append_to_List = List_of_connections.append
for toplig in dlig[0]:
    num += 1
    print size - num
    for bottomlig in dlig[0][toplig]:
        append_to_List((indexes[0][bottomlig],indexes[0][toplig]))

List_of_connections = list(set(List_of_connections))

with open('../List_of_connections.pickle', 'w') as Files:
    pickle.dump([List_of_connections], Files)

#exit()

with open('../List_of_connections.pickle') as Files:
    List_of_connections = pickle.load(Files)

Gr = Graph.Read_Pickle(fname='../Graph.pickle')
Gr.to_directed(mutual=False)
Gr.add_edges(List_of_connections[0])


Gr.write_pickle(fname='../Graph_connected.pickle')

#exit()


for pasta in os.listdir(os.curdir):
    os.chdir(pasta)
    for direct in os.listdir(os.curdir):
        if direct[-3:]=='dic':
            os.chdir(direct)
            print(direct)
            print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            Graphi = Graph.Read_Pickle(fname='../Graph_connected.pickle')


            D ={}
            for i in range(1,6):
                F = open(direct[:7]+'_energy_gsym_'+str(i)+'.txt', 'r')
                for line in F.readlines():
                    line = literal_eval(line.strip())
                    if line[-1]!='X':
                        deletedlist = protein_deleted(line[-1])
                    else:
                        deletedlist = protein_deleted(line[-2])
                    D[tuple(deletedlist)]=line[2]
                F.close()

            Weights = []
            wappend = Weights.append
            with open('../List_of_connections.pickle') as Files:
                List_of_connections = pickle.load(Files)

            num = 0
            size = (len(List_of_connections[0]))

            for conect in List_of_connections[0]:
                num += 1
                ID = Graphi.get_eid(conect[0],conect[1])
                Graphi.es[ID]['weight'] = float( D[Graphi.vs['label'][conect[0]]]/(60.0-len(Graphi.vs['label'][conect[0]])) - D[Graphi.vs['label'][conect[1]]]/(60.0-len(Graphi.vs['label'][conect[1]])))
                if num % 10000 == 0:
                    print (size-num)



            Graphi.write_pickle(fname='Graph_weighted.pickle')




            #Graphi = Graph.Read_Pickle(fname='Graph_weighted.pickle')

            with open('../Index.pickle') as Files:
                Indexes = pickle.load(Files)

            target = Graphi.vs['label'].index((1,))
            print(target)

            F = open('graph_path_dEdN.txt','w')
            for size in range(2,6):
                print(size)
                origin_list =[]
                origin_list_items=[]
                for index in Indexes[0]:
                    if len(index)==size:
                        origin_list.append(Indexes[0][index])
                        origin_list_items.append(index)

                SP = Graphi.shortest_paths_dijkstra(source=[target],target=origin_list, weights=Graphi.es['weight'], mode=IN)[0]

                sortedSP = sorted(SP)[:5]
                print(sortedSP, file=F)
                minindexes=list(set([i for i,e in enumerate(SP) if e in sortedSP]))
                for ind in minindexes:
                    print(origin_list_items[ind],SP[ind],sep='\t',file=F)
                continue


            F.close()
            del Graphi
            os.chdir('..')
            os.system('mv '+direct+' '+direct+'x')

    os.chdir('..')
