from django.urls import path
from .views import diet_requests as dr 
from .views import diet
app_name = 'doctor'

urlpatterns = [
    path('diet_request/details/<int:pk>',dr.diet_request_details,name='diet-request-details'),
    path('diet_request/delete/<int:pk>',dr.Delete.as_view(),name='diet-request-delete'),
    # Diet views 
    path('diet/create/<int:diet_request_pk>',diet.create,name='diet-create'),
    
]
