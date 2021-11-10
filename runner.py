from populacja import Populacja, ESelection, ECross, EMutation


def runner(dlugosc_chromo=100,
           wielkosc_populacji=1000,
           liczba_epok=100,
           rodzaj_selekcji=ESelection.BEST,
           parametr_selekcji=0.10,
           rodzaj_krzyzowania=ECross.ONEPOINT,
           p_krzyzowania=0.8,
           rodzaj_mutacji=EMutation.ONEPOINT,
           p_mutacji=0.5,
           p_inversji=0.5,
           liczba_elitarnych=10):
    epoki = []
    for x in range(liczba_epok):
        if x == 0:
            epoki.append(Populacja(wielkosc_populacji, dlugosc_chromo))
        else:
            epoki.append(epoki[x - 1]
                         .nowa_epoka(rodzaj_selekcji,
                                     parametr_selekcji,
                                     rodzaj_krzyzowania,
                                     p_krzyzowania,
                                     rodzaj_mutacji,
                                     p_mutacji,
                                     p_inversji,
                                     liczba_elitarnych))

    epoki[0].best_number(1).print()
    epoki[liczba_epok - 1].best_number(1).print()
