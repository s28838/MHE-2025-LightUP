"""
Algorytm brute-force

Zasada działania:
- Generuje wszystkie możliwe kombinacje umieszczenia lamp w dozwolonych polach.
- Dla każdej kombinacji tworzy planszę, rozmieszcza lampy zgodnie z kombinacją (bitmaską).
- Ocena rozwiązania to: liczba nieoświetlonych pól + konflikty (czyli funkcja celu).
- Zwracane jest najlepsze znalezione rozwiązanie (najniższy wynik funkcji celu).
- Działa tylko dla bardzo małych plansz (np. < 15 pól), ze względu na wykładniczy czas działania.
"""

# Import typów dla lepszej czytelności i autouzupełniania
from typing import List, Tuple

# Importujemy product – do generowania permutacji bitów (0/1)
from itertools import product

# Głębokie kopiowanie planszy, aby nie modyfikować oryginału
from copy import deepcopy

# Import klasy Board – reprezentuje siatkę i funkcje pomocnicze
from core.board import Board


# Funkcja pomocnicza – zbiera wszystkie pola, gdzie można legalnie postawić lampę
def get_all_valid_positions(board: Board) -> List[Tuple[int, int]]:
    """Zwraca listę współrzędnych pól, na których można postawić lampę."""
    positions = []
    for r in range(board.rows):         # Iterujemy po wszystkich wierszach
        for c in range(board.cols):     # Iterujemy po wszystkich kolumnach
            if board.is_valid_lamp(r, c):  # Sprawdzamy, czy pole jest puste
                positions.append((r, c))   # Dodajemy do listy
    return positions


# Główna funkcja – wykonuje pełne przeszukiwanie przestrzeni rozwiązań
def brute_force_solver(board: Board) -> Board:
    # Przegląda wszystkie możliwe kombinacje lamp i zwraca najlepszą planszę z punktu widzenia funkcji celu.

    best_board = None              # Najlepsze dotąd rozwiązanie (Board)
    best_score = float('inf')      # Najlepszy wynik funkcji celu (im mniej, tym lepiej)

    valid_positions = get_all_valid_positions(board)  # Lista współrzędnych możliwych do oświetlenia
    n = len(valid_positions)       # Liczba takich pozycji

    # Iterujemy przez wszystkie możliwe kombinacje w postaci ciągów bitowych
    # Każdy bit oznacza: 1 – postaw lampę, 0 – nie stawiaj
    for bits in product([0, 1], repeat=n):
        test_board = deepcopy(board)  # Robimy kopię planszy, aby nie zmieniać oryginału

        # Dla każdej pozycji, jeśli bit to 1 – postaw lampę
        for i, bit in enumerate(bits):
            r, c = valid_positions[i]  # Pobieramy współrzędne i-tej pozycji
            if bit == 1:
                test_board.place_lamp(r, c)

        score = test_board.evaluate()  # Oceniamy wynik planszy: nieoświetlone pola + konflikty

        # Sprawdzamy, czy to rozwiązanie jest lepsze od dotychczasowego
        if score < best_score:
            best_score = score
            best_board = deepcopy(test_board)  # Zapisujemy najlepszą planszę

        # Jeśli wynik idealny (score = 0), nie ma sensu dalej szukać – przerywamy
        if best_score == 0:
            break

    return best_board  # Zwracamy najlepsze znalezione rozwiązanie
