"""
Simulated Annealing (Symulowane wyżarzanie)

Zasada działania:
- Startujemy od losowego rozwiązania.
- W każdej iteracji rozważamy losowego sąsiada.
- Przechodzimy do niego jeśli jest lepszy – albo czasem jeśli gorszy (w zależności od temperatury).
- Temperatura maleje z czasem – im niższa, tym mniej akceptujemy pogorszenia.
- Dzięki temu możemy opuścić lokalne minima i znaleźć globalnie lepsze rozwiązania.
"""

# Import bibliotek matematycznych i losowych
import math
import random

# Import klasy Board – plansza do gry
from core.board import Board

# Import klasy Solution – pojedyncze rozmieszczenie lamp
from core.solution import Solution


# Główna funkcja solvera z symulowanym wyżarzaniem
def simulated_annealing_solver(
    board: Board,
    max_iterations: int = 1000,        # Maksymalna liczba kroków
    initial_temp: float = 100.0,       # Temperatura początkowa
    cooling_rate: float = 0.95,        # Współczynnik chłodzenia
    temp_threshold: float = 0.1        # Temperatura minimalna (warunek zakończenia)
) -> Board:

    current = Solution(board)       # Startowe rozwiązanie
    current.random_solution()       # Losowe rozmieszczenie lamp
    current_score = current.evaluate()  # Ocena aktualnego rozwiązania

    best = current                  # Zapamiętujemy najlepsze dotąd
    best_score = current_score

    temp = initial_temp             # Ustawiamy temperaturę startową

    for _ in range(max_iterations):
        if temp < temp_threshold:
            break  # Jeśli temperatura spadła poniżej progu – kończymy

        neighbors = current.get_neighbors()  # Sąsiedzi (dodanie/usunięcie lampy)
        if not neighbors:
            break  # Jeśli brak sąsiadów – kończymy

        next_solution = random.choice(neighbors)     # Losowo wybieramy sąsiada
        next_score = next_solution.evaluate()        # Oceniamy jego jakość
        delta = next_score - current_score           # Różnica w jakości

        # Akceptujemy:
        # - każde lepsze rozwiązanie (delta < 0)
        # - gorsze z prawdopodobieństwem zależnym od temperatury
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current = next_solution      # Przechodzimy do nowego rozwiązania
            current_score = next_score

            # Jeśli to najlepsze rozwiązanie dotąd – zapamiętujemy
            if current_score < best_score:
                best = current
                best_score = current_score

        temp *= cooling_rate  # Obniżamy temperaturę (symulujemy "wyżarzanie")

    return best.board  # Zwracamy planszę najlepszego rozwiązania
