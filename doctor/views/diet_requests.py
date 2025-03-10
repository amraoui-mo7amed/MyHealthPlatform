from patient.models import DietRequest, DiabetesAndObesity
from dashboard.views.generic import BaseDeleteView
from dashboard import mixins
from django.shortcuts import render
from dashboard.decorators import role_or_admin_required
from doctor.models import Diet

@role_or_admin_required('DOCTOR')
def diet_request_details(request,pk):
    diet_request = DietRequest.objects.get(pk=pk)
    
    context = {
        'diet_request': diet_request,
        'bmi': diet_request.bmi,
        'diabetes': diet_request.diabetes,
        'obesity': diet_request.obesity,
        'diabetes_and_obesity': diet_request.diabetes_and_obesity
    }
    try :
        diet = Diet.objects.get(diet_request=diet_request)
        context['diet'] = diet
    except Exception as e:
        pass
    return render(request, template_name="doctor/diet/details.html", context=context)

class Delete( mixins.RoleOrAdminMixin ,BaseDeleteView):
    required_role = 'DOCTOR'
    model = DietRequest