import itertools
import numpy as np
from igraph import *
from subgroups import subgroups_fromfile_generator

g = Graph()
f = Graph()
G1 = Graph()
h= Graph()

f.add_vertices(61)

f.add_edges([(1,2),(1,5),(1,10),(1,23),(2,3),(2,22),(2,42),(3,41),(3,50),(3,4),(4,49),(4,34),(4,5),(5,6),(5,33),(6,10),(10,23),(23,22),(22,42),(42,41),(41,50),(50,49),(49,34),(34,33),(33,6),(7,6),(7,8),(7,57),(8,9),(8,55),(8,56),(9,10),(9,54),(9,24),(24,23),(24,54),(24,25),(25,53),(25,26),(25,21),(21,22),(21,30),(21,43),(43,42),(43,30),(43,44),(44,29),(44,14),(44,45),(45,41),(45,13),(46,45),(46,13),(46,50),(46,47),(47,12),(47,37),(47,48),(48,49),(48,36),(48,35),(35,36),(35,34),(35,31),(31,40),(31,58),(31,32),(32,7),(32,33),(32,57),(57,56),(56,55),(55,54),(54,53),(53,26),(26,30),(30,29),(29,14),(14,13),(13,12),(12,37),(37,36),(36,40),(40,58),(58,57),(16,20),(20,19),(19,18),(18,17),(17,16),(16,28),(16,15),(20,11),(20,38),(19,39),(19,59),(18,60),(18,51),(17,52),(17,27),(15,11),(11,38),(38,39),(39,59),(59,60),(60,51),(51,52),(52,27),(27,28),(28,15),(15,14),(11,12),(38,37),(39,40),(59,58),(60,56),(51,55),(52,53),(27,26),(28,29)])

f.delete_vertices(0)

#del a[0]
colordic= {1:'black',0:'white'}

def convertobjecttoarray(object_in):
    return np.asarray(list(object_in))

