"""
Tabu – algorytm przeszukiwania lokalnego z pamięcią

Zasada działania:
- Startujemy od losowego rozwiązania.
- W każdej iteracji wybieramy najlepszego sąsiada, którego nie ma na liście tabu.
- Lista tabu to zbiór niedozwolonych (niedawno odwiedzonych) rozwiązań.
- Dzięki temu nie wracamy do poprzednich stanów i unikamy zapętlenia.
- Przerywamy po określonej liczbie iteracji lub gdy znajdziemy rozwiązanie idealne.
"""

# Import klasy Board – reprezentacja planszy
from core.board import Board

# Import klasy Solution – pojedyncze rozmieszczenie lamp
from core.solution import Solution


# Główna funkcja – Tabu Search solver
def tabu_solver(board: Board, max_iterations: int = 1000, tabu_size: int = 50) -> Board:

    current = Solution(board)      # Tworzymy początkowe rozwiązanie
    current.random_solution()      # Rozkładamy losowo lampy

    best = current                 # Zapamiętujemy najlepsze rozwiązanie
    tabu_list = [current.to_string()]  # Lista tabu – reprezentacje tekstowe rozwiązań

    # Główna pętla przeszukiwania
    for _ in range(max_iterations):
        neighbors = current.get_neighbors()  # Generujemy sąsiadów (dodanie/usunięcie lampy)

        # Filtrujemy sąsiadów – usuwamy te, które są na liście tabu
        non_tabu_neighbors = [
            neighbor for neighbor in neighbors
            if neighbor.to_string() not in tabu_list
        ]

        if not non_tabu_neighbors:
            break  # Jeśli nie ma żadnych dopuszczalnych sąsiadów – kończymy

        # Wybieramy najlepszego dopuszczalnego sąsiada (najmniejszy wynik funkcji celu)
        next_solution = min(non_tabu_neighbors, key=lambda sol: sol.evaluate())

        # Jeśli nowy osobnik jest lepszy niż dotychczasowy najlepszy – zapisz go
        if next_solution.evaluate() < best.evaluate():
            best = next_solution

        current = next_solution                      # Przechodzimy do nowego rozwiązania
        tabu_list.append(current.to_string())        # Dodajemy je do listy tabu

        if len(tabu_list) > tabu_size:               # Jeśli przekroczyliśmy długość tabu
            tabu_list.pop(0)                         # Usuwamy najstarszy wpis (FIFO)

        if best.evaluate() == 0:
            break  # Jeśli znaleźliśmy idealne rozwiązanie – zakończ wcześniej

    return best.board  # Zwracamy planszę z najlepszego rozwiązania
