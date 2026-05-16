from django.urls import path
from . import views

urlpatterns = [
    # Patients
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    
    # Appointments
    path('appointments/', views.AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/<int:pk>/cancel/', views.CancelAppointmentView.as_view(), name='appointment-cancel'),
    path('appointments/patient/<int:patientId>/', views.PatientAppointmentsView.as_view(), name='appointment-patient'),
    path('appointments/doctor/<int:doctorId>/', views.DoctorAppointmentsView.as_view(), name='appointment-doctor'),
    
    # Billing
    path('billing/', views.BillListCreateView.as_view(), name='bill-list-create'),
    path('billing/<int:appointment_id>/', views.BillDetailView.as_view(), name='bill-detail'),
]
