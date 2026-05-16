from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from administrator.models import Patient, Staff, Doctor, Specialization, Appointment, Bill
from datetime import date, timedelta

class PatientAPITests(APITestCase):
    def setUp(self):
        self.patient_data = {
            "patient_name": "John Doe",
            "contact": "+1234567890",
            "age": 30,
            "gender": "Male",
            "address": "123 Main St",
            "membership": True
        }
        self.patient = Patient.objects.create(**self.patient_data)

    def test_valid_patient_registration(self):
        # Task 54: valid patient registration -> 201 Created
        new_patient = {
            "patient_name": "Jane Doe",
            "contact": "+0987654321",
            "age": 25,
            "gender": "Female",
            "address": "456 Oak St",
            "membership": False
        }
        url = reverse('patient-list-create')
        response = self.client.post(url, new_patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('patient_id', response.data)

    def test_missing_required_field(self):
        # Task 55: missing required field -> 400 Bad Request
        invalid_patient = {"patient_name": "No Contact"}
        url = reverse('patient-list-create')
        response = self.client.post(url, invalid_patient, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_patient_update(self):
        # Task 59: valid update -> 200 OK
        url = reverse('patient-detail', args=[self.patient.id])
        update_data = {"patient_name": "John Updated", "contact": "+1234567890", "age": 31, "gender": "Male", "address": "123 Main St"}
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient_name'], "John Updated")

    def test_retrieve_patient_list(self):
        # Task 64: retrieve patient list -> 200 OK
        url = reverse('patient-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_patient_by_id(self):
        # Task 62: Get Patient by ID API
        url = reverse('patient-detail', args=[self.patient.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['patient_name'], self.patient.patient_name)



class AppointmentAPITests(APITestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            patient_name="Mark Smith", contact="+1112223333", age=40, gender="Male", address="NY"
        )
        self.staff = Staff.objects.create(username="drwho", contact="123", gender="Male", address="UK", emp_id="EMP01")
        self.specialization = Specialization.objects.create(specialization_name="Cardiology")
        self.doctor = Doctor.objects.create(staff=self.staff, specialization=self.specialization, consultation_fee=500.00)
        
        self.appointment_date = date.today() + timedelta(days=1)
        
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=self.appointment_date,
            appointment_time="10:00:00"
        )

    def test_valid_appointment_booking(self):
        # Task 70: valid appointment -> 201 Created
        url = reverse('appointment-list-create')
        new_appointment = {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "appointment_date": str(self.appointment_date + timedelta(days=1)),
            "appointment_time": "11:00:00"
        }
        response = self.client.post(url, new_appointment, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_appointment(self):
        # Task 75: update flow -> 200 OK
        url = reverse('appointment-detail', args=[self.appointment.id])
        update_data = {
            "patient": self.patient.id,
            "doctor": self.doctor.id,
            "appointment_date": str(self.appointment_date),
            "appointment_time": "14:00:00",
            "status": "Scheduled"
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_appointment(self):
        # Task 75: cancel flow -> 200 OK
        url = reverse('appointment-cancel', args=[self.appointment.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "Cancelled")

    def test_list_appointments_by_date(self):
        # Task 81: listing scenarios
        url = reverse('appointment-list-create')
        response = self.client.get(f"{url}?date={self.appointment_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class BillAPITests(APITestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            patient_name="Bill Gates", contact="+4445556666", age=60, gender="Male", address="WA"
        )
        self.staff = Staff.objects.create(username="drsome", contact="123", gender="Female", address="WA", emp_id="EMP02")
        self.doctor = Doctor.objects.create(staff=self.staff, consultation_fee=1000.00)
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=date.today(),
            appointment_time="09:00:00"
        )
        self.bill = Bill.objects.create(
            appointment=self.appointment,
            consultation_fee=1000.00,
            additional_charge=0,
            total_amount=1000.00
        )

    def test_valid_bill_generation(self):
        # Task 87: valid bill generation -> 201 Created
        appointment2 = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=date.today(),
            appointment_time="11:00:00"
        )
        url = reverse('bill-list-create')
        new_bill = {
            "appointment": appointment2.id,
            "additional_charge": 200.00
        }
        response = self.client.post(url, new_bill, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data['total_amount']), 1200.00)

    def test_bill_update(self):
        # Task 91: test case for bill update
        url = reverse('bill-detail', args=[self.appointment.id])
        update_data = {
            "appointment": self.appointment.id,
            "additional_charge": 150.00
        }
        response = self.client.put(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_amount']), 1150.00)

    def test_bill_retrieval(self):
        # Task 91: test case for bill retrieval
        url = reverse('bill-detail', args=[self.appointment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_bills_by_date_range(self):
        # Task 90: List Bills by Date Range
        url = reverse('bill-list-create')
        start_date = "2020-01-01"
        end_date = "2030-01-01"
        response = self.client.get(f"{url}?startDate={start_date}&endDate={end_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


