from flask import Flask,render_template,request,redirect,url_for,session,flash
import database
from database import get_connection
from werkzeug.security import check_password_hash, generate_password_hash
from student import add_student,view_students,delete_student,update_student
from attendance import mark_attendance,view_attendance,delete_attendance,update_attendance
from expense import add_expense,view_expense,delete_expense,update_expense
from search_student import search_students
from search_attendance import search_attendance
from search_expense import search_expense
from reports import *
from datetime import date
app=Flask(__name__)
import os
import secrets
app.secret_key=os.environ.get("SECRET_KEY") or secrets.token_hex(32)
import sqlite3

database.init_db()

@app.before_request
def protect_pages():
    path = request.path
    if path in {"/", "/login", "/student_login", "/student_logout"} or path.startswith("/static/"):
        return None
    student_paths = {"/student", "/student_dashboard", "/my_attendance", "/my_expenses", "/profile", "/student_reports"}
    if path in student_paths:
        if "student_id" not in session:
            return redirect(url_for("student_login_page"))
        conn = get_connection()
        exists = conn.execute("SELECT 1 FROM students WHERE student_id=?", (session["student_id"],)).fetchone()
        conn.close()
        if not exists:
            session.clear()
            return redirect(url_for("student_login_page"))
        return None
    if path == "/logout":
        return None
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

@app.after_request
def prevent_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/student_login")
def student_login_page():
    return render_template("student_login.html")

@app.route("/admin")
def admin():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE attendance_date=? AND status=?",(date.today().isoformat(),"Present"))
    total_present=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE attendance_date=? AND status=?",(date.today().isoformat(),"Absent"))
    total_absent=cursor.fetchone()[0]
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total_expense=cursor.fetchone()[0]
    if total_expense is None:
        total_expense=0
    attendance_list=view_attendance()
    expense_list=view_expense()
    conn.close()
    return render_template("adminboard.html",attendance=attendance_list,expense=expense_list,total_students=total_students,total_present=total_present,total_absent=total_absent,total_expense=total_expense)

@app.route("/login",methods=["POST"])
def check_login():
    username=request.form["username"]
    password=request.form["password"]
    if username==os.environ.get("ADMIN_USERNAME", "admin") and password==os.environ.get("ADMIN_PASSWORD", "admin123"):
        session.clear()
        session["admin_logged_in"] = True
        return redirect(url_for("admin"))
    flash("Invalid username or password!", "error")
    return redirect(url_for("login"))

@app.route("/student_login",methods=["POST"])
def student_login():
    student_id=request.form.get("student_id")
    password=request.form.get("password")
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT password FROM students WHERE student_id=?",(student_id,))
    row=cursor.fetchone()
    stored_password = row["password"] if row else None
    valid_password = False
    if stored_password and password:
        if stored_password.startswith(("pbkdf2:", "scrypt:")):
            valid_password = check_password_hash(stored_password, password)
        else:
            valid_password = stored_password == password
            if valid_password:
                cursor.execute("UPDATE students SET password=? WHERE student_id=?", (generate_password_hash(password), student_id))
                conn.commit()
    conn.close()
    if row and valid_password:
        session.clear()
        session["student_id"]=student_id
        return redirect(url_for("student_dashboard"))
    else:
        flash("Invalid Student ID or Password!", "error")
        return redirect(url_for("student_login_page"))
@app.route("/students")
def students():
    student_list=view_students()
    return render_template("students.html",students=student_list)

@app.route("/search_students", methods=["GET"])
def search_students_route():
    keyword = request.args.get("keyword", "").strip()

    if keyword:
        student_list = search_students(keyword)
    else:
        student_list = view_students()

    return render_template(
        "students.html",
        students=student_list,
        keyword=keyword
    )


@app.route("/add_student")
def add_student_page():
    return render_template("add_student.html")

@app.route("/save_student",methods=["POST"])
def save_student():
    student_id=request.form.get("student_id")
    name=request.form.get("name", "")
    branch=request.form.get("branch", "")
    year=request.form.get("year", "")
    semester=request.form.get("semester", "")
    email=request.form.get("mail", "")
    phone=request.form.get("phone", "")
    password=request.form.get("password", "")

    success, message = add_student(
    student_id, name, branch, year, semester, email, phone, password)

    if success:
        return redirect(url_for("students"))

    return render_template("add_student.html", error=message)
@app.route("/delete_student/<student_id>", methods=["POST"])
def delete_student_route(student_id):
    delete_student(student_id)
    flash("Student and related records deleted successfully.", "success")
    return redirect(url_for("students"))

@app.route("/edit_student/<student_id>")
def edit_student_page(student_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE student_id=?",
        (student_id,)
    )

    student = cursor.fetchone()

    conn.close()

    return render_template(
        "edit_student.html",
        student=student
    )


