import tkinter as tk
from PIL import Image, ImageTk
from validators import is_valid_sudoku_input, is_board_valid
from puzzlegen import generate_puzzle
import utils
from highscore import init_db, save_score, get_highscores

def start_puzzle_gui(player_name, mode="random", on_return=None):
    if not player_name:
        player_name = "Anon"
    utils.NAME = player_name

    init_db()
    x, y = utils.LAST_POS or (200, 100)

    root = tk.Tk()
    root.title("Sudoku Solver")
    root.geometry(f"500x600+{x}+{y}")

    def on_configure(event):
        new_x = root.winfo_x()
        new_y = root.winfo_y()
        utils.LAST_POS = (new_x, new_y)

    root.bind("<Configure>", on_configure)

    DEFAULT_STATUS = f"Hallo {utils.NAME}!\nVersuche das Sudoku zu lösen!"

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
    is_given = [[False for _ in range(9)] for _ in range(9)]
    vcmd = (root.register(is_valid_sudoku_input), '%P')
    move_count = [0]

    def focus_cell(r, c):
        if 0 <= r < 9 and 0 <= c < 9:
            entries[r][c].focus_set()

    def on_key_release(event, row, col):
        val = entries[row][col].get()
        if entries[row][col]['state'] == "readonly":
            return
        old_val = getattr(event.widget, "last_val", "")
        if val != old_val:
            move_count[0] += 1
        event.widget.last_val = val

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

    for block_row in range(3):
        for block_col in range(3):
            for inner_row in range(3):
                for inner_col in range(3):
                    row = block_row * 3 + inner_row
                    col = block_col * 3 + inner_col
                    entry = tk.Entry(root, width=2, font=("Arial", 18), justify="center",
                                     validate='key', validatecommand=vcmd, bg="white", fg="blue")
                    x = 75 + col * 30
                    y = 70 + row * 30
                    canvas.create_window(x, y, window=entry)
                    entries[row][col] = entry
                    entry.bind("<Up>", lambda e, r=row, c=col: focus_cell(r - 1, c))
                    entry.bind("<Down>", lambda e, r=row, c=col: focus_cell(r + 1, c))
                    entry.bind("<Left>", lambda e, r=row, c=col: focus_cell(r, c - 1))
                    entry.bind("<Right>", lambda e, r=row, c=col: focus_cell(r, c + 1))
                    entry.bind("<KeyRelease>", lambda e, r=row, c=col: on_key_release(e, r, c))

    puzzle = generate_puzzle(utils.MODE)
    empty_cells = 0
    for row in range(9):
        for col in range(9):
            val = puzzle[row][col]
            if val != 0:
                entries[row][col].insert(0, str(val))
                entries[row][col].config(state="readonly", disabledforeground="black", background="#e0e0e0")
                is_given[row][col] = True
            else:
                empty_cells += 1

    def restart():
        move_count[0] += 1
        for row in range(9):
            for col in range(9):
                if not is_given[row][col]:
                    entries[row][col].config(state="normal")
                    entries[row][col].delete(0, tk.END)
        set_status("Nur Nutzereingaben gelöscht.", "blue")
        entries[0][0].focus_set()

    def show_highscores():
        scores = get_highscores(utils.MODE)
        hs_window = tk.Toplevel(root)
        hs_window.title("Highscores")
        hs_window.geometry("400x300")
        tk.Label(hs_window, text=f"Top 10 ({utils.MODE})", font=("Arial", 14, "bold")).pack(pady=10)

        for idx, (name, moves, empty, score, timestamp) in enumerate(scores, start=1):
            entry_text = f"{idx}. {name} – Score: {score} (Züge: {moves}, Leer: {empty})"
            tk.Label(hs_window, text=entry_text, font=("Arial", 11)).pack(anchor="w", padx=20)

    def check_finished():
        board = []
        for row in range(9):
            row_vals = []
            for col in range(9):
                val = entries[row][col].get()
                if val.isdigit():
                    row_vals.append(int(val))
                else:
                    row_vals.append(0)
            board.append(row_vals)

        if not all(all(cell != 0 for cell in row) for row in board):
            set_status("Noch nicht vollständig!", "red")
            return

        if not is_board_valid(board):
            set_status("Leider noch Fehler im Sudoku!", "red")
            return

        a = move_count[0]
        t = empty_cells
        m_map = {"easy": 100, "normal": 1000, "hard": 10000, "god": 100000}
        m = m_map.get(utils.MODE, 1000)
        score = int(m * (t / a)) if a else 0

        save_score(utils.NAME, utils.MODE, a, t, score)
        set_status(f"Gelöst! Score: {score}", "green", reset_after=None)
        show_highscores()

    def goback():
        root.destroy()
        if on_return:
            on_return()

    canvas.create_window(125, 560, window=tk.Button(root, text="Fertig", command=check_finished))
    canvas.create_window(250, 560, window=tk.Button(root, text="Restart", command=restart))
    canvas.create_window(375, 560, window=tk.Button(root, text="Menü", command=goback))

    entries[0][0].focus_set()
    root.mainloop()
