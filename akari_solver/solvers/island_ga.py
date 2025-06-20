"""
Island Genetic Algorithm – wyspowy algorytm genetyczny

Zasada działania:
- Tworzymy wiele niezależnych populacji (wysp), które ewoluują osobno.
- Co kilka generacji migrujemy część osobników między wyspami.
- Pozwala to uniknąć lokalnych minimów i zwiększyć różnorodność.
- Na końcu wybieramy najlepsze rozwiązanie ze wszystkich wysp.
"""

# Import modułu random – do selekcji, krzyżowania i migracji
import random

# Import typów do list rozwiązań
from typing import List

# Import deepcopy – do kopiowania osobników przy migracji
from copy import deepcopy

# Import planszy i rozwiązań
from core.board import Board
from core.solution import Solution

# Import funkcji crossover i mutate z genetic.py
from solvers.genetic import crossover_one_point, mutate


# Funkcja główna algorytmu wyspowego
def island_genetic_solver(
    board: Board,
    population_size: int = 30,        # Liczba osobników na jednej wyspie
    generations: int = 100,           # Liczba generacji
    mutation_rate: float = 0.1,       # Prawdopodobieństwo mutacji
    elite_size: int = 1,              # Liczba elit zachowywanych bez zmian
    num_islands: int = 4,             # Liczba wysp
    migration_interval: int = 10,     # Co ile generacji migrują osobniki
    migrants_per_island: int = 2      # Ilu migrantów przekazujemy między wyspami
) -> Board:

    islands: List[List[Solution]] = []  # Lista wszystkich wysp = lista populacji

    # Inicjalizacja każdej wyspy – losowa populacja
    for _ in range(num_islands):
        population = []
        for _ in range(population_size):
            sol = Solution(board)       # Nowe rozwiązanie
            sol.random_solution()       # Losowe rozmieszczenie lamp
            population.append(sol)      # Dodanie do populacji
        islands.append(population)      # Dodanie wyspy do listy

    # Pętla główna ewolucji – przez określoną liczbę generacji
    for gen in range(generations):
        for i in range(num_islands):
            pop = islands[i]                         # Bierzemy populację z wyspy i
            pop.sort(key=lambda s: s.evaluate())     # Sortujemy wg jakości
            new_gen = pop[:elite_size]               # Zachowujemy elity

            # Tworzenie nowej generacji
            while len(new_gen) < population_size:
                parents = random.sample(pop[:10], 2)               # Losujemy 2 rodziców z najlepszych
                child = crossover_one_point(parents[0], parents[1])  # Krzyżowanie
                child = mutate(child, mutation_rate)               # Mutacja
                new_gen.append(child)                              # Dodanie do nowej populacji

            islands[i] = new_gen  # Nowa populacja zastępuje starą

        # Migracja osobników co migration_interval generacji
        if (gen + 1) % migration_interval == 0:
            for i in range(num_islands):
                source = islands[i]                              # Źródłowa wyspa
                target = islands[(i + 1) % num_islands]          # Wyspa docelowa (sąsiednia, cyklicznie)

                # Wybieramy losowych migrantów z wyspy source
                migrants = random.sample(source, migrants_per_island)

                # Dla każdego migranta zastępujemy losowego nie-elitarnego osobnika na wyspie target
                for m in migrants:
                    replace_idx = random.randint(elite_size, population_size - 1)
                    target[replace_idx] = deepcopy(m)  # Wstawiamy kopię osobnika

    # Po zakończeniu – wybieramy najlepsze rozwiązanie ze wszystkich wysp
    best = min((sol for island in islands for sol in island), key=lambda s: s.evaluate())
    return best.board  # Zwracamy planszę najlepszego rozwiązania
