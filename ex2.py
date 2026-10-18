from collections import deque
from itertools import combinations

cout = [[5, 3, 4],
        [6, 7, 2]]
stock = [8, 9]
demande = [4, 5, 8]

m, n = len(stock), len(demande)
assert sum(stock) == sum(demande)

def f(x):
    return sum(cout[i][j] * x[i][j] for i in range(m) for j in range(n))

def solution_initiale():
    s, d = stock[:], demande[:]
    x = [[0] * n for _ in range(m)]
    i = j = 0
    while i < m and j < n:
        q = min(s[i], d[j])
        x[i][j] = q
        s[i] -= q
        d[j] -= q
        if s[i] == 0:
            i += 1
        else:
            j += 1
    return x

def voisins(x):
    res = []
    for i1, i2 in combinations(range(m), 2):
        for j1, j2 in combinations(range(n), 2):
            if x[i1][j2] >= 1 and x[i2][j1] >= 1:
                y = [l[:] for l in x]
                y[i1][j1] += 1
                y[i2][j2] += 1
                y[i1][j2] -= 1
                y[i2][j1] -= 1
                res.append(y)
    return res

def cle(x):
    return tuple(tuple(l) for l in x)

def recherche_tabou(nb_iter=100, taille_tabou=7, stagnation_max=15):
    s = solution_initiale()
    best, f_best = s, f(s)
    tabou = deque(maxlen=taille_tabou)
    tabou.append(cle(s))
    stagnation = 0

    print(f"Solution initiale : {s}  coût = {f(s)}")
    for it in range(1, nb_iter + 1):
        candidats = [v for v in voisins(s) if cle(v) not in tabou or f(v) < f_best]
        if not candidats:
            break
        s = min(candidats, key=f)
        tabou.append(cle(s))

        if f(s) < f_best:
            best, f_best = s, f(s)
            stagnation = 0
        else:
            stagnation += 1

        print(f"Iter {it:3d} : coût courant = {f(s):3d} | meilleur = {f_best}")
        if stagnation >= stagnation_max:
            print("  -> stagnation, arrêt.")
            break

    return best, f_best


def verification_exacte():
    meilleur = [None]

    def rec(i, j, x, s, d):
        # Arrêt si on sort des limites de la matrice
        if i >= m or j >= n:
            return

        # Si on est sur la dernière cellule (en bas à droite)
        if i == m - 1 and j == n - 1:
            if s[i] == d[j]:  # Vérification de sécurité
                x[i][j] = s[i]
                if meilleur[0] is None or f(x) < f(meilleur[0]):
                    meilleur[0] = [l[:] for l in x]
            return

        # Le maximum qu'on peut allouer à cette cellule
        q = min(s[i], d[j])

        # Option 1 : On alloue le maximum (q)
        x[i][j] = q
        s[i] -= q
        d[j] -= q

        # On avance (ligne suivante si stock épuisé, sinon colonne suivante)
        if s[i] == 0:
            rec(i + 1, j, x, s, d)
        else:
            rec(i, j + 1, x, s, d)

        # On annule le choix (backtracking)
        s[i] += q
        d[j] += q
        x[i][j] = 0

        # Option 2 : On alloue 0 (seulement si on n'a pas déjà alloué 0)
        if q > 0:
            x[i][j] = 0
            if s[i] == 0:
                rec(i + 1, j, x, s, d)
            else:
                rec(i, j + 1, x, s, d)

    x = [[0] * n for _ in range(m)]
    rec(0, 0, x, stock[:], demande[:])

    if meilleur[0] is None:
        return None, None
    return meilleur[0], f(meilleur[0])

best, fb = recherche_tabou()

print("\nRésultat de la Recherche Tabou")
for i in range(m):
    for j in range(n):
        print(f"  D{i+1} -> M{j+1} : {best[i][j]} containers")
print("Coût total minimal trouvé par Tabou :", fb)

xopt, fopt = verification_exacte()
print("\n Vérification Exacte ")
print("Meilleure solution exacte :", xopt)
print("Coût exact minimal :", fopt)