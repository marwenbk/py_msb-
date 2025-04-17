"""
Student model class with related operations.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from app.database.connection import db
from app.utils.email_validator import standardize_email

@dataclass
class Student:
    """Student entity class"""
    student_id: str
    name: str
    email: str
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Student':
        """Create a Student instance from a database row"""
        return cls(
            student_id=row[0],
            name=row[1],
            email=row[2]
        )
    
    @classmethod
    def get_all(cls) -> List['Student']:
        """Retrieve all students from the database"""
        students = []
        try:
            with db.get_cursor() as cursor:
                cursor.execute("SELECT student_id, name, email FROM students ORDER BY student_id")
                for row in cursor.fetchall():
                    students.append(cls.from_db_row(row))
            return students
        except Exception as e:
            print(f"Error fetching students: {e}")
            return []
    
    @classmethod
    def get_by_id(cls, student_id: str) -> Optional['Student']:
        """Retrieve a student by ID"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute(
                    "SELECT student_id, name, email FROM students WHERE student_id = %s",
                    (student_id,)
                )
                row = cursor.fetchone()
                return cls.from_db_row(row) if row else None
        except Exception as e:
            raise Exception(f"Error fetching student: {e}")
    
    def save(self) -> None:
        """Save the student to the database (insert or update)"""
        try:
            with db.get_cursor() as cursor:
                # Check if student exists
                cursor.execute(
                    "SELECT 1 FROM students WHERE student_id = %s",
                    (self.student_id,)
                )
                if cursor.fetchone():
                    # Update existing student
                    cursor.execute(
                        """
                        UPDATE students
                        SET name = %s, email = %s
                        WHERE student_id = %s
                        """,
                        (self.name, standardize_email(self.email), self.student_id)
                    )
                else:
                    # Insert new student
                    cursor.execute(
                        """
                        INSERT INTO students (student_id, name, email)
                        VALUES (%s, %s, %s)
                        """,
                        (self.student_id, self.name, standardize_email(self.email))
                    )
        except Exception as e:
            raise Exception(f"Error saving student: {e}")
    
    @classmethod
    def delete(cls, student_id: str) -> bool:
        """Delete a student by ID"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM students WHERE student_id = %s",
                    (student_id,)
                )
                return cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Error deleting student: {e}")
    
    @classmethod
    def update_id(cls, old_id: str, new_id: str) -> bool:
        """Update a student's ID"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute(
                    "UPDATE students SET student_id = %s WHERE student_id = %s",
                    (new_id, old_id)
                )
                return cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Error updating student ID: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert student to dictionary for display"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email
        } 