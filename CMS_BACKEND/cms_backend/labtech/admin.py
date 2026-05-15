from django.contrib import admin

from .models import (
    LabTest,
    LabTestPrescription
)


admin.site.register(LabTest)
admin.site.register(LabTestPrescription)