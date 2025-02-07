from django.shortcuts import render
from patient.decorators import patient_required

@patient_required
def request_a_diet(request):
    return render(request,'patient/diet/request_a_diet.html')

@patient_required
def BMICalculator(request):
    return render(request,'patient/diet/bmi.html')