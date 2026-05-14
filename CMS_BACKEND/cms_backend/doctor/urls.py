from django.urls import path
from .views import *


urlpatterns = [

    # ==========================================
    # CONSULTATION
    # ==========================================
    path(
        'consultation/create/',
        ConsultationCreateView.as_view()
    ),

    path(
        'consultation/list/',
        ConsultationListView.as_view()
    ),

    path(
        'consultation/patient/<int:patient_id>/',
        ConsultationByPatientView.as_view()
    ),

    path(
        'consultation/doctor/<int:doctor_id>/',
        ConsultationByDoctorView.as_view()
    ),

    path(
        'consultation/appointment/<int:appointment_id>/',
        ConsultationByAppointmentView.as_view()
    ),


    # ==========================================
    # MEDICINE
    # ==========================================
    path(
        'medicine/create/',
        MedicinePrescriptionCreateView.as_view()
    ),

    path(
        'medicine/update/<int:pk>/',
        MedicinePrescriptionUpdateView.as_view()
    ),

    path(
        'medicine/list/',
        MedicinePrescriptionListView.as_view()
    ),

    path(
        'medicine/patient/<int:patient_id>/',
        MedicineByPatientView.as_view()
    ),

    path(
        'medicine/appointment/<int:appointment_id>/',
        MedicineByAppointmentView.as_view()
    ),


    # ==========================================
    # LAB TEST
    # ==========================================
    path(
        'labtest/create/',
        LabTestPrescriptionCreateView.as_view()
    ),

    path(
        'labtest/update/<int:pk>/',
        LabTestPrescriptionUpdateView.as_view()
    ),

    path(
        'labtest/list/',
        LabTestPrescriptionListView.as_view()
    ),

    path(
        'labtest/patient/<int:patient_id>/',
        LabTestByPatientView.as_view()
    ),

    path(
        'labtest/appointment/<int:appointment_id>/',
        LabTestByAppointmentView.as_view()
    ),
]