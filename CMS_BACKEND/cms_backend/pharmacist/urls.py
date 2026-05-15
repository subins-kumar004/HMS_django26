from django.urls import path
from .views import *

urlpatterns = [

    # Medicine Management

    path('medicines/add', add_medicine),  # POST: Add new medicine
    path('medicines', list_medicines),  # GET: Get all medicines
    path('medicines/<int:id>', get_medicine),  # GET: Get medicine by ID
    path('medicines/update/<int:id>', update_medicine),  # PUT: Update medicine
    path('medicines/<int:id>/deactivate', deactivate_medicine),  # PATCH: Deactivate medicine


    # Inventory Management

    path('inventory/medicine/add', add_inventory),  # POST: Add stock
    path('inventory/medicine/update/<int:id>', update_inventory),  # PUT: Update stock
    path('inventory/medicine', list_inventory),  # GET: Get all inventory
    path('inventory/medicine/<int:medicine_id>', get_inventory_by_medicine),  # GET: Get stock by medicine
    path('inventory/medicine/<int:id>/flag-low', flag_low_stock),  # PATCH: Check low stock


    # Dispense Medicine

    path('dispense', dispense_medicine),  # POST: Dispense medicine and reduce stock
]