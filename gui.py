import tkinter as tk
from solver import solve_sudoku
from validators import is_valid_sudoku_input

def start_gui():
    root = tk.Tk()
    root.title("Sudoku Solver")

    status_var = tk.StringVar()
    status_var.set("Willkommen beim Sudoku Solver!\nTragen Sie hier drunter die ihnen bakannten Ziffern ein")
    status_label = tk.Label(root, textvariable=status_var, fg="blue", font=("Arial", 12))
    status_label.pack(pady=(5, 0))

    entries = [[None for _ in range(9)] for _ in range(9)]

    vcmd = (root.register(is_valid_sudoku_input), '%P')

    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack()

    for block_row in range(3):
        for block_col in range(3):
            # Frame für jeden 3x3-Block
            block_frame = tk.Frame(
                main_frame,
                borderwidth=2,
                relief="solid",
                padx=2,
                pady=2
            )
            block_frame.grid(row=block_row, column=block_col, padx=2, pady=2)

            for inner_row in range(3):
                for inner_col in range(3):
                    row = block_row * 3 + inner_row
                    col = block_col * 3 + inner_col

                    entry = tk.Entry(
                        block_frame,
                        width=2,
                        font=("Arial", 18),
                        justify="center",
                        validate='key',
                        validatecommand=vcmd,
                        bg="white"
                    )
                    entry.grid(row=inner_row, column=inner_col, padx=1, pady=1)
                    entries[row][col] = entry

    def solve():
        # 1. Grid einsammeln
        puzzle = []
        for row in range(9):
            puzzle_row = []
            for col in range(9):
                val = entries[row][col].get()
                if val == "":
                    puzzle_row.append(0)
                elif val.isdigit():
                    puzzle_row.append(int(val))
                else:
                    status_var.set("Ungültige Eingabe erkannt!")
                    status_label.config(fg="red")
                    return
            puzzle.append(puzzle_row)

        # 2. Sudoku lösen
        if solve_sudoku(puzzle):
            # 3. Ergebnis zurückschreiben
            for row in range(9):
                for col in range(9):
                    entries[row][col].delete(0, tk.END)
                    entries[row][col].insert(0, str(puzzle[row][col]))
            status_var.set("Sudoku erfolgreich gelöst!")
            status_label.config(fg="green")
        else:
            status_var.set("Keine Lösung möglich!")
            status_label.config(fg="red")
        
    button = tk.Button(main_frame, text="Lösen", command=solve)
    button.grid(row=3, column=0, columnspan=3, pady=10)

    root.mainloop()
