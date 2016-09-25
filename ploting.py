
f = "significanceClaudio.txt"

f = open(f,'r')
p = {}

for i in f.readlines():
    i.strip()

    i = i.split()
    if i[0]=='H-W':
        p[float(i[1])]=float(i[9])


import matplotlib.pyplot as plt

x = sorted(p.keys())
y = []
for i in x:
    y.append(p[i])

plt.plot(x,y)
plt.ylim(ymax=0.1,ymin=0)
plt.show()
