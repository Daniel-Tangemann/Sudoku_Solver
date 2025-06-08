# puzzlegen.py
import random
import copy

# Ausgangs-Sudoku (vollständig gelöst)
BASE_SUDOKU = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9, 1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8]
]

def transpose(board):
    return [list(row) for row in zip(*board)]

def swap_rows_within_block(board):
    for block in range(3):
        rows = list(range(block * 3, block * 3 + 3))
        random.shuffle(rows)
        board[block*3:block*3+3] = [board[r] for r in rows]

def swap_columns_within_block(board):
    board = transpose(board)
    swap_rows_within_block(board)
    return transpose(board)

def swap_row_blocks(board):
    blocks = [0, 1, 2]
    random.shuffle(blocks)
    new_board = []
    for block in blocks:
        new_board.extend(board[block*3:block*3+3])
    return new_board

def swap_col_blocks(board):
    board = transpose(board)
    board = swap_row_blocks(board)
    return transpose(board)

def permute_numbers(board):
    mapping = list(range(1, 10))
    random.shuffle(mapping)
    return [[mapping[val - 1] for val in row] for row in board]

def generate_full_solution():
    board = copy.deepcopy(BASE_SUDOKU)
    swap_rows_within_block(board)
    board = swap_columns_within_block(board)
    board = swap_row_blocks(board)
    board = swap_col_blocks(board)
    board = permute_numbers(board)
    return board

def remove_cells(board, clues):
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    to_remove = 81 - clues
    puzzle = copy.deepcopy(board)
    for i in range(to_remove):
        r, c = cells[i]
        puzzle[r][c] = 0
    return puzzle

def generate_puzzle(difficulty="normal"):
    difficulty_map = {
        "easy": random.randint(36, 45),
        "normal": random.randint(30, 35),
        "hard": random.randint(24, 29),
        "god": 17
    }
    clues = difficulty_map.get(difficulty, 30)
    full_board = generate_full_solution()
    return remove_cells(full_board, clues)
