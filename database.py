import sqlite3
import os

os.makedirs("data", exist_ok=True)

DB_PATH = "data/workforce.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Employee Master

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id TEXT PRIMARY KEY,
    biometric_id TEXT UNIQUE,
    worker_name TEXT NOT NULL,
    contractor_name TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT DEFAULT 'Active'
)
""")

# Category Rates

cursor.execute("""
CREATE TABLE IF NOT EXISTS category_rates (
    category TEXT PRIMARY KEY,
    hourly_rate REAL NOT NULL,
    ot_multiplier REAL NOT NULL
)
""")

# Default Categories

cursor.execute("""
INSERT OR IGNORE INTO category_rates
VALUES ('Unskilled',100,2)
""")

cursor.execute("""
INSERT OR IGNORE INTO category_rates
VALUES ('Semi-Skilled',120,2)
""")

cursor.execute("""
INSERT OR IGNORE INTO category_rates
VALUES ('Skilled',150,2)
""")

cursor.execute("""
INSERT OR IGNORE INTO category_rates
VALUES ('High-Skilled',200,2)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    biometric_id TEXT,
    date TEXT,
    check_in TEXT,
    check_out TEXT,
    working_hours REAL,
    ot_hours REAL,
    source TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")