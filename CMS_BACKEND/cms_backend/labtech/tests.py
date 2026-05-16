from rest_framework.test import APITestCase
from rest_framework import status
from .models import LabTest, LabTestPrescription
from datetime import date

class LabTechTests(APITestCase):

    def setUp(self):
        # Create a sample LabTest
        self.lab_test = LabTest.objects.create(
            test_name="Complete Blood Count",
            category="Blood",
            amount=500.00,
            reference_ranges="RBC: 4.5-5.5, WBC: 4000-11000",
            sample_type="Blood"
        )
        
        # Create a sample LabTestPrescription
        self.prescription = LabTestPrescription.objects.create(
            appointment_id=101,
            patient_name="John Doe",
            doctor_name="Dr. Smith",
            lab_test=self.lab_test
        )

    # =================================
    # 150. Lab Test CRUD Operations
    # =================================

    def test_create_lab_test(self):
        data = {
            "test_name": "Lipid Profile",
            "category": "Blood",
            "amount": "800.00",
            "reference_ranges": "Cholesterol < 200",
            "sample_type": "Blood",
            "is_active": True
        }
        response = self.client.post('/api/labtests', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['test_name'], "Lipid Profile")

    def test_get_lab_tests(self):
        response = self.client.get('/api/labtests')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['test_name'], "Complete Blood Count")

    def test_get_lab_test_by_id(self):
        response = self.client.get(f'/api/labtests/{self.lab_test.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['test_name'], "Complete Blood Count")

    def test_update_lab_test(self):
        data = {
            "test_name": "Complete Blood Count Updated",
            "category": "Blood",
            "amount": "550.00",
            "reference_ranges": "RBC: 4.5-5.5, WBC: 4000-11000",
            "sample_type": "Blood"
        }
        response = self.client.put(f'/api/labtests/{self.lab_test.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['test_name'], "Complete Blood Count Updated")
        self.assertEqual(response.data['amount'], "550.00")

    def test_deactivate_lab_test(self):
        response = self.client.patch(f'/api/labtests/{self.lab_test.id}/deactivate')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lab_test.refresh_from_db()
        self.assertFalse(self.lab_test.is_active)

    # =================================
    # 155, 161, 162. Prescription & Results
    # =================================

    def test_retrieve_result_by_appointment_id(self):
        # 162. Write test case: retrieve result by appointment ID -> 200 OK with data
        response = self.client.get('/api/labtests/results/appointment/101')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['appointment_id'], 101)
        self.assertEqual(response.data[0]['patient_name'], "John Doe")

    def test_retrieve_result_by_date_range(self):
        # 155. Write test cases for prescription retrieval (by date range)
        today = date.today().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/labtests/results?startDate={today}&endDate={today}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_record_lab_result(self):
        # 161. Write test case: record result -> 200 OK
        data = {
            "lab_test_value": "RBC: 5.0, WBC: 6000",
            "remarks": "Normal"
        }
        response = self.client.put(f'/api/labtests/results/{self.prescription.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lab_test_value'], "RBC: 5.0, WBC: 6000")
        self.assertEqual(response.data['remarks'], "Normal")

    def test_add_lab_test_prescription(self):
        data = {
            "appointment_id": 102,
            "patient_name": "Alice Smith",
            "doctor_name": "Dr. Brown",
            "lab_test": self.lab_test.id
        }
        response = self.client.post('/api/labtests/prescription/add', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['appointment_id'], 102)

    def test_deactivate_lab_test_prescription(self):
        response = self.client.patch(f'/api/labtests/prescription/{self.prescription.id}/deactivate')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.prescription.refresh_from_db()
        self.assertFalse(self.prescription.is_active)
