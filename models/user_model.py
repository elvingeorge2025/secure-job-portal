from mysql.connector import Error
from models.utils import get_db_connection
from security.password_utils import hash_password


def get_user_by_email(email):
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        return user
    except Error:
        return None
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass


def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cur.fetchone()
    except Error:
        return None
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass


def create_user(name, email, phone, password, role="applicant"):
    pwd_hash = hash_password(password)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (name, email, phone, password_hash, role)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (name, email, phone, pwd_hash, role),
    )
    conn.commit()
    user_id = cur.lastrowid
    cur.close()
    conn.close()
    return user_id


def update_user_profile(user_id, name, phone, bio):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE users
        SET name = %s, phone = %s, bio = %s
        WHERE id = %s
        """,
        (name, phone, bio, user_id),
    )
    conn.commit()
    cur.close()
    conn.close()
