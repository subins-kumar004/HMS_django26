from django.urls import path

from .views import (

    RoleListView,
    RoleDetailView,

    StaffCreateView,
    StaffListView,
    StaffDetailView,
    StaffUpdateView,

    SpecializationCreateView,
    SpecializationListView,

    DoctorCreateView,
    DoctorListView,
    DoctorDetailView,
    DoctorUpdateView
)


urlpatterns = [

    # =========================
    # ROLE APIs
    # =========================

    path('roles/', RoleListView.as_view()),
    path('roles/<int:pk>/', RoleDetailView.as_view()),


    # =========================
    # STAFF APIs
    # =========================

    path('staff/create/', StaffCreateView.as_view()),
    path('staff/', StaffListView.as_view()),
    path('staff/<int:pk>/', StaffDetailView.as_view()),
    path('staff/update/<int:pk>/', StaffUpdateView.as_view()),


    # =========================
    # SPECIALIZATION APIs
    # =========================

    path('specializations/create/', SpecializationCreateView.as_view()),
    path('specializations/', SpecializationListView.as_view()),


    # =========================
    # DOCTOR APIs
    # =========================

    path('doctors/create/', DoctorCreateView.as_view()),
    path('doctors/', DoctorListView.as_view()),
    path('doctors/<int:pk>/', DoctorDetailView.as_view()),
    path('doctors/update/<int:pk>/', DoctorUpdateView.as_view()),
]