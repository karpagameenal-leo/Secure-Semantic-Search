import sqlite3

DB_FILE = "company_data.db"

def init_mock_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            security_rating TEXT NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ("ProtonMail Plus", "Software", 4.99, 9999, "A+"),
            ("ProtonVPN Visionary", "Software", 9.99, 500, "A+"),
            ("Encrypted Storage Drive", "Hardware", 89.99, 120, "A"),
            ("Hardware Security Key", "Hardware", 45.00, 350, "A+"),
            ("Standard Router", "Hardware", 59.99, 10, "B")
        ]
        cursor.executemany("INSERT INTO products (name, category, price, stock, security_rating) VALUES (?, ?, ?, ?, ?)", mock_data)
        conn.commit()
    conn.close()

def execute_read_query(sql_query: str) -> list:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = lambda cursor, row: dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    return results