from boolean import *

#      0       1       2          3          4
# G = [[1, 2], [0, 3], [0, 3, 4], [1, 2, 4], [2, 3]]

def graphColouring2SAT(G, k):
    conj = []
    for i in range(len(G)):
        conj.append(Or(*((i, j) for j in range(k))))
        for j in range(k):
            for jj in range(j+1, k):
                conj.append(Or(Not((i, j)), Not((i, jj))))
        for h in G[i]:
            for j in range(k):
                conj.append(Or(Not((h, j)), Not((i, j))))
    return And(*conj)

def SAT2graphColouring(sol):
    d = {i: j for (i, j), v in sol.items() if v}
    out = [None] * len(d)
    for i, j in d.items():
        out[i] = j
    return out
