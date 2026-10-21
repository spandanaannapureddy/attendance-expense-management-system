'''
main.py
Project entry point.
User menu ikkada untundi.
Example:
1. Student Management
2. Attendance Management
3. Expense Management
4. Reports
5. Exit
User option select chesthe corresponding module call avutundi.'''


import student
import attendance
import expense

while True:
    print("\n========= STUDENT ATTENDANCE & EXPENSE SYSTEM =========")
    print("1. Student Management")
    print("2. Attendance Management")
    print("3. Expense Management")
    print("4. Reports")
    print("5. Exit")
    
    try:
        choice=int(input("Enter Your Choice: "))
    except ValueError:
        print("Please enter a valid choice")
        continue

    if choice==1:
        while True:
            print("\n====== STUDENT MENU =====")
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Delete Student")
            print("5. Exit")
            
            try:
                ch=int(input("Enter Your Choice: "))
            except ValueError:
                print("Please enter a valid choice")
                continue
            
            if ch==1:
                student.add_student()
            elif ch==2:
                student.view_students()
            elif ch==3:
                student.search_student()
            elif ch==4:
                student.delete_student()
            elif ch==5:
                break
            else:
                print("Invalid Choice")
                
    elif choice==2:
        
        while True:
            print("\n===== ATTENDANCE MENU =====")
            print("1. mark attendance")
            print("2. view attendance")
            print("3. search attendance")
            print("4. delete attendance")
            print("5. attendance percentage")
            print("6. back")
            
            try:
                ch=int(input("Enter Your Choice: "))
            except ValueError:
                print("Please enter a valid choice")
                continue
                
            if ch==1:
                attendance.mark_attendance()
            elif ch==2:
                attendance.view_attendance()
            elif ch==3:
                attendance.search_attendance()
            elif ch==4:
                attendance.delete_attendance()
            elif ch==5:
                attendance.attendance_percentage()
            elif ch==6:
                break
            else:
                print("Invalid Choice")
            
    elif choice==3:
        while True:
            print("\n===== EXPENSE MENU =====")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Search Expense")
            print("4. Delete Expense")
            print("5. Total Expense")
            print("6. Back")
                
            try:
                ch=int(input("Enter Your Choice: "))
            except ValueError:
                print("Please enter a valid choice")
                continue
                
            if ch==1:
                expense.add_expense()
            elif ch==2:
                expense.view_expenses()
            elif ch==3:
                expense.search_expense()
            elif ch==4:
                expense.delete_expense()
            elif ch==5:
                expense.total_expense()
            elif ch==6:
                break
            else:
                print("Invalid Choice")
    elif choice==4:
        while True:
            print("\n===== REPORTS =====")
            print("1. View Students")
            print("2. View Attendance")
            print("3. View Expenses")
            print("4. Attendance Percentage")
            print("5. Total Expense")
            print("6. Back")
                
            try:
                ch=int(input("Enter Your Choice: "))
            except ValueError:
                print("Please enter a valid choice")
                continue
                
            if ch==1:
                student.view_students()
            elif ch==2:
                attendance.view_attendance()
            elif ch==3:
                expense.view_expenses()
            elif ch==4:
                attendance.attendance_percentage()
            elif ch==5:
                expense.total_expense()
            elif ch==6:
                break
            else:
                print("Invalid Choice")
                
    elif choice==5:
        print("Thank You for Using Student Attendance & Expense System!")
        break
    else:
        print("Invalid Choice")
              
                
