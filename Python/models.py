"""
Models for Clinic Management System
Defines User, Patient, Doctor, and related classes
"""

from datetime import datetime
from utils import generate_id, get_age
from auth import hash_password, verify_password


class User:
    """Base User class"""
    
    def __init__(self, user_id, username, password_hash, email, phone):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.phone = phone
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.last_login = None
        self.is_active = True
    
    def verify_password(self, password):
        """Verify if password matches"""
        return verify_password(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password_hash': self.password_hash,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at,
            'last_login': self.last_login,
            'is_active': self.is_active
        }
    
    def __str__(self):
        return f"{self.username} ({self.email})"


class Patient(User):
    """Patient class extending User"""
    
    def __init__(self, user_id, username, password_hash, email, phone, 
                 date_of_birth, gender, address, blood_type='Unknown', 
                 allergies='None', emergency_contact=''):
        super().__init__(user_id, username, password_hash, email, phone)
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.address = address
        self.blood_type = blood_type
        self.allergies = allergies
        self.emergency_contact = emergency_contact
        self.medical_history = []  # List of medical record IDs
        self.appointments = []     # List of appointment IDs
        self.height = None         # in cm
        self.weight = None         # in kg
    
    def get_age(self):
        """Get patient's age"""
        return get_age(self.date_of_birth)
    
    def add_appointment(self, appointment_id):
        """Add appointment ID to patient's appointments"""
        if appointment_id not in self.appointments:
            self.appointments.append(appointment_id)
    
    def remove_appointment(self, appointment_id):
        """Remove appointment ID from patient's appointments"""
        if appointment_id in self.appointments:
            self.appointments.remove(appointment_id)
    
    def add_medical_record(self, record_id):
        """Add medical record ID to patient's history"""
        if record_id not in self.medical_history:
            self.medical_history.append(record_id)
    
    def to_dict(self):
        """Convert patient to dictionary"""
        data = super().to_dict()
        data.update({
            'user_type': 'patient',
            'date_of_birth': self.date_of_birth,
            'gender': self.gender,
            'address': self.address,
            'blood_type': self.blood_type,
            'allergies': self.allergies,
            'emergency_contact': self.emergency_contact,
            'medical_history': self.medical_history,
            'appointments': self.appointments,
            'height': self.height,
            'weight': self.weight
        })
        return data
    
    def __str__(self):
        return f"Patient: {self.username} (Age: {self.get_age()})"


class Doctor(User):
    """Doctor class extending User"""
    
    def __init__(self, user_id, username, password_hash, email, phone,
                 specialization, license_number, experience_years=0, 
                 qualifications='', verified=False):
        super().__init__(user_id, username, password_hash, email, phone)
        self.specialization = specialization
        self.license_number = license_number
        self.experience_years = experience_years
        self.qualifications = qualifications
        self.verified = verified
        self.available_slots = []  # List of available time slots: [(date, time), ...]
        self.assigned_patients = []  # List of patient IDs
        self.appointments = []     # List of appointment IDs
        self.ratings = []          # List of ratings from patients
        self.total_rating = 0
        self.consultation_fee = 500  # Default fee
    
    def add_available_slot(self, date, time):
        """Add an available time slot"""
        slot = (date, time)
        if slot not in self.available_slots:
            self.available_slots.append(slot)
    
    def remove_available_slot(self, date, time):
        """Remove an available time slot"""
        slot = (date, time)
        if slot in self.available_slots:
            self.available_slots.remove(slot)
    
    def get_average_rating(self):
        """Get average rating from patients"""
        if not self.ratings:
            return 0
        return sum(self.ratings) / len(self.ratings)
    
    def add_rating(self, rating):
        """Add a rating from a patient (1-5)"""
        if 1 <= rating <= 5:
            self.ratings.append(rating)
            self.total_rating = sum(self.ratings)
    
    def add_assigned_patient(self, patient_id):
        """Add patient to assigned patients list"""
        if patient_id not in self.assigned_patients:
            self.assigned_patients.append(patient_id)
    
    def add_appointment(self, appointment_id):
        """Add appointment ID to doctor's appointments"""
        if appointment_id not in self.appointments:
            self.appointments.append(appointment_id)
    
    def remove_appointment(self, appointment_id):
        """Remove appointment ID from doctor's appointments"""
        if appointment_id in self.appointments:
            self.appointments.remove(appointment_id)
    
    def to_dict(self):
        """Convert doctor to dictionary"""
        data = super().to_dict()
        data.update({
            'user_type': 'doctor',
            'specialization': self.specialization,
            'license_number': self.license_number,
            'experience_years': self.experience_years,
            'qualifications': self.qualifications,
            'verified': self.verified,
            'available_slots': self.available_slots,
            'assigned_patients': self.assigned_patients,
            'appointments': self.appointments,
            'ratings': self.ratings,
            'total_rating': self.total_rating,
            'consultation_fee': self.consultation_fee
        })
        return data
    
    def __str__(self):
        return f"Dr. {self.username} ({self.specialization})"


