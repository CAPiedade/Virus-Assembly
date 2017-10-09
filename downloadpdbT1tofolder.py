
import os
import sys
import urllib

os.mkdir("EstruturaspT3")

T1_IDs= open("ListpT3.txt",'r')

for line in T1_IDs.readlines():
    line = line.strip()
    line = line.split('\t')
    if line[0]!='n':
        print line[1]
        urllib.urlretrieve("http://www.rcsb.org/pdb/files/"+line[1].upper()+".pdb1.gz", line[1]+".pdb1.gz")
        os.system("gunzip < "+line[1]+".pdb1.gz >EstruturaspT3/"+line[1]+".pdb")
        os.system("rm -r "+line[1]+".pdb1.gz")

T1_IDs.close()
