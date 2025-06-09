import sqlite3
from datetime import datetime

DB_NAME = "highscores.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mode TEXT NOT NULL,
            moves INTEGER NOT NULL,
            empty INTEGER NOT NULL,
            score INTEGER NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def save_score(name, mode, moves, empty, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO scores (name, mode, moves, empty, score)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, mode, moves, empty, score))
    conn.commit()
    conn.close()


def get_highscores(mode, limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT name, moves, empty, score, timestamp
        FROM scores
        WHERE mode = ?
        ORDER BY score DESC, moves ASC
        LIMIT ?
    ''', (mode, limit))
    results = c.fetchall()
    conn.close()
    return results
