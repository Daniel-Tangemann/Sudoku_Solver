import tkinter as tk
from PIL import Image, ImageTk
from solver import solve_sudoku
from validators import is_valid_sudoku_input, is_board_valid
from puzzlegen import generate_puzzle
import utils

def start_gui(player_name, mode="manual", on_return=None):
    if not player_name:
        player_name = "Anon"
    utils.NAME = player_name  # global speichern

    # Standardposition verwenden, falls keine gespeichert wurde
    x, y = utils.LAST_POS or (200, 100)

    root = tk.Tk()
    root.title("Sudoku Solver")
    root.geometry(f"500x600+{x}+{y}")

    def on_configure(event):
        new_x = root.winfo_x()
        new_y = root.winfo_y()
        utils.LAST_POS = (new_x, new_y)

    root.bind("<Configure>", on_configure)

    DEFAULT_STATUS = f"Hallo {utils.NAME}!\nTragen Sie hier drunter die ihnen bekannten Ziffern ein"

    # Hintergrundbild wählen
    if utils.MODE == "god":
        background_path = "game_backgr_stepped.png"
    else:
        background_path = "game_backgr_smooth.png"

    bg_image = Image.open(background_path).resize((500, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=500, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    status_var = tk.StringVar()
    status_var.set(DEFAULT_STATUS)
    status_label = tk.Label(root, textvariable=status_var, fg="black", font=("Arial", 12))
    canvas.create_window(250, 30, window=status_label)

    entries = [[None for _ in range(9)] for _ in range(9)]
    vcmd = (root.register(is_valid_sudoku_input), '%P')

    def focus_cell(r, c):
        if 0 <= r < 9 and 0 <= c < 9:
            entries[r][c].focus_set()

    def on_key_release(event, row, col):
        val = entries[row][col].get()
        if val and val.isdigit() and 1 <= int(val) <= 9:
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
        if reset_after:
            def reset_status():
                status_var.set(DEFAULT_STATUS)
                status_label.config(fg="blue")
            root.after(reset_after, reset_status)

    # Sudoku-Grid zeichnen
    for block_row in range(3):
        for block_col in range(3):
            for inner_row in range(3):
                for inner_col in range(3):
                    row = block_row * 3 + inner_row
                    col = block_col * 3 + inner_col
                    entry = tk.Entry(root, width=2, font=("Arial", 18), justify="center",
                                     validate='key', validatecommand=vcmd, bg="white")
                    x = 75 + col * 30
                    y = 70 + row * 30
                    canvas.create_window(x, y, window=entry)
                    entries[row][col] = entry
                    entry.bind("<Up>", lambda e, r=row, c=col: focus_cell(r - 1, c))
                    entry.bind("<Down>", lambda e, r=row, c=col: focus_cell(r + 1, c))
                    entry.bind("<Left>", lambda e, r=row, c=col: focus_cell(r, c - 1))
                    entry.bind("<Right>", lambda e, r=row, c=col: focus_cell(r, c + 1))
                    entry.bind("<KeyRelease>", lambda e, r=row, c=col: on_key_release(e, r, c))

    # Wenn Modus random, fülle das Grid direkt vor
    if mode == "random":
        puzzle = generate_puzzle(utils.MODE)
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] != 0:
                    entries[row][col].insert(0, str(puzzle[row][col]))

    def solve():
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

        if not is_board_valid(puzzle):
            set_status("Startzustand ungültig – doppelte Zahl?", "red")
            return

        if solve_sudoku(puzzle):
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

    def goback():
        root.destroy()
        if on_return:
            on_return()

    canvas.create_window(125, 560, window=tk.Button(root, text="Lösen", command=solve))
    canvas.create_window(250, 560, window=tk.Button(root, text="Restart", command=restart))
    canvas.create_window(375, 560, window=tk.Button(root, text="Menü", command=goback))

    entries[0][0].focus_set()
    root.mainloop()
