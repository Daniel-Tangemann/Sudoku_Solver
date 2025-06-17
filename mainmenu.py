import tkinter as tk
from PIL import Image, ImageTk
from gui import start_gui
from gui_puzzle import start_puzzle_gui
from highscore import get_highscores
import utils

def start_main_menu():
    x, y = utils.LAST_POS or (200, 100)

    new_root = tk.Tk()
    new_root.title("Sudoku Hauptmenü")
    new_root.geometry(f"500x600+{x}+{y}")

    def on_configure(event):
        new_x = new_root.winfo_x()
        new_y = new_root.winfo_y()
        utils.LAST_POS = (new_x, new_y)

    new_root.bind("<Configure>", on_configure)

    bg_image = Image.open("menu_backgr.png").resize((500, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(new_root, width=500, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    name_var = tk.StringVar(value=utils.NAME or "")
    difficulty_var = tk.StringVar(value="normal")

    canvas.create_text(250, 80, text="Dein Name:", font=("Arial", 14), fill="black")
    name_entry = tk.Entry(new_root, textvariable=name_var, font=("Arial", 12))
    canvas.create_window(250, 110, window=name_entry)

    canvas.create_text(250, 150, text="Schwierigkeitsgrad:", font=("Arial", 14), fill="black")
    difficulty_menu = tk.OptionMenu(new_root, difficulty_var, "easy", "normal", "hard", "god")
    difficulty_menu.config(font=("Arial", 10))
    canvas.create_window(250, 180, window=difficulty_menu)

    def back_to_menu():
        start_main_menu()

    def get_name():
        return name_var.get().strip() or "Anon"

    def start_user_input_mode():
        utils.MODE = "manual"
        new_root.destroy()
        start_gui(get_name(), mode="manual", on_return=back_to_menu)

    def start_random_puzzle_mode():
        utils.MODE = difficulty_var.get()
        new_root.destroy()
        start_puzzle_gui(get_name(), mode="random", on_return=back_to_menu)

    def show_highscores():
        mode = difficulty_var.get()
        scores = get_highscores(mode)
        hs_window = tk.Toplevel(new_root)
        hs_window.title("Highscores")
        hs_window.geometry("400x300")
        tk.Label(hs_window, text=f"Top 10 ({mode})", font=("Arial", 14, "bold")).pack(pady=10)

        for idx, (name, moves, empty, score, timestamp) in enumerate(scores, start=1):
            entry_text = f"{idx}. {name} – Score: {score} (Züge: {moves}, Leer: {empty})"
            tk.Label(hs_window, text=entry_text, font=("Arial", 11)).pack(anchor="w", padx=20)

    btn1 = tk.Button(new_root, text="Zufälliges Puzzle lösen", command=start_random_puzzle_mode)
    btn2 = tk.Button(new_root, text="Eigenes Puzzle eingeben", command=start_user_input_mode)
    btn3 = tk.Button(new_root, text="Highscores anzeigen", command=show_highscores)

    canvas.create_text(250, 220, text="Puzzles selber lösen:", font=("Arial", 14), fill="black")
    canvas.create_window(250, 250, window=btn1)

    canvas.create_text(250, 290, text="Puzzles lösen lassen:", font=("Arial", 14), fill="black")
    canvas.create_window(250, 320, window=btn2)

    canvas.create_text(250, 360, text="Highscores:", font=("Arial", 14), fill="black")
    canvas.create_window(250, 390, window=btn3)

    new_root.mainloop()
