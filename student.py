'''
student.py
Student operations.

Functions:
add_student()
view_students()
search_student()
delete_student()'''

import sqlite3
from database import get_connection
from werkzeug.security import generate_password_hash

def add_student(student_id, name, branch, year, semester, email, phone, password):
    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check whether Student ID already exists
        cursor.execute(
            "SELECT 1 FROM students WHERE student_id = ?",
            (student_id,)
        )

        if cursor.fetchone():
            return False, "Student ID already exists!"

        # Validate required fields
        if not all((student_id, name, branch, year, semester, password)):
            return False, "Student ID, Name, Branch, Year, Semester, and Password are required."

        # Insert student
        cursor.execute("""
            INSERT INTO students
            (student_id, name, branch, year, semester, email, phone, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, name, branch, year, semester, email, phone, generate_password_hash(password)))

        conn.commit()
        return True, "Student added successfully!"

    except sqlite3.OperationalError as e:
        if conn:
            conn.rollback()

        if "locked" in str(e).lower():
            return False, "Database is busy. Please try again."

        raise

    except sqlite3.IntegrityError:
        if conn:
            conn.rollback()

        return False, "Student ID already exists!"

    finally:
        if conn:
            conn.close()
#add_student()

def view_students():
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("SELECT id, student_id, name, branch, year, semester, email, phone FROM students")
    students=cursor.fetchall()
    conn.close()
    return students
#view_students()

def search_student():
    conn=get_connection()
    cursor=conn.cursor()
    
    try:
        student_id=input('Enter student ID: ').strip()
    except ValueError:
        print("Please enter a valid Student ID.")
        return
    
    cursor.execute("SELECT id, student_id, name, branch, year, semester, email, phone FROM students WHERE student_id=?",(student_id,))
    student=cursor.fetchone()
    
    if student:
        print("="*50)
        print("Student ID\tStudent Name\tBranch")
        print("="*50)
        print(f"{student[0]}\t\t{student[1]}\t\t{student[2]}")
        print("="*50)
    else:
        print("Student Not Found")
    conn.close()

#search_student()
def delete_student(student_id):
    
    conn=get_connection()
    try:
        cursor=conn.cursor()
        cursor.execute("DELETE FROM attendance WHERE student_id=?", (student_id,))
        cursor.execute("DELETE FROM expenses WHERE student_id=?", (student_id,))
        cursor.execute("DELETE FROM students WHERE student_id=?",(student_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

#delete_student()

def update_student(student_id, name, branch, year, semester, email, phone, password):

    conn = get_connection()
    cursor = conn.cursor()

    if password:
        cursor.execute("""UPDATE students SET name=?, branch=?, year=?, semester=?, email=?, phone=?, password=? WHERE student_id=?""",
                       (name, branch, year, semester, email, phone, generate_password_hash(password), student_id))
    else:
        cursor.execute("""UPDATE students SET name=?, branch=?, year=?, semester=?, email=?, phone=? WHERE student_id=?""",
                       (name, branch, year, semester, email, phone, student_id))

    conn.commit()
    conn.close()
