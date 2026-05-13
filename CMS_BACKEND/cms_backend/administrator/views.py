from rest_framework import generics

from .models import (
    Role,
    Staff,
    Specialization,
    Doctor
)

from .serializers import (
    RoleSerializer,
    StaffSerializer,
    SpecializationSerializer,
    DoctorSerializer
)


# =========================
# ROLE APIs
# =========================

class RoleListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDetailView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# =========================
# STAFF APIs
# =========================

class StaffCreateView(generics.CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffListView(generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffDetailView(generics.RetrieveAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffUpdateView(generics.UpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


# =========================
# SPECIALIZATION APIs
# =========================

class SpecializationCreateView(generics.CreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


class SpecializationListView(generics.ListAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


# =========================
# DOCTOR APIs
# =========================

class DoctorCreateView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorUpdateView(generics.UpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer