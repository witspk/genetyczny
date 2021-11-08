from populacja import Populacja


def runner(dlugosc_chromo=20,
           wielkosc_populacji=10,
           liczba_epok=1000,
           rodzaj_selekcji="best",
           rodzaj_krzyzowania="jedno",
           p_krzyzowania=0.8,
           rodzaj_mutacji="jedno",
           p_mutacji=0.2,
           p_inversji=0.2,
           procent_elitarnych=0.1):
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
                                     procent_elitarnych))

    epoki[0].print()
    epoki[liczba_epok - 1].print()
