# 🎓 Student Management System — Python + MySQL

A simple **Student Management System** built using **Python and MySQL**.
This project demonstrates how Python can interact with a MySQL database to perform CRUD operations on student records.

## 🚀 Features

* ➕ Add a new student
* 📋 View student records
* ✏️ Update student information
* 🗑️ Delete a student
* 🔎 Search/manage student records using Student ID
* 🗄️ Store student data permanently in MySQL
* 🔐 Store database credentials using environment variables
* 🧩 Modular database connection using a separate `database.py` file

## 🛠️ Technologies Used

* **Python 3**
* **MySQL 8**
* **mysql-connector-python**
* **python-dotenv**
* **Git & GitHub**
* **DBeaver** for database management

## 📂 Project Structure

```text
student-management-system-python-mysql/
│
├── main.py
├── database.py
├── test_mysql.py
├── requirements.txt
├── .gitignore
└── .env                 # Not uploaded to GitHub
```

### File Description

| File               | Purpose                                                  |
| ------------------ | -------------------------------------------------------- |
| `main.py`          | Main application and student management operations       |
| `database.py`      | Handles the MySQL database connection                    |
| `test_mysql.py`    | Tests the Python–MySQL connection                        |
| `requirements.txt` | Lists required Python packages                           |
| `.env`             | Stores private database credentials                      |
| `.gitignore`       | Prevents sensitive/unnecessary files from being uploaded |

## 🗄️ Database

The project uses a MySQL database named:

```sql
python_sql_demo
```

The student table contains:

```text
id
name
age
course
```

Example records:

```text
1 | Jinesh | 18 | Python
2 | Rahul  | 17 | SQL
3 | Amit   | 18 | Python
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/JineshShingvi0/student-management-system-python-mysql.git
```

Move into the project:

```bash
cd student-management-system-python-mysql
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL database

Open MySQL and create the database:

```sql
CREATE DATABASE python_sql_demo;
```

Then select it:

```sql
USE python_sql_demo;
```

Create the student table:

```sql
CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    age INT,
    course VARCHAR(100)
);
```

### 5. Configure environment variables

Create a `.env` file in the project folder:

```text
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=python_sql_demo
```

⚠️ **Never upload your `.env` file to GitHub.**

It is already excluded through `.gitignore`.

## ▶️ Run the Project

Make sure your virtual environment is activated:

```bash
source venv/bin/activate
```

Then run:

```bash
python main.py
```

## 🔄 CRUD Operations

The project demonstrates the four basic database operations:

```text
CREATE  → Add Student
READ    → View Student
UPDATE  → Update Student
DELETE  → Delete Student
```

This project helped me understand how Python applications can communicate with a relational database and perform real database operations.

## 📚 What I Learned

Through this project, I practiced:

* Python functions
* Python modules
* MySQL databases
* SQL queries
* CRUD operations
* Python–MySQL connectivity
* Environment variables
* Virtual environments
* Exception/error handling
* Git and GitHub
* Project organization

## 🔮 Future Improvements

Possible future features include:

* 🔎 Search students by name or course
* 📊 Student performance/results management
* 📈 Reports and statistics
* 🖥️ GUI using Tkinter
* 🌐 Web interface using Flask
* 👤 User authentication
* 📤 Export student data to CSV/PDF

## 👨‍💻 Author

**Jinesh Shingvi**

GitHub: [JineshShingvi0](https://github.com/JineshShingvi0)

---

⭐ If you found this project useful, feel free to explore the repository and give it a star.
