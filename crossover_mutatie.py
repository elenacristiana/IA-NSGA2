import math
import random
min_x = -1
max_x = 1

def crossover_mutatie(mama, tata):
    # aplicam incrucisarea reala, aritmetica + calculam probabilitatea de incrucisare
    r = random.random()
    # calculam probabilitatea de a returna mama / tatal
    if r > 0.5:
        probabilitate = random.random()
        # mutatia genei se produce doar daca probabilitatea este satisfacuta
        if probabilitate < 1:
            # resetam gena respectiva cu o noua valoare intre valorile minima si maxima
            mama = min_x + (max_x - min_x) * probabilitate
        return mama
    else:
        probabilitate = random.random()
        # mutatia genei se produce doar daca probabilitatea este satisfacuta
        if probabilitate < 1:
            # resetam gena respectiva cu o noua valoare intre valorile minima si maxima
            tata = min_x + (max_x - min_x) * probabilitate
        return tata
