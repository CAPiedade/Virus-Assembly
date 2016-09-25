from __future__ import print_function
from EnergyCalc_fun import dic_creator, energy_for_group_graphed
import os
import sys


os.chdir('EstruturasT1')
for direct in os.listdir(os.curdir):
    if direct[-3:]!='pdb':
        os.chdir(direct)
        try:
            D = dic_creator('dic_lig_'+direct+'.txt')
            print (direct)
            os.chdir('../../')
            for i in range(54,61):
                f = open('EstruturasT1/'+direct+'/'+direct+'_energy_gsym_'+str(i)+'.txt','w')
                for Ener in energy_for_group_graphed(D,i):
                    print(Ener , file=f)
                f.close()
            for i in range(1,7):
                f = open('EstruturasT1/'+direct+'/'+direct+'_energy_gsym_'+str(i)+'.txt','w')
                for Ener in energy_for_group_graphed(D,i):
                    print(Ener , file=f)
                f.close()
            os.chdir('EstruturasT1')
            os.system('mv '+direct+' '+direct+'pdb')
        except:
            print(sys.exc_info())
            os.chdir('..')
            continue
