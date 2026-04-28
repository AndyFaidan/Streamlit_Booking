
import sqlite3, os

DB_PATH = "data/database.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS akun_nusuk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        email TEXT,
        password TEXT,
        domain TEXT,
        gender TEXT,
        type TEXT,
        name_identity TEXT,
        status TEXT,
        checklist BOOLEAN
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        akun_id INTEGER,
        gender TEXT,
        tanggal_booking TEXT,
        qty INTEGER,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
