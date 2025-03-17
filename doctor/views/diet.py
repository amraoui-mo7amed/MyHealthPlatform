from patient.models import DietRequest
from dashboard.views.generic import BaseDeleteView
from dashboard import mixins
from django.shortcuts import render
from dashboard.decorators import role_or_admin_required
from doctor.models import WEEK_DAYS, MEAL_TYPES
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from doctor.models import Diet, DailyMealPlan, Meal
from datetime import datetime, timedelta
from django.urls import reverse

@role_or_admin_required('DOCTOR')
@csrf_exempt
def create(request, diet_request_pk:int):
    errors = []
    context = {}
    
    if request.method == 'POST':
        try:
            diet_request = DietRequest.objects.get(pk=diet_request_pk)
            diet_request.update_status = 'NONE'
            diet_request.save()
            # Calculate dates
            start_date = datetime.now().date()
            end_date = start_date + timedelta(days=7)
            notes = request.POST.get('notes')
            
            # Create diet with start and end dates
            diet = Diet.objects.create(
                diet_request=diet_request,
                start_date=start_date,
                end_date=end_date,
                notes=notes if notes else None,
            )
            diet.save()
            # If diet was just created, create daily meal plans and meals
            if diet:
                for day, _ in WEEK_DAYS:
                    daily_plan = DailyMealPlan.objects.create(diet=diet, day=day)
                    for meal_type, _ in MEAL_TYPES:
                        Meal.objects.create(daily_plan=daily_plan, meal_type=meal_type)
            
            # Update existing daily meal plans and meals
            for day, _ in WEEK_DAYS:
                daily_plan = DailyMealPlan.objects.get(diet=diet, day=day)
                for meal_type, _ in MEAL_TYPES:
                    meal = Meal.objects.get(daily_plan=daily_plan, meal_type=meal_type)
                    meal.description = request.POST.get(f'{day}_{meal_type}', '')
                    meal.save()
            
            if errors:
                return JsonResponse({
                    'success': False,
                    'errors': errors
                })
            
            return JsonResponse({
                'success': True,
                'redirect_url' : reverse('doctor:diet-request-details', kwargs={'pk': diet_request_pk})
            })
            
        except Exception as e:
            errors.append(str(e))
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
            
    else:
        try:
            diet_request = DietRequest.objects.filter(pk=diet_request_pk).last()
            context['diet_request'] = diet_request
            context['WEEK_DAYS'] = WEEK_DAYS
            context['MEAL_TYPES'] = MEAL_TYPES
            
            
            # Add existing diet to context
            try:
                diet = Diet.objects.filter(diet_request=diet_request).last()
                context['diet'] = diet
            except Diet.DoesNotExist:
                errors.append('No existing diet found')
                
        except DietRequest.DoesNotExist:
            errors.append('Diet request not found')
            return JsonResponse({
                'status': 'error',
                'message': 'Diet request not found',
                'errors': errors
            }, status=404)
        
        return render(request, 'doctor/diet/create.html', context=context)
