"""
Algorytm genetyczny (GA)

Zasada działania:
- Tworzymy początkową populację losowych rozwiązań.
- W każdej generacji:
  • wybieramy elity (najlepsze osobniki),
  • tworzymy nowe rozwiązania przez krzyżowanie i mutację,
  • zachowujemy najlepszych osobników do kolejnej generacji.
- Proces kończy się, gdy znajdziemy idealne rozwiązanie lub osiągniemy maksymalną liczbę generacji.
"""

# Import modułu random do losowości
import random

# Import typów
from typing import List

# Import deepcopy do kopiowania plansz
from copy import deepcopy

# Import klasy Board – reprezentacja planszy
from core.board import Board

# Import klasy Solution – pojedyncze rozmieszczenie lamp
from core.solution import Solution


# Funkcja krzyżująca dwa osobniki – używa jednopunktowego crossovera
def crossover_one_point(p1: Solution, p2: Solution) -> Solution:
    # Jednopunktowe krzyżowanie dwóch rozwiązań (losowy wybór z rodziców dla każdego pola).
    child_board = deepcopy(p1.board)  # Nowa plansza dziecka – na bazie rodzica 1

    # Dla każdego pola wybieramy wartość z jednego z rodziców
    for r in range(child_board.rows):
        for c in range(child_board.cols):
            if child_board.grid[r][c] in ('L', '.'):  # Krzyżujemy tylko lampy i puste pola
                # Z prawdopodobieństwem 0.5 wybieramy gen z p1 lub p2
                child_board.grid[r][c] = (
                    p1.board.grid[r][c] if random.random() < 0.5 else p2.board.grid[r][c]
                )
    return Solution(child_board)  # Tworzymy nowe rozwiązanie z wygenerowanej planszy


# Funkcja mutująca – dodaje lub usuwa lampy losowo
def mutate(solution: Solution, mutation_rate: float = 0.1) -> Solution:
    # Mutuje rozwiązanie – z pewnym prawdopodobieństwem dodaje lub usuwa lampy.
    new_sol = solution.copy()  # Kopiujemy rozwiązanie, aby nie nadpisać oryginału

    for r in range(new_sol.board.rows):
        for c in range(new_sol.board.cols):
            if new_sol.board.grid[r][c] in ('L', '.'):
                if random.random() < mutation_rate:
                    if new_sol.board.grid[r][c] == '.':
                        new_sol.board.place_lamp(r, c)  # Dodaj lampę
                    elif new_sol.board.grid[r][c] == 'L':
                        new_sol.board.remove_lamp(r, c)  # Usuń lampę
    return new_sol


# Główna funkcja solvera – uruchamia algorytm genetyczny
def genetic_solver(
    board: Board,
    population_size: int = 30,   # Liczba osobników w populacji
    generations: int = 100,      # Liczba generacji
    mutation_rate: float = 0.1,  # Prawdopodobieństwo mutacji
    elite_size: int = 1          # Liczba elit (najlepszych rozwiązań zachowywanych bez zmian)
) -> Board:

    population: List[Solution] = []  # Lista rozwiązań (osobników)

    # Inicjalizacja początkowej populacji – losowe rozmieszczenia lamp
    for _ in range(population_size):
        s = Solution(board)        # Nowe rozwiązanie
        s.random_solution()        # Losowe rozmieszczenie lamp
        population.append(s)       # Dodanie do populacji

    # Główna pętla generacyjna
    for _ in range(generations):
        population.sort(key=lambda s: s.evaluate())  # Sortujemy wg jakości (mniej = lepiej)

        next_gen = population[:elite_size]  # Elity – zachowujemy najlepszych bez zmian

        # Tworzymy nowe osobniki do osiągnięcia pełnej populacji
        while len(next_gen) < population_size:
            # Losowo wybieramy dwóch rodziców z najlepszej 10-tki
            parents = random.sample(population[:10], 2)
            child = crossover_one_point(parents[0], parents[1])  # Krzyżowanie
            child = mutate(child, mutation_rate)                 # Mutacja
            next_gen.append(child)                               # Dodajemy dziecko do nowej generacji

        population = next_gen  # Przechodzimy do nowej generacji

        # Jeśli najlepszy osobnik ma wynik 0 – zakończ (rozwiązanie idealne)
        if population[0].evaluate() == 0:
            break

    # Zwracamy planszę najlepszego osobnika
    return population[0].board
