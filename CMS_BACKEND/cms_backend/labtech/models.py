from django.db import models


class LabTest(models.Model):

    CATEGORY_CHOICES = (
        ('Blood', 'Blood'),
        ('Urine', 'Urine'),
        ('Scan', 'Scan'),
        ('Other', 'Other'),
    )

    SAMPLE_CHOICES = (
        ('Blood', 'Blood'),
        ('Urine', 'Urine'),
        ('Saliva', 'Saliva'),
        ('Other', 'Other'),
    )

    test_name = models.CharField(max_length=100)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reference_ranges = models.TextField()

    sample_type = models.CharField(
        max_length=50,
        choices=SAMPLE_CHOICES
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.test_name


class LabTestPrescription(models.Model):

    appointment_id = models.IntegerField()

    patient_name = models.CharField(max_length=100)

    doctor_name = models.CharField(max_length=100)

    lab_test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE
    )

    lab_test_value = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    remarks = models.TextField(
        null=True,
        blank=True
    )

    prescribed_date = models.DateField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.patient_name