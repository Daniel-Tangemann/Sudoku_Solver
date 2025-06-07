import tkinter as tk
from solver import solve_sudoku
from validators import is_valid_sudoku_input, is_board_valid

def start_gui():
    root = tk.Tk()
    root.title("Sudoku Solver")

    DEFAULT_STATUS = "Willkommen beim Sudoku Solver!\nTragen Sie hier drunter die ihnen bakannten Ziffern ein"

    def focus_cell(r, c):
        if 0 <= r < 9 and 0 <= c < 9:
            entries[r][c].focus_set()

    def on_key_release(event, row, col):
        val = entries[row][col].get()
        if val and val.isdigit() and 1 <= int(val) <= 9:
            # Springe zum nächsten freien Feld nach rechts, sonst nächste Zeile
            for next_col in range(col + 1, 9):
                if entries[row][next_col].get() == "":
                    entries[row][next_col].focus_set()
                    return
            for next_row in range(row + 1, 9):
                for next_col in range(9):
                    if entries[next_row][next_col].get() == "":
                        entries[next_row][next_col].focus_set()
                        return


    def set_status(message, color="blue", reset_after=3000):
        status_var.set(message)
        status_label.config(fg=color)

        # Nach reset_after ms zurücksetzen auf Standardtext + Farbe
        if reset_after:
            def reset_status():
                status_var.set(DEFAULT_STATUS)
                status_label.config(fg="blue")

            root.after(reset_after, reset_status)

    status_var = tk.StringVar()
    status_var.set(DEFAULT_STATUS)
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
                    entry.bind("<Up>", lambda e, r=row, c=col: focus_cell(r - 1, c))
                    entry.bind("<Down>", lambda e, r=row, c=col: focus_cell(r + 1, c))
                    entry.bind("<Left>", lambda e, r=row, c=col: focus_cell(r, c - 1))
                    entry.bind("<Right>", lambda e, r=row, c=col: focus_cell(r, c + 1))
                    entry.bind("<KeyRelease>", lambda e, r=row, c=col: on_key_release(e, r, c))



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
                    set_status("Ungültige Eingabe erkannt!", "red")
                    return
            puzzle.append(puzzle_row)

        # 2. Validieren
        if not is_board_valid(puzzle):
            set_status("Startzustand ungültig – doppelte Zahl?", "red")
            return

        # 3. Sudoku lösen
        if solve_sudoku(puzzle):
            # 4. Ergebnis zurückschreiben
            for row in range(9):
                for col in range(9):
                    entries[row][col].delete(0, tk.END)
                    entries[row][col].insert(0, str(puzzle[row][col]))
            set_status("Sudoku erfolgreich gelöst!", "green")

        else:
            set_status("Keine Lösung möglich!", "red")


    def restart():
        for row in range(9):
            for col in range(9):
                entries[row][col].delete(0, tk.END)
        set_status("Alle Felder gelöscht.", "blue")
        entries[0][0].focus_set()

        
    button = tk.Button(main_frame, text="Lösen", command=solve)
    button.grid(row=3, column=0, columnspan=3, pady=10)
    restartbutton = tk.Button(main_frame, text="Restart", command=restart)
    restartbutton.grid(row=4, column=0, columnspan=3, pady=10)

    entries[0][0].focus_set()
    root.mainloop()
