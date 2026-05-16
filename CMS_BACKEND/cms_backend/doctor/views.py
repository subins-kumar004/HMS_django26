# pyrefly: ignore [missing-import]
from rest_framework import generics

from administrator.models import (
    Consultation,
    MedicinePrescription,
    LabTestPrescription
)

from .serializers import (
    ConsultationSerializer,
    MedicinePrescriptionSerializer,
    LabTestPrescriptionSerializer
)


# ==========================================
# CONSULTATION
# ==========================================

# Create consultation
class ConsultationCreateView(generics.CreateAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer


# View all consultation history
class ConsultationListView(generics.ListAPIView):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer


# View consultation by patient
class ConsultationByPatientView(generics.ListAPIView):
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']

        return Consultation.objects.filter(
            appointment__patient_id=patient_id
        ).order_by('-created_at')


# View consultation by doctor
class ConsultationByDoctorView(generics.ListAPIView):
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']

        return Consultation.objects.filter(
            appointment__doctor_id=doctor_id
        ).order_by('-created_at')


# View consultation by appointment
class ConsultationByAppointmentView(generics.ListAPIView):
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        appointment_id = self.kwargs['appointment_id']

        return Consultation.objects.filter(
            appointment_id=appointment_id
        ).order_by('-created_at')


# ==========================================
# MEDICINE PRESCRIPTION
# ==========================================

# Create prescription
class MedicinePrescriptionCreateView(generics.CreateAPIView):
    queryset = MedicinePrescription.objects.all()
    serializer_class = MedicinePrescriptionSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)


# Update prescription
class MedicinePrescriptionUpdateView(generics.UpdateAPIView):
    queryset = MedicinePrescription.objects.all()
    serializer_class = MedicinePrescriptionSerializer


# View all prescription history
class MedicinePrescriptionListView(generics.ListAPIView):
    queryset = MedicinePrescription.objects.all()
    serializer_class = MedicinePrescriptionSerializer


# View by patient
class MedicineByPatientView(generics.ListAPIView):
    serializer_class = MedicinePrescriptionSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']

        return MedicinePrescription.objects.filter(
            appointment__patient_id=patient_id
        ).order_by('-created_at')


# View by appointment
class MedicineByAppointmentView(generics.ListAPIView):
    serializer_class = MedicinePrescriptionSerializer

    def get_queryset(self):
        appointment_id = self.kwargs['appointment_id']

        return MedicinePrescription.objects.filter(
            appointment_id=appointment_id
        ).order_by('-created_at')


# Medicine history by patient
class MedicineHistoryByPatientView(generics.ListAPIView):
    serializer_class = MedicinePrescriptionSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']

        return MedicinePrescription.objects.filter(
            appointment__patient_id=patient_id
        ).order_by('-created_at')


# Medicine history by doctor
class MedicineHistoryByDoctorView(generics.ListAPIView):
    serializer_class = MedicinePrescriptionSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']

        return MedicinePrescription.objects.filter(
            appointment__doctor_id=doctor_id
        ).order_by('-created_at')

# ==========================================
# LAB TEST PRESCRIPTION
# ==========================================

# Create lab test prescription
class LabTestPrescriptionCreateView(generics.CreateAPIView):
    queryset = LabTestPrescription.objects.all()
    serializer_class = LabTestPrescriptionSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)


# Update lab result
class LabTestPrescriptionUpdateView(generics.UpdateAPIView):
    queryset = LabTestPrescription.objects.all()
    serializer_class = LabTestPrescriptionSerializer


# View all lab history
class LabTestPrescriptionListView(generics.ListAPIView):
    queryset = LabTestPrescription.objects.all()
    serializer_class = LabTestPrescriptionSerializer


# View by patient
class LabTestByPatientView(generics.ListAPIView):
    serializer_class = LabTestPrescriptionSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']

        return LabTestPrescription.objects.filter(
            appointment__patient_id=patient_id
        ).order_by('-created_at')


# View by appointment
class LabTestByAppointmentView(generics.ListAPIView):
    serializer_class = LabTestPrescriptionSerializer

    def get_queryset(self):
        appointment_id = self.kwargs['appointment_id']

        return LabTestPrescription.objects.filter(
            appointment_id=appointment_id
        ).order_by('-created_at')