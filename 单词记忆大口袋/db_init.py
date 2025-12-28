import sqlite3

conn = sqlite3.connect('srs.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, sleep_hours REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY,
    word TEXT,
    difficulty REAL,
    last_review INTEGER,
    ef REAL DEFAULT 2.5,
    interval INTEGER DEFAULT 0,
    reps INTEGER DEFAULT 0,
    remaining_memory REAL DEFAULT 1.0
)''')
c.execute('''CREATE TABLE IF NOT EXISTS daily_log (
    date TEXT PRIMARY KEY,
    sleep REAL,
    afternoon_hours REAL,
    evening_hours REAL,
    avg_difficulty REAL,
    load_last_hour INTEGER,
    mu_predicted REAL,
    new_cards INTEGER,
    reviews_done INTEGER,
    correct_24h REAL
)''')

import datetime
today = datetime.date.today().isoformat()
c.execute("INSERT OR IGNORE INTO daily_log (date) VALUES (?)", (today,))

conn.commit()
conn.close()
print("数据库建好了！")
