from django.shortcuts import render
from patient.decorators import patient_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from patient.models import BMI, ILLNESS_CHOICES, Diabetes, Obesity, Illness, DietRequest
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from doctor import models as dc_models

UserModel = get_user_model()


@patient_required
def request_a_diet(request):
    return render(request,'patient/diet/request_a_diet.html')

@patient_required
def BMICalculator(request):

    if request.method == 'POST':
        errors = []
        try:
            # Get current authenticated patient
            patient = request.user
            # get height and weight
            height = request.POST.get('height')
            weight = request.POST.get('weight')
            illnesses = request.POST.getlist('illnesses')
            # Validate height and weight
            if not height or not height.strip():
                errors.append(_('height is required'))
            else:
                try:
                    height = float(height)
                except ValueError:
                    errors.append(_('height must be a number'))
            
            if not weight or not weight.strip():
                errors.append(_('weight is required'))
            else:
                try:
                    weight = float(weight)
                except ValueError:
                    errors.append(_('weight must be a number'))
            
            if not illnesses:
                errors.append(_('Please select your illness'))
            
            # Check if all selected illnesses are valid
            valid_illnesses = [choice[0] for choice in ILLNESS_CHOICES]
            for illness in illnesses:
                if illness.upper() not in valid_illnesses:
                    errors.append(_('Ilness must be Diabetes or Obesity'))
                    break
            
            # Calculate BMI
            height_float = float(height)
            weight_float = float(weight)
            # Convert height from cm to meters for BMI calculation
            bmi_value = round((weight_float / ((height_float / 100) ** 2)), 2) if height_float > 0 else None
                        # Get illness instances using the model's choices structure
            illness_instances = []
            for illness_name in illnesses:
                try:
                    # Get the illness instance using the uppercase name
                    instance = Illness.objects.get(name=illness_name.upper())
                    illness_instances.append(instance)
                except Illness.DoesNotExist:
                    # Handle case where illness doesn't exist
                    continue
            
            # Create or update BMI record
            bmi, created = BMI.objects.update_or_create(
                patient=patient,
                defaults={
                    'height': height_float,
                    'weight': weight_float,
                    'bmi_value': bmi_value
                }
            )
            if illness_instances:
                bmi.sickness.clear()  # Clear existing relations
                bmi.sickness.add(*illness_instances)  # Add new relations
                bmi.save()


            for instance in illness_instances:
                if instance.name == 'diabetes'.upper():
                    glucose_type = request.POST.get('glucose_type')
                    fasting_glucose = request.POST.get('fasting_glucose')
                    hba1c = request.POST.get('hba1c')
                    cholesterol = request.POST.get('diabetes_cholesterol')
                    
                    if not glucose_type:
                        errors.append(_('Glucose type is required'))
                    if not fasting_glucose:
                        errors.append(_('Fasting glucose is required'))
                    if not hba1c:
                        errors.append(_('HbA1c is required'))
                    if not cholesterol:
                        errors.append(_('Cholesterol is required'))
                        
                    if not errors:
                        diabetes_data = {
                            'bmi': bmi,
                            'glucose_type': glucose_type,
                            'fasting_glucose': float(fasting_glucose),
                            'hba1c': float(hba1c),
                            'cholesterol': int(cholesterol)
                        }
                        Diabetes.objects.update_or_create(bmi=bmi, defaults=diabetes_data)
                        print('good work')
                    
                if instance.name == 'OBESITY'.upper():
                    glucose = request.POST.get('obesity_glucose')
                    hdl = request.POST.get('hdl')
                    ldl = request.POST.get('ldl')
                    triglycerides = request.POST.get('triglycerides')
                    cholesterol = request.POST.get('obesity_cholesterol')
                    ac_uric = request.POST.get('ac_uric')
                    
                    if not glucose:
                        errors.append(_('Glucose is required'))
                    if not hdl:
                        errors.append(_('HDL is required'))
                    if not ldl:
                        errors.append(_('LDL is required'))
                    if not triglycerides:
                        errors.append(_('Triglycerides is required'))
                    if not cholesterol:
                        errors.append(_('Cholesterol is required'))
                    if not ac_uric:
                        errors.append(_('AC Uric is required'))
                        
                    if not errors:
                        obesity_data = {
                            'bmi': bmi,
                            'glucose': float(glucose),
                            'hdl': float(hdl),
                            'ldl': float(ldl),
                            'triglycerides': float(triglycerides),
                            'cholesterol': int(cholesterol),
                            'ac_uric': int(ac_uric)
                        }
                        Obesity.objects.update_or_create(bmi=bmi, defaults=obesity_data)
            
            # Create DietRequest after all instances are created
            diabetes_instance = Diabetes.objects.filter(bmi=bmi).first()
            obesity_instance = Obesity.objects.filter(bmi=bmi).first()
            
            DietRequest.objects.update_or_create(
                patient=patient,
                defaults={
                    'bmi': bmi,
                    'diabetes': diabetes_instance,
                    'obesity': obesity_instance,
                    'request_verified': False
                }
            )
            
            if errors:
                return JsonResponse({'success':False,'errors':errors})
            
            return JsonResponse({
                'success' : True,
                'messages': _('BMI has been created '),
                'redirect_url' : reverse_lazy('dash:pending')
            })

        except Exception as e:
            return JsonResponse({'success':False,'errors':[_(f'{str(e)}')]})
    
    else:

        return render(request,'patient/diet/bmi.html')
    
@patient_required
def diet_details(request,diet_request_pk):
    diet_request = DietRequest.objects.get(pk=diet_request_pk)
    diet = dc_models.Diet.objects.get(diet_request=diet_request)
    context = {
        'diet' : diet
    }
    return render(request,'patient/diet/diet_details.html',context=context)