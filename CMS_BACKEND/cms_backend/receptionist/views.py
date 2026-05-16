from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from administrator.models import Patient, Appointment, Bill
from .serializers import PatientSerializer, AppointmentSerializer, BillSerializer
from datetime import datetime

# =========================
# PATIENT VIEWS
# =========================

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    # permission_classes = [IsAuthenticated] # Assuming auth is required later

    def get_queryset(self):
        queryset = Patient.objects.all()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(patient_name__icontains=search_query) |
                Q(patient_id__icontains=search_query) |
                Q(contact__icontains=search_query)
            )
        return queryset

class PatientDetailView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


# =========================
# APPOINTMENT VIEWS
# =========================

class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()
        date_param = self.request.query_params.get('date', None)
        status_param = self.request.query_params.get('status', None)
        
        if date_param:
            queryset = queryset.filter(appointment_date=date_param)
        if status_param:
            queryset = queryset.filter(status=status_param)
            
        return queryset

    def perform_create(self, serializer):
        # Task 67: Check doctor availability before booking (basic check for overlapping token or time)
        # Assuming simple overlap check for demonstration if time is used
        doctor = serializer.validated_data.get('doctor')
        appointment_date = serializer.validated_data.get('appointment_date')
        appointment_time = serializer.validated_data.get('appointment_time')

        if Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date, appointment_time=appointment_time, status__in=['Scheduled']).exists():
            raise ValidationError({"appointment_time": "Doctor is already booked at this time on this date."})
            
        serializer.save()

class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class CancelAppointmentView(APIView):
    def patch(self, request, pk, format=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)
            
        appointment.status = 'Cancelled'
        appointment.save()
        return Response({"message": "Appointment cancelled successfully.", "status": appointment.status}, status=status.HTTP_200_OK)

class PatientAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patientId']
        return Appointment.objects.filter(patient_id=patient_id)

class DoctorAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctorId']
        return Appointment.objects.filter(doctor_id=doctor_id)


# =========================
# BILL VIEWS
# =========================

class BillListCreateView(generics.ListCreateAPIView):
    serializer_class = BillSerializer

    def get_queryset(self):
        queryset = Bill.objects.all()
        start_date = self.request.query_params.get('startDate', None)
        end_date = self.request.query_params.get('endDate', None)
        
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                # Add time to include end date fully if created_at is DateTime
                queryset = queryset.filter(created_at__gte=start, created_at__lt=end)
            except ValueError:
                pass
        return queryset

class BillDetailView(generics.RetrieveUpdateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    lookup_field = 'appointment_id'

