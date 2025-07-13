import argparse
import sys
import parser, bruteforce, hillclimb, genetic
from objective import objective_function

def main():
    arg_parser = argparse.ArgumentParser(description="Light UP (Akari) Solver")
    arg_parser.add_argument('--method', choices=['bruteforce', 'hillclimb', 'genetic'])
    arg_parser.add_argument('--input', type=str, required=True)

    arg_parser.add_argument('--generations', type=int, default=100) ##genetic
    arg_parser.add_argument('--pop_size', type=int, default=30) ##genetic
    arg_parser.add_argument('--iterations', type=int, default=1000) ##hillclimb

    args = arg_parser.parse_args()

    try:
        if args.input == '-':
            board_data = sys.stdin.read()
        else:
            with open(args.input, 'r') as f:
                board_data = f.read()
    except Exception as e:
        print(f"Błąd podczas wczytywania danych: {e}")
        sys.exit(1)

    try:
        board = parser.parse_board(board_data)
    except Exception as e:
        print(f"Błąd parsowania planszy: {e}")
        sys.exit(1)

    if args.method == 'bruteforce':
        solution = bruteforce.solve(board)
    elif args.method == 'hillclimb':
        solution = hillclimb.solve(board, max_iterations=args.iterations)
    elif args.method == 'genetic':
        solution = genetic.solve(board,
                                 generations=args.generations,
                                 pop_size=args.pop_size)
    else:
        print("Nieznana metoda.")
        sys.exit(1)

    print("\n=== Rozwiązanie ===")
    if solution:
        print(solution.display())
        print("Wynik funkcji celu:", objective_function(solution))
    else:
        print("Nie znaleziono poprawnego rozwiązania.")

if __name__ == '__main__':
    main()
