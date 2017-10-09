from igraph import *
import os
from ast import literal_eval
import itertools


def protein_deleted(proteintuple):
    LIST = range(1,61)

    for prot in proteintuple:
        if prot in LIST:
            LIST.remove(prot)
    return LIST



def graph_creator(dlig):
    """Creates edges for each possibility of removing proteins from the capsid"""
    G = Graph()
    G.es['weight']=[]
    for el in sorted(dlig):
        G.add_vertices(1)
        try:
            G.vs['label'] = G.vs['label'][:-1] + [el[0]]
        except:
            G.vs['label']=[el[0]]
    for lig in list(set(list(itertools.chain.from_iterable([dlig[i] for i in dlig if len(i[0])==4])))):
        if lig not in G.vs['label']:
            G.add_vertices(1)
            G.vs['label'] = G.vs['label'][:-1] + [lig[0]]
    return G


def graph_dic_index( G ):
    dictorecturn = {}
    for ind in G.vs['label']:
        dictorecturn[ind]=G.vs['label'].index(ind)
    return dictorecturn


def graph_w_energy( G , connections, IndexDic):
    """Creates an energy weighted graph of the passages from one configuration to another"""
    prev = ()
    for L in connections:
        G[(IndexDic[L[0][0]],IndexDic[L[1][0]])] = float(L[1][1]/(60.0-len(L[1][0]))-L[0][1]/(60.0-len(L[0][0])))
    return G

def graph_w_energy_inv( G , connections):
    """Creates an energy weighted graph of the passages from one configuration to another"""
    prev = ()
    for L in connections:
        if prev==L[0][0]:
            indice2 = G.vs['label'].index(L[1][0])
            G[(indice2,indice1)] = float(L[1][1]/(60.0-len(L[1][0]))-L[0][1]/(60.0-len(L[0][0])))
        else:
            indice1 = G.vs['label'].index(L[0][0])
            indice2 = G.vs['label'].index(L[1][0])
            G[(indice2,indice1)] = float(L[0][1]/(60.0-len(L[0][0]))-L[1][1]/(60.0-len(L[1][0])))
        prev = L[0][0]
    return G

def connections(dlig, D):
    for i in dlig[0]:
        for lig in dlig[0][i]:
            yield [[i[0],D[i[0]]],[lig[0],D[lig[0]]]]

def merge(*iters):
    """Faster way to join two lists ???"""
    for it in iters:
        yield it


def dlig_creator(Lista):
    """Creates a dictionary that for each vertices (keys), has a list of the vertices it will connect (values)"""
    dlig={}
    for i in range(len(Lista)-1):
        for ele1 in Lista[i]:
            for ele2 in Lista[i+1]:
                if set(ele1).issubset(set(ele2)):
                    dlig.setdefault(tuple([ele1,Lista[i][ele1]]),[]).append(tuple([ele2,Lista[i+1][ele2]]))

    return dlig