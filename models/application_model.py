from mysql.connector import Error
from models.utils import get_db_connection


def create_application(user_id, job_id, cv_filename, cover_letter):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO applications (user_id, job_id, cv_filename, cover_letter)
        VALUES (%s, %s, %s, %s)
        """,
        (user_id, job_id, cv_filename, cover_letter),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_applications_for_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT a.*, j.title AS job_title
        FROM applications a
        JOIN jobs j ON j.id = a.job_id
        WHERE a.user_id = %s
        ORDER BY a.created_at DESC
        """,
        (user_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_applications_for_job(job_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT a.*, u.name, u.email
        FROM applications a
        JOIN users u ON u.id = a.user_id
        WHERE a.job_id = %s
        ORDER BY a.created_at DESC
        """,
        (job_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_application_with_user_and_job(application_id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT a.*, u.name, u.email, j.title AS job_title
        FROM applications a
        JOIN users u ON u.id = a.user_id
        JOIN jobs j ON j.id = a.job_id
        WHERE a.id = %s
        """,
        (application_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_stats():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS open_jobs FROM jobs WHERE status = 'active'")
    open_jobs = cur.fetchone()["open_jobs"]

    cur.execute("SELECT COUNT(*) AS total_applications FROM applications")
    total_applications = cur.fetchone()["total_applications"]

    cur.execute(
        "SELECT COUNT(*) AS applications_today FROM applications WHERE DATE(created_at) = CURDATE()"
    )
    applications_today = cur.fetchone()["applications_today"]

    cur.close()
    conn.close()

    return {
        "open_jobs": open_jobs,
        "total_applications": total_applications,
        "applications_today": applications_today,
    }
