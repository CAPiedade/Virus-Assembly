from __future__ import print_function
from EnergyCalc_fun import dic_creator, energy_for_group_graphed
import os
import sys
from datetime import datetime

#CHANGE ON EnergyCalc_fun.py THE EnergyPoints { 0 : Energy Salt Bridges , 1 : Energy Hydrophobic Contacts, 2 : Energy Hydrogen Bonds}
#DIFFERENT HEURISTICS HAVE DIFFERENT ENERGY POINTS

for n in range(3,4):
    os.chdir('DadosNovoArtigo')
    os.chdir('EstruturasT1Modelo'+str(n))
    for direct in os.listdir(os.curdir):
        if direct[-3:]=='pdb':
            os.chdir(direct)
            try:
                D = dic_creator('dic_lig_'+direct[:4]+'.txt')
                print (direct)
                print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                os.chdir('../../../')
                for i in range(6,7):
                    f = open('DadosNovoArtigo/EstruturasT1Modelo'+str(n)+'/'+direct+'/'+direct+'_energy_gsym_'+str(i)+'.txt','w')
                    for Ener in energy_for_group_graphed(D,i):
                        print(Ener , file=f)
                    f.close()
                os.chdir('DadosNovoArtigo')
                os.chdir('EstruturasT1Modelo'+str(n))
                os.system('mv '+direct+' '+direct+'_dic')
            except:
                print(sys.exc_info())
                os.chdir('..')
                continue
    os.chdir('../../')
