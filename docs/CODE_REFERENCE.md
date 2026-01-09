# Clinic Management System - Code Examples & Reference

## Quick Code Reference

This document provides examples of key code sections and how to extend the system.

---

## 1. User Models

### Creating a Patient

```python
from models import Patient
from auth import hash_password
from utils import generate_id

# Create new patient
patient_id = generate_id()
password_hash = hash_password("securepass123")

patient = Patient(
    user_id=patient_id,
    username="john_doe",
    password_hash=password_hash,
    email="john@example.com",
    phone="5551234567",
    date_of_birth="1995-05-15",
    gender="Male",
    address="123 Main St",
    blood_type="O+",
    allergies="Penicillin",
    emergency_contact="5559876543"
)

# Save to database
db.add_patient(patient)
```

### Creating a Doctor

```python
from models import Doctor
from auth import hash_password
from utils import generate_id

# Create new doctor
doctor_id = generate_id()
password_hash = hash_password("drpass123")

doctor = Doctor(
    user_id=doctor_id,
    username="dr_smith",
    password_hash=password_hash,
    email="dr.smith@hospital.com",
    phone="5559876543",
    specialization="Cardiology",
    license_number="LIC12345",
    experience_years=5,
    qualifications="MBBS, MD Cardiology",
    verified=False
)

# Save to database
db.add_doctor(doctor)
```

---

## 2. Authentication

### Password Hashing

```python
from auth import hash_password, verify_password

# Hash a password
password = "mypassword123"
password_hash = hash_password(password)
# Returns: "salt$hashed_value"

# Verify password
is_correct = verify_password(password_hash, "mypassword123")  # True
is_correct = verify_password(password_hash, "wrongpassword")  # False
```

### Username Validation

```python
from utils import validate_username, validate_password, validate_email

# Check username format
valid = validate_username("john_doe")  # True
valid = validate_username("ab")        # False (too short)

# Check password strength
valid = validate_password("abc123")      # True
valid = validate_password("abc")         # False (too short)

# Check email format
valid = validate_email("john@example.com")  # True
valid = validate_email("invalid-email")     # False
```

---

## 3. Appointment Management

### Booking an Appointment

```python
from models import Appointment
from utils import generate_id

# Create appointment
appt_id = generate_id()
appointment = Appointment(
    appointment_id=appt_id,
    patient_id="patient123",
    doctor_id="doctor456",
    date="2024-12-15",
    time="14:00",
    reason="Regular checkup"
)

# Save to database
db.add_appointment(appointment)

# Appointment automatically added to patient and doctor
patient = db.get_patient("patient123")
print(appt_id in patient.appointments)  # True
```

### Confirming an Appointment

```python
# Get appointment
appointment = db.get_appointment("appt123")

# Confirm it
appointment.confirm()
db.update_appointment(appointment)

print(appointment.status)  # "confirmed"
```

### Completing an Appointment

```python
appointment = db.get_appointment("appt123")

# Mark as completed with notes
notes = "Patient's condition improving, continue medication"
appointment.complete(notes)
db.update_appointment(appointment)

print(appointment.status)  # "completed"
print(appointment.notes)   # "Patient's condition improving..."
```

### Checking for Conflicts

```python
# Get all appointments for a doctor on a specific date/time
doctor_id = "doctor456"
date = "2024-12-15"
time = "14:00"

existing_appts = db.get_doctor_appointments(doctor_id)
conflict = any(
    a.date == date and a.time == time and a.status != 'cancelled'
    for a in existing_appts
)

if conflict:
    print("Time slot already booked!")
else:
    # Create appointment
    pass
```

---

## 4. Medical Records

### Creating a Medical Record

```python
from models import MedicalRecord
from utils import generate_id

record_id = generate_id()
record = MedicalRecord(
    record_id=record_id,
    patient_id="patient123",
    doctor_id="doctor456",
    diagnosis="Type 2 Diabetes",
    prescription="Metformin 500mg twice daily",
    test_results="Fasting glucose: 145 mg/dL",
    notes="Patient advised on diet and exercise",
    follow_up_date="2024-12-25"
)

db.add_medical_record(record)
```

