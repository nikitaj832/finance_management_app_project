import sqlite3
import hashlib

def get_db_connection():
    return sqlite3.connect("finance_app.db")

def create_user_table():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    create_user_table()
    password_hash = hash_password(password)
    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
            conn.commit()
        print("✅ Registration successful.")
    except sqlite3.IntegrityError:
        print("❌ Username already exists.")

def login_user(username, password):
    password_hash = hash_password(password)
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT id FROM users WHERE username=? AND password_hash=?", (username, password_hash))
        result = cursor.fetchone()
        if result:
            print("✅ Login successful.")
            return result[0]  # user_id
        else:
            print("❌ Invalid credentials.")
            return None
