from database import get_connection


def search_attendance(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT attendance.id,
               students.student_id,
               students.name,
               attendance.attendance_date,
               attendance.status
        FROM attendance
        JOIN students
        ON attendance.student_id = students.student_id
        WHERE CAST(students.student_id AS TEXT) LIKE ?
           OR students.name LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    records = cursor.fetchall()
    conn.close()

    return records
