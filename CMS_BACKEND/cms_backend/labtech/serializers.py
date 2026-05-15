from rest_framework import serializers

from administrator.models import (
    LabTest,
    LabTestPrescription
)


class LabTestSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabTest
        fields = '__all__'


class LabTestPrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LabTestPrescription
        fields = '__all__'