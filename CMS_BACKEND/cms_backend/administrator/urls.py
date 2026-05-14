from django.urls import path

from .views import (

    LoginView,
    LogoutView,

    RoleListView,
    RoleDetailView,

    StaffCreateView,
    StaffListView,
    StaffDetailView,
    StaffUpdateView,
    StaffDeactivateView,

    SpecializationCreateView,
    SpecializationListView,
    SpecializationUpdateView,

    DoctorCreateView,
    DoctorListView,
    DoctorDetailView,
    DoctorUpdateView,
    DoctorDeactivateView,
)


urlpatterns = [

    # =========================
    # AUTH APIs
    # =========================

    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view(), name='logout'),


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

    path(
        'staff/deactivate/<int:pk>/',
        StaffDeactivateView.as_view()
    ),


    # =========================
    # SPECIALIZATION APIs
    # =========================

    path('specializations/create/', SpecializationCreateView.as_view()),
    path('specializations/', SpecializationListView.as_view()),
    path('specializations/<int:pk>/', SpecializationUpdateView.as_view()),


    # =========================
    # DOCTOR APIs
    # =========================

    path('doctors/create/', DoctorCreateView.as_view()),
    path('doctors/', DoctorListView.as_view()),
    path('doctors/<int:pk>/', DoctorDetailView.as_view()),
    path('doctors/update/<int:pk>/', DoctorUpdateView.as_view()),
    path('doctors/deactivate/<int:pk>/', DoctorDeactivateView.as_view()),
]