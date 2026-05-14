from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import (
    Role, Staff, Specialization, Doctor, Patient,
    Appointment, Consultation, Medicine, MedicineStock,
    MedicinePrescription, LabTest, LabTestPrescription, Bill
)

# =========================
# ROLE
# =========================

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


# =========================
# STAFF
# =========================

class StaffSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.role_name', read_only=True)

    class Meta:
        model = Staff
        fields = [
            "id", "username", "first_name", "last_name", "email",
            "contact", "gender", "address", "salary", "emp_id",
            "role", "role_name", "is_active", "password",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Staff(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


# =========================
# LOGIN (IMPORTANT FIXED PART)
# =========================

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        if not user.is_active:
            raise serializers.ValidationError("Account is inactive")

        refresh = RefreshToken.for_user(user)

        # FIX: We return only primitive types (strings, ints) that JSON can handle
        return {
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role.role_name if user.role else None,
                "emp_id": user.emp_id,
            },
        }


# =========================
# LOGOUT
# =========================

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        try:
            token = RefreshToken(self.validated_data["refresh"])
            token.blacklist()
        except TokenError:
            raise serializers.ValidationError("Token is invalid or already blacklisted")


# =========================
# MEDICAL CORE
# =========================

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = "__all__"


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"


class MedicineStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineStock
        fields = "__all__"


class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = "__all__"


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = "__all__"