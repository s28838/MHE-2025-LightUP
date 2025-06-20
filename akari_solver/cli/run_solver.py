# Import biblioteki argparse – służy do przetwarzania argumentów z wiersza poleceń
import argparse

# Import modułu sys – pozwala modyfikować ścieżki importów
import sys

# Import modułu os – służy do pracy z plikami i ścieżkami
import os

# Dodanie katalogu głównego projektu (jeden poziom wyżej niż ten plik) do ścieżki importów
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import klasy Board, która reprezentuje planszę Akari
from core.board import Board

# Import poszczególnych solverów (algorytmów rozwiązujących)
from solvers.brute_force import brute_force_solver
from solvers.hill_climb import hill_climb_solver
from solvers.tabu import tabu_solver
from solvers.simulated_annealing import simulated_annealing_solver
from solvers.genetic import genetic_solver
from solvers.island_ga import island_genetic_solver
from solvers.evolutionary_strategy import evolutionary_strategy_solver


# Główna funkcja programu
def main():
    # Utworzenie parsera do odczytywania argumentów z terminala
    parser = argparse.ArgumentParser(description="Akari (Light Up) Solver")

    # Argument: wybór solvera (obowiązkowy)
    parser.add_argument('--solver', type=str, required=True,
                        choices=[
                            'brute_force', 'hill_climb', 'tabu',
                            'sa', 'genetic', 'island_ga', 'es'
                        ],
                        help='Nazwa solvera')

    # Argument: ścieżka do pliku wejściowego z planszą (obowiązkowy)
    parser.add_argument('--input', type=str, required=True, help='Plik wejściowy z planszą')

    # Argument opcjonalny: plik wyjściowy, do którego zapisane zostanie rozwiązanie
    parser.add_argument('--output', type=str, help='Zapisz wynik do pliku')

    # Parametry dla hill climbing, tabu, SA – maksymalna liczba iteracji
    parser.add_argument('--iterations', type=int, default=1000, help='Maks. liczba iteracji')

    # Parametr dla hill climbing – losowy sąsiad zamiast najlepszego
    parser.add_argument('--random', action='store_true', help='Losowy wybór sąsiada (dla hill_climb)')

    # Parametr dla tabu search – maksymalna długość listy tabu
    parser.add_argument('--tabu', type=int, default=50, help='Rozmiar listy tabu')

    # Parametry dla simulated annealing
    parser.add_argument('--temp', type=float, default=100.0, help='Temperatura początkowa (SA)')
    parser.add_argument('--cooling', type=float, default=0.95, help='Współczynnik chłodzenia (SA)')
    parser.add_argument('--threshold', type=float, default=0.1, help='Temperatura końcowa (SA)')

    # Parametry dla genetic algorithm i island GA
    parser.add_argument('--pop', type=int, default=30, help='Rozmiar populacji')
    parser.add_argument('--gens', type=int, default=100, help='Liczba generacji')
    parser.add_argument('--mut', type=float, default=0.1, help='Prawdopodobieństwo mutacji')
    parser.add_argument('--elite', type=int, default=1, help='Rozmiar elity')

    # Dodatkowe parametry dla island GA
    parser.add_argument('--islands', type=int, default=4, help='Liczba wysp')
    parser.add_argument('--migrate', type=int, default=10, help='Interwał migracji (generacje)')
    parser.add_argument('--migrants', type=int, default=2, help='Liczba migrantów')

    # Parametry dla evolutionary strategy
    parser.add_argument('--mu', type=int, default=10, help='Liczba rodziców (ES)')
    parser.add_argument('--lam', type=int, default=40, help='Liczba potomków (ES)')

    # Parsowanie argumentów z terminala
    args = parser.parse_args()

    # Wczytanie planszy z pliku
    board = Board.from_file(args.input)

    # Wybór odpowiedniego solvera na podstawie argumentu
    if args.solver == 'brute_force':
        result = brute_force_solver(board)

    elif args.solver == 'hill_climb':
        result = hill_climb_solver(board, max_iterations=args.iterations, random_choice=args.random)

    elif args.solver == 'tabu':
        result = tabu_solver(board, max_iterations=args.iterations, tabu_size=args.tabu)

    elif args.solver == 'sa':
        result = simulated_annealing_solver(
            board,
            max_iterations=args.iterations,
            initial_temp=args.temp,
            cooling_rate=args.cooling,
            temp_threshold=args.threshold
        )

    elif args.solver == 'genetic':
        result = genetic_solver(
            board,
            population_size=args.pop,
            generations=args.gens,
            mutation_rate=args.mut,
            elite_size=args.elite
        )

    elif args.solver == 'island_ga':
        result = island_genetic_solver(
            board,
            population_size=args.pop,
            generations=args.gens,
            mutation_rate=args.mut,
            elite_size=args.elite,
            num_islands=args.islands,
            migration_interval=args.migrate,
            migrants_per_island=args.migrants
        )

    elif args.solver == 'es':
        result = evolutionary_strategy_solver(
            board,
            mu=args.mu,
            lam=args.lam,
            generations=args.gens,
            mutation_rate=args.mut
        )

    # Jeśli solver nie został rozpoznany – zakończ program
    else:
        print("Nieznany solver.")
        return

    # Wyświetlenie rozwiązania na ekranie
    print("\nRozwiązanie:")
    result.display()

    # Wyświetlenie wartości funkcji celu (liczba nieoświetlonych pól + konflikty)
    print(f"\nFunkcja celu: {result.evaluate()}")

    # Zapisanie wyniku do pliku, jeśli podano --output
    if args.output:
        with open(args.output, 'w') as f:
            for row in result.grid:
                f.write(' '.join(row) + '\n')
        print(f"\nZapisano do pliku: {args.output}")


# Uruchomienie funkcji main, jeśli plik został wykonany jako skrypt
if __name__ == '__main__':
    main()
