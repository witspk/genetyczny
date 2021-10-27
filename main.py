
from populacja import Populacja



print("poczatek testu")
l = 40
epoki=[]
for x in range(l):
    if(x==0):
        epoki.append(Populacja(100))
    else:
        epoki.append(epoki[x-1].epoka())

epoki[0].print()
epoki[l-1].print()
