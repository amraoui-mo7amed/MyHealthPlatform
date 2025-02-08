
from django.urls import path,include
from .views import home

app_name = 'frontend'

urlpatterns = [
    path('', home.home, name='home'),
    path('contact', home.contact, name='contact'),

]

