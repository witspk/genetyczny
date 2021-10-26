from random import randint
import copy

class Osobnik:
#konstruktor int + str + kopia
    def __init__(self, n):
        if (isinstance(n,int)):
            self.chromo = []
            for x in range(n):
                self.chromo.append(randint(0, 1))
        if (isinstance(n,str)):
            self.chromo = []
            for x in range(len(n)):
                self.chromo.append(int(n[x]))
        if(isinstance(n,Osobnik)):
            self.chromo = copy.deepcopy(n.chromo)

#wypisuje na konsole, na razie do testów
    def print(self):
        print(self.asString())   

#obliczanie decimal zgodnie ze wykładem
    def decimal(self):
        return int(self.asString(),2)

#zwraca chromosom w postaci string
    def asString(self):
        r =""
        for x in self.chromo:
            r=r+str(x)
        return r

#dekodowanie zgodnie z wykładem
    def decode(self, a, b):
        return a+self.decimal()*(b-a)/(pow(2,len(self.chromo)))


