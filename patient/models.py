from typing import Iterable
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# Define choices for illnesses that can be associated with BMI records
ILLNESS_CHOICES = [
    ('DIABETES', 'Diabetes'),
    ('COLON', 'Colon'),
    ('OBESITY', 'Obesity'),
]

class BMI(models.Model):
    # One-to-one relationship with Patient model, deleting BMI if patient is deleted
    patient = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='bmi_records')
    # Height field in meters with validation for realistic human height range
    height = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(3.0)])  # in meters
    # Weight field in kilograms with validation for realistic human weight range
    weight = models.FloatField(validators=[MinValueValidator(2.0), MaxValueValidator(600.0)])  # in kg
    # Automatically set to current date/time when record is created
    date_recorded = models.DateTimeField(auto_now_add=True)
    # Changed from CharField to ManyToManyField to allow multiple selections
    sickness = models.ManyToManyField('Illness')

    @property
    def value(self):
        """Calculate BMI using the formula: weight (kg) / (height (m) ^ 2)"""
        if self.height > 0:
            # Return BMI rounded to one decimal place
            return round(self.weight / (self.height ** 2), 1)
        return None

    def __str__(self):
        # String representation of the BMI record
        return f"BMI for {self.patient}: {self.value}"

    class Meta:
        # Customize the display name in admin interface
        verbose_name = "BMI Record"
        verbose_name_plural = "BMI Records"
        # Order records by most recent date first
        ordering = ['-date_recorded']

    def save(self, *args, **kwargs):
        # Custom save method to enforce validation rules
        if not self.pk:  # Only for new records
            try:
                # Check if the associated user is a patient
                if self.patient.profile.role == 'PATIENT':
                    super().save(*args, **kwargs)
                else:
                    raise ValidationError("Only patients can have BMI records")
            except AttributeError:
                raise ValidationError("Invalid patient profile")
        else:
            # For existing records, just save normally
            super().save(*args, **kwargs)

# Add new Illness model to store illness choices
class Illness(models.Model):
    name = models.CharField(max_length=20, choices=ILLNESS_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()
