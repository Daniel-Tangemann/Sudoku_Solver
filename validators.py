def is_valid_sudoku_input(value: str) -> bool:
    """Erlaubt nur leere Felder oder Ziffern 1–9."""
    if value == "":
        return True
    elif value.isdigit() and 1 <= int(value) <= 9:
        return True
    else:
        return False
