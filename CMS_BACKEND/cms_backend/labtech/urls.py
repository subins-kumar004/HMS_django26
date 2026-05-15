from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # LAB TEST MANAGEMENT
    # =========================

    path(
        'labtests',
        views.lab_tests
    ),

    path(
        'labtests/<int:labTestId>',
        views.lab_test_detail
    ),

    path(
        'labtests/<int:labTestId>/deactivate',
        views.deactivate_lab_test
    ),

    # =========================
    # LAB TEST PRESCRIPTION
    # =========================

    path(
        'labtests/prescription/add',
        views.add_lab_test_prescription
    ),

    path(
        'labtests/prescription/<int:labTestPrescriptionId>/deactivate',
        views.deactivate_lab_test_prescription
    ),

    # =========================
    # LAB TEST RESULTS
    # =========================

    path(
        'labtests/results',
        views.get_results_by_date_range
    ),

    path(
        'labtests/results/appointment/<int:appointmentId>',
        views.get_results_by_appointment
    ),

    path(
        'labtests/results/<int:labTestPrescriptionId>',
        views.record_lab_result
    ),
]