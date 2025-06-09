# 🧩 Sudoku Solver mit GUI

Ein grafischer Sudoku-Löser mit eingebautem Generator, manueller Eingabe und Highscore-Vorbereitung – komplett in Python mit `tkinter`.

---

## 🚀 Features

- 🔢 **Sudoku lösen** per Knopfdruck (Backtracking-Algorithmus)
- ✍️ **Eigenes Sudoku eingeben** oder
- 🎲 **Zufälliges Sudoku generieren** mit wählbarem Schwierigkeitsgrad:
  - *Einfach*, *Normal*, *Schwer*, *God-Mode* (17 Zahlen)
- 🌈 Benutzeroberfläche mit Hintergrundbildern
- ⌨️ Steuerung auch per Pfeiltasten
- 🔁 Menüführung mit Rücksprungfunktion
- 🧠 **Fehlermeldungen und Validierung**
- 💾 Vorbereitet für Highscore-System mit SQLite

---

## 🖼️ Screenshots

*(Hier kannst du später 1–2 Bilder vom Hauptmenü und Spielfeld einfügen)*

---

## 🛠️ Installation

```bash
git clone https://github.com/DEINUSERNAME/Sudoku_Solver.git
cd Sudoku_Solver
python -m venv venv
venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
python main.py
