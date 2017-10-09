import os
from ast import literal_eval
from subgroups import subgroups_fromfile_generator, class2int
import itertools
import numpy as np

def read_dicfile(filename):

    dicfile = open(filename,'r')
    for line in dicfile.readlines():
        line = line.strip()
        line = line.split('\t')
        yield {literal_eval(line[0].strip()):literal_eval(line[1].strip())}

def dic_creator(filename,location='.'):
    os.chdir(location)
    energydic={}
    for dic_element in read_dicfile(filename):
        energydic.update(dic_element)
    return energydic

EnergyPoints={0:100,1:1,2:10}

def graphsymmetry_fromfile_generator(filename):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            line = literal_eval(line)
            yield line
    return


def energy_for_group_graphed(energydic,n):
    for subgroup in graphsymmetry_fromfile_generator('GraphSymmetryMathTest'+str(n)+'.txt'):

        energy = []
        classes =class2int(subgroup[-1])
        potencial = [0,0,0]
        for comb in itertools.combinations(subgroup[1],2):
            energy.append(energydic[comb])
        for E in energy:
            potencial[0]+=E[0]*EnergyPoints[0]
            potencial[1]+=E[1]*EnergyPoints[1]
            potencial[2]+=E[2]*EnergyPoints[2]
        if subgroup[2]==n:
            yield (classes,potencial, -sum(potencial), subgroup[0], subgroup[1])
        else:
            yield (classes,potencial, -sum(potencial), subgroup[0], subgroup[1],'X')








def test():

    os.chdir('EstruturasT1')
    for direct in os.listdir(os.curdir):
        if direct[-3:]!='pdb':
            os.chdir(direct)
            #try:
            D = dic_creator('dic_lig_'+direct+'.txt')
            os.chdir('../../')
            for Ener in energy_for_group_graphed(D,58):
                print direct
                print Ener
            os.chdir('EstruturasT1')

            break
            #except:
            #    os.chdir('..')
            #    continue


if __name__ == '__main__':
    test()