@app.route("/update_student", methods=["POST"])
def update_student_route():

    student_id = request.form.get("student_id")
    name = request.form.get("name")
    branch = request.form.get("branch")
    year = request.form.get("year")
    semester = request.form.get("semester")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")

    update_student(
        student_id,
        name,
        branch,
        year,
        semester,
        email,
        phone,
        password
    )

    return redirect(url_for("students"))

@app.route("/attendance")
def attendance():
    attendance_list=view_attendance()
    return render_template("attendance.html",attendance=attendance_list)

@app.route("/search_attendance", methods=["GET"])
def search_attendance_route():
    keyword = request.args.get("keyword", "").strip()

    if keyword:
        attendance_records = search_attendance(keyword)
    else:
        attendance_records = view_attendance()

    return render_template(
        "attendance.html",
        attendance=attendance_records,
        keyword=keyword
    )


@app.route("/add_attendance")
def add_attendance_page():
    return render_template("add_attendance.html")

@app.route("/save_attendance",methods=["POST"])
def save_attendance():
    student_id=request.form.get("student_id")
    attendance_date=request.form.get("attendance_date")
    status=request.form.get("status")
    result=mark_attendance(student_id,attendance_date,status)
    if result == "Attendance Marked Successfully":
        flash(result, "success")
        return redirect(url_for("attendance"))
    else:
        flash(result, "error")
        return redirect(url_for("add_attendance_page"))

@app.route("/delete_attendance/<attendance_id>", methods=["POST"])
def delete_attendance_route(attendance_id):
    delete_attendance(attendance_id)
    flash("Attendance deleted successfully.", "success")
    return redirect(url_for("attendance"))

@app.route("/edit_attendance/<attendance_id>")
def edit_attendance_page(attendance_id):
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
        WHERE attendance.id = ?
    """, (attendance_id,))

    record = cursor.fetchone()
    conn.close()

    if record is None:
        return "Attendance record not found", 404

    return render_template("edit_attendance.html", record=record)


@app.route("/update_attendance", methods=["POST"])
def update_attendance_route():
    attendance_id = request.form.get("attendance_id")
    attendance_date = request.form.get("attendance_date")
    status = request.form.get("status")

    result = update_attendance(attendance_id, attendance_date, status)
    flash(result, "success" if result == "Attendance updated successfully" else "error")
    return redirect(url_for("attendance"))

@app.route("/expenses")
def expenses():
    expense_list=view_expense()
    return render_template("expenses.html",expense=expense_list)

@app.route("/add_expense")
def add_expense_page():
    return render_template("add_expense.html")

@app.route("/search_expenses", methods=["GET"])
def search_expenses_route():
    keyword = request.args.get("keyword", "").strip()

    if keyword:
        expense_list = search_expense(keyword)
    else:
        expense_list = view_expense()

    return render_template(
        "expenses.html",
        expense=expense_list,
        keyword=keyword
    )

@app.route("/save_expense",methods=["POST"])
def save_expense():
    student_id=request.form.get("student_id")
    category=request.form.get("category")
    amount=request.form.get("amount")
    expense_date=request.form.get("expense_date")

    success,message=add_expense(student_id,category,amount,expense_date)
    if success:
        flash(message, "success")
        return redirect(url_for("expenses"))

    flash(message, "error")
    return redirect(url_for("add_expense_page"))

@app.route("/delete_expense/<expense_id>", methods=["POST"])
def delete_expense_route(expense_id):
    delete_expense(expense_id)
    flash("Expense deleted successfully!", "success")
    return redirect(url_for("expenses"))

@app.route("/reports")
def reports():
    return render_template("reports.html",total_students=total_students(),present_today=present_today(),total_expenses=total_expenses(),attendance=attendance_report(),expenses=expense_report())

@app.route("/student")
def student():
    return redirect(url_for("student_dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/student_dashboard")
def student_dashboard():
    student_id=session["student_id"]
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'",(student_id,))
    present_days=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Absent'",(student_id,))
    absent_days=cursor.fetchone()[0]
    cursor.execute("SELECT IFNULL(SUM(amount),0) FROM expenses WHERE student_id=?",(student_id,))
    total_expenses=cursor.fetchone()[0]
    total_days=present_days+absent_days
    if total_days>0:
        attendance_percentage=round((present_days/total_days)*100)
    else:
        attendance_percentage=0

    
    cursor.execute("SELECT attendance_date,status FROM attendance WHERE student_id=? ORDER BY attendance_date DESC LIMIT 5",(student_id,))
    attendance=cursor.fetchall()
    cursor.execute("SELECT expense_date,category,amount FROM expenses WHERE student_id=? ORDER BY expense_date DESC LIMIT 5",(student_id,))
    expenses=cursor.fetchall()
    conn.close()

    return render_template("student_dashboard.html",attendance_percentage=attendance_percentage,present_days=present_days,absent_days=absent_days,total_expenses=total_expenses,attendance=attendance,expenses=expenses)

@app.route("/my_attendance")
def my_attendance():
    conn=get_connection()
    cursor=conn.cursor()
    student_id=session["student_id"]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'",(student_id,))
    present_days=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Absent'",(student_id,))
    absent_days=cursor.fetchone()[0]
    total_days=present_days+absent_days
    if total_days>0:
        attendance_percentage=round((present_days/total_days)*100)
    else:
        attendance_percentage=0

    cursor.execute("SELECT attendance_date,status FROM attendance WHERE student_id=? ORDER BY attendance_date DESC",(student_id,) )
    attendance=cursor.fetchall()
    conn.close()
    return render_template("my_attendance.html",total_days=total_days,present_days=present_days,attendance_percentage=attendance_percentage,attendance=attendance)

@app.route("/my_expenses")
def my_expenses():
    conn=get_connection()
    cursor=conn.cursor()
    student_id=session["student_id"]
    cursor.execute("SELECT IFNULL(SUM(amount),0) FROM expenses WHERE student_id=?",(student_id,))
    total_expenses=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM expenses WHERE student_id=?",(student_id,))
    total_transactions=cursor.fetchone()[0]
    cursor.execute("SELECT IFNULL(MAX(amount),0) FROM expenses WHERE student_id=?",(student_id,))
    highest_expense=cursor.fetchone()[0]
    cursor.execute("SELECT expense_date,category,amount FROM expenses WHERE student_id=? ORDER BY expense_date DESC",(student_id,))
    expenses=cursor.fetchall()
    conn.close()
    return render_template("my_expenses.html",total_expenses=total_expenses,total_transactions=total_transactions,highest_expense=highest_expense,expenses=expenses)


@app.route("/edit_expense/<int:expense_id>")
def edit_expense_page(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, student_id, category, amount, expense_date
        FROM expenses
        WHERE id=?
    """, (expense_id,))

    record = cursor.fetchone()
    conn.close()

    if record is None:
        return "Expense record not found", 404

    return render_template("edit_expense.html", record=record)

