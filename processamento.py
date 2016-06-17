from ast import literal_eval
import pickle
def processamento(Filename):
    File = open(Filename,'r')
    dic = {}
    for i in File.readlines():
        i = i.strip('\n')
        i = i.split('\t')
        try:
            i[0] = literal_eval(i[0])
            i[1] = literal_eval(i[1])
            dic[i[0]]=i[-1]
        except:
            continue
    size=0
    for i in dic.values():
        for j in dic.values():
            size+=1
    dic['size']=size
    return dic

Dic = {}
for i in range(1,6):
    D = processamento('GroupsSymmetry'+str(i)+'.txt')
    Dic[i]=D
    print i

print 'Done'
