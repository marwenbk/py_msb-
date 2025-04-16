"""
Course service with business logic for course operations.
"""
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd
from app.models.course import Course

class CourseService:
    """Service class for course-related business logic"""
    
    @staticmethod
    def get_all_courses() -> pd.DataFrame:
        """
        Get all courses as a DataFrame for display.
        
        Returns:
            DataFrame with course data
        """
        courses = Course.get_all()
        if not courses:
            return pd.DataFrame(columns=["id", "name", "code", "credits"])
            
        return pd.DataFrame([c.to_dict() for c in courses])
    
    @staticmethod
    def get_course(course_id: int) -> Optional[Course]:
        """
        Get a specific course by ID.
        
        Args:
            course_id: The course ID to look up
            
        Returns:
            Course object if found, None otherwise
        """
        return Course.get_by_id(course_id)
    
    @staticmethod
    def get_course_by_code(code: str) -> Optional[Course]:
        """
        Get a specific course by course code.
        
        Args:
            code: The course code to look up
            
        Returns:
            Course object if found, None otherwise
        """
        return Course.get_by_code(code)
    
    @staticmethod
    def add_course(name: str, code: str, credits: int) -> Tuple[bool, str]:
        """
        Add a new course with validation.
        
        Args:
            name: Course name
            code: Course code (unique)
            credits: Number of credits
            
        Returns:
            Tuple (success, message)
        """
        # Validate inputs
        if not name:
            return False, "Course name cannot be empty"
            
        if not code:
            return False, "Course code is required"
            
        if credits <= 0:
            return False, "Credits must be a positive number"
            
        try:
            # Check if course code already exists
            existing_course = Course.get_by_code(code)
            if existing_course:
                return False, f"Course with code {code} already exists"
                
            # Create and save course
            course = Course(
                name=name,
                code=code,
                credits=credits
            )
            course.save()
            
            return True, f"Course added successfully with ID: {course.id}"
        except Exception as e:
            return False, f"Error adding course: {str(e)}"
    
    @staticmethod
    def update_course(course_id: int, name: str, code: str, credits: int) -> Tuple[bool, str]:
        """
        Update an existing course with validation.
        
        Args:
            course_id: Course ID to update
            name: New course name
            code: New course code
            credits: New number of credits
            
        Returns:
            Tuple (success, message)
        """
        # Validate inputs
        if course_id <= 0:
            return False, "Invalid course ID"
            
        if not name:
            return False, "Course name cannot be empty"
            
        if not code:
            return False, "Course code is required"
            
        if credits <= 0:
            return False, "Credits must be a positive number"
            
        try:
            # Check if course exists
            course = Course.get_by_id(course_id)
            if not course:
                return False, f"Course with ID {course_id} not found"
                
            # Check if new code already exists for a different course
            if code != course.code:
                existing_course = Course.get_by_code(code)
                if existing_course and existing_course.id != course_id:
                    return False, f"Course with code {code} already exists"
            
            # Update course
            course.name = name
            course.code = code
            course.credits = credits
            course.save()
            
            return True, "Course updated successfully"
        except Exception as e:
            return False, f"Error updating course: {str(e)}"
    
    @staticmethod
    def delete_course(course_id: int) -> Tuple[bool, str]:
        """
        Delete a course by ID.
        
        Args:
            course_id: The course ID to delete
            
        Returns:
            Tuple (success, message)
        """
        if course_id <= 0:
            return False, "Invalid course ID"
            
        try:
            # Check if course exists
            course = Course.get_by_id(course_id)
            if not course:
                return False, f"Course with ID {course_id} not found"
                
            # Delete the course
            success = Course.delete(course_id)
            if not success:
                return False, "Failed to delete course"
                
            return True, "Course deleted successfully"
        except Exception as e:
            return False, f"Error deleting course: {str(e)}" 