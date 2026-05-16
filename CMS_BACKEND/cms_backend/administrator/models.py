from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# ROLE MODEL
# =========================


class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name


# =========================
# STAFF / USER MODEL
# =========================


class Staff(AbstractUser):
    contact = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    emp_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


# =========================
# SPECIALIZATION
# =========================


class Specialization(models.Model):
    specialization_name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.specialization_name


# =========================
# DOCTOR
# =========================


class Doctor(models.Model):

    staff = models.OneToOneField(
        Staff,
        on_delete=models.CASCADE
    )

    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.SET_NULL,
        null=True
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.staff.get_full_name()


# =========================
# PATIENT
# =========================


class Patient(models.Model):

    patient_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    patient_name = models.CharField(max_length=100)

    contact = models.CharField(max_length=15)

    age = models.IntegerField()

    gender = models.CharField(max_length=10)

    address = models.TextField()

    membership = models.BooleanField(default=False)

    membership_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        super().save(*args, **kwargs)

        update_fields = []

        if is_new and not self.patient_id:

            self.patient_id = f"PAT-{self.pk:04d}"

            update_fields.append('patient_id')

        if self.membership and not self.membership_id:

            self.membership_id = f"MEM-{self.pk:04d}"

            update_fields.append('membership_id')

        elif not self.membership and self.membership_id:

            self.membership_id = None

            update_fields.append('membership_id')

        if update_fields:

            kwargs.pop('force_insert', None)

            kwargs.pop('force_update', None)

            super().save(
                update_fields=update_fields,
                *args,
                **kwargs
            )

    def __str__(self):
        return f"{self.patient_id} - {self.patient_name}"


# =========================
# APPOINTMENT
# =========================


class Appointment(models.Model):

    STATUS_CHOICES = (
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    token_number = models.IntegerField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Scheduled"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.token_number:

            last_appointment = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date
            ).order_by('token_number').last()

            if last_appointment and last_appointment.token_number:

                self.token_number = (
                    last_appointment.token_number + 1
                )

            else:

                self.token_number = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient.patient_name} - {self.doctor}"


# =========================
# CONSULTATION
# =========================


class Consultation(models.Model):

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    symptoms = models.TextField()

    diagnosis = models.TextField()

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation - {self.appointment.id}"


# =========================
# MEDICINE
# =========================


class Medicine(models.Model):

    medicine_name = models.CharField(max_length=100)

    category = models.CharField(max_length=100)

    manufacturing_date = models.DateField()

    expiry_date = models.DateField()

    unit = models.CharField(max_length=50)

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.medicine_name


# =========================
# MEDICINE STOCK
# =========================


class MedicineStock(models.Model):

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()

    reorder_level = models.IntegerField(default=10)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.medicine.medicine_name} - "
            f"{self.quantity}"
        )


# =========================
# MEDICINE PRESCRIPTION
# =========================


class MedicinePrescription(models.Model):

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE
    )

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE
    )

    dosage = models.CharField(max_length=100)

    frequency = models.CharField(max_length=100)

    duration = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.appointment.id} - "
            f"{self.medicine.medicine_name}"
        )


# =========================
# LAB TEST
# =========================


class LabTest(models.Model):

    test_name = models.CharField(max_length=100)

    category = models.CharField(max_length=100)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reference_range = models.CharField(max_length=100)

    sample_type = models.CharField(max_length=100)

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.test_name


# =========================
# LAB TEST PRESCRIPTION
# =========================


class LabTestPrescription(models.Model):

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE
    )

    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE
    )

    instructions = models.TextField(
        blank=True,
        null=True
    )

    test_value = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.appointment.id} - "
            f"{self.lab_test.test_name}"
        )


# =========================
# BILL
# =========================


class Bill(models.Model):

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE
    )

    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    additional_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill - {self.appointment.id}"