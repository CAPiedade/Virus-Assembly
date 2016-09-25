
from funcoes import *
import itertools

def cluster(data, maxgap):
    '''Arrange data into groups where successive elements
       differ by no more than *maxgap*

        >>> cluster([1, 6, 9, 100, 102, 105, 109, 134, 139], maxgap=10)
        [[1, 6, 9], [100, 102, 105, 109], [134, 139]]

        >>> cluster([1, 6, 9, 99, 100, 102, 105, 134, 139, 141], maxgap=10)
        [[1, 6, 9], [99, 100, 102, 105], [134, 139, 141]]

    '''
    data.sort()
    groups = [[data[0]]]
    for x in data[1:]:
        if abs(x - groups[-1][-1]) <= maxgap:
            groups[-1].append(x)
        else:
            groups.append([x])
    return groups


m = model("1dnv.pdb1")

for i in m.keys():
    lista= []
    for line in m[i]:
        lista.append(create_Dict_Atom(line))
    m[i]=lista



for i in m.keys():
    center=Mass_Center(m[i])
    m[i]=center

d={}
for i in m:
    if i==1:
        for j in m:
            if i!=j:
                d[(i,j)]=vecdist(m[i],m[j],3)

for i in d:
    print i,'\t', d[i];

print cluster(d.values(),0.01)
