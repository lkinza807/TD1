import random


def selection_roulette(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    tirage = random.uniform(0, total_fitness)

    somme_cumulee = 0
    for i in range(len(population)):
        somme_cumulee += fitness_scores[i]
        if somme_cumulee >= tirage:
            return population[i]

    return population[-1]


population = ["Individu A", "Individu B", "Individu C"]
fitness_scores = [50, 30, 20]

resultats = [selection_roulette(population, fitness_scores) for _ in range(10)]
print("Résultats des 10 sélections :", resultats)