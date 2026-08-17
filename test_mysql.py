import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jinesh@1008",
    database="python_sql_demo"
)

cursor = connection.cursor()

student_id = int(input("Enter student ID to delete: "))

query = """
DELETE FROM student
WHERE id = %s
"""

values = (student_id,)

cursor.execute(query, values)

connection.commit()

if cursor.rowcount > 0:
    print("Student deleted successfully!")
else:
    print("Student ID not found.")

cursor.close()
connection.close()