from django.shortcuts import render, redirect
from patient.decorators import patient_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from patient.models import BMI, ILLNESS_CHOICES, Diabetes, Obesity, Illness, DietRequest, DiabetesAndObesity
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from doctor import models as dc_models
from dashboard.models import Notifications
from django.contrib import messages
import logging
from patient import utils

UserModel = get_user_model()
logger = logging.getLogger(__name__)


@patient_required
def request_a_diet(request):
    context = {}
    try:
            diet_request = DietRequest.objects.get(patient=request.user)
            context['diet_request'] = diet_request
            if diet_request.request_verified == False:
                return redirect('dash:pending')
    except Exception as e:
            pass
    return render(request,'patient/diet/request_a_diet.html')

@patient_required
def BMICalculator(request):
    context = {}  # Initialize context at the start of the function

    if request.method == 'POST':
        errors = []
        try:
            # Get current authenticated patient
            patient = request.user
            # get height and weight
            height = request.POST.get('height')
            weight = request.POST.get('weight')
            illnesses = request.POST.getlist('illnesses')
            
            diet_type = request.POST.get('diet_type')

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
                if illness == 'diabietesandobesity':
                    print('diabetesandobesity is present in user choices')
                if illness.upper() not in valid_illnesses:
                    errors.append(_('Ilness must be Diabetes or Obesity or both'))
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
                    if instance:
                        print(f'ilness instance with name {instance} exist')
                    else:
                        print('doesnt exist')
                except Illness.DoesNotExist:
                    errors.append(f'ilnness with name {illness_name} doesnt exist' )
                    continue
            # Create or update BMI record
            bmi = BMI.objects.create(
                patient=patient,
                height=height_float,
                weight=weight_float,
                bmi_value=bmi_value
            )
            bmi.save()
            print(f'User ilnesses: {illness_instances}')

            # Clear existing illness records if not selected
            # selected_illnesses = [illness.upper() for illness in illnesses]
            # if 'DIABETES' not in selected_illnesses:
            #     Diabetes.objects.filter(bmi=bmi).delete()
            # if 'OBESITY' not in selected_illnesses:
            #     Obesity.objects.filter(bmi=bmi).delete()
            # if 'DIABETESANDOBESITY' not in selected_illnesses:
            #     DiabetesAndObesity.objects.filter(bmi=bmi).delete()

            if illness_instances:
                # bmi.sickness.clear()  # Clear existing relations
                bmi.sickness.add(*illness_instances)  # Add new relations
                bmi.save()

            for instance in illness_instances:
                print(instance.name)
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
                        diabetes_instance = Diabetes.objects.create(
                            patient=patient,
                            glucose_type=glucose_type,
                            fasting_glucose=float(fasting_glucose),
                            hba1c=float(hba1c),
                            cholesterol=int(cholesterol)
                        )
                        diabetes_instance.save()
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
                            'patient': patient,
                            'glucose': float(glucose),
                            'hdl': float(hdl),
                            'ldl': float(ldl),
                            'triglycerides': float(triglycerides),
                            'cholesterol': int(cholesterol),
                            'ac_uric': int(ac_uric)
                        }
                        obesity_instance = Obesity.objects.create(**obesity_data)
                        obesity_instance.save()
                if instance.name == 'diabetesandobesity'.upper():
                    print('diabetesandobesity')
                    db_glucose = request.POST.get('db_glucose')
                    db_h1bc = request.POST.get('db_hb1ac')
                    db_hdl = request.POST.get('db_hdl')
                    db_ldl = request.POST.get('db_ldl')
                    db_triglycerides = request.POST.get('db_triglycerides')
                    db_cholesterol = request.POST.get('db_cholesterol')
                    db_ac_uric = request.POST.get('db_ac_uric')
                    db_fns = request.POST.get('db_fns')
                    db_crp = request.POST.get('db_crp')
                    db_vitamin_d = request.POST.get('db_vitamin_d')
                    db_b12 = request.POST.get('db_b12')
                    db_magnesium = request.POST.get('db_magnesium')

                    if not db_glucose:
                        errors.append(_('Glucose is required'))
                    if not db_h1bc:
                        errors.append(_('HbA1c is required'))
                    if not db_hdl:
                        errors.append(_('HDL is required'))
                    if not db_ldl:
                        errors.append(_('LDL is required'))
                    if not db_triglycerides:
                        errors.append(_('Triglycerides is required'))
                    if not db_cholesterol:
                        errors.append(_('Cholesterol is required'))
                    if not db_ac_uric:
                        errors.append(_('AC Uric is required'))
                    if not db_fns:
                        errors.append(_('FNS is required'))
                    if not db_crp:
                        errors.append(_('CRP is required'))
                    if not db_b12:
                        errors.append(_('B12 is required'))
                    if not db_magnesium:
                        errors.append(_('Magnesium is required'))
                    if not db_vitamin_d:
                        errors.append(_('Vitamine D analyse is required'))

                    if not errors:
                        try:
                            if instance.name == 'diabetesandobesity'.upper():
                                diabetes_and_obesity_data = {
                                    'patient': patient,
                                    'glucose': float(db_glucose),
                                    'hb1ac': float(db_h1bc),
                                    'hdl': float(db_hdl),
                                    'ldl': float(db_ldl),
                                    'triglycerides': float(db_triglycerides),
                                    'cholesterol': int(db_cholesterol),
                                    'ac_uric': int(db_ac_uric),
                                    'fns': float(db_fns),
                                    'crp': float(db_crp),
                                    'b12': float(db_b12),
                                    'magnesium': float(db_magnesium),
           
                                }
                                print(diabetes_and_obesity_data)
                                diabetes_and_obesity_instance = DiabetesAndObesity.objects.create(
                                    **diabetes_and_obesity_data
                                )
                                print('created ')
                        except Exception as e:
                            errors.append(_('An error occurred while saving your data. Please try again.'))
                            logger.error(f"Error saving diet data: {str(e)}")

                if errors:
                    for error in errors:
                        messages.error(request, error)
                    return render(request, 'patient/diet/bmi.html', context)


            # Get form data with error handling
            between_meals = request.POST.get('between_meals')
            sweets = request.POST.get('sweets')
            fast_food = request.POST.get('fast_food')
            enough_water = request.POST.get('enough_water')
            food_allergy = request.POST.get('food_allergy')
            allergy_details = request.POST.get('allergy_details')
            smoke = request.POST.get('smoke')
            weight_loss = request.POST.get('weight_loss')
            depression_stress = request.POST.get('depression_stress')
            medication = request.POST.get('medication')
            medication_details = request.POST.get('medication_details')
            last_meal_time = request.POST.get('last_meal_time')
            walking = request.POST.get('walking')
            sleep = request.POST.get('sleep')
            meals_per_day = request.POST.get('meals_per_day')
            if not meals_per_day:
                errors.append(_('Meals per day is required'))
            if not between_meals:
                errors.append(_('Between meals is required'))
            if not sweets:
                errors.append(_('Sweets is required'))
            if not fast_food:
                errors.append(_('Fast food is required'))
            if not enough_water:
                errors.append(_('Enough water is required'))
            if not food_allergy:
                errors.append(_('Food allergy is required'))
            if not smoke:
                errors.append(_('Smoke is required'))
            if not weight_loss:
                errors.append(_("weight loss is required"))
            if not depression_stress:
                errors.append(_('Depression stress is required'))
            if not medication:
                errors.append(_('Medication is required'))
            if not last_meal_time:
                errors.append(_('Last meal time is required'))
            if not walking:
                errors.append(_('Walking is required'))
            if not sleep:
                errors.append(_('Sleep is required'))

            if not meals_per_day:
                errors.append('Meals per day is required')
            if not between_meals:
                errors.append('Between meals selection is required')
            if not sweets:
                errors.append('Sweets selection is required')
            
            if errors:
                return JsonResponse({'status': 'error', 'errors': errors}, status=400)
                
            diet_request_instance = DietRequest.objects.create(
                patient=patient,
                bmi=bmi,
                diabetes=diabetes_instance if 'diabetes_instance' in locals() else None,
                obesity=obesity_instance if 'obesity_instance' in locals() else None,
                diabetes_and_obesity=diabetes_and_obesity_instance if 'diabetes_and_obesity_instance' in locals() else None,
                meals_per_day=int(meals_per_day),
                between_meals=between_meals == 'yes',
                sweets=sweets == 'yes',
                fast_food=fast_food == 'yes',
                enough_water=enough_water == 'yes',
                food_allergy=food_allergy == 'yes',
                allergy_details=allergy_details if food_allergy == 'yes' else None,
                smoke=smoke == 'yes',
                weight_loss=weight_loss == 'yes',
                depression_stress=depression_stress == 'yes',
                medication=medication == 'yes',
                medication_details=medication_details if medication == 'yes' else None,
                last_meal_time=last_meal_time,
                walking=walking == 'yes',
                sleep=sleep == 'yes',
                update_status = 'PENDING'
            )
            diet_request_instance.save()
            
            # get the diet diet errors :
            if diet_type not in ['ai','doctor']:
                errors.append(_('Diet type is required'))

            if errors:
                return JsonResponse({'success':False,'errors':errors})
            
            # handle the diet type selection
            if diet_type == 'ai':
                # Call the AI processing function
                print('user chosed ai')
                ai_response = utils.process_ai_diet_request(
                    patient=patient,
                    bmi=bmi,
                    diabetes=diabetes_instance if 'diabetes_instance' in locals() else None,
                    obesity=obesity_instance if 'obesity_instance' in locals() else None,
                    diabetes_and_obesity=diabetes_and_obesity_instance if 'diabetes_and_obesity_instance' in locals() else None,
                    provider='mistral'
                )

                if ai_response:
                    # Save the AI-generated diet plan to the database or display it to the user

                    diet_plan = ai_response
                    utils.createDietPlan(diet_plan,diet_request_instance)
                    return JsonResponse({
                        'success': True, 
                        'type' : 'ai_generated',
                        'message' : diet_plan,
                    })
                else:
                    errors.append(ai_response.get("error"))
            elif diet_type == 'doctor':
                doctors = UserModel.objects.filter(profile__role='DOCTOR')
                for dc in doctors:
                    Notifications.objects.create(
                        user = dc, 
                        title='A new Diet request has been created',
                        text=f'New diet request created, view it at <a href="{reverse_lazy("doctor:diet-request-details", kwargs={"pk": diet_request_instance.pk})}">View Request</a>'
                    )
                    dc.profile.notifications_count += 1
                    dc.profile.save()
                return JsonResponse({
                    'success' : True,
                    'type' : 'doctor_generated',
                    'messages': _('BMI has been created '),
                    'redirect_url' : reverse_lazy('dash:pending')
                })

        except Exception as e:
            return JsonResponse({'success':False,'errors':[_(f'{str(e)}')]})
    
    else:
        try:
            diet_request = DietRequest.objects.filter(patient=request.user).last()
            context['diet_request'] = diet_request            
            try:
                diet = dc_models.Diet.objects.get(diet_request=diet_request)
            except Exception as e:
                pass
        except Exception:
            pass
        return render(request,'patient/diet/bmi.html',context=context)
    
def diet_details(request,pk):
    diet = dc_models.Diet.objects.get(pk=pk)
    context = {
        'diet' : diet
    }
    return render(request,'patient/diet/diet_details.html',context=context)

@patient_required 
def reset_diet_request_status(request,pk):
    errors = []
    if request.method == 'POST':
        try :

            return JsonResponse({
                'success':True,
                'message' : _('Diet status has been updated, redirecting...'),
                'redirect_url' : reverse_lazy('patient:bmi_calculator')
            })
        except DietRequest.DoesNotExist:
            errors.append(_('Diet request doesnt exist'))
        except Exception as e:
            errors.append(str(e))
        if errors:
            return JsonResponse({
                'success':False,
                'errors' : errors
            })
@patient_required
def diet_history(request):
    diets = dc_models.Diet.objects.filter(diet_request__patient=request.user)
    context = {
        'diets': diets
    }
    return render(request, 'patient/diet/diet_history.html', context=context)


