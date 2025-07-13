class Board:
    def __init__(self, raw_board):
        self.height = len(raw_board)
        self.width = len(raw_board[0])
        self.grid = [row[:] for row in raw_board]
        self.lights = set()

    def in_bounds(self, y, x):
        return 0 <= y < self.height and 0 <= x < self.width

    def is_white(self, y, x):
        return self.in_bounds(y, x) and self.grid[y][x] == '.'

    def is_block(self, y, x):
        return self.in_bounds(y, x) and (self.grid[y][x] == '#' or self.grid[y][x].isdigit())

    def add_light(self, y, x):
        if not self.is_white(y, x):
            return False
        self.lights.add((y, x))
        return True

    def remove_light(self, y, x):
        self.lights.discard((y, x))

    def is_lit(self, y, x):
        if (y, x) in self.lights:
            return True
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            while self.in_bounds(ny, nx) and not self.is_block(ny, nx):
                if (ny, nx) in self.lights:
                    return True
                ny += dy
                nx += dx
        return False

    def all_white_lit(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.is_white(y, x) and not self.is_lit(y, x):
                    return False
        return True

    def no_conflicts(self):
        for y1, x1 in self.lights:
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y1 + dy, x1 + dx
                while self.in_bounds(ny, nx) and not self.is_block(ny, nx):
                    if (ny, nx) in self.lights:
                        return False
                    ny += dy
                    nx += dx
        return True

    def numbered_blocks_satisfied(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].isdigit():
                    required = int(self.grid[y][x])
                    count = 0
                    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ny, nx = y + dy, x + dx
                        if self.in_bounds(ny, nx) and (ny, nx) in self.lights:
                            count += 1
                    if count != required:
                        return False
        return True

    def is_solution(self):
        return self.all_white_lit() and self.no_conflicts() and self.numbered_blocks_satisfied()

    def copy(self):
        new_board = Board(self.grid)
        new_board.lights = self.lights.copy()
        return new_board

    def display(self):
        grid = [row[:] for row in self.grid]
        for y, x in self.lights:
            grid[y][x] = 'L'
        return '\n'.join(' '.join(row) for row in grid)
