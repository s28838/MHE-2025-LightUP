import time
import argparse
import parser, bruteforce, hillclimb, genetic
from objective import objective_function

def run_and_measure(name, func, raw_board):
    print(f"Metoda: {name}")
    start = time.time()
    solution = func(raw_board)
    end = time.time()

    if solution:
        score = objective_function(solution)
    else:
        score = "brak rozwiązania"

    print(f"  Czas wykonania: {end - start:.3f} s")
    print(f"  Wynik funkcji celu: {score}")
    print("")

    return (name, score, end - start)

def main():
    parser_arg = argparse.ArgumentParser(description="Porównanie algorytmów Akari")
    parser_arg.add_argument('--input', type=str, required=True)
    args = parser_arg.parse_args()

    with open(args.input, 'r') as f:
        board_data = f.read()
    raw_board = parser.parse_board(board_data)

    methods = [
        ("bruteforce", bruteforce.solve),
        ("hillclimb", hillclimb.solve),
        ("genetic", genetic.solve)
    ]

    print("=== Porównanie metod ===\n")
    results = []
    for name, func in methods:
        results.append(run_and_measure(name, func, raw_board))

    print("=== Podsumowanie ===")
    for name, score, duration in results:
        print(f"{name:<12} | wynik: {score:<18} | czas: {duration:.3f} s")

if __name__ == '__main__':
    main()
