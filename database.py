'''
database.py
Database ki sambandhinchina code.
Responsibilities:

SQLite connect cheyyadam
Tables create cheyyadam
Database initialization'''


import sqlite3
#CONNECT TO THE DATABASE
conn = sqlite3.connect("attendance_expense.db")
cursor=conn.cursor()

cursor.execute("PRAGMA foreign_keys=ON")

#CREATES STUDENT TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  branch TEXT NOT NULL,
  year INTEGER NOT NULL,
  semester INTEGER NOT NULL,
  email TEXT,
  phone TEXT
  )
  """)
#CREATES ATTENDANCE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id TEXT NOT NULL,
  attendance_date TEXT NOT NULL,
  status TEXT CHECK(status IN ('Present','Absent')) NOT NULL,
  FOREIGN KEY(student_id) REFERENCES students(student_id),
  UNIQUE (student_id,attendance_date)
  )
  """)

#CREATES EXPENSE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id TEXT NOT NULL,
  category TEXT NOT NULL,
  amount REAL NOT NULL CHECK(amount>0),
  expense_date TEXT NOT NULL,
  FOREIGN KEY(student_id) REFERENCES students(student_id)
  )
  """)
# Check whether the password column exists
cursor.execute("PRAGMA table_info(students)")
columns = [column[1] for column in cursor.fetchall()]

# Add the password column only if it is missing
if "password" not in columns:
    cursor.execute(
        "ALTER TABLE students ADD COLUMN password TEXT"
    )

conn.commit()
conn.close()



