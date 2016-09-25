PDB = '1lp3.pdb'
from ast import literal_eval
d ={}
Dicionario = open("1lp3/dic_lig_"+PDB[:-4]+".txt",'r')
for i in Dicionario.readlines():
    i = i.strip()
    i = i.split('\t')
    N = literal_eval(i[0])
    L = literal_eval(i[1].strip())
    d[N]=L

Dicionario.close()
s =0
h = 0
p = 0
#(saltbridges,hydrop,hbonds)

for i in d.keys():
    if i[0]==1 or i[1]==1:
        s+=d[i][0]
        h+=d[i][2]
        p+=d[i][1]

print s
print h
print p
