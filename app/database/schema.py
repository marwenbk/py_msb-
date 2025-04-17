"""
Database schema management module.
Contains functions for creating, resetting, and seeding the database.
"""
import random
import streamlit as st
import pandas as pd
from app.database.connection import db
from app.utils.id_generator import generate_student_id
from app.utils.email_validator import standardize_email

def create_tables():
    """Create database tables if they don't exist"""
    try:
        with db.get_cursor() as cursor:
            # Drop tables in correct order to respect foreign key dependencies
            cursor.execute("DROP TABLE IF EXISTS grades;")
            cursor.execute("DROP TABLE IF EXISTS courses;")
            cursor.execute("DROP TABLE IF EXISTS students;")
            
            # Create the students table
            cursor.execute("""
                CREATE TABLE students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                );
            """)
            
            # Create the courses table
            cursor.execute("""
                CREATE TABLE courses (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    code TEXT NOT NULL UNIQUE,
                    credits INTEGER NOT NULL
                );
            """)
            
            # Create the grades table with cascading rules
            cursor.execute("""
                CREATE TABLE grades (
                    id SERIAL PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    course_id INTEGER NOT NULL,
                    grade REAL NOT NULL,
                    UNIQUE(student_id, course_id),
                    FOREIGN KEY(student_id) REFERENCES students(student_id) 
                        ON DELETE CASCADE ON UPDATE CASCADE,
                    FOREIGN KEY(course_id) REFERENCES courses(id) 
                        ON DELETE CASCADE
                );
            """)
        
        return True, "Tables created successfully."
    except Exception as e:
        return False, f"Error in creating tables: {e}"

def seed_data():
    """
    Populate the tables with sample data:
      - 22 students
      - 5 courses
      - Each student gets a grade in each course
    """
    try:
        # Sample student data
        enrollment_codes = ["201", "202", "203", "204"]
        students = [
            ("Alice Johnson", "alice.johnson@example.com"),
            ("Bob Smith", "bob.smith@example.com"),
            ("Charlie Davis", "charlie.davis@example.com"),
            ("Diana Evans", "diana.evans@example.com"),
            ("Ethan Brown", "ethan.brown@example.com"),
            ("Fiona Clark", "fiona.clark@example.com"),
            ("George Miller", "george.miller@example.com"),
            ("Hannah Wilson", "hannah.wilson@example.com"),
            ("Ian Thompson", "ian.thompson@example.com"),
            ("Julia Robinson", "julia.robinson@example.com"),
            ("Kevin Walker", "kevin.walker@example.com"),
            ("Laura King", "laura.king@example.com"),
            ("Michael Scott", "michael.scott@example.com"),
            ("Nina Perez", "nina.perez@example.com"),
            ("Oliver Martinez", "oliver.martinez@example.com"),
            ("Ahmed Khalid", "ahmed.khalid@example.com"),
            ("Fatima Ali", "fatima.ali@example.com"),
            ("Omar Farouk", "omar.farouk@example.com"),
            ("Layla Hassan", "layla.hassan@example.com"),
            ("Yousef Ibrahim", "yousef.ibrahim@example.com"),
            ("Sara Nasser", "sara.nasser@example.com"),
            ("Zainab Mustafa", "zainab.mustafa@example.com")
        ]
        
        # Insert students
        students_added = 0
        with db.get_cursor() as cursor:
            for name, email in students:
                try:
                    enroll_code = random.choice(enrollment_codes)
                    student_id = generate_student_id(enroll_code)
                    standardized_email = standardize_email(email)
                    
                    cursor.execute("""
                        INSERT INTO students (student_id, name, email)
                        VALUES (%s, %s, %s);
                    """, (student_id, name, standardized_email))
                    students_added += 1
                except Exception as e:
                    print(f"Could not add student {name}: {e}")
        
        # Sample course data
        courses = [
            ("Mathematics", "MATH101", 3),
            ("Physics", "PHYS101", 4),
            ("Chemistry", "CHEM101", 3),
            ("English Literature", "ENG101", 2),
            ("History", "HIST101", 3)
        ]
        
        # Insert courses
        courses_added = 0
        with db.get_cursor() as cursor:
            for cname, code, credits in courses:
                try:
                    cursor.execute("""
                        INSERT INTO courses (name, code, credits)
                        VALUES (%s, %s, %s);
                    """, (cname, code, credits))
                    courses_added += 1
                except Exception as e:
                    print(f"Could not add course {cname}: {e}")
        
        # Get all students and courses for grade assignment
        student_ids = []
        course_ids = []
        try:
            with db.get_cursor() as cursor:
                cursor.execute("SELECT student_id FROM students ORDER BY student_id")
                student_ids = [row[0] for row in cursor.fetchall()]
                
                cursor.execute("SELECT id FROM courses ORDER BY id")
                course_ids = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            return False, f"Error retrieving students and courses: {e}"
        
        # Skip grade assignment if no students or courses
        if not student_ids or not course_ids:
            return False, "Cannot assign grades: No students or courses found"
        
        # Insert grades for each student in each course
        grades_added = 0
        with db.get_cursor() as cursor:
            for sid in student_ids:
                for cid in course_ids:
                    try:
                        # 20% chance for a failing grade (<50); otherwise, a grade between 50 and 100
                        grade = random.randint(30, 49) if random.random() < 0.2 else random.randint(50, 100)
                        
                        cursor.execute("""
                            INSERT INTO grades (student_id, course_id, grade)
                            VALUES (%s, %s, %s);
                        """, (sid, cid, grade))
                        grades_added += 1
                    except Exception as e:
                        print(f"Could not add grade for student {sid}, course {cid}: {e}")
        
        return True, f"Sample data seeded successfully: {students_added} students, {courses_added} courses, {grades_added} grades."
    except Exception as e:
        return False, f"Error seeding data: {e}" 