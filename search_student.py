import sqlite3


def search_students(keyword):
    conn = sqlite3.connect("attendance_expense.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM students
        WHERE CAST(student_id AS TEXT) LIKE ?
           OR name LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    records = cursor.fetchall()
    conn.close()

    return records