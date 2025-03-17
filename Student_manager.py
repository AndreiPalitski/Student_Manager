import csv
import sqlite3
from typing import List


class Student:
    def __init__(self, name, phone, english_grade, math_grade):
        self.name = name.title()
        self.phone = phone

        try:
            self.english_grade = int(english_grade)
        except ValueError:
            self.english_grade = -1

        try:
            self.math_grade = int(math_grade)
        except ValueError:
            self.math_grade = -1

    def __str__(self):
        return f"Student: {self.name}, {self.phone}, English: {self.english_grade}, Math: {self.math_grade}"

    def to_list(self):
        return self.name, self.phone, self.english_grade, self.math_grade


class StudentDatabase:
    def __init__(self, db_name="students.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        """Creates the students table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    english_grade INTEGER,
                    math_grade INTEGER
                )
            """)
            conn.commit()

    def add_student(self, student: Student):
        """Adds a new student to the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, phone, english_grade, math_grade) VALUES (?, ?, ?, ?)",
                           student.to_list())
            conn.commit()

    def get_all_students(self) -> List[Student]:
        """Retrieves all students from the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, phone, english_grade, math_grade FROM students")
            rows = cursor.fetchall()
            return [Student(*row) for row in rows]  # Only extracts needed columns

    def remove_student_by_name(self, name: str) -> bool:
        """Removes a student by name."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE name = ?", (name,))
            if cursor.rowcount > 0:
                conn.commit()
                return True
            return False

    def print_students(self):
        """Displays all students."""
        students = self.get_all_students()
        if students:
            for student in students:
                print(student)
        else:
            print("No students found.")


def menu():
    db = StudentDatabase()

    while True:
        print("\n----- Student Management Menu -----")
        print("1. View all students")
        print("2. Add a new student")
        print("3. Remove a student by name")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            db.print_students()
        elif choice == "2":
            name = input("Enter student name: ")
            phone = input("Enter student phone: ")

            while True:
                english_grade = input("Enter English grade (0-100): ")
                if english_grade.isdigit():
                    break
                print("Invalid input! Please enter a number.")

            while True:
                math_grade = input("Enter Math grade (0-100): ")
                if math_grade.isdigit():
                    break
                print("Invalid input! Please enter a number.")

            new_student = Student(name, phone, english_grade, math_grade)
            db.add_student(new_student)
            print(f"Added student: {new_student}")
        elif choice == "3":
            name_to_remove = input("Enter the name of the student to remove: ")
            if db.remove_student_by_name(name_to_remove):
                print(f"Removed student: {name_to_remove}")
            else:
                print(f"Student '{name_to_remove}' not found.")
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    menu()
