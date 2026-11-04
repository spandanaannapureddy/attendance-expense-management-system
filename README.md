##Attendance & Expense Management System

## About the Project

The Attendance & Expense Management System is a web application developed to manage student details, attendance, and expenses in one place. I built this project using Python Flask, HTML, CSS, and SQLite.

The main aim of this project is to make student record management easier and more organized.

## Features

* **Admin Login:** Allows the administrator to log in to the system.
* **Student Management:** Add, view, search, and delete student details.
* **Attendance Management:** Record and manage students' attendance.
* **Expense Management:** Add and track expense details.
* **Search Records:** Search for student, attendance, and expense information.
* **Reports:** View attendance and expense summaries.
* **Dashboard:** Access the main features through a simple interface.

## Technologies Used

* HTML
* CSS
* Python
* Flask
* SQLite
* Git and GitHub
* Render

## How to Run the Project

1. Clone this repository:

   ```bash
   git clone https://github.com/spandanaannapureddy/attendance-expense-management-system.git
   ```

2. Open the project folder:

   ```bash
   cd attendance-expense-management-system
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create the database tables (stored in the `instance` folder by default):

   ```bash
   python database.py
   ```

5. Run the application:

   ```bash
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

## Live Demo

**Live Website:** [Attendance & Expense Management System](https://attendance-expense-management-system.onrender.com)

## Configuration

The application uses SQLite. Set `DATABASE_PATH` to a persistent writable location when deploying (for example, a mounted persistent disk); otherwise the database is stored at `instance/attendance_expense.db` beside the application. The app creates or upgrades its tables automatically at startup.

Set these environment variables for deployment:

* `SECRET_KEY`: a long random secret used to sign sessions.
* `ADMIN_USERNAME` and `ADMIN_PASSWORD`: the administrator login. The defaults (`admin` / `admin123`) are for local demonstration only and should be replaced before deployment.
* `DATABASE_PATH`: optional full path to the SQLite database file.

Student passwords are stored as hashes. Older databases with plain text passwords continue to work; a password is converted to a hash after the student's next successful login.

## What I Learned

While developing this project, I learned how to build a web application using Flask, connect Python with SQLite, manage project files using Git and GitHub, and deploy a website using Render.

## Future Improvements

* Improve login security.
* Add more detailed reports.
* Improve the website for mobile devices.
* Use persistent database storage for online deployment.
