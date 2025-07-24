# Income and Expense Tracking
from db import get_db_connection
from datetime import datetime

def create_transaction_table():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                type TEXT CHECK(type IN ('income', 'expense')),
                amount REAL,
                category TEXT,
                date TEXT,
                note TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()

# ✅ Add Income or Expense
def add_transaction(user_id, t_type, amount, category, note=""):
    create_transaction_table()
    date = datetime.now().strftime('%Y-%m-%d')
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO transactions (user_id, type, amount, category, date, note)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, t_type, amount, category, date, note))
        conn.commit()
        print(f"✅ {t_type.capitalize()} transaction added.")

# 🔍 View all Income and Expense Entries
def view_transactions(user_id):
    with get_db_connection() as conn:
        rows = conn.execute("SELECT id, type, amount, category, date, note FROM transactions WHERE user_id=?", (user_id,)).fetchall()
        for row in rows:
            print(row)

# 🔁 Update Income or Expense Entry
def update_transaction(user_id, trans_id, amount=None, category=None, note=None):
    with get_db_connection() as conn:
        # Check ownership and transaction type
        current = conn.execute("SELECT id, amount, category, note FROM transactions WHERE id=? AND user_id=?", (trans_id, user_id)).fetchone()
        if not current:
            print("Transaction not found or not yours.")
            return

        new_amount = amount if amount is not None else current[1]
        new_category = category if category is not None else current[2]
        new_note = note if note is not None else current[3]

        conn.execute('''
            UPDATE transactions
            SET amount=?, category=?, note=?
            WHERE id=? AND user_id=?
        ''', (new_amount, new_category, new_note, trans_id, user_id))
        conn.commit()
        print("Transaction updated.")

# ❌ Delete Income or Expense Entry
def delete_transaction(user_id, trans_id):
    with get_db_connection() as conn:
        result = conn.execute("DELETE FROM transactions WHERE id=? AND user_id=?", (trans_id, user_id))
        conn.commit()
        if result.rowcount > 0:
            print("Transaction deleted.")
        else:
            print("❌ Transaction not found or not yours.")
