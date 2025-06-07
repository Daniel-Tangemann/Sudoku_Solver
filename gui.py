import tkinter as tk
from solver import solve_sudoku
from validators import is_valid_sudoku_input

def start_gui():
    root = tk.Tk()
    root.title("Sudoku Solver")

    entries = []

    vcmd = (root.register(is_valid_sudoku_input), '%P')

    for row in range(9):
        row_entries = []
        for col in range(9):
            if (row // 3 + col // 3) % 2 == 0:
                bg_color = "#f0f0f0"
            else:
                bg_color = "white"

            is_block_edge = (
                col in [0, 3, 6] or
                row in [0, 3, 6]
            )

            entry = tk.Entry(
                root,
                width=2,
                font=("Arial", 18),
                justify='center',
                validate='key',
                validatecommand=vcmd,
                highlightthickness=2 if is_block_edge else 1,
                highlightbackground="black",
                highlightcolor="black",
                bg=bg_color
            )
            entry.grid(row=row, column=col, padx=1, pady=1)
            row_entries.append(entry)
        entries.append(row_entries)

    def solve():
        print("Lösungsfunktion kommt hier hin")  # später ersetzen

    button = tk.Button(root, text="Lösen", command=solve)
    button.grid(row=9, column=0, columnspan=9, pady=10)

    root.mainloop()
