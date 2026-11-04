'''
attendance.py

Attendance operations.
Functions:

mark_attendance()
view_attendance()
search_attendance()
delete_attendance()
calculate_percentage()
'''

import sqlite3
from datetime import date
from database import get_connection


def mark_attendance(student_id, attendance_date, status):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        try:
            date.fromisoformat(attendance_date or "")
        except ValueError:
            return "Please enter a valid attendance date"
        # Validate attendance status
        if status not in ("Present", "Absent"):
            return "Invalid attendance status"

        # Check whether student exists
        cursor.execute(
            "SELECT 1 FROM students WHERE student_id = ?",
            (student_id,)
        )

        if not cursor.fetchone():
            return "Student not found"

        # Check whether attendance already exists for this date
        cursor.execute("""
            SELECT id FROM attendance
            WHERE student_id = ? AND attendance_date = ?
        """, (student_id, attendance_date))

        if cursor.fetchone():
            return "Attendance already marked for this student on this date"

        # Insert attendance only if no record exists
        cursor.execute("""
            INSERT INTO attendance
            (student_id, attendance_date, status)
            VALUES (?, ?, ?)
        """, (student_id, attendance_date, status))

        conn.commit()
        return "Attendance Marked Successfully"

    except sqlite3.IntegrityError:
        conn.rollback()
        return "Duplicate attendance is not allowed for this date"

    except sqlite3.OperationalError as e:
        conn.rollback()

        if "locked" in str(e).lower():
            return "Database is busy. Please try again"
    
        return "Unable to save attendance. Please try again"
    finally:
        conn.close()
#mark_attendance()

def view_attendance():
    
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("""
                    SELECT attendance.id,
                    students.student_id,
                    students.name,
                    attendance.attendance_date,
                    attendance.status
    FROM attendance
    JOIN students
    ON attendance.student_id=students.student_id
    """)
    attendance=cursor.fetchall()


    conn.close()
    return attendance

#view_attendance()
def search_attendance():
    
    conn=get_connection()
    cursor=conn.cursor()
    
    try:
        student_id=input("Enter Student ID: ").strip()
    except ValueError:
        print("Please Enter a valid Student ID")
        conn.close()
        return
    
    cursor.execute("""
            SELECT attendance.id,
                   students.student_id,
                   students.name,
                   attendance.attendance_date,
                   attendance.status
            FROM attendance
            JOIN students
            ON attendance.student_id=students.student_id
            WHERE attendance.student_id=?""",(student_id,))
    records=cursor.fetchall()
    
    if records:
        print("="*75)
        print("Attendance ID\tStudent ID\tStudent Name\tDate\t\tStatus")
        print("="*75)
        
        for record in records:
            print(f"{record[0]}\t\t{record[1]}\t\t{record[2]}\t\t{record[3]}\t{record[4]}")
        print("="*75)
    else:
        print("Records Not Found")
    conn.close()
#search_attendance()



def delete_attendance(attendance_id):
    
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("DELETE FROM attendance WHERE id=?",(attendance_id,))
    conn.commit()
    conn.close()
#delete_attendance()


def attendance_percentage():
    
    conn=get_connection()
    cursor=conn.cursor()
    
    student_id=int(input("Enter Student ID: "))
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=?",(student_id,))
    total_classes=cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'",(student_id,))
    present_classes=cursor.fetchone()[0]
    
    if total_classes>0:
        percentage=(present_classes/total_classes)*100
        print(f'Attendance Percentage:{percentage:.2f}%')
    else:
        print('No Attendance Records Found')
#attendance_percentage()
def update_attendance(attendance_id, attendance_date, status):
    conn = get_connection()
    try:
        try:
            date.fromisoformat(attendance_date or "")
        except ValueError:
            return "Please enter a valid attendance date"
        if status not in ("Present", "Absent"):
            return "Invalid attendance status"
        conn.execute("UPDATE attendance SET attendance_date=?, status=? WHERE id=?",
                     (attendance_date, status, attendance_id))
        conn.commit()
        return "Attendance updated successfully"
    except sqlite3.IntegrityError:
        conn.rollback()
        return "Attendance already exists for this student on that date"
    finally:
        conn.close()
