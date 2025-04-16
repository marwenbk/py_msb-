"""
Student service with business logic for student operations.
"""
from typing import List, Optional, Dict, Any, Tuple
import pandas as pd
import re
from app.models.student import Student
from app.utils.id_generator import generate_student_id
from app.utils.email_validator import standardize_email, validate_email

class StudentService:
    """Service class for student-related business logic"""
    
    @staticmethod
    def get_all_students() -> pd.DataFrame:
        """
        Get all students as a DataFrame for display.
        
        Returns:
            DataFrame with student data
        """
        students = Student.get_all()
        if not students:
            return pd.DataFrame(columns=["student_id", "name", "email"])
            
        return pd.DataFrame([s.to_dict() for s in students])
    
    @staticmethod
    def get_student(student_id: str) -> Optional[Student]:
        """
        Get a specific student by ID.
        
        Args:
            student_id: The student ID to look up
            
        Returns:
            Student object if found, None otherwise
        """
        return Student.get_by_id(student_id)
    
    @staticmethod
    def add_student(name: str, email: str, enrollment_code: str) -> Tuple[bool, str]:
        """
        Add a new student with validation.
        
        Args:
            name: Student name
            email: Student email (will be standardized)
            enrollment_code: 3-digit enrollment code
            
        Returns:
            Tuple (success, message)
        """
        # Validate inputs
        if not name:
            return False, "Student name cannot be empty"
            
        if not enrollment_code:
            return False, "Enrollment code is required"
            
        # Validate enrollment code format
        if not enrollment_code.isdigit() or len(enrollment_code) != 3:
            return False, "Enrollment code must be a 3-digit number"
            
        # Validate email
        valid, error = validate_email(email)
        if not valid:
            return False, error
            
        try:
            # Generate student ID
            student_id = generate_student_id(enrollment_code)
            
            # Create and save student
            student = Student(
                student_id=student_id,
                name=name,
                email=standardize_email(email)
            )
            student.save()
            
            return True, f"Student added successfully with ID: {student_id}"
        except Exception as e:
            return False, f"Error adding student: {str(e)}"
    
    @staticmethod
    def update_student(old_id: str, new_id: Optional[str], name: str, email: str) -> Tuple[bool, str]:
        """
        Update an existing student with validation.
        
        Args:
            old_id: Current student ID
            new_id: New student ID (if updating ID)
            name: New student name
            email: New student email
            
        Returns:
            Tuple (success, message)
        """
        # Validate inputs
        if not old_id:
            return False, "Current student ID is required"
            
        if not name:
            return False, "Student name cannot be empty"
            
        # Validate email
        valid, error = validate_email(email)
        if not valid:
            return False, error
            
        try:
            # Check if student exists
            student = Student.get_by_id(old_id)
            if not student:
                return False, f"Student with ID {old_id} not found"
                
            # Handle ID update if needed
            if new_id and new_id != old_id:
                # Validate new ID format
                if not re.match(r'^\d{3}-\d{4}$', new_id):
                    return False, "New student ID must be in format XXX-YYYY"
                    
                # Update the ID
                success = Student.update_id(old_id, new_id)
                if not success:
                    return False, "Failed to update student ID"
                    
                # Use new ID for the rest of the update
                student_id = new_id
            else:
                student_id = old_id
                
            # Update other fields
            student = Student(
                student_id=student_id,
                name=name,
                email=standardize_email(email)
            )
            student.save()
            
            return True, "Student updated successfully"
        except Exception as e:
            return False, f"Error updating student: {str(e)}"
    
    @staticmethod
    def delete_student(student_id: str) -> Tuple[bool, str]:
        """
        Delete a student by ID.
        
        Args:
            student_id: The student ID to delete
            
        Returns:
            Tuple (success, message)
        """
        if not student_id:
            return False, "Student ID is required"
            
        try:
            # Check if student exists
            student = Student.get_by_id(student_id)
            if not student:
                return False, f"Student with ID {student_id} not found"
                
            # Delete the student
            success = Student.delete(student_id)
            if not success:
                return False, "Failed to delete student"
                
            return True, "Student deleted successfully"
        except Exception as e:
            return False, f"Error deleting student: {str(e)}" 