### Updating a Medical Record

```python
record = db.get_medical_record("record123")

# Update specific fields
record.update(
    diagnosis="Type 2 Diabetes (controlled)",
    test_results="Fasting glucose: 120 mg/dL"
)

db.update_medical_record(record)
```

### Retrieving Patient Medical Records

```python
# Get all active records for a patient
patient_id = "patient123"
records = db.get_patient_medical_records(patient_id)

# Sort by date (newest first)
records.sort(key=lambda r: r.date_created, reverse=True)

for record in records:
    print(f"Date: {record.date_created}")
    print(f"Diagnosis: {record.diagnosis}")
    print(f"Doctor: {record.doctor_id}")
```

---

## 5. Complaint Management

### Filing a Complaint

```python
from models import Complaint
from utils import generate_id

complaint_id = generate_id()
complaint = Complaint(
    complaint_id=complaint_id,
    filed_by_type="patient",
    filed_by_id="patient123",
    against_id="doctor456",
    complaint_type="Medical",
    description="Prescribed medication caused side effects"
)

db.add_complaint(complaint)
```

### Resolving a Complaint (Admin)

```python
complaint = db.get_complaint("complaint123")

# Admin marks as under review
complaint.mark_under_review()
db.update_complaint(complaint)

# Later, resolve the complaint
resolution = "Medication changed to alternative with better tolerance"
admin_id = "admin_user"

complaint.resolve(resolution, admin_id)
db.update_complaint(complaint)

print(complaint.status)      # "resolved"
print(complaint.resolution)  # "Medication changed..."
```

### Viewing Complaints

```python
# Get all pending complaints
pending = db.get_complaints_by_status('pending')

# Get complaints against specific doctor
doctor_complaints = db.get_complaints_against_doctor("doctor456")

# Get complaints filed by patient
patient_complaints = db.get_complaints_by_patient("patient123")

for complaint in patient_complaints:
    print(f"Type: {complaint.complaint_type}")
    print(f"Status: {complaint.status}")
    print(f"Filed: {complaint.date_filed}")
```

---

## 6. Prescriptions

### Issuing a Prescription

```python
from models import Prescription
from utils import generate_id

presc_id = generate_id()
prescription = Prescription(
    prescription_id=presc_id,
    patient_id="patient123",
    doctor_id="doctor456",
    medication="Aspirin",
    dosage="75mg",
    duration="30 days",
    instructions="Take one tablet daily with food"
)

db.add_prescription(prescription)
```

### Getting Patient Prescriptions

```python
# Get all active prescriptions for a patient
patient_id = "patient123"
prescriptions = db.get_patient_prescriptions(patient_id)

for presc in prescriptions:
    print(f"Medication: {presc.medication}")
    print(f"Dosage: {presc.dosage}")
    print(f"Duration: {presc.duration}")
    print(f"Issued: {presc.date_issued}")
```

---

## 7. Doctor Schedule Management

### Adding Available Slots

```python
doctor = db.get_doctor("doctor456")

# Add multiple slots
doctor.add_available_slot("2024-12-15", "09:00")
doctor.add_available_slot("2024-12-15", "10:00")
doctor.add_available_slot("2024-12-16", "14:00")

db.update_doctor(doctor)
```

### Checking Available Slots

```python
doctor = db.get_doctor("doctor456")

print(f"Available slots: {doctor.available_slots}")
# Output: [('2024-12-15', '09:00'), ('2024-12-15', '10:00'), ...]

# Check if slot is available
slot = ("2024-12-15", "09:00")
if slot in doctor.available_slots:
    print("Slot available!")
```

### Removing Unavailable Slots

```python
doctor = db.get_doctor("doctor456")
doctor.remove_available_slot("2024-12-15", "09:00")
db.update_doctor(doctor)
```

---

## 8. Doctor Rating System

### Adding a Rating

```python
doctor = db.get_doctor("doctor456")

# Patient rates doctor (1-5 stars)
doctor.add_rating(5)
db.update_doctor(doctor)

print(f"Current ratings: {doctor.ratings}")  # [5]
print(f"Average: {doctor.get_average_rating()}")  # 5.0
```

