from django.test import TestCase
from rest_framework.test import APIClient
from administrator.models import LabTest, LabTestPrescription, Appointment, Patient, Doctor, Staff, Specialization, Role
from datetime import date

class LabTechModuleTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create basic required models
        self.patient = Patient.objects.create(patient_name="John Doe", contact="1234567890", age=30, gender="Male", address="NY")
        self.role = Role.objects.create(role_name="Doctor")
        self.staff = Staff.objects.create(username="doc_lab", emp_id="E002", role=self.role)
        self.spec = Specialization.objects.create(specialization_name="General")
        self.doctor = Doctor.objects.create(staff=self.staff, specialization=self.spec, consultation_fee=500.00)
        
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, appointment_date=date.today(), 
            appointment_time="10:00:00", token_number=1, status="Scheduled"
        )

        # Create Lab Test
        self.labtest_data = {
            "test_name": "Complete Blood Count",
            "category": "Blood Test",
            "amount": 500.00,
            "reference_range": "Normal",
            "sample_type": "Blood",
            "status": True
        }
        self.labtest = LabTest.objects.create(**self.labtest_data)

        # Create Lab Test Prescription
        self.prescription = LabTestPrescription.objects.create(
            appointment=self.appointment,
            lab_test=self.labtest,
            instructions="Fasting required"
        )

    # =========================
    # LAB TEST MANAGEMENT
    # =========================

    def test_list_lab_tests(self):
        # Task 148: List All Lab Tests API
        response = self.client.get('/api/labtests')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_add_lab_test(self):
        # Task 145: Add New Lab Test API
        data = {
            "test_name": "Lipid Profile",
            "category": "Blood Test",
            "amount": 800.00,
            "reference_range": "Normal",
            "sample_type": "Blood",
            "status": True
        }
        response = self.client.post('/api/labtests', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_lab_test_by_id(self):
        # Task 147: Get Lab Test by ID
        response = self.client.get(f'/api/labtests/{self.labtest.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['test_name'], "Complete Blood Count")

    def test_update_lab_test(self):
        # Task 146: Update Lab Test
        data = {
            "test_name": "Complete Blood Count Updated",
            "category": "Blood Test",
            "amount": 600.00,
            "reference_range": "Normal",
            "sample_type": "Blood",
            "status": True
        }
        response = self.client.put(f'/api/labtests/{self.labtest.id}', data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_deactivate_lab_test(self):
        # Task 149: Deactivate Lab Test
        response = self.client.patch(f'/api/labtests/{self.labtest.id}/deactivate')
        self.assertEqual(response.status_code, 200)

    # =========================
    # LAB TEST PRESCRIPTIONS & RESULTS
    # =========================

    def test_add_lab_test_prescription(self):
        data = {
            "appointment": self.appointment.id,
            "lab_test": self.labtest.id,
            "instructions": "No specific instructions"
        }
        response = self.client.post('/api/labtests/prescription/add', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_record_lab_result(self):
        # Task 157: Record Lab Test Result
        data = {
            "test_value": "120",
            "remarks": "Normal range"
        }
        response = self.client.put(f'/api/labtests/results/{self.prescription.id}', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['test_value'], "120")

    def test_get_results_by_appointment(self):
        # Task 153: Get Lab Test Result by Appointment
        response = self.client.get(f'/api/labtests/results/appointment/{self.appointment.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_get_results_by_date_range(self):
        # Task 154: List Lab Test Results by Date Range
        response = self.client.get(f'/api/labtests/results?startDate=2020-01-01&endDate=2030-01-01')
        self.assertEqual(response.status_code, 200)

    def test_deactivate_lab_test_prescription(self):
        # Task 160: Deactivate Lab Test Prescription
        response = self.client.patch(f'/api/labtests/prescription/{self.prescription.id}/deactivate')
        self.assertEqual(response.status_code, 200)
