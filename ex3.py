import math
import random
from collections import deque
from itertools import permutations

random.seed(1)
INF = 1000

aretes = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13,
}


def d(a, b):
    return aretes.get((a, b), aretes.get((b, a), INF))


def f(tour):
    return sum(d(tour[k], tour[(k + 1) % len(tour)]) for k in range(len(tour)))


def echange(tour, i, j):
    t = tour[:]
    t[i], t[j] = t[j], t[i]
    return t


initiale = [1, 2, 3, 4, 5, 6, 7, 8]


def tabou(nb_iter=20, taille_tabou=4):
    s = initiale[:]
    best, f_best = s[:], f(s)
    liste_tabou = deque(maxlen=taille_tabou)
    print(f"[TABOU] départ : {s + [1]}  longueur = {f(s)}")
    for it in range(1, nb_iter + 1):
        meilleur_voisin, f_voisin, mouvement = None, float("inf"), None
        for i in range(1, len(s) - 1):
            for j in range(i + 1, len(s)):
                v = echange(s, i, j)
                mv = frozenset((s[i], s[j]))
                est_tabou = mv in liste_tabou
                if (not est_tabou or f(v) < f_best) and f(v) < f_voisin:
                    meilleur_voisin, f_voisin, mouvement = v, f(v), mv
        if meilleur_voisin is None:
            break
        s = meilleur_voisin
        liste_tabou.append(mouvement)
        if f(s) < f_best:
            best, f_best = s[:], f(s)
        print(f"  iter {it:2d} : échange {sorted(mouvement)}  -> {s + [1]}  L = {f(s)}  (best = {f_best})")
    return best, f_best


def recuit(nb_iter=5, T0=20.0, alpha=0.8, verbose=True):
    s = initiale[:]
    best, f_best = s[:], f(s)
    T = T0
    if verbose:
        print(f"[RECUIT] départ : {s + [1]}  longueur = {f(s)}  T0 = {T0}")
    for it in range(1, nb_iter + 1):
        i, j = random.sample(range(1, len(s)), 2)
        r = echange(s, i, j)
        delta = f(r) - f(s)
        p = 1.0 if delta < 0 else math.exp(-delta / T)
        u = random.random()
        accepte = u < p
        if accepte:
            s = r
            if f(s) < f_best:
                best, f_best = s[:], f(s)
        if verbose:
            print(f"  iter {it:2d} : T = {T:6.2f} | échange pos ({i},{j}) | delta = {delta:5d}"
                  f" | p = {p:.2f} | u = {u:.2f} | {'accepté' if accepte else 'refusé '}"
                  f" | L courant = {f(s)} | best = {f_best}")
        T *= alpha
    return best, f_best


def optimum_exact():
    meilleur = min(([1] + list(p) for p in permutations(range(2, 9))), key=f)
    return meilleur + [1], f(meilleur)


print("Longueur de la solution initiale :", f(initiale))
print("\nRECHERCHE TABOU ")
b, fb = tabou()
print("Meilleur circuit :", b + [1], "longueur =", fb)

print("\nRECUIT SIMULÉ")
b, fb = recuit(nb_iter=5, T0=20, alpha=0.8)
print("Meilleur circuit :", b + [1], "longueur =", fb)

print("\nRECUIT SIMULÉ")
b, fb = recuit(nb_iter=2000, T0=30, alpha=0.995, verbose=False)
print("Meilleur circuit :", b + [1], "longueur =", fb)

print("\nvérification :", optimum_exact())

