# Clinic Management System

A comprehensive CLI-based Clinic Management System built with Python, featuring patient and doctor management, appointment scheduling, medical records, and complaint handling.

## Features

### 🏥 Core Features

#### Patient Management

- ✅ **Registration & Authentication**: Secure patient registration with password hashing
- ✅ **Profile Management**: View and edit personal information
- ✅ **Appointment Booking**: Book appointments with available doctors
- ✅ **Appointment Management**: View, reschedule, and cancel appointments
- ✅ **Medical Records**: Secure access to personal medical history
- ✅ **Prescription Management**: View active prescriptions
- ✅ **Complaint System**: File complaints about service or medical care
- ✅ **Doctor Rating**: Rate doctors after completing appointments

#### Doctor Management

- ✅ **Registration & Authentication**: Doctor registration with credentials
- ✅ **Profile Management**: Manage professional information and rates
- ✅ **Schedule Management**: Set availability slots for appointments
- ✅ **Appointment Management**: Confirm, reschedule, and complete appointments
- ✅ **Patient Records**: Create and update medical records for assigned patients
- ✅ **Prescription Issuance**: Issue prescriptions to patients
- ✅ **Complaint Review**: View complaints filed against them
- ✅ **Rating System**: Track patient ratings and average rating

#### Admin Features

- ✅ **Doctor Verification**: Approve or reject doctor registrations
- ✅ **User Management**: View all registered patients and doctors
- ✅ **Complaint Resolution**: Review and resolve filed complaints
- ✅ **System Statistics**: View comprehensive system analytics
- ✅ **Appointment Monitoring**: Track all appointments in the system

### 🛡️ Security Features

- Password hashing with SHA-256 and salt
- Session-based authentication
- Role-based access control (Patient/Doctor/Admin)
- Admin account with default credentials

## Project Structure

```
Clinic-Management-System/
├── main.py                      # Main application with CLI interface
├── models.py                    # Data models (User, Patient, Doctor, etc.)
├── auth.py                      # Authentication and password hashing
├── database.py                  # Database management and persistence
├── utils.py                     # Utility functions and helpers
├── data/
│   ├── patients.json            # Patient data storage
│   ├── doctors.json             # Doctor data storage
│   ├── appointments.json        # Appointment data
│   ├── medical_records.json     # Medical records
│   ├── complaints.json          # Complaints
│   ├── prescriptions.json       # Prescriptions
│   └── admin_users.json         # Admin credentials
├── IMPLEMENTATION_PLAN.md       # Detailed implementation documentation
└── README.md                    # This file
```

## Technical Architecture

### Technology Stack

- **Language**: Python 3.8+
- **Database**: Dictionary-based storage + JSON persistence
- **Authentication**: SHA-256 password hashing with salt
- **OOP Features**: Class inheritance, encapsulation, polymorphism
- **Data Structures**: Lists, Tuples, Dictionaries

### Key Classes

#### `User` (Base Class)

- `Patient` - Extends User with patient-specific attributes
- `Doctor` - Extends User with doctor-specific attributes

#### Core Models

- `Appointment` - Represents appointment between patient and doctor
- `MedicalRecord` - Stores patient medical history and diagnoses
- `Complaint` - Handles complaints from patients and doctors
- `Prescription` - Represents medication prescriptions

#### `Database`

- Manages all CRUD operations
- Handles JSON persistence
- Provides query methods for filtering and searching

### Data Flow

1. **User Input** → CLI Interface
2. **Validation** → Utility functions
3. **Processing** → Business logic in main.py
4. **Storage** → Database class
5. **Persistence** → JSON files

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- No external dependencies (uses only Python standard library)

### Running the Application

1. Navigate to the project directory:

```bash
cd Clinic-Management-System
```

2. Run the main application:

```bash
python main.py
```

3. You'll see the main menu with login and registration options

## Usage Guide

### First-Time Setup

1. The system automatically creates a default admin account:
   - **Username**: `admin`
   - **Password**: `admin123`

### Patient Workflow

