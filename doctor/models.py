from django.db import models
from patient import models as p_models

WEEK_DAYS = [
    ('SAT', 'Saturday'),
    ('SUN', 'Sunday'),
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),

]

MEAL_TYPES = [
    ('BREAKFAST', 'Breakfast'),
    ('LUNCH', 'Lunch'),
    ('SNACK', 'Snack'),
    ('DINNER', 'Dinner')
]

class Diet(models.Model):
    diet_request = models.ForeignKey(p_models.DietRequest, on_delete=models.CASCADE, related_name="diet")
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(null=True,blank=True)
    def __str__(self):
        return f"Diet for {self.diet_request.patient}"

class DailyMealPlan(models.Model):
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE, related_name="daily_plans")
    day = models.CharField(max_length=3, choices=WEEK_DAYS)
    
    def __str__(self):
        return f"{self.get_day_display()} Plan for {self.diet}"

class Meal(models.Model):
    daily_plan = models.ForeignKey(DailyMealPlan, on_delete=models.CASCADE, related_name="meals")
    meal_type = models.CharField(max_length=9, choices=MEAL_TYPES)
    description = models.TextField()

    
    def __str__(self):
        return f"{self.get_meal_type_display()} for {self.daily_plan}"
    