from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import Role, Staff, Specialization, Doctor

# =========================
# ROLE SERIALIZER
# =========================


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


# =========================
# STAFF SERIALIZER
# =========================


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "contact",
            "gender",
            "address",
            "salary",
            "emp_id",
            "role",
            "is_active",
            "password",
        ]

        extra_kwargs = {"password": {"write_only": True}} 

        

    # CREATE STAFF
    def create(self, validated_data):
        password = validated_data.pop("password")

        user = Staff(**validated_data)
        user.set_password(password)
        user.save()

        return user

    # UPDATE STAFF
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


# =========================
# SPECIALIZATION SERIALIZER
# =========================


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


# =========================
# DOCTOR SERIALIZER
# =========================


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"


# =========================
# LOGIN SERIALIZER
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

        return {
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
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
# LOGOUT SERIALIZER
# =========================


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self):
        try:
            refresh_token = self.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
             raise serializers.ValidationError("Token is invalid or already blacklisted")
