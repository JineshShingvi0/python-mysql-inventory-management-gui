from database import get_connection

def add_student():
    connection = get_connection()
    cursor = connection.cursor()

    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    course = input("Enter student course: ")

    query = """
    INSERT INTO student (name, age, course)
    VALUES (%s, %s, %s)
    """

    values = (name, age, course)

    cursor.execute(query, values)
    connection.commit()

    print("\nStudent added successfully!")

    cursor.close()
    connection.close()

def view_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM student")

    students = cursor.fetchall()

    print("\n========== ALL STUDENTS ==========")

    if len(students) == 0:
        print("No students found.")
    else:
        for student in students:
            print(
                f"ID: {student[0]} | "
                f"Name: {student[1]} | "
                f"Age: {student[2]} | "
                f"Course: {student[3]}"
            )

    cursor.close()
    connection.close()

def search_student():
    connection = get_connection()
    cursor = connection.cursor()

    cursor = connection.cursor()

    student_id = int(input("Enter student ID to search: "))

    query = """
    SELECT * FROM student
    WHERE id = %s
    """

    values = (student_id,)

    cursor.execute(query, values)

    student = cursor.fetchone()

    if student:
        print("\n========== STUDENT FOUND ==========")
        print(f"ID: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Age: {student[2]}")
        print(f"Course: {student[3]}")
    else:
        print("\nStudent ID not found.")

    cursor.close()
    connection.close()

def update_student():

    connection = get_connection()
    cursor = connection.cursor()

    cursor=connection.cursor()

    student_id = int(input("Enter student ID to update: "))
    name=input("Enter student name to update:")
    age=int(input("Enter student age to update:"))
    course=input("Enter student course to update:")

    query="""
    UPDATE student
    SET name=%s, age=%s, course=%s
    WHERE id=%s
    """
    values = (name, age, course, student_id)

    cursor.execute(query,values)


    connection.commit()

    if cursor.rowcount > 0:
        print("Student updated successfully!")
    else:
        print("Student ID not found.")

    cursor.close()
    connection.close()

def delete_student():
    connection = get_connection()
    cursor = connection.cursor()

    cursor=connection.cursor()

    student_id=int(input("Enter student id to delete:"))

    query="""
    DELETE FROM student
    WHERE id=%s
    """ 

    values=(student_id,)

    cursor.execute(query,values)

    connection.commit()

    if cursor.rowcount>0:
        print("Student Deleted Successfully")
    else:
        print("Student ID not found")

def show_menu():
    print("\n==============================")
    print("   STUDENT MANAGEMENT SYSTEM")
    print("==============================")
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")
    print("==============================")


while True:
    show_menu()

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        print("\nThank you for using Student Management System!")
        break

    else:
        print("\nInvalid choice. Please try again.")