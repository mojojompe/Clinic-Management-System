import os
import sys
from datetime import datetime, timedelta
from utils import (
    generate_id, print_header, print_subheader, print_separator, 
    print_success, print_error, print_info, input_with_validation,
    validate_email, validate_phone, validate_username, validate_password,
    validate_date, validate_time, validate_age, input_yes_no,
    display_menu, pause, format_date, format_datetime, get_age,
    get_specializations, get_complaint_types, get_blood_types, get_genders
)
from auth import hash_password, verify_password, check_username_exists
from models import Patient, Doctor, Appointment, MedicalRecord, Complaint, Prescription
from database import Database


class ClinicManagementSystem:
    """Main application class"""
    
    def __init__(self):
        self.db = Database()
        self.current_user = None
        self.current_user_type = None  # 'patient', 'doctor', 'admin'
    
    def run(self):
        """Main application loop"""
        # Initialize default admin if not exists
        if not self.db.admin_exists('admin'):
            admin_hash = hash_password('admin123')
            self.db.add_admin('admin', admin_hash)
        
        while True:
            if self.current_user is None:
                self.main_menu()
            elif self.current_user_type == 'patient':
                self.patient_dashboard()
            elif self.current_user_type == 'doctor':
                self.doctor_dashboard()
            elif self.current_user_type == 'admin':
                self.admin_dashboard()
    
    # ==================== MAIN MENU ====================
    
    def main_menu(self):
        """Main menu for unauthenticated users"""
        clear_screen()
        print_header("CLINIC MANAGEMENT SYSTEM")
        options = [
            "Login as Patient",
            "Login as Doctor",
            "Login as Admin",
            "Register as Patient",
            "Register as Doctor",
            "Exit"
        ]
        choice = display_menu(options, "Main Menu")
        
        if choice == 1:
            self.patient_login()
        elif choice == 2:
            self.doctor_login()
        elif choice == 3:
            self.admin_login()
        elif choice == 4:
            self.patient_registration()
        elif choice == 5:
            self.doctor_registration()
        elif choice == 6:
            print("\nThank you for using Clinic Management System. Goodbye!")
            sys.exit(0)
    
    # ==================== AUTHENTICATION ====================
    
    def patient_login(self):
        """Patient login"""
        clear_screen()
        print_header("PATIENT LOGIN")
        
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        patient = self.db.get_patient_by_username(username)
        
        if patient and patient.verify_password(password):
            patient.update_last_login()
            self.db.update_patient(patient)
            self.current_user = patient
            self.current_user_type = 'patient'
            print_success(f"Welcome back, {patient.username}!")
            pause()
        else:
            print_error("Invalid username or password!")
            pause()
    
    def doctor_login(self):
        """Doctor login"""
        clear_screen()
        print_header("DOCTOR LOGIN")
        
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        doctor = self.db.get_doctor_by_username(username)
        
        if doctor and doctor.verify_password(password):
            if not doctor.verified:
                print_error("Your account is pending verification by admin.")
                pause()
                return
            
            doctor.update_last_login()
            self.db.update_doctor(doctor)
            self.current_user = doctor
            self.current_user_type = 'doctor'
            print_success(f"Welcome back, Dr. {doctor.username}!")
            pause()
        else:
            print_error("Invalid username or password!")
            pause()
    
    def admin_login(self):
        """Admin login"""
        clear_screen()
        print_header("ADMIN LOGIN")
        
        username = input("Enter admin username: ").strip()
        password = input("Enter admin password: ").strip()
        
        stored_hash = self.db.get_admin_password_hash(username)
        
        if stored_hash and verify_password(stored_hash, password):
            self.current_user = {'username': username}
            self.current_user_type = 'admin'
            print_success(f"Welcome, Admin {username}!")
            pause()
        else:
            print_error("Invalid admin credentials!")
            pause()
    
    def patient_registration(self):
        """Patient registration"""
        clear_screen()
        print_header("PATIENT REGISTRATION")
        
        # Get username
        while True:
            username = input_with_validation(
                "Enter username (3-20 chars): ",
                validate_username,
                "Invalid username format"
            )
            if username and not check_username_exists(username, {**self.db.patients, **self.db.doctors}):
                break
            elif username:
                print_error("Username already exists!")
        
        # Get password
        password = input_with_validation(
            "Enter password (min 6 chars): ",
            validate_password,
            "Password too short"
        )
        
        # Get email
        email = input_with_validation(
            "Enter email: ",
            validate_email,
            "Invalid email format"
        )
        
        # Get phone
        phone = input_with_validation(
            "Enter phone number: ",
            validate_phone,
            "Invalid phone format"
        )
        
        # Get date of birth
        while True:
            dob = input("Enter date of birth (YYYY-MM-DD): ").strip()
            if validate_date(dob) and validate_age(dob):
                break
            else:
                print_error("Must be at least 18 years old!")
        
        # Get gender
        genders = get_genders()
        gender = genders[display_menu(genders, "Select Gender") - 1]
        
        # Get address
        address = input("Enter address: ").strip()
        
        # Get blood type
        blood_types = get_blood_types()
        blood_type = blood_types[display_menu(blood_types, "Select Blood Type") - 1]
        
        # Get allergies
        allergies = input("Enter allergies (or 'None'): ").strip() or 'None'
        
        # Get emergency contact
        emergency_contact = input("Enter emergency contact (phone): ").strip()
        
        # Create patient
        patient_id = generate_id()
        password_hash = hash_password(password)
        
        patient = Patient(
            user_id=patient_id,
            username=username,
            password_hash=password_hash,
            email=email,
            phone=phone,
            date_of_birth=dob,
            gender=gender,
            address=address,
            blood_type=blood_type,
            allergies=allergies,
            emergency_contact=emergency_contact
        )
        
        self.db.add_patient(patient)
        print_success("Patient registration successful! You can now login.")
        pause()
    
    def doctor_registration(self):
        """Doctor registration"""
        clear_screen()
        print_header("DOCTOR REGISTRATION")
        
        # Get username
        while True:
            username = input_with_validation(
                "Enter username (3-20 chars): ",
                validate_username,
                "Invalid username format"
            )
            if username and not check_username_exists(username, {**self.db.patients, **self.db.doctors}):
                break
            elif username:
                print_error("Username already exists!")
        
        # Get password
        password = input_with_validation(
            "Enter password (min 6 chars): ",
            validate_password,
            "Password too short"
        )
        
        # Get email
        email = input_with_validation(
            "Enter email: ",
            validate_email,
            "Invalid email format"
        )
        
        # Get phone
        phone = input_with_validation(
            "Enter phone number: ",
            validate_phone,
            "Invalid phone format"
        )
        
        # Get specialization
        specializations = get_specializations()
        specialization = specializations[display_menu(specializations, "Select Specialization") - 1]
        
        # Get license number
        license_number = input("Enter license number: ").strip()
        
        # Get experience
        while True:
            try:
                experience = int(input("Enter years of experience: ").strip())
                break
            except ValueError:
                print_error("Please enter a valid number!")
        
        # Get qualifications
        qualifications = input("Enter qualifications (comma-separated): ").strip()
        
        # Create doctor
        doctor_id = generate_id()
        password_hash = hash_password(password)
        
        doctor = Doctor(
            user_id=doctor_id,
            username=username,
            password_hash=password_hash,
            email=email,
            phone=phone,
            specialization=specialization,
            license_number=license_number,
            experience_years=experience,
            qualifications=qualifications,
            verified=False  # Requires admin verification
        )
        
        self.db.add_doctor(doctor)
        print_success("Doctor registration successful! Awaiting admin verification.")
        print_info("You will be able to login once your account is verified.")
        pause()
    
    # ==================== PATIENT DASHBOARD ====================
    
    def patient_dashboard(self):
        """Patient main dashboard"""
        clear_screen()
        print_header(f"PATIENT DASHBOARD - {self.current_user.username}")
        
        options = [
            "View Profile",
            "Edit Profile",
            "Book Appointment",
            "View Appointments",
            "Cancel Appointment",
            "View Medical Records",
            "View Prescriptions",
            "Submit Complaint",
            "View Complaints",
            "Rate Doctor",
            "Logout"
        ]
        
        choice = display_menu(options, "Patient Menu")
        
        if choice == 1:
            self.view_patient_profile()
        elif choice == 2:
            self.edit_patient_profile()
        elif choice == 3:
            self.book_appointment()
        elif choice == 4:
            self.view_patient_appointments()
        elif choice == 5:
            self.cancel_appointment()
        elif choice == 6:
            self.view_patient_medical_records()
        elif choice == 7:
            self.view_patient_prescriptions()
        elif choice == 8:
            self.submit_complaint()
        elif choice == 9:
            self.view_patient_complaints()
        elif choice == 10:
            self.rate_doctor()
        elif choice == 11:
            self.current_user = None
            self.current_user_type = None
    
    def view_patient_profile(self):
        """View patient profile"""
        clear_screen()
        print_header("YOUR PROFILE")
        print(f"Username: {self.current_user.username}")
        print(f"Email: {self.current_user.email}")
        print(f"Phone: {self.current_user.phone}")
        print(f"Date of Birth: {format_date(self.current_user.date_of_birth)}")
        print(f"Age: {self.current_user.get_age()} years")
        print(f"Gender: {self.current_user.gender}")
        print(f"Address: {self.current_user.address}")
        print(f"Blood Type: {self.current_user.blood_type}")
        print(f"Allergies: {self.current_user.allergies}")
        print(f"Emergency Contact: {self.current_user.emergency_contact}")
        if self.current_user.height:
            print(f"Height: {self.current_user.height} cm")
        if self.current_user.weight:
            print(f"Weight: {self.current_user.weight} kg")
        print(f"Member Since: {format_date(self.current_user.created_at.split()[0])}")
        print_separator()
        pause()
    
    def edit_patient_profile(self):
        """Edit patient profile"""
        clear_screen()
        print_header("EDIT PROFILE")
        
        options = [
            "Change Password",
            "Update Phone Number",
            "Update Address",
            "Update Allergies",
            "Update Emergency Contact",
            "Update Height",
            "Update Weight",
            "Back"
        ]
        
        choice = display_menu(options, "Edit Options")
        
        if choice == 1:
            old_password = input("Enter current password: ").strip()
            if self.current_user.verify_password(old_password):
                new_password = input_with_validation(
                    "Enter new password: ",
                    validate_password,
                    "Password too short"
                )
                self.current_user.password_hash = hash_password(new_password)
                self.db.update_patient(self.current_user)
                print_success("Password updated successfully!")
            else:
                print_error("Incorrect current password!")
        elif choice == 2:
            phone = input_with_validation("Enter new phone number: ", validate_phone, "Invalid phone format")
            self.current_user.phone = phone
            self.db.update_patient(self.current_user)
            print_success("Phone number updated!")
        elif choice == 3:
            address = input("Enter new address: ").strip()
            self.current_user.address = address
            self.db.update_patient(self.current_user)
            print_success("Address updated!")
        elif choice == 4:
            allergies = input("Enter allergies (or 'None'): ").strip() or 'None'
            self.current_user.allergies = allergies
            self.db.update_patient(self.current_user)
            print_success("Allergies updated!")
        elif choice == 5:
            emergency_contact = input("Enter emergency contact: ").strip()
            self.current_user.emergency_contact = emergency_contact
            self.db.update_patient(self.current_user)
            print_success("Emergency contact updated!")
        elif choice == 6:
            try:
                height = int(input("Enter height (cm): ").strip())
                self.current_user.height = height
                self.db.update_patient(self.current_user)
                print_success("Height updated!")
            except ValueError:
                print_error("Invalid height value!")
        elif choice == 7:
            try:
                weight = int(input("Enter weight (kg): ").strip())
                self.current_user.weight = weight
                self.db.update_patient(self.current_user)
                print_success("Weight updated!")
            except ValueError:
                print_error("Invalid weight value!")
        
        pause()
    
    def book_appointment(self):
        """Book an appointment"""
        clear_screen()
        print_header("BOOK APPOINTMENT")
        
        # Get specialization
        specializations = get_specializations()
        spec_choice = display_menu(specializations, "Select Doctor Specialization")
        specialization = specializations[spec_choice - 1]
        
        # Get doctors with that specialization
        doctors = self.db.get_doctors_by_specialization(specialization)
        
        if not doctors:
            print_error("No doctors available for this specialization!")
            pause()
            return
        
        # Display available doctors
        clear_screen()
        print_subheader("Available Doctors")
        for i, doctor in enumerate(doctors, 1):
            rating = doctor.get_average_rating()
            print(f"{i}. Dr. {doctor.username} ({doctor.specialization}) - Rating: {rating:.1f}/5")
        print_separator()
        
        try:
            doctor_choice = int(input("Select doctor (number): ").strip())
            if 1 <= doctor_choice <= len(doctors):
                doctor = doctors[doctor_choice - 1]
            else:
                print_error("Invalid choice!")
                pause()
                return
        except ValueError:
            print_error("Invalid input!")
            pause()
            return
        
        # Get appointment date
        while True:
            date = input("Enter appointment date (YYYY-MM-DD): ").strip()
            if validate_date(date):
                # Check if date is in future
                appt_date = datetime.strptime(date, '%Y-%m-%d')
                if appt_date > datetime.now():
                    break
                else:
                    print_error("Date must be in the future!")
            else:
                print_error("Invalid date format!")
        
        # Get appointment time
        while True:
            time = input("Enter appointment time (HH:MM, 09:00-17:30): ").strip()
            if validate_time(time):
                # Check if time is within clinic hours
                try:
                    appt_time = datetime.strptime(time, '%H:%M')
                    clinic_start = datetime.strptime('09:00', '%H:%M')
                    clinic_end = datetime.strptime('18:00', '%H:%M')
                    if clinic_start <= appt_time < clinic_end:
                        break
                    else:
                        print_error("Clinic hours are 09:00 to 18:00!")
                except ValueError:
                    print_error("Invalid time format!")
            else:
                print_error("Invalid time format!")
        
        # Check for conflicts
        existing_appts = self.db.get_doctor_appointments(doctor.user_id)
        conflict = False
        for appt in existing_appts:
            if appt.date == date and appt.time == time and appt.status != 'cancelled':
                conflict = True
                break
        
        if conflict:
            print_error("Doctor is not available at this time!")
            pause()
            return
        
        # Get reason
        reason = input("Enter reason for appointment: ").strip()
        
        # Create appointment
        appt_id = generate_id()
        appointment = Appointment(
            appointment_id=appt_id,
            patient_id=self.current_user.user_id,
            doctor_id=doctor.user_id,
            date=date,
            time=time,
            reason=reason
        )
        
        self.db.add_appointment(appointment)
        doctor.add_assigned_patient(self.current_user.user_id)
        self.db.update_doctor(doctor)
        
        print_success(f"Appointment booked successfully!")
        print(f"Doctor: Dr. {doctor.username}")
        print(f"Date & Time: {format_datetime(date, time)}")
        print(f"Consultation Fee: Rs. {doctor.consultation_fee}")
        pause()
    
    def view_patient_appointments(self):
        """View patient appointments"""
        clear_screen()
        print_header("MY APPOINTMENTS")
        
        appointments = self.db.get_patient_appointments(self.current_user.user_id)
        
        if not appointments:
            print_info("No appointments found!")
            pause()
            return
        
        # Sort by date
        appointments.sort(key=lambda x: (x.date, x.time))
        
        for i, appt in enumerate(appointments, 1):
            doctor = self.db.get_doctor(appt.doctor_id)
            print(f"\n{i}. Date & Time: {format_datetime(appt.date, appt.time)}")
            print(f"   Doctor: Dr. {doctor.username} ({doctor.specialization})")
            print(f"   Reason: {appt.reason}")
            print(f"   Status: {appt.status.upper()}")
            if appt.notes:
                print(f"   Notes: {appt.notes}")
        
        print_separator()
        pause()
    
    def cancel_appointment(self):
        """Cancel an appointment"""
        clear_screen()
        print_header("CANCEL APPOINTMENT")
        
        appointments = [a for a in self.db.get_patient_appointments(self.current_user.user_id) 
                       if a.status in ['pending', 'confirmed']]
        
        if not appointments:
            print_info("No active appointments to cancel!")
            pause()
            return
        
        for i, appt in enumerate(appointments, 1):
            doctor = self.db.get_doctor(appt.doctor_id)
            print(f"{i}. {format_datetime(appt.date, appt.time)} - Dr. {doctor.username}")
        print_separator()
        
        try:
            choice = int(input("Select appointment to cancel (number): ").strip())
            if 1 <= choice <= len(appointments):
                appt = appointments[choice - 1]
                if input_yes_no("Are you sure you want to cancel this appointment? (yes/no): "):
                    appt.cancel()
                    self.db.update_appointment(appt)
                    print_success("Appointment cancelled successfully!")
                else:
                    print_info("Cancellation aborted!")
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")
        
        pause()
    
    def view_patient_medical_records(self):
        """View patient medical records"""
        clear_screen()
        print_header("MY MEDICAL RECORDS")
        
        records = self.db.get_patient_medical_records(self.current_user.user_id)
        
        if not records:
            print_info("No medical records found!")
            pause()
            return
        
        # Sort by date (newest first)
        records.sort(key=lambda x: x.date_created, reverse=True)
        
        for i, record in enumerate(records, 1):
            doctor = self.db.get_doctor(record.doctor_id)
            print(f"\n{i}. Date: {format_date(record.date_created)}")
            print(f"   Doctor: Dr. {doctor.username}")
            print(f"   Diagnosis: {record.diagnosis}")
            print(f"   Prescription: {record.prescription}")
            if record.test_results:
                print(f"   Test Results: {record.test_results}")
            if record.follow_up_date:
                print(f"   Follow-up Date: {format_date(record.follow_up_date)}")
            if record.notes:
                print(f"   Notes: {record.notes}")
        
        print_separator()
        pause()
    
    def view_patient_prescriptions(self):
        """View patient prescriptions"""
        clear_screen()
        print_header("MY PRESCRIPTIONS")
        
        prescriptions = self.db.get_patient_prescriptions(self.current_user.user_id)
        
        if not prescriptions:
            print_info("No active prescriptions!")
            pause()
            return
        
        # Sort by date (newest first)
        prescriptions.sort(key=lambda x: x.date_issued, reverse=True)
        
        for i, presc in enumerate(prescriptions, 1):
            doctor = self.db.get_doctor(presc.doctor_id)
            print(f"\n{i}. Medication: {presc.medication}")
            print(f"   Dosage: {presc.dosage}")
            print(f"   Duration: {presc.duration}")
            print(f"   Prescribed by: Dr. {doctor.username}")
            print(f"   Date Issued: {format_date(presc.date_issued)}")
            if presc.instructions:
                print(f"   Instructions: {presc.instructions}")
        
        print_separator()
        pause()
    
    def submit_complaint(self):
        """Submit a complaint"""
        clear_screen()
        print_header("SUBMIT COMPLAINT")
        
        complaint_types = get_complaint_types()
        complaint_type = complaint_types[display_menu(complaint_types, "Select Complaint Type") - 1]
        
        # If medical complaint, select doctor
        against_id = None
        if complaint_type == 'Medical':
            doctors = self.db.get_all_doctors()
            if not doctors:
                print_error("No doctors to complain against!")
                pause()
                return
            
            for i, doctor in enumerate(doctors, 1):
                print(f"{i}. Dr. {doctor.username} ({doctor.specialization})")
            print_separator()
            
            try:
                doctor_choice = int(input("Select doctor (number): ").strip())
                if 1 <= doctor_choice <= len(doctors):
                    against_id = doctors[doctor_choice - 1].user_id
                else:
                    print_error("Invalid choice!")
                    pause()
                    return
            except ValueError:
                print_error("Invalid input!")
                pause()
                return
        
        description = input("Enter complaint description: ").strip()
        
        complaint_id = generate_id()
        complaint = Complaint(
            complaint_id=complaint_id,
            filed_by_type='patient',
            filed_by_id=self.current_user.user_id,
            against_id=against_id,
            complaint_type=complaint_type,
            description=description
        )
        
        self.db.add_complaint(complaint)
        print_success("Complaint submitted successfully!")
        print_info(f"Complaint ID: {complaint_id}")
        pause()
    
    def view_patient_complaints(self):
        """View patient complaints"""
        clear_screen()
        print_header("MY COMPLAINTS")
        
        complaints = self.db.get_complaints_by_patient(self.current_user.user_id)
        
        if not complaints:
            print_info("No complaints filed!")
            pause()
            return
        
        # Sort by date (newest first)
        complaints.sort(key=lambda x: x.date_filed, reverse=True)
        
        for i, complaint in enumerate(complaints, 1):
            print(f"\n{i}. ID: {complaint.complaint_id}")
            print(f"   Type: {complaint.complaint_type}")
            print(f"   Status: {complaint.status.upper()}")
            print(f"   Date Filed: {complaint.date_filed}")
            print(f"   Description: {complaint.description}")
            if complaint.status == 'resolved':
                print(f"   Resolution: {complaint.resolution}")
        
        print_separator()
        pause()
    
    def rate_doctor(self):
        """Rate a doctor"""
        clear_screen()
        print_header("RATE DOCTOR")
        
        # Get completed appointments
        appointments = [a for a in self.db.get_patient_appointments(self.current_user.user_id) 
                       if a.status == 'completed']
        
        if not appointments:
            print_info("No completed appointments to rate!")
            pause()
            return
        
        for i, appt in enumerate(appointments, 1):
            doctor = self.db.get_doctor(appt.doctor_id)
            print(f"{i}. Dr. {doctor.username} ({format_datetime(appt.date, appt.time)})")
        print_separator()
        
        try:
            appt_choice = int(input("Select appointment (number): ").strip())
            if 1 <= appt_choice <= len(appointments):
                appt = appointments[appt_choice - 1]
                doctor = self.db.get_doctor(appt.doctor_id)
                
                while True:
                    try:
                        rating = int(input("Enter rating (1-5): ").strip())
                        if 1 <= rating <= 5:
                            doctor.add_rating(rating)
                            self.db.update_doctor(doctor)
                            print_success(f"Thank you for rating! Average rating: {doctor.get_average_rating():.1f}/5")
                            break
                        else:
                            print_error("Please enter a rating between 1 and 5!")
                    except ValueError:
                        print_error("Invalid input!")
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")
        
        pause()
    
    # ==================== DOCTOR DASHBOARD ====================
    
    def doctor_dashboard(self):
        """Doctor main dashboard"""
        clear_screen()
        print_header(f"DOCTOR DASHBOARD - {self.current_user.username}")
        
        options = [
            "View Profile",
            "Edit Profile",
            "Manage Schedule",
            "View Appointments",
            "Confirm/Complete Appointment",
            "View Assigned Patients",
            "Create Medical Record",
            "Update Medical Record",
            "View Patient Records",
            "Issue Prescription",
            "View Complaints",
            "View Ratings",
            "Logout"
        ]
        
        choice = display_menu(options, "Doctor Menu")
        
        if choice == 1:
            self.view_doctor_profile()
        elif choice == 2:
            self.edit_doctor_profile()
        elif choice == 3:
            self.manage_doctor_schedule()
        elif choice == 4:
            self.view_doctor_appointments()
        elif choice == 5:
            self.confirm_complete_appointment()
        elif choice == 6:
            self.view_assigned_patients()
        elif choice == 7:
            self.create_medical_record()
        elif choice == 8:
            self.update_medical_record()
        elif choice == 9:
            self.view_patient_records_doctor()
        elif choice == 10:
            self.issue_prescription()
        elif choice == 11:
            self.view_doctor_complaints()
        elif choice == 12:
            self.view_doctor_ratings()
        elif choice == 13:
            self.current_user = None
            self.current_user_type = None
    
    def view_doctor_profile(self):
        """View doctor profile"""
        clear_screen()
        print_header(f"PROFILE - DR. {self.current_user.username.upper()}")
        print(f"Specialization: {self.current_user.specialization}")
        print(f"License Number: {self.current_user.license_number}")
        print(f"Email: {self.current_user.email}")
        print(f"Phone: {self.current_user.phone}")
        print(f"Experience: {self.current_user.experience_years} years")
        print(f"Qualifications: {self.current_user.qualifications}")
        print(f"Verified: {'Yes' if self.current_user.verified else 'No'}")
        print(f"Consultation Fee: Rs. {self.current_user.consultation_fee}")
        print(f"Average Rating: {self.current_user.get_average_rating():.1f}/5 ({len(self.current_user.ratings)} ratings)")
        print(f"Assigned Patients: {len(self.current_user.assigned_patients)}")
        print_separator()
        pause()
    
    def edit_doctor_profile(self):
        """Edit doctor profile"""
        clear_screen()
        print_header("EDIT PROFILE")
        
        options = [
            "Change Password",
            "Update Phone Number",
            "Update Qualifications",
            "Update Consultation Fee",
            "Back"
        ]
        
        choice = display_menu(options, "Edit Options")
        
        if choice == 1:
            old_password = input("Enter current password: ").strip()
            if self.current_user.verify_password(old_password):
                new_password = input_with_validation(
                    "Enter new password: ",
                    validate_password,
                    "Password too short"
                )
                self.current_user.password_hash = hash_password(new_password)
                self.db.update_doctor(self.current_user)
                print_success("Password updated successfully!")
            else:
                print_error("Incorrect current password!")
        elif choice == 2:
            phone = input_with_validation("Enter new phone number: ", validate_phone, "Invalid phone format")
            self.current_user.phone = phone
            self.db.update_doctor(self.current_user)
            print_success("Phone number updated!")
        elif choice == 3:
            qualifications = input("Enter qualifications (comma-separated): ").strip()
            self.current_user.qualifications = qualifications
            self.db.update_doctor(self.current_user)
            print_success("Qualifications updated!")
        elif choice == 4:
            try:
                fee = int(input("Enter consultation fee (Rs.): ").strip())
                self.current_user.consultation_fee = fee
                self.db.update_doctor(self.current_user)
                print_success("Consultation fee updated!")
            except ValueError:
                print_error("Invalid fee amount!")
        
        pause()
    
    def manage_doctor_schedule(self):
        """Manage doctor availability schedule"""
        clear_screen()
        print_header("MANAGE SCHEDULE")
        
        options = [
            "Add Available Slot",
            "Remove Available Slot",
            "View Current Schedule",
            "Back"
        ]
        
        choice = display_menu(options, "Schedule Options")
        
        if choice == 1:
            while True:
                date = input("Enter date (YYYY-MM-DD): ").strip()
                if validate_date(date):
                    appt_date = datetime.strptime(date, '%Y-%m-%d')
                    if appt_date > datetime.now():
                        break
                    else:
                        print_error("Date must be in the future!")
                else:
                    print_error("Invalid date format!")
            
            while True:
                time = input("Enter time (HH:MM): ").strip()
                if validate_time(time):
                    break
                else:
                    print_error("Invalid time format!")
            
            self.current_user.add_available_slot(date, time)
            self.db.update_doctor(self.current_user)
            print_success(f"Slot added: {format_datetime(date, time)}")
        
        elif choice == 2:
            if not self.current_user.available_slots:
                print_info("No available slots!")
                pause()
                return
            
            for i, (date, time) in enumerate(self.current_user.available_slots, 1):
                print(f"{i}. {format_datetime(date, time)}")
            print_separator()
            
            try:
                slot_choice = int(input("Select slot to remove (number): ").strip())
                if 1 <= slot_choice <= len(self.current_user.available_slots):
                    date, time = self.current_user.available_slots[slot_choice - 1]
                    self.current_user.remove_available_slot(date, time)
                    self.db.update_doctor(self.current_user)
                    print_success("Slot removed!")
                else:
                    print_error("Invalid choice!")
            except ValueError:
                print_error("Invalid input!")
        
        elif choice == 3:
            if not self.current_user.available_slots:
                print_info("No available slots scheduled!")
            else:
                print_subheader("Current Schedule")
                for i, (date, time) in enumerate(sorted(self.current_user.available_slots), 1):
                    print(f"{i}. {format_datetime(date, time)}")
        
        pause()
    
    def view_doctor_appointments(self):
        """View doctor appointments"""
        clear_screen()
        print_header("MY APPOINTMENTS")
        
        appointments = self.db.get_doctor_appointments(self.current_user.user_id)
        
        if not appointments:
            print_info("No appointments!")
            pause()
            return
        
        # Sort by date
        appointments.sort(key=lambda x: (x.date, x.time))
        
        for i, appt in enumerate(appointments, 1):
            patient = self.db.get_patient(appt.patient_id)
            print(f"\n{i}. Date & Time: {format_datetime(appt.date, appt.time)}")
            print(f"   Patient: {patient.username}")
            print(f"   Reason: {appt.reason}")
            print(f"   Status: {appt.status.upper()}")
        
        print_separator()
        pause()
    
    def confirm_complete_appointment(self):
        """Confirm or complete an appointment"""
        clear_screen()
        print_header("MANAGE APPOINTMENTS")
        
        appointments = [a for a in self.db.get_doctor_appointments(self.current_user.user_id) 
                       if a.status in ['pending', 'confirmed']]
        
        if not appointments:
            print_info("No pending or confirmed appointments!")
            pause()
            return
        
        for i, appt in enumerate(appointments, 1):
            patient = self.db.get_patient(appt.patient_id)
            print(f"{i}. {format_datetime(appt.date, appt.time)} - {patient.username} ({appt.status})")
        print_separator()
        
        try:
            choice = int(input("Select appointment (number): ").strip())
            if 1 <= choice <= len(appointments):
                appt = appointments[choice - 1]
                
                if appt.status == 'pending':
                    if input_yes_no("Confirm this appointment? (yes/no): "):
                        appt.confirm()
                        self.db.update_appointment(appt)
                        print_success("Appointment confirmed!")
                
                elif appt.status == 'confirmed':
                    options = ["Mark as Completed", "Reschedule", "Cancel"]
                    action = display_menu(options, "Select Action")
                    
                    if action == 1:
                        notes = input("Enter appointment notes: ").strip()
                        appt.complete(notes)
                        self.db.update_appointment(appt)
                        print_success("Appointment marked as completed!")
                    
                    elif action == 2:
                        new_date = input("Enter new date (YYYY-MM-DD): ").strip()
                        new_time = input("Enter new time (HH:MM): ").strip()
                        if validate_date(new_date) and validate_time(new_time):
                            appt.reschedule(new_date, new_time)
                            self.db.update_appointment(appt)
                            print_success("Appointment rescheduled!")
                        else:
                            print_error("Invalid date or time!")
                    
                    elif action == 3:
                        if input_yes_no("Cancel this appointment? (yes/no): "):
                            appt.cancel()
                            self.db.update_appointment(appt)
                            print_success("Appointment cancelled!")
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")
        
        pause()
    
    def view_assigned_patients(self):
        """View assigned patients"""
        clear_screen()
        print_header("MY PATIENTS")
        
        if not self.current_user.assigned_patients:
            print_info("No assigned patients!")
            pause()
            return
        
        patients = [self.db.get_patient(pid) for pid in self.current_user.assigned_patients if self.db.get_patient(pid)]
        
        for i, patient in enumerate(patients, 1):
            print(f"{i}. {patient.username} (Age: {patient.get_age()}, {patient.gender})")
            print(f"   Contact: {patient.email}, {patient.phone}")
            print(f"   Blood Type: {patient.blood_type}")
        
        print_separator()
        pause()
    
    def create_medical_record(self):
        """Create a new medical record for a patient"""
        clear_screen()
        print_header("CREATE MEDICAL RECORD")
        
        if not self.current_user.assigned_patients:
            print_info("No assigned patients!")
            pause()
            return
        
        patients = [self.db.get_patient(pid) for pid in self.current_user.assigned_patients if self.db.get_patient(pid)]
        
        for i, patient in enumerate(patients, 1):
            print(f"{i}. {patient.username}")
        print_separator()
        
        try:
            patient_choice = int(input("Select patient (number): ").strip())
            if 1 <= patient_choice <= len(patients):
                patient = patients[patient_choice - 1]
                
                diagnosis = input("Enter diagnosis: ").strip()
                prescription = input("Enter prescription: ").strip()
                test_results = input("Enter test results (optional): ").strip()
                notes = input("Enter notes (optional): ").strip()
                
                follow_up = input("Enter follow-up date (YYYY-MM-DD, optional): ").strip()
                if follow_up and not validate_date(follow_up):
                    print_error("Invalid follow-up date!")
                    pause()
                    return
                
                record_id = generate_id()
                record = MedicalRecord(
                    record_id=record_id,
                    patient_id=patient.user_id,
                    doctor_id=self.current_user.user_id,
                    diagnosis=diagnosis,
                    prescription=prescription,
                    test_results=test_results,
                    notes=notes,
                    follow_up_date=follow_up
                )
                
                self.db.add_medical_record(record)
                print_success(f"Medical record created for {patient.username}!")
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")
        
        pause()
    
    def update_medical_record(self):
        """Update an existing medical record"""
        clear_screen()
        print_header("UPDATE MEDICAL RECORD")
        
        records = self.db.get_doctor_patient_records(self.current_user.user_id)
        
        if not records:
            print_info("No medical records to update!")
            pause()
            return
        
        # Sort by date (newest first)
        records.sort(key=lambda x: x.date_created, reverse=True)
        
        for i, record in enumerate(records, 1):
            patient = self.db.get_patient(record.patient_id)
            print(f"{i}. {patient.username} - {format_date(record.date_created)}")
        print_separator()
        
        try:
            record_choice = int(input("Select record to update (number): ").strip())
            if 1 <= record_choice <= len(records):
                record = records[record_choice - 1]
                
                print("\nCurrent Details:")
                print(f"Diagnosis: {record.diagnosis}")
                print(f"Prescription: {record.prescription}")
                
                diagnosis = input("Update diagnosis (or press Enter to skip): ").strip()
                prescription = input("Update prescription (or press Enter to skip): ").strip()
                test_results = input("Update test results (or press Enter to skip): ").strip()
                notes = input("Update notes (or press Enter to skip): ").strip()
                follow_up = input("Update follow-up date (or press Enter to skip): ").strip()
                
                record.update(
                    diagnosis=diagnosis,
                    prescription=prescription,
                    test_results=test_results,
                    notes=notes,
                    follow_up_date=follow_up
                )
                
                self.db.update_medical_record(record)
                print_success("Medical record updated!")
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")
        
        pause()
    
    def view_patient_records_doctor(self):
        """View all patient records created by this doctor"""
        clear_screen()
        print_header("MY PATIENT RECORDS")
        
        records = self.db.get_doctor_patient_records(self.current_user.user_id)
        
        if not records:
            print_info("No patient records created!")
            pause()
            return
        
        # Sort by date (newest first)
        records.sort(key=lambda x: x.date_created, reverse=True)
        
        for i, record in enumerate(records, 1):
            patient = self.db.get_patient(record.patient_id)
            print(f"\n{i}. Patient: {patient.username}")
            print(f"   Date: {format_date(record.date_created)}")
            print(f"   Diagnosis: {record.diagnosis}")
            print(f"   Prescription: {record.prescription}")
        
        print_separator()
        pause()
    
    def issue_prescription(self):
        """Issue a prescription to a patient"""
        clear_screen()
        print_header("ISSUE PRESCRIPTION")
        
        if not self.current_user.assigned_patients:
            print_info("No assigned patients!")
            pause()
            return
        
        patients = [self.db.get_patient(pid) for pid in self.current_user.assigned_patients if self.db.get_patient(pid)]
        
        for i, patient in enumerate(patients, 1):
            print(f"{i}. {patient.username}")
        print_separator()
        
        try:
            patient_choice = int(input("Select patient (number): ").strip())
            if 1 <= patient_choice <= len(patients):
                patient = patients[patient_choice - 1]
                
                medication = input("Enter medication name: ").strip()
                dosage = input("Enter dosage (e.g., 500mg): ").strip()
                duration = input("Enter duration (e.g., 10 days): ").strip()
                instructions = input("Enter instructions (optional): ").strip()
                
                presc_id = generate_id()
                prescription = Prescription(
                    prescription_id=presc_id,
                    patient_id=patient.user_id,
                    doctor_id=self.current_user.user_id,
                    medication=medication,
                    dosage=dosage,
                    duration=duration,
                    instructions=instructions
                )
                
                self.db.add_prescription(prescription)
                print_success(f"Prescription issued to {patient.username}!")
            else:
                print_error("Invalid choice!")
        except ValueError:
            print_error("Invalid input!")
        
        pause()
    
    def view_doctor_complaints(self):
        """View complaints against this doctor"""
        clear_screen()
        print_header("COMPLAINTS AGAINST ME")
        
        complaints = self.db.get_complaints_against_doctor(self.current_user.user_id)
        
        if not complaints:
            print_info("No complaints!")
            pause()
            return
        
        # Sort by date (newest first)
        complaints.sort(key=lambda x: x.date_filed, reverse=True)
        
        for i, complaint in enumerate(complaints, 1):
            patient = self.db.get_patient(complaint.filed_by_id)
            print(f"\n{i}. Type: {complaint.complaint_type}")
            print(f"   Filed by: {patient.username if patient else 'Unknown'}")
            print(f"   Status: {complaint.status.upper()}")
            print(f"   Date: {complaint.date_filed}")
            print(f"   Description: {complaint.description}")
            if complaint.status == 'resolved':
                print(f"   Resolution: {complaint.resolution}")
        
        print_separator()
        pause()
    
    def view_doctor_ratings(self):
        """View doctor ratings"""
        clear_screen()
        print_header("MY RATINGS")
        
        if not self.current_user.ratings:
            print_info("No ratings yet!")
        else:
            print(f"Average Rating: {self.current_user.get_average_rating():.1f}/5")
            print(f"Total Ratings: {len(self.current_user.ratings)}")
            print(f"\nRatings: {self.current_user.ratings}")
        
        print_separator()
        pause()
    
    # ==================== ADMIN DASHBOARD ====================
    
    def admin_dashboard(self):
        """Admin main dashboard"""
        clear_screen()
        print_header(f"ADMIN DASHBOARD - {self.current_user['username']}")
        
        options = [
            "View System Statistics",
            "Manage Doctors",
            "View All Users",
            "Manage Complaints",
            "View Appointments",
            "Change Admin Password",
            "Logout"
        ]
        
        choice = display_menu(options, "Admin Menu")
        
        if choice == 1:
            self.view_system_statistics()
        elif choice == 2:
            self.manage_doctors_admin()
        elif choice == 3:
            self.view_all_users()
        elif choice == 4:
            self.manage_complaints_admin()
        elif choice == 5:
            self.view_all_appointments()
        elif choice == 6:
            self.change_admin_password()
        elif choice == 7:
            self.current_user = None
            self.current_user_type = None
    
    def view_system_statistics(self):
        """View system statistics"""
        clear_screen()
        print_header("SYSTEM STATISTICS")
        
        stats = self.db.get_system_statistics()
        
        print(f"\nPatients: {stats['total_patients']}")
        print(f"Total Doctors: {stats['total_doctors']}")
        print(f"Verified Doctors: {stats['verified_doctors']}")
        print(f"Pending Doctor Verifications: {stats['total_doctors'] - stats['verified_doctors']}")
        
        print(f"\nAppointments:")
        print(f"  Total: {stats['total_appointments']}")
        print(f"  Pending: {stats['pending_appointments']}")
        print(f"  Completed: {stats['completed_appointments']}")
        
        print(f"\nMedical Records: {stats['total_medical_records']}")
        
        print(f"\nComplaints:")
        print(f"  Pending: {stats['pending_complaints']}")
        print(f"  Resolved: {stats['resolved_complaints']}")
        
        print_separator()
        pause()
    
    def manage_doctors_admin(self):
        """Manage doctors (verify, remove)"""
        clear_screen()
        print_header("MANAGE DOCTORS")
        
        options = [
            "Verify Pending Doctors",
            "Remove Doctor",
            "View All Doctors",
            "Back"
        ]
        
        choice = display_menu(options, "Doctor Management")
        
        if choice == 1:
            unverified = self.db.get_all_unverified_doctors()
            
            if not unverified:
                print_info("No pending doctor verifications!")
                pause()
                return
            
            for i, doctor in enumerate(unverified, 1):
                print(f"{i}. Dr. {doctor.username} ({doctor.specialization})")
                print(f"   License: {doctor.license_number}")
                print(f"   Experience: {doctor.experience_years} years")
            print_separator()
            
            try:
                doctor_choice = int(input("Select doctor to verify (number): ").strip())
                if 1 <= doctor_choice <= len(unverified):
                    doctor = unverified[doctor_choice - 1]
                    self.db.verify_doctor(doctor.user_id)
                    print_success(f"Dr. {doctor.username} verified successfully!")
                else:
                    print_error("Invalid choice!")
            except ValueError:
                print_error("Invalid input!")
        
        elif choice == 2:
            all_doctors = self.db.get_all_doctors()
            
            if not all_doctors:
                print_info("No doctors to remove!")
                pause()
                return
            
            for i, doctor in enumerate(all_doctors, 1):
                print(f"{i}. Dr. {doctor.username} ({doctor.specialization})")
            print_separator()
            
            try:
                doctor_choice = int(input("Select doctor to remove (number): ").strip())
                if 1 <= doctor_choice <= len(all_doctors):
                    doctor = all_doctors[doctor_choice - 1]
                    if input_yes_no(f"Remove Dr. {doctor.username}? (yes/no): "):
                        self.db.delete_doctor(doctor.user_id)
                        print_success("Doctor removed!")
                    else:
                        print_info("Cancelled!")
                else:
                    print_error("Invalid choice!")
            except ValueError:
                print_error("Invalid input!")
        
        elif choice == 3:
            all_doctors = self.db.get_all_doctors()
            
            if not all_doctors:
                print_info("No doctors!")
                pause()
                return
            
            print_subheader("All Doctors")
            for i, doctor in enumerate(all_doctors, 1):
                print(f"{i}. Dr. {doctor.username}")
                print(f"   Specialization: {doctor.specialization}")
                print(f"   Experience: {doctor.experience_years} years")
                print(f"   Rating: {doctor.get_average_rating():.1f}/5")
                print(f"   Patients: {len(doctor.assigned_patients)}")
            
            print_separator()
        
        pause()
    
    def view_all_users(self):
        """View all registered users"""
        clear_screen()
        print_header("ALL USERS")
        
        patients = self.db.get_all_patients()
        doctors = self.db.get_all_doctors()
        
        print(f"\nPATIENTS ({len(patients)}):")
        print_separator()
        if patients:
            for i, patient in enumerate(patients, 1):
                print(f"{i}. {patient.username} ({patient.email})")
        else:
            print("No patients registered!")
        
        print(f"\nDOCTORS ({len(doctors)}):")
        print_separator()
        if doctors:
            for i, doctor in enumerate(doctors, 1):
                print(f"{i}. Dr. {doctor.username} ({doctor.specialization})")
        else:
            print("No doctors registered!")
        
        print_separator()
        pause()
    
    def manage_complaints_admin(self):
        """Manage complaints"""
        clear_screen()
        print_header("MANAGE COMPLAINTS")
        
        options = [
            "View Pending Complaints",
            "View All Complaints",
            "Resolve Complaint",
            "Back"
        ]
        
        choice = display_menu(options, "Complaint Management")
        
        if choice == 1:
            pending = self.db.get_complaints_by_status('pending')
            
            if not pending:
                print_info("No pending complaints!")
                pause()
                return
            
            print_subheader(f"Pending Complaints ({len(pending)})")
            for i, complaint in enumerate(pending, 1):
                print(f"{i}. ID: {complaint.complaint_id}")
                print(f"   Type: {complaint.complaint_type}")
                print(f"   Date: {complaint.date_filed}")
                print(f"   Description: {complaint.description}")
            
            print_separator()
        
        elif choice == 2:
            all_complaints = list(self.db.complaints.values())
            
            if not all_complaints:
                print_info("No complaints!")
                pause()
                return
            
            print_subheader(f"All Complaints ({len(all_complaints)})")
            for i, complaint in enumerate(all_complaints, 1):
                print(f"{i}. ID: {complaint.complaint_id}")
                print(f"   Status: {complaint.status.upper()}")
                print(f"   Type: {complaint.complaint_type}")
            
            print_separator()
        
        elif choice == 3:
            pending = self.db.get_complaints_by_status('pending')
            
            if not pending:
                print_info("No pending complaints to resolve!")
                pause()
                return
            
            for i, complaint in enumerate(pending, 1):
                print(f"{i}. {complaint.complaint_type} - {complaint.date_filed}")
            print_separator()
            
            try:
                complaint_choice = int(input("Select complaint to resolve (number): ").strip())
                if 1 <= complaint_choice <= len(pending):
                    complaint = pending[complaint_choice - 1]
                    resolution = input("Enter resolution: ").strip()
                    
                    complaint.resolve(resolution, self.current_user['username'])
                    self.db.update_complaint(complaint)
                    print_success("Complaint resolved!")
                else:
                    print_error("Invalid choice!")
            except ValueError:
                print_error("Invalid input!")
        
        pause()
    
    def view_all_appointments(self):
        """View all appointments"""
        clear_screen()
        print_header("ALL APPOINTMENTS")
        
        all_appointments = list(self.db.appointments.values())
        
        if not all_appointments:
            print_info("No appointments!")
            pause()
            return
        
        # Group by status
        pending = [a for a in all_appointments if a.status == 'pending']
        confirmed = [a for a in all_appointments if a.status == 'confirmed']
        completed = [a for a in all_appointments if a.status == 'completed']
        cancelled = [a for a in all_appointments if a.status == 'cancelled']
        
        print(f"\nPending ({len(pending)}):")
        for appt in pending[:5]:
            patient = self.db.get_patient(appt.patient_id)
            doctor = self.db.get_doctor(appt.doctor_id)
            print(f"  {format_datetime(appt.date, appt.time)} - {patient.username} & Dr. {doctor.username}")
        
        print(f"\nConfirmed ({len(confirmed)}):")
        for appt in confirmed[:5]:
            patient = self.db.get_patient(appt.patient_id)
            doctor = self.db.get_doctor(appt.doctor_id)
            print(f"  {format_datetime(appt.date, appt.time)} - {patient.username} & Dr. {doctor.username}")
        
        print(f"\nCompleted ({len(completed)}):")
        for appt in completed[:5]:
            patient = self.db.get_patient(appt.patient_id)
            doctor = self.db.get_doctor(appt.doctor_id)
            print(f"  {format_datetime(appt.date, appt.time)} - {patient.username} & Dr. {doctor.username}")
        
        print(f"\nCancelled ({len(cancelled)}):")
        for appt in cancelled[:5]:
            patient = self.db.get_patient(appt.patient_id)
            doctor = self.db.get_doctor(appt.doctor_id)
            print(f"  {format_datetime(appt.date, appt.time)} - {patient.username} & Dr. {doctor.username}")
        
        print_separator()
        pause()
    
    def change_admin_password(self):
        """Change admin password"""
        clear_screen()
        print_header("CHANGE ADMIN PASSWORD")
        
        current_password = input("Enter current password: ").strip()
        stored_hash = self.db.get_admin_password_hash(self.current_user['username'])
        
        if not verify_password(stored_hash, current_password):
            print_error("Incorrect password!")
            pause()
            return
        
        new_password = input_with_validation(
            "Enter new password: ",
            validate_password,
            "Password too short"
        )
        
        new_hash = hash_password(new_password)
        self.db.admin_users[self.current_user['username']] = new_hash
        self.db.save_admin_users()
        
        print_success("Password changed successfully!")
        pause()


def clear_screen():
    """Clear console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    app = ClinicManagementSystem()
    app.run()
