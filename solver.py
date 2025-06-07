def is_valid(board, row, col, num):
    # Zeile prüfen
    if num in board[row]:
        return False

    # Spalte prüfen
    if num in [board[i][col] for i in range(9)]:
        return False

    # 3x3-Block prüfen
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False  # keine Zahl passt
    return True  # vollständig gelöst
