"""
Utility Functions for Clinic Management System
Handles validation, formatting, and helper functions
"""

import re
from datetime import datetime, timedelta
import uuid


def generate_id():
    """Generate a unique ID using UUID"""
    return str(uuid.uuid4())[:8]


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """Validate phone number (10-15 digits)"""
    pattern = r'^\d{10,15}$'
    return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None


def validate_username(username):
    """Validate username (3-20 chars, alphanumeric and underscore)"""
    if len(username) < 3 or len(username) > 20:
        return False
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None


def validate_password(password):
    """Validate password (min 6 chars)"""
    return len(password) >= 6


def validate_date(date_string):
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_time(time_string):
    """Validate time format (HH:MM)"""
    try:
        datetime.strptime(time_string, '%H:%M')
        return True
    except ValueError:
        return False


def validate_datetime(date_string, time_string):
    """Validate date and time combination"""
    try:
        dt = datetime.strptime(f"{date_string} {time_string}", '%Y-%m-%d %H:%M')
        # Check if date is in future
        if dt > datetime.now():
            return True
        return False
    except ValueError:
        return False


def validate_age(date_of_birth):
    """Validate if person is at least 18 years old"""
    try:
        dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age >= 18
    except ValueError:
        return False


def format_date(date_string):
    """Format date for display"""
    try:
        dt = datetime.strptime(date_string, '%Y-%m-%d')
        return dt.strftime('%d-%b-%Y')
    except ValueError:
        return date_string


def format_datetime(date_string, time_string):
    """Format datetime for display"""
    try:
        dt = datetime.strptime(f"{date_string} {time_string}", '%Y-%m-%d %H:%M')
        return dt.strftime('%d-%b-%Y %H:%M')
    except ValueError:
        return f"{date_string} {time_string}"


def get_age(date_of_birth):
    """Calculate age from date of birth"""
    try:
        dob = datetime.strptime(date_of_birth, '%Y-%m-%d')
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except ValueError:
        return None


def clear_screen():
    """Clear console screen"""
    print("\n" * 50)


def print_separator(char="-", length=70):
    """Print a separator line"""
    print(char * length)


def print_header(text, length=70):
    """Print a formatted header"""
    print_separator("=", length)
    print(f" {text.center(length-2)} ")
    print_separator("=", length)


def print_subheader(text, length=70):
    """Print a formatted subheader"""
    print(f"\n{text}")
    print_separator("-", length)


def input_with_validation(prompt, validation_func=None, error_message="Invalid input"):
    """Get user input with optional validation"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("Input cannot be empty. Please try again.")
                continue
            if validation_func and not validation_func(user_input):
                print(f"{error_message}. Please try again.")
                continue
            return user_input
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
        except Exception as e:
            print(f"Error: {str(e)}. Please try again.")


def input_yes_no(prompt):
    """Get yes/no input from user"""
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please enter 'yes' or 'no'.")


def get_time_slot_options():
    """Get list of available time slots"""
    slots = []
    for hour in range(9, 18):  # 9 AM to 6 PM
        for minute in [0, 30]:
            time_str = f"{hour:02d}:{minute:02d}"
            slots.append(time_str)
    return slots


def is_valid_specialization(specialization):
    """Check if specialization is valid"""
    valid_specs = [
        'General Medicine',
        'Cardiology',
        'Pediatrics',
        'Orthopedics',
        'Neurology',
        'Dermatology',
        'ENT',
        'Ophthalmology',
        'Dentistry',
        'Psychiatry',
        'Gynecology',
        'Urology'
    ]
    return specialization in valid_specs


def get_specializations():
    """Get list of specializations"""
    return [
        'General Medicine',
        'Cardiology',
        'Pediatrics',
        'Orthopedics',
        'Neurology',
        'Dermatology',
        'ENT',
        'Ophthalmology',
        'Dentistry',
        'Psychiatry',
        'Gynecology',
        'Urology'
    ]


def is_valid_complaint_type(complaint_type):
    """Check if complaint type is valid"""
    valid_types = ['Service', 'Medical', 'Staff', 'Billing', 'Other']
    return complaint_type in valid_types


def get_complaint_types():
    """Get list of complaint types"""
    return ['Service', 'Medical', 'Staff', 'Billing', 'Other']


def is_valid_blood_type(blood_type):
    """Check if blood type is valid"""
    valid_types = ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']
    return blood_type in valid_types


def get_blood_types():
    """Get list of blood types"""
    return ['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-']


def is_valid_gender(gender):
    """Check if gender is valid"""
    valid_genders = ['Male', 'Female', 'Other']
    return gender in valid_genders


def get_genders():
    """Get list of genders"""
    return ['Male', 'Female', 'Other']


def display_menu(options, title="Menu"):
    """Display a menu and get user choice"""
    print_subheader(title)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print_separator()
    
    while True:
        try:
            choice = input("Enter your choice (number): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Please enter a valid number.")


def pause():
    """Pause execution and wait for user input"""
    input("\nPress Enter to continue...")


def print_success(message):
    """Print success message"""
    print(f"\n✓ {message}")


def print_error(message):
    """Print error message"""
    print(f"\n✗ {message}")


def print_info(message):
    """Print info message"""
    print(f"\nℹ {message}")


def truncate_string(text, length=50):
    """Truncate string to specified length"""
    if len(text) > length:
        return text[:length-3] + "..."
    return text


def format_table_row(values, widths):
    """Format a row for table display"""
    row = ""
    for value, width in zip(values, widths):
        row += str(value).ljust(width) + " | "
    return row.rstrip(" | ")


def format_table_separator(widths):
    """Create a table separator line"""
    sep = ""
    for width in widths:
        sep += "-" * width + "-+-"
    return sep.rstrip("-+-")
