
from populacja import Populacja



print("poczatek testu")
l = 200
epoki=[]
for x in range(l):
    if(x==0):
        epoki.append(Populacja(20))
    else:
        epoki.append(epoki[x-1].epoka())

epoki[0].print()
epoki[l-1].print()

#pop = Populacja(20)
# pop.print()
# print("selekcja")
# new_pop = pop.selekcja()
# new_pop.print()
# print("krzyzowanie")
# po_krzyzowaniu = new_pop.krzyzowanie()
# po_krzyzowaniu.print()
# print("mutacja")
# po_mutacji=po_krzyzowaniu.mutuj()
# po_mutacji.print()
# print("inversja")
# po_inversji=po_mutacji.inversja();
# po_inversji.print()

# o = Osobnik(25)
# print(o.asString())
# o2 = Osobnik(o)
# print(o2.asString())
# o=pop.findBest()
# d=o.decode(-10,10)
# print(o.asString()+":"+str(d)+":"+str(pop.f.value(d)))

# print("test 50 gen + decimal + dekodowanie")
# o = Osobnik(50)
# o.print()
# print(o.decimal())
# print(str(o.decode(-10, 10)))
# print("test 0100001000111111001001110 przeliczone na -4.82447727573")
# o2 = Osobnik("0100001000111111001001110");
# o2.print()
# print(str(o2.decode(-10, 10)))
# print("test kopiowania poprzedniego osobnika")
# o3 = Osobnik(o2)
# o3.print()
