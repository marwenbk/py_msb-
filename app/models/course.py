"""
Course model class with related operations.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from app.database.connection import db

@dataclass
class Course:
    """Course entity class"""
    id: int = 0  # 0 for new courses
    name: str = ""
    code: str = ""
    credits: int = 0
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Course':
        """Create a Course instance from a database row"""
        return cls(
            id=row[0],
            name=row[1],
            code=row[2],
            credits=row[3]
        )
    
    @classmethod
    def get_all(cls) -> List['Course']:
        """Retrieve all courses from the database"""
        courses = []
        try:
            with db.get_cursor() as cursor:
                cursor.execute("SELECT id, name, code, credits FROM courses ORDER BY id")
                for row in cursor.fetchall():
                    courses.append(cls.from_db_row(row))
            return courses
        except Exception as e:
            raise Exception(f"Error fetching courses: {e}")
    
    @classmethod
    def get_by_id(cls, course_id: int) -> Optional['Course']:
        """Retrieve a course by ID"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, code, credits FROM courses WHERE id = %s",
                    (course_id,)
                )
                row = cursor.fetchone()
                return cls.from_db_row(row) if row else None
        except Exception as e:
            raise Exception(f"Error fetching course: {e}")
    
    @classmethod
    def get_by_code(cls, code: str) -> Optional['Course']:
        """Retrieve a course by course code"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, code, credits FROM courses WHERE code = %s",
                    (code,)
                )
                row = cursor.fetchone()
                return cls.from_db_row(row) if row else None
        except Exception as e:
            raise Exception(f"Error fetching course by code: {e}")
    
    def save(self) -> None:
        """Save the course to the database (insert or update)"""
        try:
            with db.get_cursor() as cursor:
                if self.id:
                    # Update existing course
                    cursor.execute(
                        """
                        UPDATE courses
                        SET name = %s, code = %s, credits = %s
                        WHERE id = %s
                        """,
                        (self.name, self.code, self.credits, self.id)
                    )
                else:
                    # Insert new course
                    cursor.execute(
                        """
                        INSERT INTO courses (name, code, credits)
                        VALUES (%s, %s, %s)
                        RETURNING id
                        """,
                        (self.name, self.code, self.credits)
                    )
                    self.id = cursor.fetchone()[0]
        except Exception as e:
            raise Exception(f"Error saving course: {e}")
    
    @classmethod
    def delete(cls, course_id: int) -> bool:
        """Delete a course by ID"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM courses WHERE id = %s",
                    (course_id,)
                )
                return cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Error deleting course: {e}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert course to dictionary for display"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits
        } 