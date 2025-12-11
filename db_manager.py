import sqlite3
import datetime

DB_NAME = "stress_data.db"

def init_db():
    """Creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, emotion TEXT, intensity INTEGER)''')
    conn.commit()
    conn.close()

def log_stress(emotion, intensity):
    """
    Saves a new entry.
    emotion: string (e.g., "High Stress", "Calm")
    intensity: int (0-10)
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Save current time in HH:MM:SS format
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    c.execute("INSERT INTO history (timestamp, emotion, intensity) VALUES (?, ?, ?)", 
              (current_time, emotion, intensity))
    conn.commit()
    conn.close()

def get_recent_history(limit=7):
    """Returns the last 'limit' entries for the graph."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT timestamp, intensity FROM history ORDER BY id DESC LIMIT ?", (limit,))
    data = c.fetchall()
    conn.close()
    # Reverse so the graph goes from Left (Old) -> Right (New)
    return data[::-1]

# Initialize DB when this file is imported
init_db()