import sqlite3
import os

DB_PATH = "data/database.db"

# ======================
# CONNECT DATABASE
# ======================
def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ======================
# INIT DATABASE
# ======================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    # ======================
    # USERS
    # ======================
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        role TEXT DEFAULT 'user'
    )
    """)

    # ======================
    # SEED USERS (PENTING BANGET)
    # ======================
    users = [
        (1, "andy", "123", "Andy Sofyan Guspriyanto", "admin"),
        (2, "zedd", "1933", "Peri Romadon", "admin"),
        (3, "ariefksf", "123", "Arief Zaenal Hakim", "admin"),
    ]

    for u in users:
        c.execute("""
            INSERT OR IGNORE INTO users (id, username, password, full_name, role)
            VALUES (?, ?, ?, ?, ?)
        """, u)

    # ======================
    # AKUN
    # ======================
    c.execute("""
    CREATE TABLE IF NOT EXISTS akun_nusuk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        email TEXT NOT NULL,
        password TEXT,
        domain TEXT,
        gender TEXT,
        type TEXT,
        name_identity TEXT,
        group_id TEXT,
        status TEXT DEFAULT 'READY',
        checklist BOOLEAN DEFAULT 0,

        UNIQUE(user_id, email, gender),

        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # ======================
    # BOOKING
    # ======================
    c.execute("""
    CREATE TABLE IF NOT EXISTS booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        akun_id INTEGER NOT NULL,
        gender TEXT,
        tanggal_booking TEXT,
        qty INTEGER DEFAULT 1,
        status TEXT DEFAULT 'BOOKED',

        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(akun_id) REFERENCES akun_nusuk(id) ON DELETE CASCADE
    )
    """)

    # ======================
    # INDEX
    # ======================
    c.execute("CREATE INDEX IF NOT EXISTS idx_email ON akun_nusuk(email)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_group ON akun_nusuk(group_id)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_booking_user ON booking(user_id)")

    conn.commit()
    conn.close()
