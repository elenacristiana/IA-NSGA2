import math

#VARIABLE GLOBALE
infinit = 999999999999999

#Selectia dupa rang
def selectie(valori1, valori2):
    S=[]
    n=[]
    rang=[]
    for i in range(0, len(valori1)):
        S.append([])
        n.append(0)
        rang.append(0)
    front_pareto = [[]]
    for x in range(0, len(valori1)):
        S[x] = []
        n[x] = 0
        for y in range(0, len(valori1)):
            # facem verificarile ca sa vedem care solutii sunt dominante/nedominante
            # Daca x domina y
            if (valori1[x] > valori1[y] and valori2[x] > valori2[y]) or (
                    valori1[x] >= valori1[y] and valori2[x] > valori2[y]) or (
                    valori1[x] > valori1[y] and valori2[x] >= valori2[y]):
                # anexam solutia gasita la lista noastra
                if y not in S[x]:
                    S[x].append(y)
            # Daca y domina x
            elif (valori1[y] > valori1[x] and valori2[y] > valori2[x]) or (
                    valori1[y] >= valori1[x] and valori2[y] > valori2[x]) or (
                    valori1[y] > valori1[x] and valori2[y] >= valori2[x]):
                # Se mareste numarul de fronturi pareto de care este dominat
                n[x] = n[x] + 1
        # Daca nu mai este dominat de niciun front, ci el le domina pe toate:
        if n[x] == 0:
            # rangul apartine primului front
            rang[x] = 0
            if x not in front_pareto[0]:
                front_pareto[0].append(x)

    # Initializam numarul de fronturi
    i = 0
    while (front_pareto[i] != []):
        # Q este folosit pentru a stoca lista de membri din frontul urmator
        Q = []
        for x in front_pareto[i]:
            for y in S[x]:
                n[y] = n[y] - 1
                # Daca nu mai este dominat de niciun front
                if (n[y] == 0):
                    # Rangul apartine front_paretoului urmator, adaugand in lista elementele necesare
                    rang[y] = i + 1
                    if y not in Q:
                        Q.append(y)
        i = i + 1
        front_pareto.append(Q)
    # se sterge ultimul element
    del front_pareto[len(front_pareto)-1]
    return front_pareto

# functie pentru sortarea elementelor
def sortare(lista1, valori):
    lista_sortata = []
    while (len(lista_sortata) != len(lista1)):
        if valori.index(min(valori)) in lista1:
            lista_sortata.append(valori.index(min(valori)))
        valori[valori.index(min(valori))] = infinit
    return lista_sortata


def distanta_aglomerare(valori1, valori2, front_pareto):
    distanta=[]
    for i in range(0, len(front_pareto)):
        distanta.append(0)

    # Sortarea in functie de fiecare functie obiectiv
    sortarea1 = sortare(front_pareto, valori1[:])
    sortarea2 = sortare(front_pareto, valori2[:])

    # Punctele extreme/limita vor fi mereu selectate
    distanta[0] = infinit
    distanta[len(front_pareto) - 1] = infinit

    # luam fiecare cromozom in parte
    for k in range(1, len(front_pareto) - 1):
        # calculam distanta de aglomerare ca fiind suma dintre distanta calculata pana in acel moment si
        # numitorul reprezinta diferenta dintre cel mai mare element si urmatorul cel mai mic
        distanta[k] = distanta[k] + (valori1[sortarea1[k + 1]] - valori2[sortarea1[k - 1]]) / (
                max(valori1) - min(valori1))
    for k in range(1, len(front_pareto) - 1):
        distanta[k] = distanta[k] + (valori1[sortarea2[k + 1]] - valori2[sortarea2[k - 1]]) / (
                max(valori2) - min(valori2))
    return distanta
