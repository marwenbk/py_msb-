"""
Email validation and standardization utilities.
"""
import re
from typing import Optional, Tuple

def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate an email address format.
    
    Args:
        email: The email address to validate.
        
    Returns:
        A tuple (is_valid, error_message) where:
            - is_valid is a boolean indicating if the email is valid
            - error_message is None if valid, or a string explaining the issue if invalid
    """
    if not email:
        return False, "Email cannot be empty"
    
    # Simple regex for basic email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, None

def standardize_email(email: str) -> str:
    """
    Ensure that the email uses the '@outlook.com' domain.
    
    Args:
        email: The email address to standardize.
        
    Returns:
        The email with @outlook.com domain.
    """
    # Check if the email already contains @
    if '@' in email:
        local_part = email.split('@')[0]
    else:
        local_part = email
        
    return f"{local_part}@outlook.com" 