import hashlib

from database import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(full_name, login, password):
    full_name = full_name.strip()
    login = login.strip()
    password = password.strip()

    if not full_name or not login or not password:
        return False, "Заполните все поля"

    if len(full_name) < 3:
        return False, "ФИО должно содержать минимум 3 символа"

    if len(login) < 4:
        return False, "Логин должен содержать минимум 4 символа"

    if len(password) < 6:
        return False, "Пароль должен содержать минимум 6 символов"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE login = ?",
        (login,)
    )

    if cur.fetchone():
        conn.close()
        return False, "Пользователь с таким логином уже существует"

    cur.execute(
        """
        INSERT INTO users (
            full_name,
            login,
            password,
            role_id
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            full_name,
            login,
            hash_password(password),
            2
        )
    )

    conn.commit()
    conn.close()

    return True, "Аккаунт создан"


def login_user(login, password):
    login = login.strip()
    password = password.strip()

    if not login or not password:
        return None

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            users.id,
            users.full_name,
            roles.name AS role
        FROM users
        JOIN roles
            ON roles.id = users.role_id
        WHERE users.login = ?
          AND users.password = ?
        """,
        (
            login,
            hash_password(password)
        )
    )

    user = cur.fetchone()

    conn.close()

    return user