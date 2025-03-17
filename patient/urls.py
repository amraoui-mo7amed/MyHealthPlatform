from django.urls import path
from .views import diet

app_name = 'patient'

urlpatterns = [
    # Diet views
    path('request-a-diet', diet.request_a_diet , name='request_a_diet'),
    path('bmi-calculator', diet.BMICalculator , name='bmi_calculator'),
    path('reset_diet_request_status/<int:pk>', diet.reset_diet_request_status , name='reset_diet_request_status'),
    path('diet-history', diet.diet_history , name='diet_history'),
    
    path('diet_details/<int:pk>', diet.diet_details , name='diet_details'),
    

]
