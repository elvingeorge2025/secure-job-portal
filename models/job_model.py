from mysql.connector import Error
from models.utils import get_db_connection


def search_jobs(q="", location="", category=""):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    query = "SELECT * FROM jobs WHERE status = 'active'"
    params = []

    if q:
        query += " AND (title LIKE %s OR description LIKE %s)"
        like = f"%{q}%"
        params.extend([like, like])
    if location:
        query += " AND location LIKE %s"
        params.append(f"%{location}%")
    if category:
        query += " AND category LIKE %s"
        params.append(f"%{category}%")

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_job_by_id(job_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def create_job(title, description, requirements, salary, location, category, created_by):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO jobs (title, description, requirements, salary, location, category, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (title, description, requirements, salary, location, category, created_by),
    )
    conn.commit()
    cur.close()
    conn.close()


def update_job(job_id, title, description, requirements, salary, location, category, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE jobs
        SET title=%s, description=%s, requirements=%s, salary=%s,
            location=%s, category=%s, status=%s
        WHERE id=%s
        """,
        (title, description, requirements, salary, location, category, status, job_id),
    )
    conn.commit()
    cur.close()
    conn.close()


def delete_job(job_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
    conn.commit()
    cur.close()
    conn.close()


def get_jobs_with_counts():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT j.*, COUNT(a.id) AS app_count
        FROM jobs j
        LEFT JOIN applications a ON a.job_id = j.id
        GROUP BY j.id
        ORDER BY j.created_at DESC
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
