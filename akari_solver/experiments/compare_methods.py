# Importujemy bibliotekę time – do mierzenia czasu działania algorytmów
import time

# Importy systemowe do manipulowania ścieżkami
import sys
import os

# Dodajemy katalog główny projektu do sys.path, aby importować z core/ i solvers/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import klasy Board – wczytywanie i operacje na planszy
from core.board import Board

# Import wszystkich solverów, które chcemy porównać
from solvers.brute_force import brute_force_solver
from solvers.hill_climb import hill_climb_solver
from solvers.tabu import tabu_solver
from solvers.simulated_annealing import simulated_annealing_solver
from solvers.genetic import genetic_solver
from solvers.island_ga import island_genetic_solver
from solvers.evolutionary_strategy import evolutionary_strategy_solver


# Główna funkcja do porównania działania wszystkich solverów na tej samej planszy
def compare_methods(input_path: str):
    # Wczytanie planszy z pliku wejściowego
    board = Board.from_file(input_path)

    # Lista wyników: (nazwa, wynik, czas)
    results = []

    # Pomocnicza funkcja testująca jeden solver
    def test_solver(name, func, **kwargs):
        print(f"⏳ {name}...")  # Informacja że algorytm się rozpoczął
        start = time.time()  # Początek pomiaru czasu

        # Uruchomienie solvera z argumentami
        result = func(board, **kwargs)

        end = time.time()  # Koniec pomiaru czasu

        score = result.evaluate()  # Ocena rozwiązania (niższa = lepsza)
        duration = end - start     # Czas działania

        results.append((name, score, duration))  # Dodajemy do listy
        print(f"✅ {name}: score={score}, time={duration:.2f}s\n")

    # Testujemy każdy solver z ustalonymi parametrami
    test_solver("Brute Force", brute_force_solver)
    test_solver("Hill Climb", hill_climb_solver, max_iterations=1000, random_choice=False)
    test_solver("Tabu", tabu_solver, max_iterations=1000, tabu_size=50)
    test_solver("Simulated Annealing", simulated_annealing_solver,
                max_iterations=1000, initial_temp=100.0, cooling_rate=0.95, temp_threshold=0.1)
    test_solver("Genetic", genetic_solver,
                population_size=30, generations=100, mutation_rate=0.1, elite_size=1)
    test_solver("Island GA", island_genetic_solver,
                population_size=30, generations=100, mutation_rate=0.1,
                elite_size=1, num_islands=4, migration_interval=10, migrants_per_island=2)
    test_solver("Evolutionary Strategy", evolutionary_strategy_solver,
                mu=10, lam=40, generations=100, mutation_rate=0.1)

    # Podsumowanie wyników: posortowane po score (najlepsze rozwiązania na górze)
    print("\n📊 Porównanie metod:")
    for name, score, duration in sorted(results, key=lambda x: x[1]):
        print(f"{name:25s} | Score: {score:3d} | Time: {duration:.2f}s")


# Jeśli uruchomiono ten plik jako skrypt, a nie jako import
if __name__ == "__main__":
    import sys

    # Oczekujemy jednego argumentu: ścieżki do pliku planszy
    if len(sys.argv) != 2:
        print("Użycie: python experiments/compare_methods.py <ścieżka_do_pliku_wejściowego>")
    else:
        compare_methods(sys.argv[1])  # Wywołujemy główną funkcję porównującą
