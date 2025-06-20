"""
Hill Climbing – algorytm lokalnego przeszukiwania

Zasada działania:
- Startujemy od losowego rozmieszczenia lamp (rozwiązanie początkowe).
- Generujemy sąsiadów (rozwiązania z jedną lampą więcej/mniej).
- Przechodzimy do najlepszego (lub losowego) sąsiada tylko jeśli jest lepszy.
- Powtarzamy do osiągnięcia optimum lokalnego lub wyniku idealnego (0).
"""

# Import biblioteki random – potrzebna do losowego wyboru sąsiadów
import random

# Import klasy Board – reprezentacja planszy
from core.board import Board

# Import klasy Solution – jedno możliwe rozmieszczenie lamp
from core.solution import Solution


# Główna funkcja hill climbing solvera
def hill_climb_solver(board: Board, max_iterations: int = 1000, random_choice: bool = False) -> Board:

    # Tworzymy rozwiązanie początkowe i generujemy losowe lampy
    current = Solution(board)
    current.random_solution()

    # Oceniamy jego jakość (liczba nieoświetlonych + konflikty)
    current_score = current.evaluate()

    # Główna pętla iteracyjna – wykonujemy maksymalnie max_iterations kroków
    for _ in range(max_iterations):
        # Generujemy listę sąsiednich rozwiązań (dodanie/usunięcie jednej lampy)
        neighbors = current.get_neighbors()

        if not neighbors:
            break  # Jeśli brak sąsiadów – zakończ

        # Wybieramy sąsiada: najlepszego lub losowego
        if random_choice:
            next_solution = random.choice(neighbors)
        else:
            next_solution = min(neighbors, key=lambda sol: sol.evaluate())

        # Oceniamy jakość nowego rozwiązania
        next_score = next_solution.evaluate()

        # Jeśli jest lepsze – przechodzimy do niego
        if next_score < current_score:
            current = next_solution
            current_score = next_score
        else:
            break  # Nie ma poprawy – osiągnięto optimum lokalne

        # Jeśli uzyskaliśmy idealny wynik – przerywamy wcześniej
        if current_score == 0:
            break

    # Zwracamy planszę z najlepszego rozwiązania
    return current.board
