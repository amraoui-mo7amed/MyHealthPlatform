from typing import Iterable
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# Define choices for illnesses that can be associated with BMI records
ILLNESS_CHOICES = [
    ('DIABETES', 'Diabetes'),
    ('OBESITY', 'Obesity'),
    ('DIABETESANDOBESITY', 'Diabetes and Obesity'),
    
]


# Add new Illness model to store illness choices
class Illness(models.Model):
    name = models.CharField(max_length=20, choices=ILLNESS_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()

class BMI(models.Model):
    # One-to-one relationship with Patient model, deleting BMI if patient is deleted
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='bmi_records')
    # Height field in meters with validation for realistic human height range
    height = models.FloatField(validators=[MinValueValidator(0.5), MaxValueValidator(3.0)])  # in meters
    # Weight field in kilograms with validation for realistic human weight range
    weight = models.FloatField(validators=[MinValueValidator(2.0), MaxValueValidator(600.0)])  # in kg
    # Automatically set to current date/time when record is created
    date_recorded = models.DateTimeField(auto_now_add=True)
    # Changed from CharField to ManyToManyField to allow multiple selections
    sickness = models.ManyToManyField(Illness)
    bmi_value = models.FloatField(null=True, blank=True)  # New field to store calculated BMI


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

class Diabetes(models.Model):
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='diabetes')
    glucose_type = models.CharField(max_length=10, choices=[('mg/dl', 'mg/dl'), ('mmol/l', 'mmol/l')])
    fasting_glucose = models.FloatField()
    hba1c = models.FloatField()
    cholesterol = models.IntegerField()

    def __str__(self):
        return f"Diabetes data for {self.bmi.patient}"

    class Meta:
        verbose_name = "Diabetes Record"
        verbose_name_plural = "Diabetes Records"

class Obesity(models.Model):
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='obesity')
    glucose = models.FloatField()
    hdl = models.FloatField()
    ldl = models.FloatField()
    triglycerides = models.FloatField()
    cholesterol = models.IntegerField()
    ac_uric = models.IntegerField()

    def __str__(self):
        return f"Obesity data for {self.bmi.patient}"

    class Meta:
        verbose_name = "Obesity Record"
        verbose_name_plural = "Obesity Records"



class DiabetesAndObesity(models.Model):
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='diabetes_and_obesity')
    glucose = models.FloatField()
    hb1ac = models.FloatField()
    hdl = models.FloatField()
    ldl = models.FloatField()
    triglycerides = models.FloatField()
    cholesterol = models.IntegerField()
    ac_uric = models.IntegerField()
    fns = models.FloatField()
    crp = models.FloatField()
    vitamin_d = models.FloatField()
    b12 = models.FloatField()
    magnesium = models.FloatField()

    def __str__(self):
        return f"Diabetes and Obesity data for {self.bmi.patient}"

    class Meta:
        verbose_name = "Diabetes and Obesity Record"
        verbose_name_plural = "Diabetes and Obesity Records"



class DietRequest(models.Model):
    patient = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='diet_request')
    bmi = models.OneToOneField(BMI, on_delete=models.CASCADE)
    diabetes = models.OneToOneField(Diabetes, on_delete=models.CASCADE, null=True, blank=True)
    obesity = models.OneToOneField(Obesity, on_delete=models.CASCADE, null=True, blank=True)
    diabetes_and_obesity = models.OneToOneField(DiabetesAndObesity, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    meals_per_day = models.PositiveSmallIntegerField(choices=[(1, 'Once a day'), (2, 'Twice a day'), (3, 'Three times a day'), (4, 'Four times a day')], default=1)
    between_meals = models.BooleanField(default=False)
    sweets = models.BooleanField(default=False)
    
    # New field to track update status
    update_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('REVISED', 'REVISED'),
            ('NONE', 'NONE')
        ],
        default='NONE'
    )
    
    fast_food = models.BooleanField(default=False)
    enough_water = models.BooleanField(default=False)
    food_allergy = models.BooleanField(default=False)
    allergy_details = models.CharField(max_length=255, blank=True, null=True)
    smoke = models.BooleanField(default=False)
    weight_loss = models.BooleanField(default=False)
    depression_stress = models.BooleanField(default=False)
    medication = models.BooleanField(default=False)
    medication_details = models.CharField(max_length=255, blank=True, null=True)
    last_meal_time = models.TimeField()
    walking = models.BooleanField(default=False)
    sleep = models.BooleanField(default=False)