### Multiple Ratings

```python
doctor = db.get_doctor("doctor456")

# Multiple patients rate
doctor.add_rating(5)  # Patient 1: 5 stars
doctor.add_rating(4)  # Patient 2: 4 stars
doctor.add_rating(5)  # Patient 3: 5 stars

db.update_doctor(doctor)

avg_rating = doctor.get_average_rating()
print(f"Average rating: {avg_rating}")  # 4.67
print(f"Total ratings: {len(doctor.ratings)}")  # 3
```

---

## 9. Database Queries

### Filtering Patients

```python
# Get all active patients
patients = db.get_all_patients()

# Get patient by username
patient = db.get_patient_by_username("john_doe")

# Get patient by ID
patient = db.get_patient("patient123")

# Custom filtering
patients_with_allergies = [
    p for p in db.get_all_patients()
    if p.allergies != 'None'
]
```

### Filtering Doctors

```python
# Get all verified doctors
doctors = db.get_all_doctors()

# Get unverified doctors (for admin)
pending = db.get_all_unverified_doctors()

# Get doctors by specialization
cardiologists = db.get_doctors_by_specialization("Cardiology")

# Find top-rated doctor
top_doctor = max(
    doctors,
    key=lambda d: d.get_average_rating()
)
```

### Filtering Appointments

```python
# Get appointments by status
pending_appts = db.get_appointments_by_status('pending')
completed_appts = db.get_appointments_by_status('completed')

# Get patient's appointments
patient_appts = db.get_patient_appointments("patient123")

# Get doctor's appointments
doctor_appts = db.get_doctor_appointments("doctor456")

# Filter by date
appts_today = [
    a for a in db.get_patient_appointments("patient123")
    if a.date == "2024-12-15"
]
```

---

## 10. Data Persistence

### Saving Data

```python
# Data is automatically saved after operations:
db.add_patient(patient)      # Auto-saves to patients.json
db.add_appointment(appt)     # Auto-saves to appointments.json
db.add_medical_record(rec)   # Auto-saves to medical_records.json
db.add_complaint(comp)       # Auto-saves to complaints.json

# You can also manually trigger saves:
db.save_patients()
db.save_doctors()
db.save_appointments()
db.save_medical_records()
db.save_complaints()
db.save_prescriptions()
```

### Loading Data

```python
# Data is automatically loaded on startup:
db = Database()

# Manual loading (rarely needed):
db.load_patients()
db.load_doctors()
db.load_appointments()
db.load_medical_records()
db.load_complaints()
db.load_prescriptions()

# Load all data at once
db.load_all_data()
```

### Checking Data

```python
# Check if data exists
if "patient123" in db.patients:
    print("Patient exists!")

# Get all data
all_patients = dict(db.patients)
all_doctors = dict(db.doctors)
all_appointments = dict(db.appointments)

# Get statistics
stats = db.get_system_statistics()
print(f"Total patients: {stats['total_patients']}")
print(f"Total doctors: {stats['total_doctors']}")
print(f"Pending appointments: {stats['pending_appointments']}")
```

---

## 11. Input Validation

### Date Validation

```python
from utils import validate_date, validate_time, validate_datetime, format_date

# Validate date
if validate_date("2024-12-15"):
    print("Valid date!")

# Validate time
if validate_time("14:30"):
    print("Valid time!")

# Validate both together
if validate_datetime("2024-12-15", "14:30"):
    print("Valid datetime!")

# Format for display
formatted = format_date("2024-12-15")  # "15-Dec-2024"
formatted = format_datetime("2024-12-15", "14:30")  # "15-Dec-2024 14:30"
```

### Email and Phone Validation

```python
from utils import validate_email, validate_phone

# Email validation
if validate_email("john@example.com"):
    print("Valid email!")

# Phone validation
if validate_phone("555-123-4567"):
    print("Valid phone!")
```

### Age Validation

```python
from utils import validate_age, get_age

# Check if person is at least 18
if validate_age("2005-06-15"):
    print("Person is 18+!")

# Get actual age
age = get_age("1995-05-15")  # 29
```

---

