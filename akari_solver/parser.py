def parse_board(board_str):
    board = []
    for line in board_str.strip().splitlines():
        row = [char for char in line if char != ' ']
        board.append(row)
    return board


def print_board(board):
    for row in board:
        print(' '.join(row))
