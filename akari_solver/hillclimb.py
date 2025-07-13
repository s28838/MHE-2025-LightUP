import random
from board import Board
from objective import (
    objective_function,
    generate_neighbors,
    generate_random_solution
)

def solve(raw_board, max_iterations=1000):
    current = generate_random_solution(Board(raw_board))
    current_score = objective_function(current)
    for _ in range(max_iterations):
        neighbors = generate_neighbors(current)
        best_neighbor = current
        best_score = current_score
        for neighbor in neighbors:
            score = objective_function(neighbor)
            if score < best_score:
                best_neighbor = neighbor
                best_score = score
        if best_score == current_score:
            break
        current = best_neighbor
        current_score = best_score
        if current_score == 0:
            break

    return current if current.is_solution() else None
