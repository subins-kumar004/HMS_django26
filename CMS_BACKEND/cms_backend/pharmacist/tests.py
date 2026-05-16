from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from administrator.models import Medicine, MedicineStock, Patient, Appointment, Doctor, Staff, Specialization, Role, MedicinePrescription, Bill
from decimal import Decimal

class PharmacistAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Set up a Medicine
        self.medicine_data = {
            "medicine_name": "Paracetamol",
            "category": "Painkiller",
            "manufacturing_date": "2023-01-01",
            "expiry_date": "2025-01-01",
            "unit": "10 mg",
            "status": True
        }
        self.medicine = Medicine.objects.create(**self.medicine_data)

        # Set up Medicine Stock
        self.stock_data = {
            "medicine": self.medicine,
            "quantity": 100,
            "reorder_level": 20
        }
        self.stock = MedicineStock.objects.create(**self.stock_data)

        # Set up basic models for Dispense
        self.patient = Patient.objects.create(
            patient_name="John Doe", contact="1234567890", age=30, gender="Male", address="NY"
        )
        self.role = Role.objects.create(role_name="Doctor")
        self.staff = Staff.objects.create(username="doc1", emp_id="E001", role=self.role)
        self.spec = Specialization.objects.create(specialization_name="General")
        self.doctor = Doctor.objects.create(staff=self.staff, specialization=self.spec, consultation_fee=500.00)
        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, appointment_date="2023-10-01", 
            appointment_time="10:00:00", token_number=1, status="Scheduled"
        )
        self.bill = Bill.objects.create(
            appointment=self.appointment, consultation_fee=500.00, total_amount=500.00
        )
        self.prescription = MedicinePrescription.objects.create(
            appointment=self.appointment, medicine=self.medicine, dosage="1-0-1", frequency="Twice daily", duration="5 days"
        )

    # 1. Medicine Tests
    def test_add_medicine(self):
        new_med = {
            "medicine_name": "Aspirin",
            "category": "Painkiller",
            "manufacturing_date": "2023-02-01",
            "expiry_date": "2025-02-01",
            "unit": "5 mg",
            "status": True
        }
        response = self.client.post('/api/medicines', new_med, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medicine.objects.count(), 2)

    def test_list_medicines(self):
        response = self.client.get('/api/medicines')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_medicine(self):
        response = self.client.get(f'/api/medicines/{self.medicine.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['medicine_name'], "Paracetamol")

    def test_update_medicine(self):
        update_data = {
            "medicine_name": "Paracetamol 500",
            "category": "Painkiller",
            "manufacturing_date": "2023-01-01",
            "expiry_date": "2025-01-01",
            "unit": "10 mg",
            "status": True
        }
        response = self.client.put(f'/api/medicines/{self.medicine.id}', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medicine.refresh_from_db()
        self.assertEqual(self.medicine.medicine_name, "Paracetamol 500")

    def test_deactivate_medicine(self):
        response = self.client.patch(f'/api/medicines/{self.medicine.id}/deactivate')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medicine.refresh_from_db()
        self.assertFalse(self.medicine.status)

    # 2. Inventory Tests
    def test_add_inventory(self):
        med2 = Medicine.objects.create(
            medicine_name="Ibuprofen", category="Painkiller", manufacturing_date="2023-01-01",
            expiry_date="2025-01-01", unit="10 mg", status=True
        )
        new_stock = {
            "medicine": med2.id,
            "quantity": 50,
            "reorder_level": 10
        }
        response = self.client.post('/api/inventory/medicine', new_stock, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicineStock.objects.count(), 2)

    def test_get_inventory_by_medicine(self):
        response = self.client.get(f'/api/inventory/medicine/{self.medicine.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['quantity'], 100)

    def test_list_all_inventory(self):
        # Task 135: List All Inventory API
        response = self.client.get('/api/inventory/medicine')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_update_inventory(self):
        update_data = {"quantity": 120}
        response = self.client.put(f'/api/inventory/medicine/stock/{self.stock.id}', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 120)

    def test_flag_low_stock(self):
        # Quantity is 100, reorder is 20 -> should not flag
        response = self.client.patch(f'/api/inventory/medicine/stock/{self.stock.id}/flag-low')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Stock level is sufficient")

        # Update to low stock
        self.stock.quantity = 15
        self.stock.save()
        response2 = self.client.patch(f'/api/inventory/medicine/stock/{self.stock.id}/flag-low')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data['message'], "Low stock alert!")

    # 3. Dispense Tests
    def test_get_patient_prescriptions(self):
        response = self.client.get(f'/api/prescriptions/patient/{self.patient.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['medicine_name'], "Paracetamol")

    def test_dispense_medicine_success(self):
        dispense_data = {
            "appointment_id": self.appointment.id,
            "dispensed_items": [
                {
                    "medicine_id": self.medicine.id,
                    "quantity": 10,
                    "cost": 50.00
                }
            ]
        }
        response = self.client.post('/api/dispense', dispense_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 90)  # 100 - 10
        
        self.bill.refresh_from_db()
        self.assertEqual(self.bill.additional_charge, Decimal('50.00'))
        self.assertEqual(self.bill.total_amount, Decimal('550.00'))  # 500 + 50

    def test_dispense_medicine_insufficient_stock(self):
        dispense_data = {
            "appointment_id": self.appointment.id,
            "dispensed_items": [
                {
                    "medicine_id": self.medicine.id,
                    "quantity": 150,  # More than available 100
                    "cost": 750.00
                }
            ]
        }
        response = self.client.post('/api/dispense', dispense_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient stock", response.data['error'])
        
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 100)  # Unchanged
