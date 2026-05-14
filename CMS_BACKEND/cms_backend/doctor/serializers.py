from rest_framework import serializers

from administrator.models import (
    Consultation,
    MedicinePrescription,
    LabTestPrescription
)


# ==========================================
# CONSULTATION SERIALIZER
# ==========================================
class ConsultationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultation
        fields = '__all__'


# ==========================================
# MEDICINE PRESCRIPTION SERIALIZER
# ==========================================
class MedicinePrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicinePrescription
        fields = '__all__'


# ==========================================
# LAB TEST PRESCRIPTION SERIALIZER
# ==========================================
class LabTestPrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabTestPrescription
        fields = '__all__'