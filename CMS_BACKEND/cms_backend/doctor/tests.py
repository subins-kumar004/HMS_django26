from django.test import TestCase
from rest_framework.test import APIClient

from administrator.models import (
    Role,
    Staff,
    Specialization,
    Doctor,
    Patient,
    Appointment,
    Medicine,
    LabTest
)


class DoctorModuleTest(TestCase):

    def setUp(self):

        self.client = APIClient()

        # Create Role
        self.role = Role.objects.create(
            role_name="Doctor"
        )

        # Create Staff
        self.staff = Staff.objects.create_user(
            username="doctor_test",
            password="test123",
            emp_id="DOC999",
            contact="9999999999",
            gender="Male",
            address="Kerala",
            role=self.role
        )

        # Create Specialization
        self.specialization = Specialization.objects.create(
            specialization_name="General Medicine"
        )

        # Create Doctor
        self.doctor = Doctor.objects.create(
            staff=self.staff,
            specialization=self.specialization,
            consultation_fee=500
        )

        # Create Patient
        self.patient = Patient.objects.create(
            patient_name="Test Patient",
            contact="8888888888",
            age=25,
            gender="Male",
            address="Kerala"
        )

        # Create Appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date="2026-05-14",
            appointment_time="10:30:00",
            token_number=1
        )

        # Create Medicine
        self.medicine = Medicine.objects.create(
            medicine_name="Paracetamol",
            category="Tablet",
            manufacturing_date="2025-01-01",
            expiry_date="2027-01-01",
            unit="Strip"
        )

        # Create Lab Test
        self.labtest = LabTest.objects.create(
            test_name="Blood Sugar",
            category="Blood Test",
            amount=250,
            reference_range="70-140",
            sample_type="Blood"
        )

        from administrator.models import Consultation, MedicinePrescription, LabTestPrescription
        
        self.consultation = Consultation.objects.create(
            appointment=self.appointment,
            symptoms="Fever",
            diagnosis="Viral Fever",
            notes="Rest"
        )
        
        self.medicine_prescription = MedicinePrescription.objects.create(
            appointment=self.appointment,
            medicine=self.medicine,
            dosage="500mg",
            frequency="Twice daily",
            duration="5 days"
        )
        
        self.labtest_prescription = LabTestPrescription.objects.create(
            appointment=self.appointment,
            lab_test=self.labtest,
            instructions="Fasting"
        )



    # TASK 96 + 102
    def test_create_consultation(self):
        appointment2 = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date="2026-05-15",
            appointment_time="11:30:00",
            token_number=2
        )
        response = self.client.post(
            '/api/consultation/create/',
            {
                "appointment": appointment2.id,
                "symptoms": "Cough",
                "diagnosis": "Cold",
                "notes": "Syrup"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_consultation_history_patient(self):
        response = self.client.get(f'/api/consultation/patient/{self.patient.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_consultation_history_doctor(self):
        response = self.client.get(f'/api/consultation/doctor/{self.doctor.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_consultation_by_appointment(self):
        response = self.client.get(f'/api/consultation/appointment/{self.appointment.id}/')
        self.assertEqual(response.status_code, 200)


    # TASK 107 + 113
    def test_create_medicine_prescription(self):
        appointment2 = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, appointment_date="2026-05-16", appointment_time="11:30:00", token_number=3
        )
        response = self.client.post(
            '/api/medicine/create/',
            {
                "appointment": appointment2.id,
                "medicine": self.medicine.id,
                "dosage": "500mg",
                "frequency": "Twice daily",
                "duration": "5 days"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_update_medicine_prescription(self):
        response = self.client.patch(
            f'/api/medicine/update/{self.medicine_prescription.id}/',
            {"dosage": "250mg"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['dosage'], "250mg")

    def test_medicine_by_appointment(self):
        response = self.client.get(f'/api/medicine/appointment/{self.appointment.id}/')
        self.assertEqual(response.status_code, 200)

    def test_medicine_by_patient(self):
        response = self.client.get(f'/api/medicine/patient/{self.patient.id}/')
        self.assertEqual(response.status_code, 200)

    def test_medicine_history_patient(self):
        response = self.client.get(f'/api/medicine/history/patient/{self.patient.id}/')
        self.assertEqual(response.status_code, 200)

    def test_medicine_history_doctor(self):
        response = self.client.get(f'/api/medicine/history/doctor/{self.doctor.id}/')
        self.assertEqual(response.status_code, 200)


    # TASK 118 + 123
    def test_create_labtest_prescription(self):
        appointment2 = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, appointment_date="2026-05-17", appointment_time="11:30:00", token_number=4
        )
        response = self.client.post(
            '/api/labtest/create/',
            {
                "appointment": appointment2.id,
                "lab_test": self.labtest.id,
                "instructions": "Fasting"
            },
            format='json'
        )
        self.assertEqual(response.status_code, 201)

    def test_update_labtest_prescription(self):
        response = self.client.patch(
            f'/api/labtest/update/{self.labtest_prescription.id}/',
            {"instructions": "Non-fasting"},
            format='json'
        )
        self.assertEqual(response.status_code, 200)

    def test_labtest_by_appointment(self):
        response = self.client.get(f'/api/labtest/appointment/{self.appointment.id}/')
        self.assertEqual(response.status_code, 200)

    def test_labtest_by_patient(self):
        response = self.client.get(f'/api/labtest/patient/{self.patient.id}/')
        self.assertEqual(response.status_code, 200)