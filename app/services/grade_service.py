"""
Grade service with business logic for grade operations.
"""
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd
from app.models.grade import Grade
from app.models.student import Student
from app.models.course import Course
from app.database.connection import db
from app.utils.grade_calculator import calculate_weighted_gpa, has_failing_grade

class GradeService:
    """Service class for grade-related business logic"""
    
    @staticmethod
    def get_all_grades() -> pd.DataFrame:
        """
        Get all grades as a DataFrame for display.
        
        Returns:
            DataFrame with detailed grade data
        """
        grades = Grade.get_all()
        if not grades:
            return pd.DataFrame(columns=["id", "student_id", "student_name", "course_id", 
                                        "course_name", "raw_grade", "letter", "gpa"])
            
        return pd.DataFrame([g.to_dict() for g in grades])
    
    @staticmethod
    def get_grade(grade_id: int) -> Optional[Grade]:
        """
        Get a specific grade by ID.
        
        Args:
            grade_id: The grade ID to look up
            
        Returns:
            Grade object if found, None otherwise
        """
        return Grade.get_by_id(grade_id)
    
    @staticmethod
    def add_grade(student_id: str, course_id: int, grade_value: float) -> Tuple[bool, str]:
        """
        Add a new grade with validation.
        
        Args:
            student_id: Student ID
            course_id: Course ID
            grade_value: Grade value (0-100)
            
        Returns:
            Tuple (success, message)
        """
        # Validate inputs
        if not student_id:
            return False, "Student ID is required"
            
        if course_id <= 0:
            return False, "Invalid course ID"
            
        if grade_value < 0 or grade_value > 100:
            return False, "Grade must be between 0 and 100"
            
        try:
            # Check if student exists
            student = Student.get_by_id(student_id)
            if not student:
                return False, f"Student with ID {student_id} not found"
                
            # Check if course exists
            course = Course.get_by_id(course_id)
            if not course:
                return False, f"Course with ID {course_id} not found"
                
            # Create and save grade
            grade = Grade(
                student_id=student_id,
                course_id=course_id,
                grade=grade_value
            )
            grade.save()
            
            return True, "Grade assigned successfully"
        except Exception as e:
            return False, f"Error assigning grade: {str(e)}"
    
    @staticmethod
    def update_grade(grade_id: int, grade_value: float) -> Tuple[bool, str]:
        """
        Update an existing grade with validation.
        
        Args:
            grade_id: Grade ID to update
            grade_value: New grade value
            
        Returns:
            Tuple (success, message)
        """
        # Validate inputs
        if grade_id <= 0:
            return False, "Invalid grade ID"
            
        if grade_value < 0 or grade_value > 100:
            return False, "Grade must be between 0 and 100"
            
        try:
            # Check if grade exists
            grade = Grade.get_by_id(grade_id)
            if not grade:
                return False, f"Grade with ID {grade_id} not found"
                
            # Update grade
            grade.grade = grade_value
            grade.save()
            
            return True, "Grade updated successfully"
        except Exception as e:
            return False, f"Error updating grade: {str(e)}"
    
    @staticmethod
    def update_grade_by_student_course(student_id: str, course_id: int, grade_value: float) -> Tuple[bool, str]:
        """
        Update a grade by student and course with validation.
        
        Args:
            student_id: Student ID
            course_id: Course ID
            grade_value: New grade value
            
        Returns:
            Tuple (success, message)
        """
        # Validate inputs
        if not student_id:
            return False, "Student ID is required"
            
        if course_id <= 0:
            return False, "Invalid course ID"
            
        if grade_value < 0 or grade_value > 100:
            return False, "Grade must be between 0 and 100"
            
        try:
            # Check if student exists
            student = Student.get_by_id(student_id)
            if not student:
                return False, f"Student with ID {student_id} not found"
                
            # Check if course exists
            course = Course.get_by_id(course_id)
            if not course:
                return False, f"Course with ID {course_id} not found"
                
            # Get existing grade or create new one
            grade = Grade.get_by_student_course(student_id, course_id)
            if grade:
                grade.grade = grade_value
            else:
                grade = Grade(
                    student_id=student_id,
                    course_id=course_id,
                    grade=grade_value
                )
            
            # Save changes
            grade.save()
            
            return True, "Grade updated successfully"
        except Exception as e:
            return False, f"Error updating grade: {str(e)}"
    
    @staticmethod
    def delete_grade(grade_id: int) -> Tuple[bool, str]:
        """
        Delete a grade by ID.
        
        Args:
            grade_id: The grade ID to delete
            
        Returns:
            Tuple (success, message)
        """
        if grade_id <= 0:
            return False, "Invalid grade ID"
            
        try:
            # Check if grade exists
            grade = Grade.get_by_id(grade_id)
            if not grade:
                return False, f"Grade with ID {grade_id} not found"
                
            # Delete the grade
            success = Grade.delete(grade_id)
            if not success:
                return False, "Failed to delete grade"
                
            return True, "Grade deleted successfully"
        except Exception as e:
            return False, f"Error deleting grade: {str(e)}"
    
    @staticmethod
    def get_student_gpa(student_id: str) -> float:
        """
        Calculate a student's GPA.
        
        Args:
            student_id: The student ID
            
        Returns:
            GPA on a 4.0 scale
        """
        try:
            # Get student's grades with course credits
            with db.get_cursor() as cursor:
                cursor.execute("""
                    SELECT g.grade, c.credits
                    FROM grades g
                    JOIN courses c ON g.course_id = c.id
                    WHERE g.student_id = %s
                """, (student_id,))
                grades = cursor.fetchall()
                
            return calculate_weighted_gpa(grades)
        except Exception:
            return 0.0
    
    @staticmethod
    def get_analytics_data() -> Tuple[pd.DataFrame, Dict[str, Dict[str, Any]]]:
        """
        Generate analytics data for students and courses.
        
        Returns:
            Tuple with (students_with_gpa DataFrame, course_analytics dictionary)
        """
        try:
            # Get all students with GPA data
            students = Student.get_all()
            students_data = []
            
            for student in students:
                # Get all grades for the student
                grades = Grade.get_student_grades(student.student_id)
                
                # Extract raw grades for failure check
                raw_grades = [g.grade for g in grades]
                
                # Calculate GPA
                with db.get_cursor() as cursor:
                    cursor.execute("""
                        SELECT g.grade, c.credits
                        FROM grades g
                        JOIN courses c ON g.course_id = c.id
                        WHERE g.student_id = %s
                    """, (student.student_id,))
                    grade_data = cursor.fetchall()
                
                student_gpa = calculate_weighted_gpa(grade_data)
                is_failing = "Yes" if has_failing_grade(raw_grades) or student_gpa < 2.0 else "No"
                
                # Create student record
                students_data.append({
                    "student_id": student.student_id,
                    "name": student.name,
                    "email": student.email,
                    "gpa": student_gpa,
                    "failed": is_failing
                })
            
            # Create DataFrame
            students_df = pd.DataFrame(students_data)
            
            # Get course analytics
            courses = Course.get_all()
            course_analytics = {}
            
            for course in courses:
                # Get all grades for the course
                grades = Grade.get_course_grades(course.id)
                
                # Calculate average grade
                avg_grade = sum(g.grade for g in grades) / len(grades) if grades else 0
                
                # Get top 3 students
                top_students = [{
                    "name": g.student_name,
                    "grade": g.grade,
                    "letter": g.letter_grade
                } for g in grades[:3]]  # Already sorted by grade DESC
                
                course_analytics[course.name] = {
                    "average_grade": round(avg_grade, 2),
                    "top_students": pd.DataFrame(top_students) if top_students else pd.DataFrame()
                }
            
            return students_df, course_analytics
            
        except Exception as e:
            # Return empty results on error
            return pd.DataFrame(), {} 