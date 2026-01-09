"""
Database Module for Clinic Management System
Handles all data storage and persistence with JSON
"""

import json
import os
from datetime import datetime
from models import Patient, Doctor, Appointment, MedicalRecord, Complaint, Prescription
from auth import hash_password


class Database:
    """Database class for managing all clinic data"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.patients = {}
        self.doctors = {}
        self.appointments = {}
        self.medical_records = {}
        self.complaints = {}
        self.prescriptions = {}
        self.admin_users = {}  # username -> password_hash
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Load existing data
        self.load_all_data()
    
    # ==================== PATIENT MANAGEMENT ====================
    
    def add_patient(self, patient):
        """Add a patient to the database"""
        self.patients[patient.user_id] = patient
        self.save_patients()
        return True
    
    def get_patient(self, patient_id):
        """Get a patient by ID"""
        return self.patients.get(patient_id)
    
    def get_patient_by_username(self, username):
        """Get a patient by username"""
        for patient in self.patients.values():
            if patient.username == username:
                return patient
        return None
    
    def update_patient(self, patient):
        """Update patient information"""
        if patient.user_id in self.patients:
            self.patients[patient.user_id] = patient
            self.save_patients()
            return True
        return False
    
    def delete_patient(self, patient_id):
        """Delete a patient (soft delete - mark as inactive)"""
        if patient_id in self.patients:
            self.patients[patient_id].is_active = False
            self.save_patients()
            return True
        return False
    
    def get_all_patients(self):
        """Get all active patients"""
        return [p for p in self.patients.values() if p.is_active]
    
    # ==================== DOCTOR MANAGEMENT ====================
    
    def add_doctor(self, doctor):
        """Add a doctor to the database"""
        self.doctors[doctor.user_id] = doctor
        self.save_doctors()
        return True
    
    def get_doctor(self, doctor_id):
        """Get a doctor by ID"""
        return self.doctors.get(doctor_id)
    
    def get_doctor_by_username(self, username):
        """Get a doctor by username"""
        for doctor in self.doctors.values():
            if doctor.username == username:
                return doctor
        return None
    
    def update_doctor(self, doctor):
        """Update doctor information"""
        if doctor.user_id in self.doctors:
            self.doctors[doctor.user_id] = doctor
            self.save_doctors()
            return True
        return False
    
    def delete_doctor(self, doctor_id):
        """Delete a doctor (soft delete - mark as inactive)"""
        if doctor_id in self.doctors:
            self.doctors[doctor_id].is_active = False
            self.save_doctors()
            return True
        return False
    
    def get_all_doctors(self):
        """Get all active, verified doctors"""
        return [d for d in self.doctors.values() if d.is_active and d.verified]
    
    def get_all_unverified_doctors(self):
        """Get all unverified doctors"""
        return [d for d in self.doctors.values() if d.is_active and not d.verified]
    
    def get_doctors_by_specialization(self, specialization):
        """Get doctors by specialization"""
        return [d for d in self.get_all_doctors() if d.specialization == specialization]
    
    def verify_doctor(self, doctor_id):
        """Verify a doctor"""
        if doctor_id in self.doctors:
            self.doctors[doctor_id].verified = True
            self.save_doctors()
            return True
        return False
    
    # ==================== APPOINTMENT MANAGEMENT ====================
    
    def add_appointment(self, appointment):
        """Add an appointment"""
        self.appointments[appointment.appointment_id] = appointment
        
        # Add to patient and doctor
        patient = self.get_patient(appointment.patient_id)
        doctor = self.get_doctor(appointment.doctor_id)
        
        if patient:
            patient.add_appointment(appointment.appointment_id)
        if doctor:
            doctor.add_appointment(appointment.appointment_id)
        
        self.save_appointments()
        return True
    
    def get_appointment(self, appointment_id):
        """Get appointment by ID"""
        return self.appointments.get(appointment_id)
    
    def update_appointment(self, appointment):
        """Update appointment"""
        if appointment.appointment_id in self.appointments:
            self.appointments[appointment.appointment_id] = appointment
            self.save_appointments()
            return True
        return False
    
    def get_patient_appointments(self, patient_id):
        """Get all appointments for a patient"""
        return [a for a in self.appointments.values() if a.patient_id == patient_id]
    
    def get_doctor_appointments(self, doctor_id):
        """Get all appointments for a doctor"""
        return [a for a in self.appointments.values() if a.doctor_id == doctor_id]
    
    def get_appointments_by_status(self, status):
        """Get appointments by status"""
        return [a for a in self.appointments.values() if a.status == status]
    
    # ==================== MEDICAL RECORDS MANAGEMENT ====================
    
    def add_medical_record(self, medical_record):
        """Add a medical record"""
        self.medical_records[medical_record.record_id] = medical_record
        
        # Add to patient
        patient = self.get_patient(medical_record.patient_id)
        if patient:
            patient.add_medical_record(medical_record.record_id)
        
        self.save_medical_records()
        return True
    
    def get_medical_record(self, record_id):
        """Get medical record by ID"""
        return self.medical_records.get(record_id)
    
    def get_patient_medical_records(self, patient_id):
        """Get all medical records for a patient"""
        return [r for r in self.medical_records.values() 
                if r.patient_id == patient_id and r.is_active]
    
    def get_doctor_patient_records(self, doctor_id):
        """Get all records created by a doctor"""
        return [r for r in self.medical_records.values() if r.doctor_id == doctor_id]
    
    def update_medical_record(self, medical_record):
        """Update medical record"""
        if medical_record.record_id in self.medical_records:
            self.medical_records[medical_record.record_id] = medical_record
            self.save_medical_records()
            return True
        return False
    
    # ==================== COMPLAINT MANAGEMENT ====================
    
    def add_complaint(self, complaint):
        """Add a complaint"""
        self.complaints[complaint.complaint_id] = complaint
        self.save_complaints()
        return True
    
    def get_complaint(self, complaint_id):
        """Get complaint by ID"""
        return self.complaints.get(complaint_id)
    
    def get_complaints_by_status(self, status):
        """Get complaints by status"""
        return [c for c in self.complaints.values() if c.status == status]
    
    def get_complaints_against_doctor(self, doctor_id):
        """Get complaints against a doctor"""
        return [c for c in self.complaints.values() if c.against_id == doctor_id]
    
    def get_complaints_by_patient(self, patient_id):
        """Get complaints filed by a patient"""
        return [c for c in self.complaints.values() 
                if c.filed_by_type == 'patient' and c.filed_by_id == patient_id]
    
    def update_complaint(self, complaint):
        """Update complaint"""
        if complaint.complaint_id in self.complaints:
            self.complaints[complaint.complaint_id] = complaint
            self.save_complaints()
            return True
        return False
    
    # ==================== PRESCRIPTION MANAGEMENT ====================
    
    def add_prescription(self, prescription):
        """Add a prescription"""
        self.prescriptions[prescription.prescription_id] = prescription
        self.save_prescriptions()
        return True
    
    def get_prescription(self, prescription_id):
        """Get prescription by ID"""
        return self.prescriptions.get(prescription_id)
    
    def get_patient_prescriptions(self, patient_id):
        """Get all prescriptions for a patient"""
        return [p for p in self.prescriptions.values() 
                if p.patient_id == patient_id and p.is_active]
    
    def get_doctor_prescriptions(self, doctor_id):
        """Get all prescriptions created by a doctor"""
        return [p for p in self.prescriptions.values() if p.doctor_id == doctor_id]
    
    def update_prescription(self, prescription):
        """Update prescription"""
        if prescription.prescription_id in self.prescriptions:
            self.prescriptions[prescription.prescription_id] = prescription
            self.save_prescriptions()
            return True
        return False
    
    # ==================== ADMIN MANAGEMENT ====================
    
    def add_admin(self, username, password_hash):
        """Add an admin user"""
        self.admin_users[username] = password_hash
        self.save_admin_users()
        return True
    
    def get_admin_password_hash(self, username):
        """Get admin password hash"""
        return self.admin_users.get(username)
    
    def admin_exists(self, username):
        """Check if admin exists"""
        return username in self.admin_users
    
    # ==================== DATA PERSISTENCE ====================
    
    def save_patients(self):
        """Save patients to JSON"""
        data = {user_id: patient.to_dict() for user_id, patient in self.patients.items()}
        self._save_json(os.path.join(self.data_dir, 'patients.json'), data)
    
    def save_doctors(self):
        """Save doctors to JSON"""
        data = {user_id: doctor.to_dict() for user_id, doctor in self.doctors.items()}
        self._save_json(os.path.join(self.data_dir, 'doctors.json'), data)
    
    def save_appointments(self):
        """Save appointments to JSON"""
        data = {appt_id: appt.to_dict() for appt_id, appt in self.appointments.items()}
        self._save_json(os.path.join(self.data_dir, 'appointments.json'), data)
    
    def save_medical_records(self):
        """Save medical records to JSON"""
        data = {record_id: record.to_dict() for record_id, record in self.medical_records.items()}
        self._save_json(os.path.join(self.data_dir, 'medical_records.json'), data)
    
    def save_complaints(self):
        """Save complaints to JSON"""
        data = {complaint_id: complaint.to_dict() for complaint_id, complaint in self.complaints.items()}
        self._save_json(os.path.join(self.data_dir, 'complaints.json'), data)
    
    def save_prescriptions(self):
        """Save prescriptions to JSON"""
        data = {presc_id: presc.to_dict() for presc_id, presc in self.prescriptions.items()}
        self._save_json(os.path.join(self.data_dir, 'prescriptions.json'), data)
    
    def save_admin_users(self):
        """Save admin users to JSON"""
        self._save_json(os.path.join(self.data_dir, 'admin_users.json'), self.admin_users)
    
    def _save_json(self, filepath, data):
        """Save data to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving to {filepath}: {str(e)}")
            return False
    
    def load_patients(self):
        """Load patients from JSON"""
        filepath = os.path.join(self.data_dir, 'patients.json')
        data = self._load_json(filepath)
        if data:
            for user_id, patient_data in data.items():
                patient = Patient(
                    user_id=patient_data['user_id'],
                    username=patient_data['username'],
                    password_hash=patient_data['password_hash'],
                    email=patient_data['email'],
                    phone=patient_data['phone'],
                    date_of_birth=patient_data['date_of_birth'],
                    gender=patient_data['gender'],
                    address=patient_data['address'],
                    blood_type=patient_data.get('blood_type', 'Unknown'),
                    allergies=patient_data.get('allergies', 'None'),
                    emergency_contact=patient_data.get('emergency_contact', '')
                )
                patient.created_at = patient_data['created_at']
                patient.last_login = patient_data.get('last_login')
                patient.is_active = patient_data.get('is_active', True)
                patient.medical_history = patient_data.get('medical_history', [])
                patient.appointments = patient_data.get('appointments', [])
                patient.height = patient_data.get('height')
                patient.weight = patient_data.get('weight')
                self.patients[user_id] = patient
    
    def load_doctors(self):
        """Load doctors from JSON"""
        filepath = os.path.join(self.data_dir, 'doctors.json')
        data = self._load_json(filepath)
        if data:
            for user_id, doctor_data in data.items():
                doctor = Doctor(
                    user_id=doctor_data['user_id'],
                    username=doctor_data['username'],
                    password_hash=doctor_data['password_hash'],
                    email=doctor_data['email'],
                    phone=doctor_data['phone'],
                    specialization=doctor_data['specialization'],
                    license_number=doctor_data['license_number'],
                    experience_years=doctor_data.get('experience_years', 0),
                    qualifications=doctor_data.get('qualifications', ''),
                    verified=doctor_data.get('verified', False)
                )
                doctor.created_at = doctor_data['created_at']
                doctor.last_login = doctor_data.get('last_login')
                doctor.is_active = doctor_data.get('is_active', True)
                doctor.available_slots = doctor_data.get('available_slots', [])
                doctor.assigned_patients = doctor_data.get('assigned_patients', [])
                doctor.appointments = doctor_data.get('appointments', [])
                doctor.ratings = doctor_data.get('ratings', [])
                doctor.total_rating = doctor_data.get('total_rating', 0)
                doctor.consultation_fee = doctor_data.get('consultation_fee', 500)
                self.doctors[user_id] = doctor
    
    def load_appointments(self):
        """Load appointments from JSON"""
        filepath = os.path.join(self.data_dir, 'appointments.json')
        data = self._load_json(filepath)
        if data:
            for appt_id, appt_data in data.items():
                appointment = Appointment(
                    appointment_id=appt_data['appointment_id'],
                    patient_id=appt_data['patient_id'],
                    doctor_id=appt_data['doctor_id'],
                    date=appt_data['date'],
                    time=appt_data['time'],
                    reason=appt_data.get('reason', '')
                )
                appointment.status = appt_data.get('status', 'pending')
                appointment.notes = appt_data.get('notes', '')
                appointment.created_at = appt_data.get('created_at', '')
                appointment.created_by = appt_data.get('created_by', 'patient')
                self.appointments[appt_id] = appointment
    
    def load_medical_records(self):
        """Load medical records from JSON"""
        filepath = os.path.join(self.data_dir, 'medical_records.json')
        data = self._load_json(filepath)
        if data:
            for record_id, record_data in data.items():
                record = MedicalRecord(
                    record_id=record_data['record_id'],
                    patient_id=record_data['patient_id'],
                    doctor_id=record_data['doctor_id'],
                    diagnosis=record_data.get('diagnosis', ''),
                    prescription=record_data.get('prescription', ''),
                    test_results=record_data.get('test_results', ''),
                    notes=record_data.get('notes', ''),
                    follow_up_date=record_data.get('follow_up_date', '')
                )
                record.date_created = record_data.get('date_created', '')
                record.is_active = record_data.get('is_active', True)
                self.medical_records[record_id] = record
    
    def load_complaints(self):
        """Load complaints from JSON"""
        filepath = os.path.join(self.data_dir, 'complaints.json')
        data = self._load_json(filepath)
        if data:
            for complaint_id, complaint_data in data.items():
                complaint = Complaint(
                    complaint_id=complaint_data['complaint_id'],
                    filed_by_type=complaint_data['filed_by_type'],
                    filed_by_id=complaint_data['filed_by_id'],
                    against_id=complaint_data['against_id'],
                    complaint_type=complaint_data['complaint_type'],
                    description=complaint_data['description']
                )
                complaint.date_filed = complaint_data.get('date_filed', '')
                complaint.status = complaint_data.get('status', 'pending')
                complaint.resolution = complaint_data.get('resolution', '')
                complaint.resolved_by = complaint_data.get('resolved_by', '')
                complaint.resolved_at = complaint_data.get('resolved_at', '')
                self.complaints[complaint_id] = complaint
    
    def load_prescriptions(self):
        """Load prescriptions from JSON"""
        filepath = os.path.join(self.data_dir, 'prescriptions.json')
        data = self._load_json(filepath)
        if data:
            for presc_id, presc_data in data.items():
                prescription = Prescription(
                    prescription_id=presc_data['prescription_id'],
                    patient_id=presc_data['patient_id'],
                    doctor_id=presc_data['doctor_id'],
                    medication=presc_data['medication'],
                    dosage=presc_data['dosage'],
                    duration=presc_data['duration'],
                    instructions=presc_data.get('instructions', ''),
                    date_issued=presc_data.get('date_issued', '')
                )
                prescription.is_active = presc_data.get('is_active', True)
                self.prescriptions[presc_id] = prescription
    
    def load_admin_users(self):
        """Load admin users from JSON"""
        filepath = os.path.join(self.data_dir, 'admin_users.json')
        self.admin_users = self._load_json(filepath) or {}
    
    def _load_json(self, filepath):
        """Load data from JSON file"""
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading from {filepath}: {str(e)}")
                return None
        return None
    
    def load_all_data(self):
        """Load all data from JSON files"""
        self.load_patients()
        self.load_doctors()
        self.load_appointments()
        self.load_medical_records()
        self.load_complaints()
        self.load_prescriptions()
        self.load_admin_users()
    
    def get_system_statistics(self):
        """Get system statistics"""
        return {
            'total_patients': len([p for p in self.patients.values() if p.is_active]),
            'total_doctors': len([d for d in self.doctors.values() if d.is_active]),
            'verified_doctors': len([d for d in self.doctors.values() if d.is_active and d.verified]),
            'total_appointments': len(self.appointments),
            'pending_appointments': len([a for a in self.appointments.values() if a.status == 'pending']),
            'completed_appointments': len([a for a in self.appointments.values() if a.status == 'completed']),
            'total_medical_records': len(self.medical_records),
            'pending_complaints': len([c for c in self.complaints.values() if c.status == 'pending']),
            'resolved_complaints': len([c for c in self.complaints.values() if c.status == 'resolved']),
        }
