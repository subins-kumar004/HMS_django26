from rest_framework import serializers

from .models import (
    Role,
    Staff,
    Specialization,
    Doctor
)


# =========================
# ROLE SERIALIZER
# =========================

class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


# =========================
# STAFF SERIALIZER
# =========================

class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'contact',
            'gender',
            'address',
            'salary',
            'emp_id',
            'role',
            'is_active',
            'password'
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    # CREATE STAFF
    def create(self, validated_data):

        password = validated_data.pop('password')

        user = Staff(**validated_data)

        user.set_password(password)

        user.save()

        return user

    # UPDATE STAFF
    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

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
        fields = '__all__'


# =========================
# DOCTOR SERIALIZER
# =========================

class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'