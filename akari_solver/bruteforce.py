from itertools import product
from board import Board
from objective import objective_function

def solve(raw_board):

    board = Board(raw_board)

    white_cells = [
        (y, x)
        for y in range(board.height)
        for x in range(board.width)
        if board.is_white(y, x)
    ]

    for pattern in product([0, 1], repeat=len(white_cells)):
        candidate = board.copy()
        for include, (y, x) in zip(pattern, white_cells):
            if include:
                candidate.add_light(y, x)
        if objective_function(candidate) == 0:
            return candidate

    return None
