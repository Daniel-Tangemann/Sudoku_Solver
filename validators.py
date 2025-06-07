def is_valid_sudoku_input(value: str) -> bool:
    """Erlaubt nur leere Felder oder Ziffern 1–9."""
    if value == "":
        return True
    elif value.isdigit() and 1 <= int(value) <= 9:
        return True
    else:
        return False

def is_board_valid(board):
    def has_duplicates(group):
        nums = [x for x in group if x != 0]
        return len(nums) != len(set(nums))

    for row in board:
        if has_duplicates(row):
            return False

    for col in zip(*board):
        if has_duplicates(col):
            return False

    for box_row in range(3):
        for box_col in range(3):
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(board[box_row * 3 + i][box_col * 3 + j])
            if has_duplicates(block):
                return False

    return True
