import random
from board import Board

def objective_function(board):

    score = 0

    for y in range(board.height):
        for x in range(board.width):
            if board.is_white(y, x) and not board.is_lit(y, x):
                score += 1

    if not board.no_conflicts():
        score += 2

    if not board.numbered_blocks_satisfied():
        score += 5

    return score

def generate_random_solution(board):
    white_cells = [
        (y, x)
        for y in range(board.height)
        for x in range(board.width)
        if board.is_white(y, x)
    ]

    solution = board.copy()

    for y, x in white_cells:
        if random.random() < 0.25:
            solution.add_light(y, x)

    return solution

def generate_neighbors(board):

    neighbors = []

    white_cells = [
        (y, x)
        for y in range(board.height)
        for x in range(board.width)
        if board.is_white(y, x)
    ]

    # Dodaj żarówkę w pustym miejscu
    for y, x in white_cells:
        if (y, x) not in board.lights:
            neighbor = board.copy()
            neighbor.add_light(y, x)
            neighbors.append(neighbor)

    # Usuń istniejącą żarówkę
    for y, x in list(board.lights):
        neighbor = board.copy()
        neighbor.remove_light(y, x)
        neighbors.append(neighbor)

    # Przesuń żarówkę z A do B
    for y1, x1 in list(board.lights):
        for y2, x2 in white_cells:
            if (y2, x2) not in board.lights:
                neighbor = board.copy()
                neighbor.remove_light(y1, x1)
                neighbor.add_light(y2, x2)
                neighbors.append(neighbor)

    return neighbors
