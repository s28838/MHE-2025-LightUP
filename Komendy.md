# Brute Force
python cli/run_solver.py --solver brute_force --input data/board_5x5.txt

# Hill Climb
### Deterministyczny (najlepszy sąsiad)
python cli/run_solver.py --solver hill_climb --input data/board_5x5.txt
### Losowy sąsiad
python cli/run_solver.py --solver hill_climb --input data/board_5x5.txt --random
### Zmiana liczby iteracji
python cli/run_solver.py --solver hill_climb --input data/board_5x5.txt --iterations 2000

# Tabu
### Domyślna konfiguracja
python cli/run_solver.py --solver tabu --input data/board_5x5.txt
### Zmiana długości listy tabu
python cli/run_solver.py --solver tabu --input data/board_5x5.txt --tabu 100

# Simulated Annealing
### Domyślne parametry
python cli/run_solver.py --solver sa --input data/board_5x5.txt
### Zmodyfikowane parametry
python cli/run_solver.py --solver sa --input data/board_5x5.txt --temp 150 --cooling 0.9 --threshold 0.5

# Genetic Algorithm
### Domyślna konfiguracja
python cli/run_solver.py --solver genetic --input data/board_5x5.txt
### Zmiana parametrów GA
python cli/run_solver.py --solver genetic --input data/board_5x5.txt --pop 50 --gens 200 --mut 0.2 --elite 2

# Island Genetic Algorithm
### Domyślne parametry
python cli/run_solver.py --solver island_ga --input data/board_5x5.txt
### Z pełną kontrolą parametrów
python cli/run_solver.py --solver island_ga --input data/board_5x5.txt --pop 40 --gens 150 --mut 0.15 --elite 2 --islands 5 --migrate 10 --migrants 3

# Evolutionary Strategy
### Domyślna konfiguracja
python cli/run_solver.py --solver es --input data/board_5x5.txt
### Zmodyfikowane μ, λ i mutacje
python cli/run_solver.py --solver es --input data/board_5x5.txt --mu 20 --lam 80 --gens 200 --mut 0.05
