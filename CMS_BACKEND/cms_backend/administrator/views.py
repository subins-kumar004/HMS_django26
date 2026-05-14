from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdmin

from .models import Role, Staff, Specialization, Doctor

from .serializers import (
    RoleSerializer,
    StaffSerializer,
    SpecializationSerializer,
    DoctorSerializer,
    LoginSerializer,
    LogoutSerializer,
)

# =========================
# ROLE APIs
# =========================

class RoleListView(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


class RoleDetailView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]


# =========================
# STAFF APIs (RBAC APPLIED HERE)
# =========================

class StaffCreateView(generics.CreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class StaffListView(generics.ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        queryset = Staff.objects.all()

        search = self.request.query_params.get("search")
        role = self.request.query_params.get("role")

        if search:
            queryset = queryset.filter(username__icontains=search)

        if role:
            queryset = queryset.filter(role__role_name__icontains=role)

        return queryset


class StaffDetailView(generics.RetrieveAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class StaffUpdateView(generics.UpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class StaffDeactivateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        try:
            staff = Staff.objects.get(pk=pk)
        except Staff.DoesNotExist:
            return Response(
                {"error": "Staff not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        staff.is_active = False
        staff.save()

        return Response(
            {"message": "Staff deactivated successfully"},
            status=status.HTTP_200_OK
        )


# =========================
# SPECIALIZATION APIs
# =========================

class SpecializationCreateView(generics.CreateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAuthenticated]


class SpecializationListView(generics.ListAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAuthenticated]


class SpecializationUpdateView(generics.UpdateAPIView):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer
    permission_classes = [IsAuthenticated]


# =========================
# DOCTOR APIs
# =========================

class DoctorCreateView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


class DoctorUpdateView(generics.UpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


class DoctorDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            doctor = Doctor.objects.get(pk=pk)
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        doctor.is_active = False
        doctor.save()

        return Response(
            {"message": "Doctor deactivated successfully"},
            status=status.HTTP_200_OK
        )


# =========================
# AUTH APIs
# =========================

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK
        )