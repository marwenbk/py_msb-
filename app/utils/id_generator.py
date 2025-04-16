"""
Utility functions for generating IDs and codes.
"""
import random
from typing import Optional

def generate_student_id(enrollment_code: str) -> str:
    """
    Generate a student ID in the format <enrollment_code>-<4-digit random number>.
    
    Args:
        enrollment_code: A 3-digit string representing the enrollment code.
        
    Returns:
        A string in the format "XXX-YYYY" where XXX is the enrollment code 
        and YYYY is a random 4-digit number.
    
    Raises:
        ValueError: If enrollment_code is not a 3-digit string.
    """
    # Validate enrollment code format
    if not enrollment_code.isdigit() or len(enrollment_code) != 3:
        raise ValueError("Enrollment code must be a 3-digit number")
        
    # Generate a random 4-digit number
    random_part = random.randint(1000, 9999)
    
    return f"{enrollment_code}-{random_part}" 