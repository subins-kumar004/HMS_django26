from django.contrib import admin

from .models import (
    Role,
    Staff,
    Specialization,
    Doctor,
    Patient,
    Appointment,
    Consultation,
    Medicine,
    MedicineStock,
    MedicinePrescription,
    LabTest,
    LabTestPrescription,
    Bill
)

admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(Specialization)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Consultation)
admin.site.register(Medicine)
admin.site.register(MedicineStock)
admin.site.register(MedicinePrescription)
admin.site.register(LabTest)
admin.site.register(LabTestPrescription)
admin.site.register(Bill)