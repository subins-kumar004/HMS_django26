import os
import django
import random
from datetime import date, timedelta, datetime
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms_backend.settings")
django.setup()

from administrator.models import (
    Role, Staff, Specialization, Doctor, Patient,
    Appointment, Consultation, Medicine, MedicineStock,
    MedicinePrescription, LabTest, LabTestPrescription, Bill
)

def create_staff(username, email, role_name, first_name, last_name, is_doctor=False):
    role = Role.objects.get(role_name=role_name)
    staff, created = Staff.objects.get_or_create(
        username=username,
        defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': role,
            'emp_id': f"EMP-{random.randint(1000, 9999)}",
            'is_active': True
        }
    )
    if created:
        staff.set_password('password123')
        staff.save()
    return staff

def run_seeder():
    print("Starting Dummy Data Seeder...")

    # 1. Master Data
    print("Seeding Roles...")
    roles = ['Admin', 'Receptionist', 'Doctor', 'Pharmacist', 'Lab Technician']
    for r in roles:
        Role.objects.get_or_create(role_name=r)

    print("Seeding Specializations...")
    specs = ['Cardiology', 'Neurology', 'Pediatrics', 'Orthopedics', 'General Practice']
    for s in specs:
        Specialization.objects.get_or_create(specialization_name=s)

    print("Seeding Medicines & Stock...")
    meds = [
        ('Paracetamol', 'Painkiller', 'Tablet'),
        ('Amoxicillin', 'Antibiotic', 'Capsule'),
        ('Ibuprofen', 'Painkiller', 'Tablet'),
        ('Cetirizine', 'Antihistamine', 'Tablet'),
        ('Omeprazole', 'Antacid', 'Capsule'),
        ('Azithromycin', 'Antibiotic', 'Tablet'),
        ('Metformin', 'Anti-diabetic', 'Tablet'),
        ('Amlodipine', 'Anti-hypertensive', 'Tablet'),
        ('Cough Syrup X', 'Expectorant', 'Syrup'),
        ('Vitamin C', 'Supplement', 'Tablet')
    ]
    for name, cat, unit in meds:
        med, _ = Medicine.objects.get_or_create(
            medicine_name=name,
            defaults={
                'category': cat,
                'unit': unit,
                'manufacturing_date': date.today() - timedelta(days=100),
                'expiry_date': date.today() + timedelta(days=365)
            }
        )
        # Create low stock for a couple of items to trigger alerts
        qty = 5 if name in ['Amoxicillin', 'Amlodipine'] else 100
        MedicineStock.objects.get_or_create(
            medicine=med,
            defaults={'quantity': qty, 'reorder_level': 10}
        )

    print("Seeding Lab Tests...")
    tests = [
        ('Complete Blood Count', 'Hematology', 50.00, 'Normal', 'Blood'),
        ('Lipid Profile', 'Biochemistry', 80.00, 'Normal', 'Blood'),
        ('Chest X-Ray', 'Radiology', 150.00, 'N/A', 'Imaging'),
        ('Urinalysis', 'Clinical Pathology', 30.00, 'Normal', 'Urine'),
        ('Fasting Blood Sugar', 'Biochemistry', 40.00, '70-100 mg/dL', 'Blood')
    ]
    for name, cat, amount, ref, samp in tests:
        LabTest.objects.get_or_create(
            test_name=name,
            defaults={
                'category': cat,
                'amount': Decimal(amount),
                'reference_range': ref,
                'sample_type': samp
            }
        )

    # 2. Personnel
    print("Seeding Staff...")
    create_staff('admin1', 'admin@hms.com', 'Admin', 'Super', 'Admin')
    create_staff('receptionist1', 'rec@hms.com', 'Receptionist', 'Sarah', 'Connor')
    create_staff('labtech1', 'lab@hms.com', 'Lab Technician', 'Walter', 'White')
    create_staff('pharmacist1', 'pharm@hms.com', 'Pharmacist', 'Jesse', 'Pinkman')

    print("Seeding Doctors...")
    dr1_staff = create_staff('doctor1', 'dr1@hms.com', 'Doctor', 'Gregory', 'House')
    dr2_staff = create_staff('doctor2', 'dr2@hms.com', 'Doctor', 'Meredith', 'Grey')
    dr3_staff = create_staff('doctor3', 'dr3@hms.com', 'Doctor', 'Stephen', 'Strange')

    dr1, _ = Doctor.objects.get_or_create(staff=dr1_staff, defaults={'specialization': Specialization.objects.get(specialization_name='General Practice'), 'consultation_fee': Decimal('100.00')})
    dr2, _ = Doctor.objects.get_or_create(staff=dr2_staff, defaults={'specialization': Specialization.objects.get(specialization_name='Cardiology'), 'consultation_fee': Decimal('150.00')})
    dr3, _ = Doctor.objects.get_or_create(staff=dr3_staff, defaults={'specialization': Specialization.objects.get(specialization_name='Neurology'), 'consultation_fee': Decimal('200.00')})

    doctors = [dr1, dr2, dr3]

    # 3. Patients
    print("Seeding Patients...")
    patients = []
    for i in range(1, 11):
        pat, _ = Patient.objects.get_or_create(
            patient_name=f'Dummy Patient {i}',
            defaults={
                'contact': f'555-010{i}',
                'age': random.randint(5, 80),
                'gender': random.choice(['Male', 'Female']),
                'address': f'{i} Main St, City',
                'membership': random.choice([True, False])
            }
        )
        patients.append(pat)

    # 4. Appointments & Clinical Records
    print("Seeding Appointments & Records...")
    status_choices = ['Completed'] * 5 + ['Cancelled'] * 2 + ['Scheduled'] * 8
    
    # Give some scheduled appointments to today
    all_meds = list(Medicine.objects.all())
    all_tests = list(LabTest.objects.all())

    for i, status in enumerate(status_choices):
        appt_date = date.today() if status == 'Scheduled' else date.today() - timedelta(days=random.randint(1, 10))
        
        appt, created = Appointment.objects.get_or_create(
            patient=random.choice(patients),
            doctor=random.choice(doctors),
            appointment_date=appt_date,
            appointment_time=datetime.now().time(),
            defaults={'status': status}
        )

        if status == 'Completed' and created:
            # Create Consultation
            Consultation.objects.create(
                appointment=appt,
                symptoms='Fever and headache' if i % 2 == 0 else 'Chest pain and shortness of breath',
                diagnosis='Viral infection' if i % 2 == 0 else 'Mild angina',
                notes='Rest advised.'
            )

            # Create Prescription
            MedicinePrescription.objects.create(
                appointment=appt,
                medicine=random.choice(all_meds),
                dosage='500mg',
                frequency='1-0-1',
                duration='5 days'
            )

            # Create Lab Test
            lab_test = random.choice(all_tests)
            LabTestPrescription.objects.create(
                appointment=appt,
                lab_test=lab_test,
                instructions='Fasting required' if lab_test.test_name == 'Fasting Blood Sugar' else '',
                test_value='Normal limits' if i % 2 == 0 else 'Elevated',
                remarks='Monitor closely'
            )

            # Create Bill
            Bill.objects.create(
                appointment=appt,
                consultation_fee=appt.doctor.consultation_fee,
                additional_charge=Decimal('50.00'),
                total_amount=appt.doctor.consultation_fee + Decimal('50.00')
            )

    print("Dummy Data Seeding Completed Successfully!")

if __name__ == "__main__":
    run_seeder()
