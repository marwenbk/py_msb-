"""
Grade model class with related operations.
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple
from app.database.connection import db
from app.utils.grade_calculator import raw_grade_to_gpa, raw_grade_to_letter
from app.models.student import Student
from app.models.course import Course

@dataclass
class Grade:
    """Grade entity class"""
    id: int = 0  # 0 for new grades
    student_id: str = ""
    course_id: int = 0
    grade: float = 0.0
    
    # Calculated fields (not stored in database)
    student_name: str = ""
    course_name: str = ""
    
    @classmethod
    def from_db_row(cls, row: tuple) -> 'Grade':
        """Create a Grade instance from a database row"""
        return cls(
            id=row[0],
            student_id=row[1],
            course_id=row[2],
            grade=row[3]
        )
    
    @classmethod
    def get_all(cls) -> List['Grade']:
        """Retrieve all grades with student and course information"""
        grades = []
        try:
            with db.get_cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, g.student_id, g.course_id, g.grade, 
                           s.name as student_name, c.name as course_name
                    FROM grades g
                    JOIN students s ON g.student_id = s.student_id
                    JOIN courses c ON g.course_id = c.id
                    ORDER BY g.id
                """)
                for row in cursor.fetchall():
                    grade = cls(
                        id=row[0],
                        student_id=row[1],
                        course_id=row[2],
                        grade=row[3],
                        student_name=row[4],
                        course_name=row[5]
                    )
                    grades.append(grade)
            return grades
        except Exception as e:
            raise Exception(f"Error fetching grades: {e}")
    
    @classmethod
    def get_by_id(cls, grade_id: int) -> Optional['Grade']:
        """Retrieve a grade by ID with student and course information"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, g.student_id, g.course_id, g.grade, 
                           s.name as student_name, c.name as course_name
                    FROM grades g
                    JOIN students s ON g.student_id = s.student_id
                    JOIN courses c ON g.course_id = c.id
                    WHERE g.id = %s
                """, (grade_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                    
                return cls(
                    id=row[0],
                    student_id=row[1],
                    course_id=row[2],
                    grade=row[3],
                    student_name=row[4],
                    course_name=row[5]
                )
        except Exception as e:
            raise Exception(f"Error fetching grade: {e}")
    
    @classmethod
    def get_by_student_course(cls, student_id: str, course_id: int) -> Optional['Grade']:
        """Retrieve a grade by student ID and course ID"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, g.student_id, g.course_id, g.grade, 
                           s.name as student_name, c.name as course_name
                    FROM grades g
                    JOIN students s ON g.student_id = s.student_id
                    JOIN courses c ON g.course_id = c.id
                    WHERE g.student_id = %s AND g.course_id = %s
                """, (student_id, course_id))
                row = cursor.fetchone()
                if not row:
                    return None
                    
                return cls(
                    id=row[0],
                    student_id=row[1],
                    course_id=row[2],
                    grade=row[3],
                    student_name=row[4],
                    course_name=row[5]
                )
        except Exception as e:
            raise Exception(f"Error fetching grade by student and course: {e}")
    
    @classmethod
    def get_student_grades(cls, student_id: str) -> List['Grade']:
        """Retrieve all grades for a specific student"""
        grades = []
        try:
            with db.get_cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, g.student_id, g.course_id, g.grade, 
                           s.name as student_name, c.name as course_name
                    FROM grades g
                    JOIN students s ON g.student_id = s.student_id
                    JOIN courses c ON g.course_id = c.id
                    WHERE g.student_id = %s
                    ORDER BY c.name
                """, (student_id,))
                for row in cursor.fetchall():
                    grade = cls(
                        id=row[0],
                        student_id=row[1],
                        course_id=row[2],
                        grade=row[3],
                        student_name=row[4],
                        course_name=row[5]
                    )
                    grades.append(grade)
            return grades
        except Exception as e:
            raise Exception(f"Error fetching student grades: {e}")
    
    @classmethod
    def get_course_grades(cls, course_id: int) -> List['Grade']:
        """Retrieve all grades for a specific course"""
        grades = []
        try:
            with db.get_cursor() as cursor:
                cursor.execute("""
                    SELECT g.id, g.student_id, g.course_id, g.grade, 
                           s.name as student_name, c.name as course_name
                    FROM grades g
                    JOIN students s ON g.student_id = s.student_id
                    JOIN courses c ON g.course_id = c.id
                    WHERE g.course_id = %s
                    ORDER BY g.grade DESC, s.name
                """, (course_id,))
                for row in cursor.fetchall():
                    grade = cls(
                        id=row[0],
                        student_id=row[1],
                        course_id=row[2],
                        grade=row[3],
                        student_name=row[4],
                        course_name=row[5]
                    )
                    grades.append(grade)
            return grades
        except Exception as e:
            raise Exception(f"Error fetching course grades: {e}")
    
    def save(self) -> None:
        """Save the grade to the database (insert or update)"""
        try:
            with db.get_cursor() as cursor:
                if self.id:
                    # Update existing grade
                    cursor.execute(
                        "UPDATE grades SET grade = %s WHERE id = %s",
                        (self.grade, self.id)
                    )
                else:
                    # Insert new grade or update if student-course pair exists
                    cursor.execute(
                        """
                        INSERT INTO grades (student_id, course_id, grade)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (student_id, course_id) 
                        DO UPDATE SET grade = EXCLUDED.grade
                        RETURNING id
                        """,
                        (self.student_id, self.course_id, self.grade)
                    )
                    self.id = cursor.fetchone()[0]
        except Exception as e:
            raise Exception(f"Error saving grade: {e}")
    
    @classmethod
    def delete(cls, grade_id: int) -> bool:
        """Delete a grade by ID"""
        try:
            with db.get_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM grades WHERE id = %s",
                    (grade_id,)
                )
                return cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Error deleting grade: {e}")
    
    @property
    def gpa(self) -> float:
        """Convert raw grade to GPA equivalent"""
        return raw_grade_to_gpa(self.grade)
    
    @property
    def letter_grade(self) -> str:
        """Convert raw grade to letter grade"""
        return raw_grade_to_letter(self.grade)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert grade to dictionary for display"""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "student_name": self.student_name,
            "course_id": self.course_id,
            "course_name": self.course_name,
            "raw_grade": self.grade,
            "gpa": self.gpa,
            "letter": self.letter_grade
        } 