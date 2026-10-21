'''
student.py
Student operations.

Functions:
add_student()
view_students()
search_student()
delete_student()'''

import sqlite3

def add_student(student_id, name, branch, year, semester, email, phone, password):
    conn = None

    try:
        conn = sqlite3.connect("attendance_expense.db", timeout=10)
        cursor = conn.cursor()

        # Check whether Student ID already exists
        cursor.execute(
            "SELECT 1 FROM students WHERE student_id = ?",
            (student_id,)
        )

        if cursor.fetchone():
            return False, "Student ID already exists!"

        # Validate required fields
        if not student_id or not name or not branch:
            return False, "Student ID, Name and Branch are required."

        # Insert student
        cursor.execute("""
            INSERT INTO students
            (student_id, name, branch, year, semester, email, phone, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, name, branch, year, semester, email, phone, password))

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
    conn=sqlite3.connect("attendance_expense.db")
    cursor=conn.cursor()
    
    cursor.execute("SELECT * FROM students")
    students=cursor.fetchall()
    conn.close()
    return students
#view_students()

def search_student():
    conn=sqlite3.connect("attendance_expense.db")
    cursor=conn.cursor()
    
    try:
        student_id=int(input('Enter student ID: '))
    except ValueError:
        print("Please enter a valid Student ID.")
        return
    
    cursor.execute("SELECT * FROM students WHERE id=?",(student_id,))
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
    
    conn=sqlite3.connect("attendance_expense.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id=?",(student_id,))
    conn.commit()
    conn.close()

#delete_student()

def update_student(student_id, name, branch, year, semester, email, phone, password):

    conn = sqlite3.connect("attendance_expense.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name=?,
            branch=?,
            year=?,
            semester=?,
            email=?,
            phone=?,
            password=?
        WHERE student_id=?
    """, (name, branch, year, semester, email, phone, password, student_id))

    conn.commit()
    conn.close()