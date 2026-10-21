import sqlite3


def search_expense(keyword):
    conn = sqlite3.connect("attendance_expense.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT expenses.id,
               students.student_id,
               students.name,
               expenses.category,
               expenses.amount,
               expenses.expense_date
        FROM expenses
        JOIN students
        ON expenses.student_id = students.student_id
        WHERE CAST(students.student_id AS TEXT) LIKE ?
           OR students.name LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    records = cursor.fetchall()
    conn.close()

    return records