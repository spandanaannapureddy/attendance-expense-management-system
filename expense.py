'''expense.py
Expense operations.
Functions:

add_expense()
view_expenses()
delete_expense()
total_expense()'''

import sqlite3
#from datetime import date
def add_expense(student_id, category, amount, expense_date):
    conn = sqlite3.connect("attendance_expense.db")
    cursor = conn.cursor()

    try:
        # Check whether student exists
        cursor.execute(
            "SELECT student_id FROM students WHERE student_id = ?",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            return False, "Student not found!"

        # Validate amount
        try:
            amount = float(amount)

            if amount <= 0:
                return False, "Amount must be greater than zero!"

        except (ValueError, TypeError):
            return False, "Please enter a valid amount!"

        # Check for an exact duplicate expense
        cursor.execute("""
            SELECT id FROM expenses
            WHERE student_id = ?
              AND category = ?
              AND amount = ?
              AND expense_date = ?
        """, (student_id, category, amount, expense_date))

        duplicate = cursor.fetchone()

        if duplicate:
            return False, "This expense already exists!"

        # Save expense
        cursor.execute("""
            INSERT INTO expenses
            (student_id, category, amount, expense_date)
            VALUES (?, ?, ?, ?)
        """, (student_id, category, amount, expense_date))

        conn.commit()
        return True, "Expense added successfully!"

    except sqlite3.Error:
        return False, "Unable to save expense. Please try again!"

    finally:
        conn.close()
#add_expense()

def view_expense():
    conn=sqlite3.connect("attendance_expense.db")
    cursor=conn.cursor()
    
    cursor.execute("""
           SELECT expenses.id,
                   students.student_id,
                   students.name,
                   expenses.category,
                   expenses.amount,
                   expenses.expense_date
           FROM expenses
           JOIN students
           ON expenses.student_id=students.student_id""")
    expense=cursor.fetchall()

    
    conn.close()
    return expense

#view_expense()
    
def search_expense():
    
    conn=sqlite3.connect("attendance_expense.db")
    cursor=conn.cursor()
    
    try:
        student_id=int(input("Enter Student ID: "))
    except ValueError:
        print("Please Enter a valid Student ID")
        conn.close()
        return
    
    cursor.execute("""
         SELECT expenses.id,
                   students.student_id,
                   students.name,
                   expenses.category,
                   expenses.amount,
                   expenses.expense_date,
                   expenses.description
        FROM expenses
        JOIN students
        ON expenses.student_id=students.id
        WHERE expenses.student_id=?""",(student_id,))
    records=cursor.fetchall()
    
    if records:
        print("=" * 110)
        print("Expense ID\tStudent ID\tStudent Name\tCategory\tAmount\t\tDate\t\tDescription")
        print("=" * 110)
        
        for record in records:
            print(f"{record[0]}\t\t{record[1]}\t\t{record[2]}\t\t{record[3]}\t\t{record[4]}\t{record[5]}\t{record[6]}")
        print("=" * 110)
    else:
        print("No Expense Records Found")
    conn.close()
#search_expense()

def delete_expense(expense_id):
    
    conn=sqlite3.connect("attendance_expense.db")
    cursor=conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?",(expense_id,))
    conn.commit()
    conn.close()
#delete_expense()
    
def total_expense():
    
    conn=sqlite3.connect("attendance_expense.db")
    cursor=conn.cursor()
    
    student_id=int(input("Enter Student ID: "))
    cursor.execute("SELECT * FROM expenses WHERE student_id=?",(student_id,))
    student=cursor.fetchone()
    
    if student:
        
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE student_id=?",(student_id,))
        total=cursor.fetchone()[0]
        
        if total is None:
            print("Total Expense = ₹0")
        else:
            print(f"Total Expense = ₹{total}")
    else:
        print("Student Not Found")
    conn.close()
    
#total_expense()  
def update_expense(expense_id, student_id, category, amount, expense_date):
    conn = sqlite3.connect("attendance_expense.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE student_id=?",
        (student_id,)
    )
    student = cursor.fetchone()

    if not student:
        conn.close()
        return "Student Not Found"

    cursor.execute("""
        UPDATE expenses
        SET student_id=?, category=?, amount=?, expense_date=?
        WHERE id=?
    """, (student_id, category, amount, expense_date, expense_id))

    conn.commit()
    conn.close()

    return "Expense Updated Successfully"