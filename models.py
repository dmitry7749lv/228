import hashlib
from database import get_connection
from config import DEFAULT_ADMIN_LOGIN, DEFAULT_ADMIN_PASSWORD


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role_id INTEGER NOT NULL,
        FOREIGN KEY (role_id) REFERENCES roles(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article TEXT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER DEFAULT 0,
        description TEXT,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )
    """)

    conn.commit()

    # Добавляем роли
    roles = ["Администратор", "Менеджер"]
    for role in roles:
        cur.execute("INSERT OR IGNORE INTO roles (name) VALUES (?)", (role,))

    # Получаем ID роли администратора
    cur.execute("SELECT id FROM roles WHERE name = 'Администратор'")
    admin_role = cur.fetchone()
    
    if admin_role:
        admin_role_id = admin_role[0] if isinstance(admin_role, tuple) else admin_role["id"]
        
        cur.execute("SELECT id FROM users WHERE login = ?", (DEFAULT_ADMIN_LOGIN,))
        
        if not cur.fetchone():
            cur.execute("""
            INSERT INTO users (full_name, login, password, role_id)
            VALUES (?, ?, ?, ?)
            """, (
                "Главный администратор",
                DEFAULT_ADMIN_LOGIN,
                hash_password(DEFAULT_ADMIN_PASSWORD),
                admin_role_id
            ))

    conn.commit()
    conn.close()