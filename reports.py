'''reports.py
Reports generate cheyyadam.

Examples:

attendance_report()
expense_report()
monthly_report()'''

import sqlite3
from datetime import date
from database import get_connection


def total_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]

    conn.close()
    return total


def present_today():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM attendance WHERE attendance_date=? AND status='Present'", (date.today().isoformat(),))
    present = cursor.fetchone()[0]

    conn.close()
    return present


def total_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    conn.close()
    return total


def attendance_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            students.student_id,
            students.name,
            SUM(CASE WHEN attendance.status='Present' THEN 1 ELSE 0 END) AS present,
            SUM(CASE WHEN attendance.status='Absent' THEN 1 ELSE 0 END) AS absent,
            COALESCE(ROUND(
                SUM(CASE WHEN attendance.status='Present' THEN 1 ELSE 0 END) * 100.0 /
                NULLIF(COUNT(attendance.id), 0), 2
            ), 0) AS percentage

        FROM students

        LEFT JOIN attendance
        ON students.student_id = attendance.student_id

        GROUP BY students.student_id
    """)

    records = cursor.fetchall()

    conn.close()
    return records


def expense_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            students.name,
            expenses.category,
            expenses.amount,
            expenses.expense_date

        FROM expenses

        JOIN students
        ON expenses.student_id = students.student_id
    """)

    records = cursor.fetchall()

    conn.close()
    return records