1. **Register** → Provide personal information and health details
2. **Login** → Access patient dashboard
3. **Book Appointment** → Select doctor and available time slot
4. **Manage Appointments** → View, reschedule, or cancel
5. **View Medical Records** → Access health history
6. **Submit Complaints** → File service or medical complaints
7. **Rate Doctors** → Provide feedback after appointments

### Doctor Workflow

1. **Register** → Provide credentials and specialization (Pending admin approval)
2. **Wait for Verification** → Admin must verify your account
3. **Login** → Access doctor dashboard
4. **Manage Schedule** → Add available time slots
5. **Manage Appointments** → Confirm and complete appointments
6. **Create Records** → Document patient medical history
7. **Issue Prescriptions** → Provide medication details
8. **View Ratings** → Check patient feedback

### Admin Workflow

1. **Login** → Use default admin credentials
2. **Verify Doctors** → Approve pending doctor registrations
3. **Manage Users** → View patients and doctors
4. **Resolve Complaints** → Review and resolve filed complaints
5. **Monitor System** → View statistics and reports
6. **Change Password** → Update admin credentials

## Data Models

### Patient

```python
{
    'user_id': str,
    'username': str,
    'email': str,
    'phone': str,
    'date_of_birth': 'YYYY-MM-DD',
    'gender': 'Male|Female|Other',
    'address': str,
    'blood_type': 'O+|O-|A+|A-|B+|B-|AB+|AB-',
    'allergies': str,
    'emergency_contact': str,
    'medical_history': [record_ids],
    'appointments': [appointment_ids],
    'height': int (cm),
    'weight': int (kg)
}
```

### Doctor

```python
{
    'user_id': str,
    'username': str,
    'email': str,
    'phone': str,
    'specialization': str,
    'license_number': str,
    'experience_years': int,
    'qualifications': str,
    'verified': bool,
    'available_slots': [(date, time), ...],
    'assigned_patients': [patient_ids],
    'consultation_fee': int,
    'ratings': [1-5],
    'average_rating': float
}
```

### Appointment

```python
{
    'appointment_id': str,
    'patient_id': str,
    'doctor_id': str,
    'date': 'YYYY-MM-DD',
    'time': 'HH:MM',
    'reason': str,
    'status': 'pending|confirmed|completed|cancelled',
    'notes': str,
    'created_at': 'YYYY-MM-DD HH:MM:SS'
}
```

### Medical Record

```python
{
    'record_id': str,
    'patient_id': str,
    'doctor_id': str,
    'date_created': 'YYYY-MM-DD',
    'diagnosis': str,
    'prescription': str,
    'test_results': str,
    'notes': str,
    'follow_up_date': 'YYYY-MM-DD'
}
```

### Complaint

```python
{
    'complaint_id': str,
    'filed_by_type': 'patient|doctor',
    'filed_by_id': str,
    'against_id': str,
    'complaint_type': 'Service|Medical|Staff|Billing|Other',
    'description': str,
    'date_filed': 'YYYY-MM-DD HH:MM:SS',
    'status': 'pending|under_review|resolved',
    'resolution': str,
    'resolved_by': str
}
```

## Key Features & Implementation

### 1. User Authentication

- Secure password hashing using SHA-256 with random salt
- Password strength validation (minimum 6 characters)
- Username uniqueness checking
- Session management on login

### 2. Appointment System

- Real-time conflict detection
- Automatic availability checking
- Appointment status tracking
- Reschedule and cancellation support

### 3. Medical Records

- Secure patient-doctor access control
- Record creation and updates
- Follow-up date tracking
- Test result storage

### 4. Complaint Management

- Multiple complaint types (Service, Medical, Staff, Billing)
- Status tracking (Pending, Under Review, Resolved)
- Admin resolution with documentation

### 5. Rating System

- Patients can rate doctors (1-5 stars)
- Average rating calculation
- Rating history tracking

## Specializations Supported

- General Medicine
- Cardiology
- Pediatrics
- Orthopedics
- Neurology
- Dermatology
- ENT (Ear, Nose, Throat)
- Ophthalmology
- Dentistry
- Psychiatry
- Gynecology
- Urology

