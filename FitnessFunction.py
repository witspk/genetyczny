import math

class FitnessFunction:
    a = -5.12
    b = 5.12

    def __init__(self):
        pass

    # DROP-WAVE FUNCTION
    def value(self, x, y):
        return -(1 + math.cos(12 * math.sqrt(pow(x, 2) + pow(y, 2)))) / (0.5 * (pow(x, 2) + pow(y, 2)) + 2)

    # test function
    # def value(self, x, y):
    #     return 2 * pow(x, 2) + 2 * pow(y, 2) + 5

    def changeAB(self, a, b):
        self.a = a
        self.b = b