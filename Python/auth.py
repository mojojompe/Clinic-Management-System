"""
Authentication Module for Clinic Management System
Handles password hashing and verification
"""

import hashlib
import os
from utils import validate_password, validate_username


def hash_password(password, salt=None):
    """
    Hash password with salt using SHA-256
    """
    if salt is None:
        salt = os.urandom(32).hex()
    
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"


def verify_password(stored_hash, provided_password):
    """
    Verify if provided password matches stored hash
    """
    try:
        salt, hashed = stored_hash.split('$')
        provided_hash = hashlib.sha256((salt + provided_password).encode()).hexdigest()
        return provided_hash == hashed
    except:
        return False


def validate_credentials(username, password):
    """
    Validate username and password format
    Returns (valid, error_message)
    """
    if not validate_username(username):
        return False, "Username must be 3-20 characters long and contain only letters, numbers, and underscores."
    
    if not validate_password(password):
        return False, "Password must be at least 6 characters long."
    
    return True, "Valid"


def check_username_exists(username, users_dict):
    """Check if username already exists in users dictionary"""
    for user_id, user in users_dict.items():
        if user.get('username') == username:
            return True
    return False