## Data Persistence

All data is automatically saved to JSON files in the `data/` directory:

- **patients.json** - All patient profiles
- **doctors.json** - All doctor profiles
- **appointments.json** - All appointment records
- **medical_records.json** - All medical records
- **complaints.json** - All complaints
- **prescriptions.json** - All prescriptions
- **admin_users.json** - Admin credentials

Data is automatically loaded from JSON files when the system starts.

## Input Validation

### Email Validation

- Standard email format (user@domain.com)

### Phone Validation

- 10-15 digits with optional dashes and spaces

### Username Validation

- 3-20 characters
- Alphanumeric and underscore only
- Unique across all users

### Password Validation

- Minimum 6 characters
- Hashed with SHA-256 before storage

### Date Validation

- Format: YYYY-MM-DD
- Must be in the future for appointments
- Must be at least 18 years old for patient registration

### Time Validation

- Format: HH:MM
- Within clinic hours (09:00 - 18:00)

## Error Handling

The system includes comprehensive error handling for:

- Invalid input formats
- Duplicate username/email
- Authentication failures
- Data not found scenarios
- File I/O operations
- Invalid choice selections

## Testing Scenarios

### Patient Registration & Login

1. Register a new patient with all required information
2. Login with created credentials
3. Verify profile data is saved correctly

### Doctor Registration & Verification

1. Register a new doctor
2. Verify account is initially unverified
3. Login as admin and verify the doctor
4. Doctor can now login and access dashboard

### Appointment Booking

1. Login as patient
2. Select doctor and available time
3. Verify appointment appears in both patient and doctor views
4. Cancel and rebook appointment

### Medical Records

1. Login as doctor
2. Create medical record for assigned patient
3. Login as patient and view the record
4. Doctor updates record with new diagnosis
5. Patient sees updated information

### Complaints & Resolution

1. Patient files complaint
2. Admin views complaint as pending
3. Admin resolves complaint with resolution text
4. Patient can view resolved complaint

## Performance Notes

- Fast lookups using dictionary-based storage
- JSON persistence for data durability
- In-memory caching of all entities
- Efficient filtering with list comprehensions

## Future Enhancements

Potential features for future development:

1. Email notification system
2. SMS notifications for appointments
3. Billing and payment integration
4. Lab report generation
5. Mobile app interface
6. Database migration to SQL
7. API-based architecture (REST)
8. User dashboard analytics
9. Appointment reminder system
10. Doctor availability calendar view

## Troubleshooting

### Data Not Persisting

- Ensure the `data/` directory is created
- Check file permissions for write access
- Verify JSON file format is valid

### Login Issues

- Confirm username and password are correct
- Check if account is verified (for doctors)
- Ensure user account is active

### Appointment Booking Issues

- Verify doctor has available slots
- Check appointment date is in the future
- Ensure time is within clinic hours (09:00-18:00)

## Code Structure & Best Practices

### OOP Principles

- **Encapsulation**: Private attributes with getter/setter methods
- **Inheritance**: User base class extended by Patient and Doctor
- **Polymorphism**: Common interface for different user types
- **Abstraction**: Complex operations hidden in methods

### Python Features Used

- Class definitions and inheritance
- Dictionary comprehensions and filtering
- List operations and sorting
- String formatting and validation with regex
- Exception handling with try-except
- File I/O with JSON module
- Datetime operations

### Code Quality

- Clear variable naming
- Comprehensive docstrings
- Modular function design
- DRY (Don't Repeat Yourself) principle
- Consistent code formatting

## License

This project is created as an educational demonstration of Python programming concepts including OOP, dictionaries, lists, tuples, and file handling.

## Author

Clinic Management System - Python Education Project

---

**Note**: This is a CLI-based system designed for educational purposes. For production use, consider:

- Adding a web interface (Flask/Django)
- Implementing a proper database (SQL/NoSQL)
- Adding encryption for sensitive data
- Implementing proper session management
- Adding comprehensive logging and monitoring
