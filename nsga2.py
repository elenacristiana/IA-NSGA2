import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
import random
import numpy as np
import numpy as npy
from selectie import selectie
from selectie import distanta_aglomerare
from selectie import sortare
from crossover_mutatie import crossover_mutatie

# Functie pentru optimizarea pretului laptopului introdus de utilizator
def functie_pret_laptop(x):
    y = x**2;
    return y

def eval_fct_pret(dim_populatie,solutie):
    valori_pentru_pret = []
    for i in range(0, dim_populatie):
        val=functie_pret_laptop(solutie[i])
        valori_pentru_pret.append(val)
    return valori_pentru_pret

# Functie pentru optimizarea memoriei RAM introdusa de utilizator
def functie_rata_vanzari(x):
    y = (1+3*x)/x;
    return y

def eval_fct_rata(dim_populatie,solutie):
    valori_pentru_ram = []
    for i in range(0, dim_populatie):
        val=functie_rata_vanzari(solutie[i])
        valori_pentru_ram.append(val)
    return valori_pentru_ram

# Functie pt initializarea populatiei
def initializare_populatie(dim_pop,minim,maxim):
    solutie=[]
    for i in range(0, dim_pop):
        # Setam o valoare initiala intre minim si maxim
        val_init=minim + (maxim-minim) * random.random()
        solutie.append(val_init)
    return solutie

#  Afisarea frontului, adica a solutiilor celor mai optime pentru fiecare generatie
def afisare_front(solutie,rez_selectie,numarul_generatiei):
    print("Cel mai bun front pentru generatia ", numarul_generatiei, " este")
    for  r in rez_selectie[0]:
        print(round(solutie[r], 3), end=" ")
    print("\n")

# Functie pentru generarea valorilor din vectorul de distanta de aglomerare, in functie de valorile functiilor
def generare_valori_distanta_aglomerare(valori_pentru_pret,valori_pentru_ram,rez_selectie):
    valori_pentru_distanta_aglomerare = []
    for i in range(0, len(rez_selectie)):
        dist=distanta_aglomerare(valori_pentru_pret[:], valori_pentru_ram[:], rez_selectie[i][:])
        valori_pentru_distanta_aglomerare.append(dist)
    return valori_pentru_distanta_aglomerare

def main():
    # Citire valori initiale
    print("\nInitializare date pentru generarea algoritmului NSGA-II")
    print("\nDimensiunea populatiei:")
    dim = input()
    dim_populatie = int(dim);

    print("\nNumar maxim de indivizi:")
    ind = input()
    nr_max_indivizi = int(ind);

    # Initializarea minim-maxim a functiilor. Un cromozom are o gena (x) care poate lua valori in intervalul (-1, 1)
    min_x = -1
    max_x = 1

    # Generatia curenta
    numarul_generatiei = 0

    # Initialiarea populatiei
    solutie = initializare_populatie(dim_populatie, min_x, max_x)

    while (numarul_generatiei < nr_max_indivizi):
        # Evaluarea functiilor obiectiv
        valori_pentru_pret=eval_fct_pret(dim_populatie,solutie)
        valori_pentru_rata=eval_fct_rata(dim_populatie,solutie)

        # Selectia dupa rang
        rez_selectie = selectie(valori_pentru_pret[:], valori_pentru_rata[:])
        afisare_front(solutie,rez_selectie,numarul_generatiei)
        valori_pentru_distanta_aglomerare=generare_valori_distanta_aglomerare(valori_pentru_pret,valori_pentru_rata,rez_selectie)

        # Generarea copiilor
        solutie_noua = solutie[:]
        while (2 * dim_populatie != len(solutie_noua)):
            # Se executa incrucisarea si mutatia, iar rezultatul acesteia se pune in noua solutie
            cross_mut=crossover_mutatie(solutie[random.randint(0, dim_populatie - 1)], solutie[random.randint(0, dim_populatie - 1)])
            solutie_noua.append(cross_mut)

        # Evaluarea functiilor obiectiv pentru solutia copil
        valori_pentru_pret_2 = eval_fct_pret(2 * dim_populatie, solutie_noua)
        valori_pentru_rata_2 = eval_fct_rata(2 * dim_populatie, solutie_noua)

        # Selectia dupa rang
        rez_selectie_2 = selectie(valori_pentru_pret_2[:], valori_pentru_rata_2[:])

        # Calculam distanta de aglomerare dintre ceea ce s-a selectat in solutia noua
        valori_pentru_dist_aglomerare_2=generare_valori_distanta_aglomerare(valori_pentru_pret_2,valori_pentru_rata_2,rez_selectie_2)

        # Calcul solutie finala
        solutie_finala = []

        # Generarea frontului Pareto in urma sortarii solutiilor non-dominante, parcurgand matricea de elemente selectate
        sol_non_dominated=[]
        for i in range(0, len(rez_selectie_2)):
            for j in range(0, len(rez_selectie_2[i])):
                sol_non_dominated.append(rez_selectie_2[i].index(rez_selectie_2[i][j]))
            #Aici se sorteaza propriu zis, solutiile non-dominante in functie de lista de indecsi si crowding distance
            front22 = sortare(sol_non_dominated[:], valori_pentru_dist_aglomerare_2[i][:])
            for j in range(0, len(rez_selectie_2[i])):
                front = [rez_selectie_2[i][front22[j]]]
                for f in front:
                    solutie_finala.append(f)
                    if (len(solutie_finala) == dim_populatie):
                        break
            if (len(solutie_finala) == dim_populatie):
                break
        solutie = [solutie_noua[i] for i in solutie_finala]
        # trecem la generatia urmatoare
        numarul_generatiei = numarul_generatiei + 1

    # CONSTRUIREA GRAFICULUI PENTRU FUNCTIA PARETO CARE CUPRINDE STOCUL DE LAPTOPURI DIN MAGAZIN
    print("\nBuna ziua ! In stoc avem " + str(dim_populatie) + " de calculatoare. ")

    print("\nPretul maxim pe care doriti sa il aiba un laptop este ( euro ) :")
    cmd1 = input()
    var1 = int(cmd1);
    if var1 > 600:
        print("Cel mai scump laptop din magazin costa 600 euro ! Alegeti o valoare mai mica");
        print("Pretul maxim pe care doriti sa il aiba un laptop este ( euro ) :")
        cmd11 = input()
        var11 = int(cmd11)

    fig = figure()
    plt.title('Fiecare punct reprezinta un laptop. Alegeti laptopul dorit si vedeti rata vanzarii')

    functie1_v=[]
    for i in valori_pentru_pret:
        functie1_v.append(i*var1)

    functie2_v = []
    for j in valori_pentru_rata:
        functie2_v.append(j)

    plt.xlabel('Pretul produsului[euro]', fontsize=15)
    plt.ylabel('Rata de vanzari  ', fontsize=15)


    # plt.scatter(functie1, functie2)

    def onpick3(event):
        ind = event.ind
        print('\n Laptopul ales are urmatoarele caracteristici: id ', ind)
        ro = npy.take(functie1_v, ind)
        print('-pretul este: ', np.rint(ro), 'euro')
        ru = npy.take(functie2_v, ind)
        print('-Rata de vanzari este ', np.rint(ru))


    col = plt.scatter(functie1_v, functie2_v, picker=True)
    fig.canvas.mpl_connect('pick_event', onpick3)

    plt.show()

if __name__== "__main__":
  main()
