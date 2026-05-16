from rest_framework import serializers
from administrator.models import Patient, Appointment, Bill, Doctor
from datetime import date
import re

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['patient_id', 'membership_id', 'created_at']

    def validate_contact(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.patient_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.staff.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['token_number', 'status', 'created_at']

    def validate_appointment_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value

    def validate(self, data):
        # Additional validations if needed
        return data


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ['created_at', 'consultation_fee', 'total_amount']

    def validate(self, data):
        appointment = data.get('appointment')
        
        # Pull consultation fee from the doctor associated with the appointment
        if appointment and hasattr(appointment, 'doctor'):
            doctor = appointment.doctor
            consultation_fee = doctor.consultation_fee
        else:
            consultation_fee = 0
            
        additional_charge = data.get('additional_charge', 0)
        
        # Calculate total amount
        data['consultation_fee'] = consultation_fee
        data['total_amount'] = consultation_fee + additional_charge
        
        return data
