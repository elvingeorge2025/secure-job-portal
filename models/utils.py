import mysql.connector
from mysql.connector import Error
from flask import current_app
import os
from config import Config
import logging


def get_db_connection():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
    )


def init_db(app):
    # Setup logging
    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
    logging.basicConfig(
        filename=Config.LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    # Simple connectivity check
    try:
        conn = get_db_connection()
        conn.close()
    except Error as e:
        app.logger.error(f"Database connection failed: {e}")


def get_upload_folder():
    return Config.UPLOAD_FOLDER


def log_action(user_id, action, details, ip_address):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO audit_logs (user_id, action, details, ip_address)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, action, details, ip_address),
        )
        conn.commit()
    except Error as e:
        logging.error(f"Failed to log action: {e}")
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass
