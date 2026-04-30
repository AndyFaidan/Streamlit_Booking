import sqlite3
import os

DB_PATH = "data/database.db"

# ======================
# CONNECT DATABASE
# ======================
def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# ======================
# INIT DATABASE
# ======================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    # USERS
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        full_name TEXT,
        role TEXT
    )
    """)

    # AKUN
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
        group_id TEXT,
        status TEXT,
        checklist BOOLEAN
    )
    """)

    # BOOKING
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
