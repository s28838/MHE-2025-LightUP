# Import losowości (np. do generowania losowych rozwiązań)
import random

# Import typów pomocniczych
from typing import List

# Import głębokiego kopiowania obiektów (by nie nadpisywać oryginału)
from copy import deepcopy


# Klasa reprezentująca jedno możliwe rozwiązanie (czyli planszę z rozstawionymi lampami)
class Solution:
    def __init__(self, board):
        # Przechowuje kopię planszy – oryginał nie jest modyfikowany
        self.board = deepcopy(board)

    def random_solution(self):
        # Generuje losowe rozmieszczenie lamp.
        # Dla każdego pustego pola istnieje 20% szans na postawienie lampy.
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                if self.board.is_valid_lamp(r, c):
                    if random.random() < 0.2:
                        self.board.place_lamp(r, c)

    def get_neighbors(self) -> List["Solution"]:
        # Zwraca listę sąsiadów (nowych rozwiązań), które różnią się dodaniem lub usunięciem jednej lampy.
        neighbors = []

        for r in range(self.board.rows):
            for c in range(self.board.cols):
                # Jeśli pole jest puste – możemy dodać lampę
                if self.board.is_valid_lamp(r, c):
                    new_board = deepcopy(self.board)
                    new_board.place_lamp(r, c)
                    neighbors.append(Solution(new_board))

                # Jeśli pole zawiera lampę – możemy ją usunąć
                elif self.board.grid[r][c] == 'L':
                    new_board = deepcopy(self.board)
                    new_board.remove_lamp(r, c)
                    neighbors.append(Solution(new_board))

        return neighbors

    def evaluate(self) -> int:
        # Zwraca wartość funkcji celu danego rozwiązania.
        # Im niższa, tym lepiej. 0 = rozwiązanie idealne.
        return self.board.evaluate()

    def to_string(self) -> str:
        # Zwraca tekstową reprezentację planszy – używana np. w tabu list.
        return '\n'.join(' '.join(row) for row in self.board.grid)

    def copy(self) -> "Solution":
        # Zwraca kopię bieżącego obiektu Solution (głęboka kopia planszy).
        return Solution(self.board)