@app.route("/update_expense", methods=["POST"])
def update_expense_route():
    expense_id = request.form.get("expense_id")
    student_id = request.form.get("student_id")
    category = request.form.get("category")
    amount = request.form.get("amount")
    expense_date = request.form.get("expense_date")

    result = update_expense(
        expense_id, student_id, category, amount, expense_date
    )

    if result != "Expense Updated Successfully":
        flash(result, "error")
        return redirect(url_for("edit_expense_page", expense_id=expense_id))

    flash(result, "success")
    return redirect(url_for("expenses"))

@app.route("/profile")
def profile():
    student_id=session["student_id"]
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT name,student_id,branch,year,semester,email,phone FROM students WHERE student_id=?",(student_id,))
    student=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'",(student_id,))
    present_days=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Absent'",(student_id,))
    absent_days=cursor.fetchone()[0]
    cursor.execute("SELECT IFNULL(SUM(amount),0) FROM expenses WHERE student_id=?",(student_id,))
    total_expenses=cursor.fetchone()[0]
    total_days=present_days+absent_days
    if total_days>0:
        attendance_percentage=round((present_days/total_days)*100)
    else:
        attendance_percentage=0

    conn.close()
    return render_template("profile.html",student=student,attendance_percentage=attendance_percentage,total_expenses=total_expenses)

@app.route("/student_reports")
def student_reports():
    student_id=session["student_id"]
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'",(student_id,))
    present_days=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Absent'",(student_id,))
    absent_days=cursor.fetchone()[0]
    cursor.execute("SELECT IFNULL(SUM(amount),0) FROM expenses WHERE student_id=?",(student_id,))
    total_expenses=cursor.fetchone()[0]
    total_days=present_days+absent_days
    if total_days>0:
        attendance_percentage=round((present_days/total_days)*100)
    else:
        attendance_percentage=0
    cursor.execute("SELECT COUNT(*) FROM expenses WHERE student_id=?",(student_id,))
    total_transactions=cursor.fetchone()[0]
    cursor.execute("SELECT IFNULL(MAX(amount),0) FROM expenses WHERE student_id=?",(student_id,))
    highest_expense=cursor.fetchone()[0]
    conn.close()
    return render_template("student_reports.html",total_days=total_days,present_days=present_days,absent_days=absent_days,attendance_percentage=attendance_percentage,total_expenses=total_expenses,total_transactions=total_transactions,highest_expense=highest_expense)

@app.route("/student_logout")
def student_logout():
    session.clear()
    return redirect(url_for("student_login_page"))




if __name__== "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")


