from populacja import Populacja, ESelection, ECross, EMutation


def runner(dlugosc_chromo=20,
           wielkosc_populacji=10,
           liczba_epok=1000,
           rodzaj_selekcji=ESelection.BEST,
           rodzaj_krzyzowania=ECross.ONEPOINT,
           p_krzyzowania=0.8,
           rodzaj_mutacji=EMutation.ONEPOINT,
           p_mutacji=0.2,
           p_inversji=0.2,
           liczba_elitarnych=4):
    epoki = []
    for x in range(liczba_epok):
        if x == 0:
            epoki.append(Populacja(wielkosc_populacji, dlugosc_chromo))
        else:
            epoki.append(epoki[x - 1]
                         .nowa_epoka(rodzaj_selekcji,
                                     rodzaj_krzyzowania,
                                     p_krzyzowania,
                                     rodzaj_mutacji,
                                     p_mutacji,
                                     p_inversji,
                                     liczba_elitarnych))

    epoki[0].print()
    epoki[liczba_epok - 1].print()
