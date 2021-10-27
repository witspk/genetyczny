import random

from osobnik import Osobnik
from FitnessFunction import FitnessFunction
from statistics import median


class Populacja:
    f = FitnessFunction()

    def __init__(self, *args):
        if (len(args) > 0):
            n = args[0]
            if (isinstance(n, int)):
                self.population = []
                for x in range(n):
                    self.population.append(Osobnik(50))
        else:
            self.population = []

    # wypisuje po pulacje na konsle do testów
    def print(self):
        print("Lp:Binarnie:Przeliczenie:Fitness")
        counter = 1;

        for x in self.population:
            d = x.decode(-10, 10, -10, 10)
            print(str(counter) + ":" + str(x.asString()) + ":" + str(d) + ":" + str(self.f.value(d[0], d[1])))
            counter = counter + 1

    # znajdownie najlepszego osobnika do stratgii elitarnej
    def findBest(self):
        r = 1000000
        for x in self.population:
            decoded = x.decode(-10, 10, -10, 10)
            v = self.f.value(decoded[0], decoded[1])
            if (v < r):
                r = v
                robj = x
        return Osobnik(robj)

    #znajdownie drugiego najlepszego osobnika do stratgii elitarnej
    def find2ndBest(self, best):
        if (isinstance(best, Osobnik)):
            r = 1000;
            for x in self.population:
                decoded = x.decode(-10, 10, -10, 10)
                v = self.f.value(decoded[0], decoded[1])
                if (v < r and x != best):
                    r = v
                    rx = x
            return rx
    #selekcja zwraca 50% najlepszych osobnikow
    def selekcja(self):
        # print("selekcja" + str(len(self.population)))
        przeliczone = []
        for x in range(len(self.population)):
            decoded = self.population[x].decode(-10, 10, -10, 10)
            przeliczone.append(self.f.value(decoded[0], decoded[1]))
        mediana = median(przeliczone)
        # print(mediana)
        new_pop = Populacja()
        mediany = []
        for x in range(len(self.population)):
            if przeliczone[x] < mediana:
                new_pop.dodaj(self.population[x])
            if przeliczone[x] == mediana:
                mediany.append(self.population[x])
        y = 0
        while (len(new_pop.population) < len(self.population) / 2):
            new_pop.dodaj(mediany[y])
            y = y + 1
        # new_pop.print()
        return new_pop

    #helper dodaje  osobnika do populacji
    def dodaj(self, n):
        if (isinstance(n, Osobnik)):
            self.population.append(n)

    #krzyżuje osobniki aż powstanie cała populacja bez 2 ze strateii elitarnej
    def krzyzowanie(self):
        # print("krzyzowanie" + str(len(self.population)))
        new_pop = Populacja()
        while (len(new_pop.population) < len(self.population) * 2 - 2 and len(self.population) != 0):
            # losowanie pary
            a = 0
            b = 0
            l = len(self.population)
            while (a == b and l != 0):
                a = random.randint(0, len(self.population) - 1)
                b = random.randint(0, len(self.population) - 1)
            # losowanie prawdopodobienstwa krzyżowania
            p = random.random()
            # losowanie miejsca krzyżowania
            m = random.randint(1, len(self.population[a].chromo) / 2 - 1)
            # krzyzowanie wylosowanych osobników
            if (p < 0.8):
                o1str = self.population[a].asString()
                o2str = self.population[b].asString()

                newstr1 = o1str[0][:m] + o2str[0][m:] + o2str[1][:m] + o1str[1][m:]
                newstr2 = o2str[0][:m] + o1str[0][m:] + o1str[1][:m] + o2str[1][m:]
                new1 = Osobnik(newstr1)
                new2 = Osobnik(newstr2)
                new_pop.dodaj(new1)
                new_pop.dodaj(new2)
        return new_pop

#mutoawanie punktowe
    def mutuj(self):
        new_pop = Populacja()
        for x in self.population:
            # losowanie prawdopodobienstwa
            p = random.random()
            # mutowanie
            if (p < 0.3):
                # losowanie punktu mutowania
                a = random.randint(0, len(x.chromo) - 1)
                o = Osobnik(x)
                if (o.chromo[a] == 1):
                    o.chromo[a] = 0
                else:
                    o.chromo[a] = 1
                new_pop.dodaj(o)
            else:
                new_pop.dodaj(x)
        return new_pop
#inversja
    def inversja(self):
        new_pop = Populacja()
        for x in self.population:
            # losowanie prawdopodobienstwa
            p = random.random()
            # inversja
            if (p <= 0.3):
                a = random.randint(0, len(x.chromo) - 3)
                if a <= len(x.chromo) / 2 - 2:
                    b = random.randint(a + 2, len(x.chromo) / 2)
                else:
                    b = random.randint(a + 2, len(x.chromo) - 1)  # TBD sprawdzic czy dobrze początek przedziału
                ostr = x.asString();
                ostr_concat = ostr[0] + ostr[1]
                reverse = ostr_concat[a:b]
                reverse = reverse[::-1]
                new_pop.dodaj(Osobnik(ostr_concat[:a] + reverse + ostr_concat[b:]))
            else:
                new_pop.dodaj(x)
        return new_pop

    def epoka(self):
        best = self.findBest()
        sec_best = self.find2ndBest(best)
        new_pop = self.selekcja().krzyzowanie().mutuj().inversja()
        new_pop.dodaj(best)
        new_pop.dodaj(sec_best)
        return new_pop