## 12. Menu Display

### Creating Menus

```python
from utils import display_menu, print_header, print_subheader

# Create a menu
options = [
    "Book Appointment",
    "View Medical Records",
    "Submit Complaint",
    "Logout"
]

choice = display_menu(options, "Patient Menu")
# Returns: 1, 2, 3, or 4

if choice == 1:
    # Book appointment logic
    pass
elif choice == 2:
    # View records logic
    pass
```

### Formatting Output

```python
from utils import print_header, print_subheader, print_separator
from utils import print_success, print_error, print_info

# Print header
print_header("PATIENT DASHBOARD")

# Print subheader
print_subheader("Appointments")

# Print separator line
print_separator()

# Print styled messages
print_success("Appointment booked successfully!")
print_error("Doctor not available at this time!")
print_info("Your account is pending verification.")

# Pause and wait for input
from utils import pause
pause()
```

---

## 13. Extending the System

### Adding a New Feature

Example: Add "Prescription Refill" feature

```python
# 1. Add method to Patient class (models.py)
class Patient(User):
    def request_prescription_refill(self, prescription_id):
        # Logic here
        pass

# 2. Add database method (database.py)
class Database:
    def get_pending_refills(self):
        # Return prescriptions needing refill
        pass

# 3. Add UI menu item (main.py)
def patient_dashboard(self):
    options = [
        # ... existing options ...
        "Request Prescription Refill",
    ]

    if choice == 11:  # New option
        self.request_prescription_refill()

# 4. Implement UI function
def request_prescription_refill(self):
    prescriptions = db.get_patient_prescriptions(self.current_user.user_id)
    # Display menu and process request
    pass
```

### Adding a New Data Model

```python
# 1. Create model in models.py
class LabReport:
    def __init__(self, report_id, patient_id, test_name, result):
        self.report_id = report_id
        self.patient_id = patient_id
        self.test_name = test_name
        self.result = result
        self.date_created = datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            'report_id': self.report_id,
            'patient_id': self.patient_id,
            'test_name': self.test_name,
            'result': self.result,
            'date_created': self.date_created
        }

# 2. Add to Database class
class Database:
    def __init__(self, data_dir='data'):
        # ... existing code ...
        self.lab_reports = {}

    def add_lab_report(self, report):
        self.lab_reports[report.report_id] = report
        self.save_lab_reports()

    def save_lab_reports(self):
        data = {rid: r.to_dict() for rid, r in self.lab_reports.items()}
        self._save_json('data/lab_reports.json', data)
```

---

## 14. Error Handling

### Try-Except Blocks

```python
try:
    choice = int(input("Enter number: "))
    if 1 <= choice <= len(options):
        # Process choice
        pass
    else:
        print("Invalid choice!")
except ValueError:
    print("Please enter a valid number!")
except Exception as e:
    print(f"Error: {str(e)}")
```

### Validation Before Operations

```python
# Always validate before creating records
email = input("Enter email: ")
if not validate_email(email):
    print_error("Invalid email format!")
    return

# Check for duplicates
if db.get_patient_by_username(username):
    print_error("Username already exists!")
    return

# Verify user exists
doctor = db.get_doctor(doctor_id)
if not doctor:
    print_error("Doctor not found!")
    return
```

---

## 15. List Comprehensions

### Filtering Data

```python
# Get all doctors in a specialization
cardiologists = [
    d for d in db.get_all_doctors()
    if d.specialization == "Cardiology"
]

# Get completed appointments
completed = [
    a for a in db.get_doctor_appointments(doctor_id)
    if a.status == 'completed'
]

# Get high-rated doctors (4+ stars)
top_doctors = [
    d for d in db.get_all_doctors()
    if d.get_average_rating() >= 4.0
]

# Get appointments with notes
detailed_appts = [
    a for a in db.appointments.values()
    if a.notes
]
```

### Sorting Data

```python
# Sort appointments by date
appointments.sort(key=lambda a: (a.date, a.time))

# Sort doctors by rating
doctors.sort(key=lambda d: d.get_average_rating(), reverse=True)

# Sort complaints by date
complaints.sort(key=lambda c: c.date_filed, reverse=True)

# Sort patients by name
patients.sort(key=lambda p: p.username)
```

