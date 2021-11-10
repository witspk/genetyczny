import random
from enum import Enum
from math import ceil, floor

from osobnik import Osobnik
from FitnessFunction import FitnessFunction
import copy


class ESelection(Enum):
    BEST = 1
    ROULETTE = 2
    TOURNAMENT = 3


class ECross(Enum):
    ONEPOINT = 1
    TWOPOINT = 2
    TREEPOINT = 3
    HOMOGENOUS = 4


class EMutation(Enum):
    ONEPOINT = 1
    TWOPOINT = 2
    EDGE = 3


class Populacja:
    f = FitnessFunction()

    def __init__(self, *args):
        if len(args) > 0:
            n = args[0]
            if len(args) == 1:
                m = 25
            else:
                m = args[1]

            if isinstance(n, int) and isinstance(m, int):
                self.population = []
                for x in range(n):
                    self.population.append(Osobnik(m))
        else:
            self.population = []

    # wypisuje po pulacje na konsle do testów
    def print(self):
        print("Lp:Binarnie:Przeliczenie:Fitness")
        counter = 1

        for x in self.population:
            d = x.decode(self.f.a, self.f.b, self.f.a, self.f.b)
            print(str(counter) + ":" + str(x.asString()) + ":" + str(d) + ":" + str(self.f.value(d[0], d[1])))
            counter = counter + 1

    def selekcja(self, rodzaj_selekcji, parametr_selekcji):
        if rodzaj_selekcji == ESelection.BEST:
            return self.selkcja_best(parametr_selekcji)

        elif rodzaj_selekcji == ESelection.ROULETTE:
            return self.selekcja_kolem()
        elif rodzaj_selekcji == ESelection.TOURNAMENT:
            return self.selekcja_turniejowa(parametr_selekcji)
        else:
            pass

    # helper dodaje  osobnika do populacji
    def dodaj(self, n):
        if isinstance(n, Osobnik):
            self.population.append(n)

    # krzyżuje osobniki aż powstanie cała populacja bez tych ze strateii elitarnej
    def krzyzowanie(self, rodzaj_krzyzowania, p_krzyzowania, ilosc_po_krzyżowaniu):
        if rodzaj_krzyzowania == ECross.ONEPOINT:
            return self.krzyzowanie_one( p_krzyzowania, ilosc_po_krzyżowaniu)
        elif rodzaj_krzyzowania == ECross.TWOPOINT:
            return self.krzyzowanie_two( p_krzyzowania, ilosc_po_krzyżowaniu)
        elif rodzaj_krzyzowania == ECross.TREEPOINT:
            return self.krzyzowanie_three( p_krzyzowania, ilosc_po_krzyżowaniu)
        elif rodzaj_krzyzowania == ECross.HOMOGENOUS:
            return self.krzyzowanie_jednorodne (p_krzyzowania, ilosc_po_krzyżowaniu)
        else:
            pass

    def krzyzowanie_one(self, p_krzyzowania, ilosc_po_krzyżowaniu):
        # print("krzyzowanie" + str(len(self.population)))
        new_pop = Populacja()
        while len(new_pop.population) < ilosc_po_krzyżowaniu and len(self.population) != 0:
            # losowanie pary
            a = 0
            b = 0
            l = len(self.population)
            while a == b and l != 0:
                a = random.randint(0, len(self.population) - 1)
                b = random.randint(0, len(self.population) - 1)
            # losowanie prawdopodobienstwa krzyżowania
            p = random.random()
            # losowanie miejsca krzyżowania
            m = random.randint(1, len(self.population[a].chromo) // 2 - 1)
            # krzyzowanie wylosowanych osobników
            if (p < p_krzyzowania):
                o1str = self.population[a].asString()
                o2str = self.population[b].asString()

                newstr1 = o1str[0][:m] + o2str[0][m:] + o2str[1][:m] + o1str[1][m:]
                newstr2 = o2str[0][:m] + o1str[0][m:] + o1str[1][:m] + o2str[1][m:]
                new1 = Osobnik(newstr1)
                new2 = Osobnik(newstr2)
                new_pop.dodaj(new1)
                new_pop.dodaj(new2)
        return new_pop

    def mutuj(self, rodzaj_mutacji, p_mutacji):
        if rodzaj_mutacji == EMutation.ONEPOINT:
            return self.mutacja_one(p_mutacji)
        elif rodzaj_mutacji == EMutation.TWOPOINT:
            return self.mutacja_two(p_mutacji)
        elif rodzaj_mutacji == EMutation.EDGE:
            return self.mutacja_brzeg(p_mutacji)
        else:
            pass

    # mutoawanie punktowe
    def mutacja_one(self, p_mutacji):
        new_pop = Populacja()
        for x in self.population:
            # losowanie prawdopodobienstwa
            p = random.random()
            # mutowanie
            if (p < p_mutacji):
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

    # inversja
    def inversja(self, p_inversji):
        new_pop = Populacja()
        for x in self.population:
            # losowanie prawdopodobienstwa
            p = random.random()
            # inversja
            if (p <= p_inversji):
                a = random.randint(0, len(x.chromo) - 3)
                b = random.randint(a + 2, len(x.chromo))
                ostr = x.asString()
                ostr_concat = ostr[0] + ostr[1]
                reverse = ostr_concat[a:b]
                reverse = reverse[::-1]
                new_pop.dodaj(Osobnik(ostr_concat[:a] + reverse + ostr_concat[b:]))
            else:
                new_pop.dodaj(x)
        return new_pop

    def nowa_epoka(self, rodzaj_selekcji, parametr_selekcji, rodzaj_krzyzowania, p_krzyzowania, rodzaj_mutacji, p_mutacji, p_inversji,
                   liczba_elitarnych):
        best_pop = self.best_number(liczba_elitarnych)
        ilosc_elit = len(best_pop.population)
        wielkosc_populacji = len(self.population)
        ilosc_po_krzyżowaniu = wielkosc_populacji - ilosc_elit
        new_pop = self \
            .selekcja(rodzaj_selekcji, parametr_selekcji) \
            .krzyzowanie(rodzaj_krzyzowania, p_krzyzowania, ilosc_po_krzyżowaniu) \
            .mutuj(rodzaj_mutacji, p_mutacji) \
            .inversja(p_inversji)
        return new_pop + best_pop

    def findBest(self):
        r = 1000000
        for x in self.population:
            decoded = x.decode(self.f.a, self.f.b, self.f.a, self.f.b)
            v = self.f.value(decoded[0], decoded[1])
            if (v < r):
                r = v
            robj = x

        return Osobnik(robj)

    # zakładam, że dla obydwu zmiennych przedział jest ten sam.
    def best(self, param):
        new_pop = Populacja()
        ranking = []
        for i in range(len(self.population)):
            decoded = self.population[i].decode(self.f.a, self.f.b, self.f.a, self.f.b)
            ranking.append((i, self.f.value(decoded[0], decoded[1])))
        ranking.sort(key=lambda x: x[1])
        end = int(len(self.population) * param)
        for x in ranking[:end]:
            new_pop.dodaj(self.population[x[0]])
        return new_pop

    def __add__(self, other):
        new_pop = copy.deepcopy(self)
        new_pop.population.extend(other.population)
        return new_pop

    def best_number(self, param):
        new_pop = Populacja()
        ranking = []
        for i in range(len(self.population)):
            decoded = self.population[i].decode(self.f.a, self.f.b, self.f.a, self.f.b)
            ranking.append((i, self.f.value(decoded[0], decoded[1])))
        ranking.sort(key=lambda x: x[1])
        for x in ranking[:int(param)]:
            new_pop.dodaj(self.population[x[0]])
        return new_pop

    def selkcja_best(self, parametr_selekcji):
        return self.best(parametr_selekcji)

    def selekcja_kolem(self):
        new_pop = Populacja()
        przeliczone = []
        dystrybuantaSum = 0
        dystrybuanta = []

        # przelicznenie na decimal
        for x in range(len(self.population)):
            decoded = self.population[x].decode(self.f.a, self.f.b, self.f.a, self.f.b)
            przeliczone.append(self.f.value(decoded[0], decoded[1]))
        prawdopodobienstwo = []
        sumaOdwrotnosci = 0
        # Obliczamy sumę funkcji dopasowania wszystkich osobników
        for var in przeliczone:
            sumaOdwrotnosci = sumaOdwrotnosci + 1.00 / var
        # Obliczamy prawdopodobieństwo wyboru poszczególnych osobników
        prawdopodobienstwoSum = 0
        for var in przeliczone:
            prawdopodobienstwo.append((1 / var) / sumaOdwrotnosci)
            prawdopodobienstwoSum = prawdopodobienstwoSum + (1 / var) / sumaOdwrotnosci
        # Liczymy dystrubuante
        for var in prawdopodobienstwo:
            dystrybuanta.append(dystrybuantaSum + var)
            dystrybuantaSum = dystrybuantaSum + var
        # Teraz „kręcimy naszym kołem ruletki”. Losujemy liczby z zakresu [0,1].
        for i in range(0, floor(len(przeliczone) / 2)):
            wylosowana = random.random()
            roznicaNajmniejsza = 1

            for j in range(0, len(dystrybuanta) - 1):
                roznica = abs(abs(dystrybuanta[j]) - wylosowana)
                if (roznica < roznicaNajmniejsza):
                    roznicaNajmniejsza = roznica
                    dobranyOsobnik = j
            new_pop.dodaj(self.population[dobranyOsobnik+1])
        return new_pop

    def selekcja_turniejowa(self, k):
        new_pop = Populacja()
        group = []
        przeliczone = []
        for x in range(len(self.population)):
            decoded = self.population[x].decode(self.f.a, self.f.b, self.f.a, self.f.b)
            przeliczone.append(self.f.value(decoded[0], decoded[1]))

        indexList = list(range(len(self.population) - 1))
        for i in range(0, floor(len(przeliczone) / k)):
            if len(indexList) >= k:
                indexGroup = random.sample(indexList, k=int(k))
            else :
                indexGroup = indexList
            for var in indexGroup:
                group.append([var, przeliczone[var]])
                indexList.remove(var)
            groupWinner = min(group, key=lambda x: x[1])
            new_pop.dodaj(self.population[groupWinner[0]])
        return new_pop

    def krzyzowanie_two(self, p_krzyzowania, ilosc_po_krzyżowaniu):
        new_pop = Populacja()
        for i in range(0, len(self.population) - 1, 2):
            p = random.random()
            if p < p_krzyzowania:
                pointOfCut1 = random.randint(0, len(self.population[0].chromo) - 1);
                pointOfCut2 = random.randint(pointOfCut1, len(self.population[0].chromo) - 1);
                newOsobnik1 = Osobnik(self.population[i])
                newOsobnik2 = Osobnik(self.population[i + 1])
                osobnik1ValueHolder = Osobnik(self.population[i])

                for j in range(pointOfCut1, pointOfCut2):
                    newOsobnik1.chromo[j] = newOsobnik2.chromo[j]
                    newOsobnik2.chromo[j] = osobnik1ValueHolder.chromo[j]
                new_pop.dodaj(newOsobnik1)
                new_pop.dodaj(newOsobnik2)
            else:
                new_pop.dodaj(Osobnik(self.population[i]))
                new_pop.dodaj(Osobnik(self.population[i + 1]))

        new_pop.dodaj(Osobnik(self.population[len(self.population) - 1]))
        new_pop.dodaj(Osobnik(self.population[len(self.population) - 1]))
        return new_pop

    def krzyzowanie_three(self, p_krzyzowania, ilosc_po_krzyżowaniu):
        new_pop = Populacja()
        for i in range(0, len(self.population) - 1, 2):
            p = random.random()
            if p < p_krzyzowania:
                pointOfCut1 = random.randint(0, len(self.population[0].chromo) - 1)
                pointOfCut2 = random.randint(pointOfCut1, len(self.population[0].chromo) - 1)
                pointOfCut3 = random.randint(pointOfCut2, len(self.population[0].chromo) - 1)
                newOsobnik1 = Osobnik(self.population[i])
                newOsobnik2 = Osobnik(self.population[i + 1])
                osobnik1ValueHolder = Osobnik(self.population[i])

                for j in range(pointOfCut1, pointOfCut2):
                    newOsobnik1.chromo[j] = newOsobnik2.chromo[j]
                    newOsobnik2.chromo[j] = osobnik1ValueHolder.chromo[j]
                osobnik1ValueHolder = Osobnik(newOsobnik1)
                for z in range(pointOfCut3, len(self.population[0].chromo)):
                    newOsobnik1.chromo[z] = newOsobnik2.chromo[z]
                    newOsobnik2.chromo[z] = osobnik1ValueHolder.chromo[z]
                new_pop.dodaj(newOsobnik1)
                new_pop.dodaj(newOsobnik2)
            else:
                new_pop.dodaj(Osobnik(self.population[i]))
                new_pop.dodaj(Osobnik(self.population[i + 1]))

        new_pop.dodaj(Osobnik(self.population[len(self.population) - 1]))
        new_pop.dodaj(Osobnik(self.population[len(self.population) - 1]))
        return new_pop

    def krzyzowanie_jednorodne(self, p_krzyzowania, ilosc_po_krzyżowaniu):
        new_pop = Populacja()
        for i in range(0, len(self.population) - 1, 2):
            p = random.random()
            if p < p_krzyzowania:
                newOsobnik1 = Osobnik(self.population[i])
                newOsobnik2 = Osobnik(self.population[i + 1])
                osobnik1ValueHolder = Osobnik(self.population[i])

                for j in range(1, len(self.population[0].chromo)-1, 2):
                    newOsobnik1.chromo[j] = newOsobnik2.chromo[j]
                    newOsobnik2.chromo[j] = osobnik1ValueHolder.chromo[j]
                new_pop.dodaj(newOsobnik1)
                new_pop.dodaj(newOsobnik2)
            else:
                new_pop.dodaj(Osobnik(self.population[i]))
                new_pop.dodaj(Osobnik(self.population[i + 1]))

        new_pop.dodaj(Osobnik(self.population[len(self.population) - 1]))
        new_pop.dodaj(Osobnik(self.population[len(self.population) - 1]))
        return new_pop

    def mutacja_two(self, p_mutacji):
        new_pop = Populacja()
        for i in range(0, len(self.population)):
            p = random.random()
            if p < p_mutacji:
                pointOfMutation1 = random.randint(0, len(self.population[0].chromo)-2)
                pointOfMutation2 = random.randint(0, len(self.population[0].chromo)-1)
                while pointOfMutation2 == pointOfMutation1:
                    pointOfMutation2 = random.randint(0, len(self.population[0].chromo)-1)
                newOsobnik1 = Osobnik(self.population[i])

                newOsobnik1.chromo[pointOfMutation1]=1 if newOsobnik1.chromo[pointOfMutation1]==0 else 1
                newOsobnik1.chromo[pointOfMutation2]=1 if newOsobnik1.chromo[pointOfMutation2]==0 else 1
                new_pop.dodaj(newOsobnik1)
            else:
                new_pop.dodaj(Osobnik(self.population[i]))
        return new_pop

    def mutacja_brzeg(self, p_mutacji):
        new_pop = Populacja()
        for i in range(0, len(self.population)):
            p = random.random()
            if p < p_mutacji:
                newOsobnik1 = Osobnik(self.population[i])
                newOsobnik1.chromo[len(self.population)-1] = 1 if newOsobnik1.chromo[len(self.population)-1] == 0 else 1
                new_pop.dodaj(newOsobnik1)
            else:
                new_pop.dodaj(Osobnik(self.population[i]))
        return new_pop