class Appointment:
    """Appointment class"""
    
    def __init__(self, appointment_id, patient_id, doctor_id, date, time, reason=''):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.time = time
        self.reason = reason
        self.status = 'pending'  # pending, confirmed, completed, cancelled
        self.notes = ''
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.created_by = 'patient'  # who created this appointment
    
    def confirm(self):
        """Confirm the appointment"""
        self.status = 'confirmed'
    
    def complete(self, notes=''):
        """Mark appointment as completed"""
        self.status = 'completed'
        self.notes = notes
    
    def cancel(self):
        """Cancel the appointment"""
        self.status = 'cancelled'
    
    def reschedule(self, new_date, new_time):
        """Reschedule appointment"""
        self.date = new_date
        self.time = new_time
        self.status = 'pending'
    
    def to_dict(self):
        """Convert appointment to dictionary"""
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date': self.date,
            'time': self.time,
            'reason': self.reason,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at,
            'created_by': self.created_by
        }
    
    def __str__(self):
        return f"Appointment: {self.date} {self.time} - Status: {self.status}"


class MedicalRecord:
    """Medical Record class"""
    
    def __init__(self, record_id, patient_id, doctor_id, diagnosis='', 
                 prescription='', test_results='', notes='', follow_up_date=''):
        self.record_id = record_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date_created = datetime.now().strftime('%Y-%m-%d')
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.test_results = test_results
        self.notes = notes
        self.follow_up_date = follow_up_date
        self.is_active = True
    
    def update(self, diagnosis='', prescription='', test_results='', 
               notes='', follow_up_date=''):
        """Update medical record"""
        if diagnosis:
            self.diagnosis = diagnosis
        if prescription:
            self.prescription = prescription
        if test_results:
            self.test_results = test_results
        if notes:
            self.notes = notes
        if follow_up_date:
            self.follow_up_date = follow_up_date
    
    def to_dict(self):
        """Convert medical record to dictionary"""
        return {
            'record_id': self.record_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date_created': self.date_created,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'test_results': self.test_results,
            'notes': self.notes,
            'follow_up_date': self.follow_up_date,
            'is_active': self.is_active
        }
    
    def __str__(self):
        return f"Medical Record: {self.date_created} - {self.diagnosis}"


class Complaint:
    """Complaint class"""
    
    def __init__(self, complaint_id, filed_by_type, filed_by_id, against_id, 
                 complaint_type, description):
        self.complaint_id = complaint_id
        self.filed_by_type = filed_by_type  # 'patient' or 'doctor'
        self.filed_by_id = filed_by_id
        self.against_id = against_id
        self.complaint_type = complaint_type  # Service, Medical, Staff, Billing, Other
        self.description = description
        self.date_filed = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.status = 'pending'  # pending, under_review, resolved
        self.resolution = ''
        self.resolved_by = ''
        self.resolved_at = ''
    
    def mark_under_review(self):
        """Mark complaint as under review"""
        self.status = 'under_review'
    
    def resolve(self, resolution, admin_id):
        """Resolve the complaint"""
        self.status = 'resolved'
        self.resolution = resolution
        self.resolved_by = admin_id
        self.resolved_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self):
        """Convert complaint to dictionary"""
        return {
            'complaint_id': self.complaint_id,
            'filed_by_type': self.filed_by_type,
            'filed_by_id': self.filed_by_id,
            'against_id': self.against_id,
            'complaint_type': self.complaint_type,
            'description': self.description,
            'date_filed': self.date_filed,
            'status': self.status,
            'resolution': self.resolution,
            'resolved_by': self.resolved_by,
            'resolved_at': self.resolved_at
        }
    
    def __str__(self):
        return f"Complaint #{self.complaint_id}: {self.complaint_type} - {self.status}"


class Prescription:
    """Prescription class"""
    
    def __init__(self, prescription_id, patient_id, doctor_id, medication, dosage, 
                 duration, instructions='', date_issued=''):
        self.prescription_id = prescription_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.medication = medication
        self.dosage = dosage  # e.g., "500mg"
        self.duration = duration  # e.g., "10 days"
        self.instructions = instructions
        self.date_issued = date_issued or datetime.now().strftime('%Y-%m-%d')
        self.is_active = True
    
    def deactivate(self):
        """Deactivate prescription"""
        self.is_active = False
    
    def to_dict(self):
        """Convert prescription to dictionary"""
        return {
            'prescription_id': self.prescription_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'medication': self.medication,
            'dosage': self.dosage,
            'duration': self.duration,
            'instructions': self.instructions,
            'date_issued': self.date_issued,
            'is_active': self.is_active
        }
    
    def __str__(self):
        return f"{self.medication} - {self.dosage} ({self.duration})"
