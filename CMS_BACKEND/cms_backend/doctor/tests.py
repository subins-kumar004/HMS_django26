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


    # TASK 96 + 102
    def test_create_consultation(self):

        response = self.client.post(
            '/api/consultation/create/',
            {
                "appointment": self.appointment.id,
                "symptoms": "Fever",
                "diagnosis": "Viral Fever",
                "notes": "Rest"
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)


    # TASK 107 + 113
    def test_create_medicine_prescription(self):

        response = self.client.post(
            '/api/medicine/create/',
            {
                "appointment": self.appointment.id,
                "medicine": self.medicine.id,
                "dosage": "500mg",
                "frequency": "Twice daily",
                "duration": "5 days"
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)


    # TASK 118 + 123
    def test_create_labtest_prescription(self):

        response = self.client.post(
            '/api/labtest/create/',
            {
                "appointment": self.appointment.id,
                "lab_test": self.labtest.id,
                "instructions": "Fasting"
            },
            format='json'
        )

        self.assertEqual(response.status_code, 201)