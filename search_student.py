from database import get_connection


def search_students(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, student_id, name, branch, year, semester, email, phone
        FROM students
        WHERE CAST(student_id AS TEXT) LIKE ?
           OR name LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    records = cursor.fetchall()
    conn.close()

    return records
