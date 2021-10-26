import random

from osobnik import Osobnik
from FitnessFunction import FitnessFunction
from statistics import median

class Populacja:
    f = FitnessFunction();

    def __init__(self, *args):
        if(len(args)>0):
            n = args[0]
            if(isinstance(n,int)):
                self.population = [];
                for x in range(n):
                    self.population.append(Osobnik(25))
        else:
            self.population = []

    def print(self):
        print("Lp:Binarnie:Przeliczenie:Fitness")
        counter = 1;

        for x in self.population:
            d = x.decode(-10,10)
            print(str(counter)+":"+x.asString()+":"+str(d)+":"+str(self.f.value(d)))
            counter=counter+1

    def findBest(self):
        r = 1000000;
        for x in self.population:
            v = self.f.value(x.decode(-10,10))
            if(v<r):
                r = v
                rstr=x.asString()
        return Osobnik(rstr)

    def find2ndBest(self, best):
        if(isinstance(best, Osobnik)):
            r = 1000;
            for x in self.population:
                v = self.f.value(x.decode(-10, 10))
                if (v < r and x!=best):
                    r = v
                    rx = x
            return rx

    def selekcja(self):
        przeliczone = []
        for x in range(len(self.population)):
            przeliczone.append(self.f.value(self.population[x].decode(-10, 10)))
        mediana = median(przeliczone)
        #print(mediana)
        new_pop = Populacja();
        for x in range(len(self.population)):
            if(przeliczone[x]<=mediana):
                new_pop.dodaj(self.population[x])
        return new_pop

    def dodaj(self, n):
        if(isinstance(n,Osobnik)):
            self.population.append(n)

    def krzyzowanie(self):
        new_pop = Populacja()
        while(len(new_pop.population)<18 and len(self.population)!=0):
            #losowanie pary
            a=0
            b=0
            l = len(self.population)
            while(a==b and l!=0):
                a = random.randint(0,len(self.population)-1)
                b = random.randint(0,len(self.population)-1)
            #losowanie prawdopodobienstwa krzyżowania
            p = random.random()
            #losowanie miejsca krzyżowania
            m = random.randint(0,len(self.population[a].chromo))
            #krzyzowanie wylosowanych osobników
            if(p<0.8):
                o1str = self.population[a].asString()
                o2str = self.population[b].asString()
                new1 = Osobnik(o1str[:m]+o2str[m:])
                new2 = Osobnik(o2str[:m]+o1str[m:])
                new_pop.dodaj(new1)
                new_pop.dodaj(new2)
            else:
                pass
                # print("p = "+str(p))
        return new_pop

    def mutuj(self):
        new_pop = Populacja()
        for x in self.population:
            #losowanie prawdopodobienstwa
            p = random.random()
            #mutowanie
            if(p<0.3):
                #losowanie punktu mutowania
                a = random.randint(0, len(self.population) - 1)
                o = Osobnik(x)
                if(o.chromo[a]==1):
                    o.chromo[a]=0
                else:
                    o.chromo[a]=1
                new_pop.dodaj(o)
            else:
                new_pop.dodaj(x)
        return new_pop

    def inversja(self):
        new_pop = Populacja()
        for x in self.population:
            #losowanie prawdopodobienstwa
            p = random.random()
            #inversja
            if(p<=0.3):
                a = random.randint(0, len(self.population) - 3)
                b = random.randint(a+2, len(self.population) - 1) # TBD sprawdzic czy dobrze początek przedziału
                ostr = x.asString();
                reverse = ostr[a:b]
                reverse = reverse[::-1]
                # print(ostr)
                # print("a:"+str(a)+" b:"+str(b)+" "+ostr[a:b]+" "+reverse)
                # print(ostr[:a]+reverse+ostr[b:])
                new_pop.dodaj(Osobnik(ostr[:a]+reverse+ostr[b:]))
            else:
                new_pop.dodaj(x)

        return new_pop

    def epoka(self):
        best = self.findBest()
        secBest = self.find2ndBest(best)
        new_pop = self.selekcja().krzyzowanie().mutuj().inversja()
        new_pop.dodaj(best)
        new_pop.dodaj(secBest)
        return new_pop