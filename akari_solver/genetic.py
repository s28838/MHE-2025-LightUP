import random
from board import Board
from objective import objective_function

def solve(raw_board, pop_size=30, generations=1000, mutation_rate=0.2, keep_best=True):
    base_board = Board(raw_board)
    white_cells = [
        (y, x)
        for y in range(base_board.height)
        for x in range(base_board.width)
        if base_board.is_white(y, x)
    ]

    population = [random_chromosome(white_cells) for _ in range(pop_size)]

    for gen in range(generations):
        scored = [(chrom, objective_function(apply_chromosome(base_board, chrom))) for chrom in population]
        scored.sort(key=lambda x: x[1])

        if scored[0][1] == 0:
            return apply_chromosome(base_board, scored[0][0])

        new_population = []

        if keep_best:
            new_population.append(scored[0][0])

        while len(new_population) < pop_size:
            parent1 = tournament_selection(scored)
            parent2 = tournament_selection(scored)

            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, white_cells, mutation_rate)
            child2 = mutate(child2, white_cells, mutation_rate)

            new_population.append(child1)
            if len(new_population) < pop_size:
                new_population.append(child2)

        population = new_population

    best = min(population, key=lambda c: objective_function(apply_chromosome(base_board, c)))
    result = apply_chromosome(base_board, best)
    return result if objective_function(result) == 0 else None

def random_chromosome(white_cells):
    return [
        cell for cell in white_cells if random.random() < 0.3
    ]

def apply_chromosome(base_board, chrom):
    board = base_board.copy()
    for y, x in chrom:
        board.add_light(y, x)
    return board

def crossover(parent1, parent2):
    if random.random() < 0.5:
        cut = len(parent1) // 2
        child1 = parent1[:cut] + parent2[cut:]
        child2 = parent2[:cut] + parent1[cut:]
    else:
        combined = list(set(parent1 + parent2))
        child1 = random.sample(combined, k=min(len(combined), random.randint(3, len(combined))))
        child2 = random.sample(combined, k=min(len(combined), random.randint(3, len(combined))))
    return child1, child2

def mutate(chrom, white_cells, rate):
    new = chrom[:]
    if random.random() < rate:
        if random.random() < 0.5 and new:
            new.remove(random.choice(new))
        else:
            options = [cell for cell in white_cells if cell not in new]
            if options:
                new.append(random.choice(options))
    return new

def tournament_selection(scored, k=3):
    candidates = random.sample(scored, k)
    candidates.sort(key=lambda x: x[1])
    return candidates[0][0]