---

## Tips & Best Practices

### 1. Always Validate Input

```python
# ❌ Wrong
username = input("Enter username: ")
db.add_patient(username)

# ✅ Right
username = input("Enter username: ")
if validate_username(username):
    db.add_patient(username)
else:
    print_error("Invalid username format!")
```

### 2. Check for Duplicates

```python
# ❌ Wrong
db.add_appointment(appointment)  # What if slot already booked?

# ✅ Right
doctor_appts = db.get_doctor_appointments(doctor_id)
if any(a.date == date and a.time == time for a in doctor_appts):
    print_error("Time slot already booked!")
else:
    db.add_appointment(appointment)
```

### 3. Use Constants

```python
# ❌ Wrong
if user_type == "patient":  # Magic string
    # ...

# ✅ Right
PATIENT = "patient"
DOCTOR = "doctor"
ADMIN = "admin"

if user_type == PATIENT:
    # ...
```

### 4. Handle Errors Gracefully

```python
# ❌ Wrong
patient = db.get_patient(patient_id)
print(patient.email)  # Might crash if patient is None

# ✅ Right
patient = db.get_patient(patient_id)
if patient:
    print(patient.email)
else:
    print_error("Patient not found!")
```

---

## Debugging Tips

### 1. Print Debug Information

```python
# Add temporary debug prints
print(f"DEBUG: patient_id = {patient_id}")
print(f"DEBUG: patient object = {patient}")
print(f"DEBUG: all patients = {list(db.patients.keys())}")
```

### 2. Check JSON Files

```bash
# View data directory
ls data/

# Check JSON content (on Windows)
type data\patients.json

# Pretty print JSON
python -m json.tool data/patients.json
```

### 3. Test Individual Components

```python
# Test authentication
from auth import hash_password, verify_password
pw_hash = hash_password("test123")
print(verify_password(pw_hash, "test123"))  # Should be True

# Test validation
from utils import validate_email
print(validate_email("test@example.com"))  # Should be True
```

---

## Complete Example: Adding a Patient and Booking Appointment

```python
from models import Patient, Appointment, Database
from auth import hash_password
from utils import generate_id, validate_email

# Initialize database
db = Database()

# 1. Create and add patient
patient_id = generate_id()
patient = Patient(
    user_id=patient_id,
    username="alice_smith",
    password_hash=hash_password("pass123"),
    email="alice@example.com",
    phone="5551234567",
    date_of_birth="1990-03-20",
    gender="Female",
    address="456 Oak Ave",
    blood_type="A+"
)
db.add_patient(patient)

# 2. Create doctor (already registered and verified)
doctor = db.get_doctor("doctor456")

# 3. Create appointment
appt_id = generate_id()
appointment = Appointment(
    appointment_id=appt_id,
    patient_id=patient_id,
    doctor_id=doctor.user_id,
    date="2024-12-20",
    time="15:00",
    reason="Annual checkup"
)
db.add_appointment(appointment)

# 4. Verify data was saved
saved_patient = db.get_patient(patient_id)
patient_appts = db.get_patient_appointments(patient_id)

print(f"Patient: {saved_patient.username}")
print(f"Appointments: {len(patient_appts)}")
print(f"Doctor: Dr. {doctor.username}")

# 5. Doctor confirms appointment
appointment.confirm()
db.update_appointment(appointment)
print(f"Appointment status: {appointment.status}")

# 6. Create medical record
from models import MedicalRecord
record = MedicalRecord(
    record_id=generate_id(),
    patient_id=patient_id,
    doctor_id=doctor.user_id,
    diagnosis="Healthy",
    prescription="Continue current regimen"
)
db.add_medical_record(record)

# 7. Complete appointment
appointment.complete("Patient in good health")
db.update_appointment(appointment)

# 8. Patient rates doctor
doctor.add_rating(5)
db.update_doctor(doctor)

print(f"\nDoctor rating: {doctor.get_average_rating()}/5")
```

---

This code reference guide should help you understand and extend the Clinic Management System!
