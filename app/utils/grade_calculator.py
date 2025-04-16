"""
Grade calculation utilities.
"""
from typing import List, Dict, Tuple, Optional, Any

def raw_grade_to_gpa(raw: float) -> float:
    """
    Convert a raw grade (0–100) to a 0–4.0 GPA scale.
    
    Args:
        raw: A numeric grade between 0 and 100.
        
    Returns:
        The equivalent GPA on a 4.0 scale.
    """
    if raw >= 90:
        return 4.0
    elif raw >= 80:
        return 3.0
    elif raw >= 70:
        return 2.0
    elif raw >= 60:
        return 1.0
    else:
        return 0.0

def raw_grade_to_letter(raw: float) -> str:
    """
    Convert a raw grade (0–100) to a letter grade.
    
    Args:
        raw: A numeric grade between 0 and 100.
        
    Returns:
        The equivalent letter grade (A, B, C, D, or F).
    """
    if raw >= 90:
        return "A"
    elif raw >= 80:
        return "B"
    elif raw >= 70:
        return "C"
    elif raw >= 60:
        return "D"
    else:
        return "F"

def calculate_weighted_gpa(grades: List[Tuple[float, int]]) -> float:
    """
    Calculate a weighted GPA based on raw grades and course credits.
    
    Args:
        grades: A list of tuples (raw_grade, credits).
        
    Returns:
        The weighted GPA on a 4.0 scale, or 0.0 if no grades.
    """
    if not grades:
        return 0.0
        
    total_points = sum(raw_grade_to_gpa(grade) * credits for grade, credits in grades)
    total_credits = sum(credits for _, credits in grades)
    
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

def has_failing_grade(grades: List[float]) -> bool:
    """
    Check if any grade is below passing (less than 60).
    
    Args:
        grades: A list of raw grades.
        
    Returns:
        True if any grade is failing, False otherwise.
    """
    return any(grade < 60 for grade in grades) 