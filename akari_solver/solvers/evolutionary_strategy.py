"""
Strategia ewolucyjna (μ + λ)

Zasada działania:
- Tworzymy μ losowych rozwiązań (rodzice).
- W każdej generacji generujemy λ potomków poprzez mutacje losowych rodziców.
- Łączymy rodziców i potomków, a następnie wybieramy najlepszych μ do kolejnej generacji.
- Proces powtarzamy przez określoną liczbę generacji lub do osiągnięcia idealnego wyniku.
"""

# Import modułu random – do losowych wyborów i mutacji
import random

# Typowanie: listy rozwiązań
from typing import List

# Import klasy Board – struktura planszy
from core.board import Board

# Import klasy Solution – pojedyncze rozmieszczenie lamp na planszy
from core.solution import Solution


# Główna funkcja solvera typu Evolutionary Strategy
def evolutionary_strategy_solver(
    board: Board,
    mu: int = 10,               # Liczba rodziców
    lam: int = 40,              # Liczba potomków
    generations: int = 100,     # Maksymalna liczba generacji
    mutation_rate: float = 0.1  # Prawdopodobieństwo mutacji
) -> Board:

    parents: List[Solution] = []  # Lista początkowych rodziców

    # Generowanie początkowej populacji rodziców (mu rozwiązań losowych)
    for _ in range(mu):
        s = Solution(board)      # Tworzymy nowy obiekt Solution
        s.random_solution()      # Generujemy losowe rozmieszczenie lamp
        parents.append(s)        # Dodajemy do listy rodziców

    # Główna pętla generacyjna
    for _ in range(generations):
        offspring: List[Solution] = []  # Lista potomków w tej generacji

        # Tworzenie lam potomków przez mutacje losowych rodziców
        for _ in range(lam):
            parent = random.choice(parents)     # Losowy rodzic z obecnej populacji
            child = parent.copy()               # Kopia rodzica
            child = mutate(child, mutation_rate)  # Mutacja kopii
            offspring.append(child)             # Dodanie dziecka do potomków

        # Łączenie rodziców i potomków (model μ + λ)
        combined = parents + offspring

        # Sortowanie całej populacji według wartości funkcji celu
        combined.sort(key=lambda s: s.evaluate())

        # Nowa populacja rodziców – najlepsze mu osobników
        parents = combined[:mu]

        # Jeśli najlepsze rozwiązanie ma score = 0 (idealne) – kończymy
        if parents[0].evaluate() == 0:
            break

    # Zwracamy planszę najlepszego rozwiązania
    return parents[0].board


# Funkcja pomocnicza – mutuje istniejące rozwiązanie
def mutate(solution: Solution, mutation_rate: float = 0.1) -> Solution:
    # Mutuje rozwiązanie poprzez losowe dodanie/usunięcie lamp na polach z prawdopodobieństwem mutation_rate.
    new_sol = solution.copy()  # Głęboka kopia
    for r in range(new_sol.board.rows):
        for c in range(new_sol.board.cols):
            if new_sol.board.grid[r][c] in ('L', '.'):
                if random.random() < mutation_rate:
                    # Zamień '.' na 'L' lub odwrotnie
                    if new_sol.board.grid[r][c] == '.':
                        new_sol.board.place_lamp(r, c)
                    elif new_sol.board.grid[r][c] == 'L':
                        new_sol.board.remove_lamp(r, c)
    return new_sol
