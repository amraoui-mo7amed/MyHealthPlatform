from django.urls import path
from .views import diet

app_name = 'patient'

urlpatterns = [
    # Diet views
    path('request-a-diet', diet.request_a_diet , name='request_a_diet'),
    path('bmi-calculator', diet.BMICalculator , name='bmi_calculator'),
    path('diet_details/<int:diet_request_pk>', diet.diet_details , name='diet_details'),
    

]
