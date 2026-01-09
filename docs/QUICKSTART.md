# Quick Start Guide - Clinic Management System

## Installation

No installation required! The system uses only Python's standard library.

**Requirements:**

- Python 3.8 or higher
- Command line/terminal access

## Running the System

### Step 1: Open Terminal

Navigate to the project folder:

```bash
cd path\to\Clinic-Management-System
```

### Step 2: Start the Application

```bash
python main.py
```

You should see the main menu appear in your terminal.

## Quick Demo Walkthrough

### 1. Default Admin Login

```
Login as Admin → admin / admin123
```

### 2. Register as Patient

```
From Main Menu → Register as Patient
  - Username: john_patient
  - Password: password123
  - Email: john@example.com
  - Phone: 1234567890
  - DOB: 1995-05-15 (must be 18+)
  - Gender: Male
  - Address: 123 Main St
  - Blood Type: O+
  - Allergies: None
  - Emergency Contact: 9876543210
```

### 3. Register as Doctor

```
From Main Menu → Register as Doctor
  - Username: dr_smith
  - Password: password123
  - Email: dr.smith@hospital.com
  - Phone: 9876543210
  - Specialization: Cardiology
  - License: LIC12345
  - Experience: 5
  - Qualifications: MBBS, MD
  - Status: Pending (Admin must verify)
```

### 4. Admin Verification

```
Login as Admin → Manage Doctors → Verify Pending Doctors → Select Dr. Smith
```

### 5. Doctor Sets Schedule

```
Login as Doctor → Manage Schedule → Add Available Slot
  - Date: 2024-12-15
  - Time: 14:00
```

### 6. Patient Books Appointment

```
Login as Patient → Book Appointment
  - Select Specialization: Cardiology
  - Select Doctor: Dr. Smith
  - Date: 2024-12-15
  - Time: 14:00
  - Reason: Chest pain checkup
```

### 7. Doctor Completes Appointment

```
Login as Doctor → Confirm/Complete Appointment
  - Select the appointment
  - Confirm it
  - Later: Mark as Completed with notes
```

### 8. Create Medical Record

```
Login as Doctor → Create Medical Record
  - Select Patient: john_patient
  - Diagnosis: Hypertension
  - Prescription: Amlodipine 5mg
  - Follow-up: 2024-12-25
```

### 9. Patient Rates Doctor

```
Login as Patient → Rate Doctor
  - Select completed appointment
  - Give 5-star rating
```

### 10. Patient Files Complaint

```
Login as Patient → Submit Complaint
  - Type: Medical
  - Select Doctor: Dr. Smith
  - Description: Prescription didn't help
```

### 11. Admin Resolves Complaint

```
Login as Admin → Manage Complaints → Resolve Complaint
  - Select pending complaint
  - Add resolution: Medication adjusted
```

## File Structure After First Run

After running the system, you'll see:

```
Clinic-Management-System/
├── main.py
├── models.py
├── auth.py
├── database.py
├── utils.py
├── README.md
├── IMPLEMENTATION_PLAN.md
└── data/                    (Created automatically)
    ├── patients.json
    ├── doctors.json
    ├── appointments.json
    ├── medical_records.json
    ├── complaints.json
    ├── prescriptions.json
    └── admin_users.json
```

## Menu Navigation

### Main Menu (Unauthenticated)

```
1. Login as Patient
2. Login as Doctor
3. Login as Admin
4. Register as Patient
5. Register as Doctor
6. Exit
```

### Patient Dashboard

```
1. View Profile
2. Edit Profile
3. Book Appointment
4. View Appointments
5. Cancel Appointment
6. View Medical Records
7. View Prescriptions
8. Submit Complaint
9. View Complaints
10. Rate Doctor
11. Logout
```

### Doctor Dashboard

```
1. View Profile
2. Edit Profile
3. Manage Schedule
4. View Appointments
5. Confirm/Complete Appointment
6. View Assigned Patients
7. Create Medical Record
8. Update Medical Record
9. View Patient Records
10. Issue Prescription
11. View Complaints
12. View Ratings
13. Logout
```

### Admin Dashboard

```
1. View System Statistics
2. Manage Doctors
3. View All Users
4. Manage Complaints
5. View Appointments
6. Change Admin Password
7. Logout
```

## Test Data Examples

### Sample Patient Data

- **Username**: alice_doe
- **Email**: alice@example.com
- **Phone**: 5551234567
- **Blood Type**: A+
- **Allergies**: Penicillin

### Sample Doctor Data

- **Username**: dr_johnson
- **Specialization**: Pediatrics
- **License**: LIC98765
- **Experience**: 8 years
- **Consultation Fee**: 500

## Important Notes

1. **Dates & Times**: Always use YYYY-MM-DD and HH:MM formats
2. **Clinic Hours**: 09:00 to 18:00 (9 AM to 6 PM)
3. **Age Requirement**: Patients must be 18+ years old
4. **Doctor Verification**: Doctors need admin approval before patient interaction
5. **Data Persistence**: All changes are automatically saved to JSON files

## Troubleshooting

### Application won't start

- Check Python version: `python --version`
- Ensure you're in the correct directory
- Check for file permission issues

### Can't login

- Verify username and password are correct
- For doctors: Check if account is verified by admin
- Ensure user account hasn't been deactivated

### Can't book appointment

- Doctor must have available slots configured
- Date must be in the future
- Time must be within clinic hours (09:00-18:00)

### Lost default admin password

- Delete `data/admin_users.json`
- Restart the system (will recreate default admin)
- Default: admin / admin123

## Key Features to Try

1. ✅ Complete user registration and authentication
2. ✅ Role-based access control (Patient/Doctor/Admin)
3. ✅ Appointment booking with conflict detection
4. ✅ Medical record creation and updates
5. ✅ Complaint filing and resolution
6. ✅ Doctor rating system
7. ✅ Schedule management
8. ✅ Prescription management
9. ✅ Data persistence with JSON

## Support

For more detailed information, see:

- `README.md` - Complete system documentation
- `IMPLEMENTATION_PLAN.md` - Architecture and design details
- Source code comments for specific functions

## Tips for Best Experience

1. Start by logging in as Admin to verify a test doctor
2. Register as both Patient and Doctor to test all features
3. Try booking multiple appointments to test conflict detection
4. File complaints and use admin resolution feature
5. Check JSON files in `data/` folder to see persisted data

---

**Happy Testing!** 🏥
