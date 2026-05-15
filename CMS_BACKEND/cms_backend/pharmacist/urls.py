from django.urls import path
from .views import *

urlpatterns = [
    # Medicine Management
    path('medicines', manage_medicines),  # GET, POST
    path('medicines/<int:id>', medicine_detail),  # GET, PUT
    path('medicines/<int:id>/deactivate', deactivate_medicine),  # PATCH

    # Inventory Management
    path('inventory/medicine', manage_inventory),  # GET all, POST
    path('inventory/medicine/<int:medicine_id>', get_inventory_by_medicine),  # GET
    path('inventory/medicine/stock/<int:id>', update_inventory_stock),  # PUT
    path('inventory/medicine/stock/<int:id>/flag-low', flag_low_stock),  # PATCH

    # Dispense Medicine
    path('prescriptions/patient/<int:patient_id>', get_patient_prescriptions),
    path('dispense', dispense_medicine),
]