def graphsymmetry(r):
    Lista=[]
    for n in range(r):
        filename = "GroupsSymmetry"+str(n+1)+'.txt'
        for subgroup, n_subgroup in subgroups_fromfile_generator(filename, 60):
            
            f = Graph()
            f.add_vertices(61)
            f.add_edges([(1,2),(1,5),(1,10),(1,23),(2,3),(2,22),(2,42),(3,41),(3,50),(3,4),(4,49),(4,34),(4,5),(5,6),(5,33),(6,10),(10,23),(23,22),(22,42),(42,41),(41,50),(50,49),(49,34),(34,33),(33,6),(7,6),(7,8),(7,57),(8,9),(8,55),(8,56),(9,10),(9,54),(9,24),(24,23),(24,54),(24,25),(25,53),(25,26),(25,21),(21,22),(21,30),(21,43),(43,42),(43,30),(43,44),(44,29),(44,14),(44,45),(45,41),(45,13),(46,45),(46,13),(46,50),(46,47),(47,12),(47,37),(47,48),(48,49),(48,36),(48,35),(35,36),(35,34),(35,31),(31,40),(31,58),(31,32),(32,7),(32,33),(32,57),(57,56),(56,55),(55,54),(54,53),(53,26),(26,30),(30,29),(29,14),(14,13),(13,12),(12,37),(37,36),(36,40),(40,58),(58,57),(16,20),(20,19),(19,18),(18,17),(17,16),(16,28),(16,15),(20,11),(20,38),(19,39),(19,59),(18,60),(18,51),(17,52),(17,27),(15,11),(11,38),(38,39),(39,59),(59,60),(60,51),(51,52),(52,27),(27,28),(28,15),(15,14),(11,12),(38,37),(39,40),(59,58),(60,56),(51,55),(52,53),(27,26),(28,29)])
            f.delete_vertices(0)
            f.vs['number'] = range(1,61)
            
            deletelist = [i for i, bit in enumerate(subgroup) if bit == 0]

            f.delete_vertices(deletelist)

            if not f.is_connected():
                side = min(f.clusters(), key=len)
                templist = []
                for node in side:
                    for d in deletelist:
                        if node >= d:
                            node += 1
                    templist.append(node)

                deletelist2 = deletelist + templist

                f = None
                f = Graph()
                f.add_vertices(61)
                f.add_edges([(1,2),(1,5),(1,10),(1,23),(2,3),(2,22),(2,42),(3,41),(3,50),(3,4),(4,49),(4,34),(4,5),(5,6),(5,33),(6,10),(10,23),(23,22),(22,42),(42,41),(41,50),(50,49),(49,34),(34,33),(33,6),(7,6),(7,8),(7,57),(8,9),(8,55),(8,56),(9,10),(9,54),(9,24),(24,23),(24,54),(24,25),(25,53),(25,26),(25,21),(21,22),(21,30),(21,43),(43,42),(43,30),(43,44),(44,29),(44,14),(44,45),(45,41),(45,13),(46,45),(46,13),(46,50),(46,47),(47,12),(47,37),(47,48),(48,49),(48,36),(48,35),(35,36),(35,34),(35,31),(31,40),(31,58),(31,32),(32,7),(32,33),(32,57),(57,56),(56,55),(55,54),(54,53),(53,26),(26,30),(30,29),(29,14),(14,13),(13,12),(12,37),(37,36),(36,40),(40,58),(58,57),(16,20),(20,19),(19,18),(18,17),(17,16),(16,28),(16,15),(20,11),(20,38),(19,39),(19,59),(18,60),(18,51),(17,52),(17,27),(15,11),(11,38),(38,39),(39,59),(59,60),(60,51),(51,52),(52,27),(27,28),(28,15),(15,14),(11,12),(38,37),(39,40),(59,58),(60,56),(51,55),(52,53),(27,26),(28,29)])
                f.delete_vertices(0)
                f.vs['number'] = range(1,61)
                f.delete_vertices(sorted(deletelist2))
                Lista.append(tuple([n_subgroup, tuple(f.vs['number']),len(deletelist),tuple(sorted(deletelist)),tuple(sorted(deletelist2))]))

            else:
                Lista.append(tuple([n_subgroup,tuple(f.vs['number']),len(deletelist),tuple(sorted(deletelist)),tuple(sorted(deletelist))]))
            f = None
    return Lista

List = graphsymmetry(5)

print len(set(List))
dlist= {}

for i in List:
    dlist[i[-2]] = i[-1]

size = 0
Logical = True

ligacoes = {}

while Logical: # is this a "for size in 1, 2:"   ???
    size += 1
    values_size = [v for v in dlist.values() if len(v) == size]
    for v in values_size:
        for d in dlist.keys():
            if len(d) == size+1 and set(v).issubset(set(d)):
                if v not in ligacoes:
                    ligacoes[v]=[d]
                else:
                    ligacoes[v].append(d)
    if size > 1:
        Logical = False


G = Graph()

for el in sorted(ligacoes.keys()):
    try:
        indice1 = G.vs['label'].index(el)
        for lig in sorted(ligacoes[el]):
            try:
                indice2 = G.vs['label'].index(lig)

            except:
                G.add_vertices(1)
                G.vs['label'] = G.vs['label'][:-1] + [lig]
                indice2 = G.vs['label'].index(lig)

            G.add_edges([(indice1,indice2)])

    except:
        G.add_vertices(1)
        try:
            # G.vs['label'][-1] = el
            G.vs['label'] = G.vs['label'][:-1] + [el]

        except:
            G.vs['label']=[el]

        indice1 = G.vs['label'].index(el)
        for lig in sorted(ligacoes[el]):
            try:
                indice2 = G.vs['label'].index(lig)

            except:
                G.add_vertices(1)
                G.vs['label'] = G.vs['label'][:-1] + [lig]
                indice2 = G.vs['label'].index(lig)

            G.add_edges([(indice1,indice2)])
print(G)
plot(G, layout='rt', bbox = (8000,8000))
