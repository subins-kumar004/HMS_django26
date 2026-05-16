from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from administrator.models import Role, Staff, Specialization, Doctor

class AuthAPITests(APITestCase):
    def setUp(self):
        self.role = Role.objects.create(role_name="Admin")
        self.staff = Staff.objects.create_user(
            username="adminuser", 
            password="testpassword123", 
            email="admin@test.com", 
            role=self.role,
            is_active=True
        )

    def test_login_flow(self):
        # Task 7: Login flow
        url = '/api/auth/login/'
        data = {"username": "adminuser", "password": "testpassword123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        url = '/api/auth/login/'
        data = {"username": "adminuser", "password": "wrongpassword"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_flow(self):
        # Task 7: Logout flow
        login_url = '/api/auth/login/'
        login_data = {"username": "adminuser", "password": "testpassword123"}
        login_resp = self.client.post(login_url, login_data, format='json')
        refresh_token = login_resp.data.get('refresh')
        
        url = '/api/auth/logout/'
        response = self.client.post(url, {"refresh": refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StaffAPITests(APITestCase):
    def setUp(self):
        self.role_admin = Role.objects.create(role_name="Administrator")
        self.role_receptionist = Role.objects.create(role_name="Receptionist")
        
        self.admin_user = Staff.objects.create_user(
            username="superadmin", 
            password="adminpassword", 
            role=self.role_admin,
            is_active=True
        )
        self.client.force_authenticate(user=self.admin_user)
        
        self.staff_user = Staff.objects.create_user(
            username="receptionist1",
            password="password123",
            role=self.role_receptionist,
            emp_id="EMP1001",
            contact="1234567890",
            gender="Female",
            address="Some Address",
            is_active=True
        )

    def test_create_staff_valid(self):
        # Task 13: valid data -> 201 Created
        url = '/api/staff/create/'
        data = {
            "username": "newstaff",
            "password": "newpassword123",
            "email": "newstaff@test.com",
            "role": self.role_receptionist.id,
            "emp_id": "EMP1002",
            "contact": "9876543210",
            "gender": "Male",
            "address": "123 Main St"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_staff_missing_fields(self):
        # Task 14: missing fields -> 400 Bad Request
        url = '/api/staff/create/'
        data = {
            "username": "incompleteuser"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_staff_valid(self):
        # Task 19: valid update -> 200 OK
        url = f'/api/staff/update/{self.staff_user.id}/'
        data = {
            "username": "receptionist1",
            "contact": "1112223333"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deactivate_staff(self):
        # Task 24: valid deactivation -> 200 OK
        url = f'/api/staff/deactivate/{self.staff_user.id}/'
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.staff_user.refresh_from_db()
        self.assertFalse(self.staff_user.is_active)

    def test_list_staff(self):
        # Task 29: retrieve all staff -> 200 OK
        url = '/api/staff/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_staff_by_id(self):
        # Task 27: Get Staff by ID API
        url = f'/api/staff/{self.staff_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.staff_user.username)

    def test_search_staff_by_name(self):
        # Task 28: Search by name
        url = '/api/staff/?search=receptionist1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_staff_by_role(self):
        # Task 28: Filter by role
        url = '/api/staff/?role=Receptionist'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)



class SpecializationAPITests(APITestCase):
    def setUp(self):
        self.role_admin = Role.objects.create(role_name="Administrator")
        self.admin_user = Staff.objects.create_user(username="admin1", password="password", role=self.role_admin)
        self.client.force_authenticate(user=self.admin_user)
        self.specialization = Specialization.objects.create(specialization_name="Neurology")

    def test_create_specialization(self):
        url = '/api/specializations/create/'
        data = {"specialization_name": "Orthopedics"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_specializations(self):
        url = '/api/specializations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_specialization(self):
        # Task 44: specialization CRUD (Update)
        url = f'/api/specializations/{self.specialization.id}/'
        data = {"specialization_name": "Updated Neurology"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['specialization_name'], "Updated Neurology")


class DoctorAPITests(APITestCase):
    def setUp(self):
        self.role_admin = Role.objects.create(role_name="Administrator")
        self.admin_user = Staff.objects.create_user(username="admin_doc", password="pwd", role=self.role_admin)
        self.client.force_authenticate(user=self.admin_user)
        
        self.role_doctor = Role.objects.create(role_name="Doctor")
        self.doc_staff = Staff.objects.create_user(username="drsmith", password="pwd", role=self.role_doctor, emp_id="DOC001")
        self.spec = Specialization.objects.create(specialization_name="Cardiology")
        
        self.doctor = Doctor.objects.create(staff=self.doc_staff, specialization=self.spec, consultation_fee=1000.00)

    def test_create_doctor(self):
        # Task 34: valid doctor creation -> 201 Created
        new_doc_staff = Staff.objects.create_user(username="drjones", password="pwd", role=self.role_doctor, emp_id="DOC002")
        url = '/api/doctors/create/'
        data = {
            "staff": new_doc_staff.id,
            "specialization": self.spec.id,
            "consultation_fee": 800.00
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_doctor(self):
        # Task 39: test case for update
        url = f'/api/doctors/update/{self.doctor.id}/'
        data = {
            "consultation_fee": 1200.00
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deactivate_doctor(self):
        # Task 39: test case for deactivation
        url = f'/api/doctors/deactivate/{self.doctor.id}/'
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.doctor.refresh_from_db()
        self.assertFalse(self.doctor.is_active)

    def test_list_doctors(self):
        url = '/api/doctors/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_doctor_by_id(self):
        url = f'/api/doctors/{self.doctor.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.doctor.id)



class RoleAPITests(APITestCase):
    def setUp(self):
        self.role_admin = Role.objects.create(role_name="Administrator")
        self.admin_user = Staff.objects.create_user(username="admin_role", password="pwd", role=self.role_admin)
        self.client.force_authenticate(user=self.admin_user)
        
        # Task 45: Seed default roles (Simulated via setup)
        Role.objects.get_or_create(role_name="Receptionist")
        Role.objects.get_or_create(role_name="Doctor")

    def test_retrieve_all_roles(self):
        # Task 47: List All Roles -> 200 OK
        url = '/api/roles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_role_by_id(self):
        # Task 49: Retrieve role by valid ID -> 200 OK
        url = f'/api/roles/{self.role_admin.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
