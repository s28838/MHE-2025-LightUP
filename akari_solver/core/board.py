# Import typów z biblioteki typing (dla lepszej czytelności i podpowiedzi typów)
from typing import List, Tuple


# Klasa reprezentująca planszę Akari
class Board:
    def __init__(self, grid: List[List[str]]):
        # Siatka planszy – dwuwymiarowa lista znaków (np. ".", "#", "1", ..., "L")
        self.grid = grid

        # Liczba wierszy na planszy
        self.rows = len(grid)

        # Liczba kolumn na planszy (zakładamy, że każda linia ma tyle samo kolumn co pierwsza)
        self.cols = len(grid[0]) if self.rows > 0 else 0

    # Metoda klasowa do wczytania planszy z pliku tekstowego
    @classmethod
    def from_file(cls, filename: str) -> "Board":
        with open(filename, 'r') as file:
            lines = file.readlines()  # Czytamy wszystkie linie
        # Usuwamy białe znaki i dzielimy każdą linię na komórki
        grid = [line.strip().split() for line in lines if line.strip()]
        return cls(grid)  # Tworzymy nową instancję Board

    # Wyświetlenie planszy w terminalu (np. do debugowania)
    def display(self) -> None:
        for row in self.grid:
            print(" ".join(row))  # Każda linia jako jeden ciąg

    # Sprawdzenie, czy dany indeks mieści się w granicach planszy
    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    # Sprawdza, czy dana wartość to ściana (czarne pole lub numerowana ściana)
    def is_wall(self, value: str) -> bool:
        return value == '#' or value.isdigit()

    # Umieszcza lampę (L) na polu jeśli to puste białe pole (".")
    def place_lamp(self, r: int, c: int):
        if self.grid[r][c] == '.':
            self.grid[r][c] = 'L'

    # Usuwa lampę z danego pola (zamienia 'L' na '.')
    def remove_lamp(self, r: int, c: int):
        if self.grid[r][c] == 'L':
            self.grid[r][c] = '.'

    # Sprawdza, czy można legalnie postawić lampę na danym polu
    def is_valid_lamp(self, r: int, c: int) -> bool:
        return self.in_bounds(r, c) and self.grid[r][c] == '.'

    # Zwraca wszystkie pola oświetlone przez istniejące lampy
    def get_illuminated(self) -> List[Tuple[int, int]]:
        illuminated = set()  # Używamy zbioru, by uniknąć duplikatów
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Góra, dół, lewo, prawo

        # Przechodzimy przez wszystkie pola planszy
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'L':
                    # Sama lampa też jest oświetlona
                    illuminated.add((r, c))

                    # Sprawdzamy każdy kierunek
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        while self.in_bounds(nr, nc) and not self.is_wall(self.grid[nr][nc]):
                            illuminated.add((nr, nc))  # To pole jest oświetlone

                            if self.grid[nr][nc] == 'L':
                                break  # Inna lampa – przerywamy, by uniknąć zliczania za ścianą
                            nr += dr
                            nc += dc
        return list(illuminated)

    # Liczy konflikty – czyli przypadki, gdzie lampy się wzajemnie widzą
    def count_conflicts(self) -> int:
        conflict_count = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Kierunki

        # Przeszukiwanie wszystkich lamp
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'L':
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        while self.in_bounds(nr, nc) and not self.is_wall(self.grid[nr][nc]):
                            if self.grid[nr][nc] == 'L':
                                conflict_count += 1  # Znalazł się konflikt
                                break
                            nr += dr
                            nc += dc
        return conflict_count // 2  # Każdy konflikt jest liczony dwa razy (raz z każdej lampy)

    # Liczy liczbę białych pól, które NIE są oświetlone
    def count_unlit(self) -> int:
        illuminated = set(self.get_illuminated())
        unlit = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == '.' and (r, c) not in illuminated:
                    unlit += 1
        return unlit

    # Funkcja oceny rozwiązania – sumuje błędy
    def evaluate(self) -> int:
        return self.count_unlit() + self.count_conflicts()
