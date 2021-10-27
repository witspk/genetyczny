from random import randint
import copy


class Osobnik:
    # konstruktor int + str + kopia
    def __init__(self, n):
        if isinstance(n, int):
            self.chromo = []
            for x in range(n * 2):
                self.chromo.append(randint(0, 1))
        if isinstance(n, str):
            self.chromo = []
            for x in range(len(n)):
                self.chromo.append(int(n[x]))
        if isinstance(n, Osobnik):
            self.chromo = copy.deepcopy(n.chromo)

    # wypisuje na konsole, na razie do testów
    def print(self):
        print(self.asString())

    # obliczanie decimal zgodnie ze wykładem
    def decimal(self):
        decimal_str = self.asString()
        return [int(decimal_str[0], 2), int(decimal_str[1], 2)]

    # zwraca chromosom w postaci listy 2 string
    def asString(self):
        r1 = ""
        r2 = ""
        chromo_len = int(len(self.chromo) / 2)
        for x in range(chromo_len):
            r1 = r1 + str(self.chromo[x])
            r2 = r2 + str(self.chromo[x + chromo_len])
        return [r1, r2]

    # dekodowanie zgodnie z wykładem zwraca tablice float
    def decode(self, a1, b1, a2, b2):
        chromo_len = len(self.chromo) / 2
        decimal = self.decimal()
        decoded1 = a1 + decimal[0] * (b1 - a1) / ((pow(2, chromo_len)) - 1)
        decoded2 = a2 + decimal[1] * (b2 - a2) / ((pow(2, chromo_len)) - 1)
        return [decoded1, decoded2]
