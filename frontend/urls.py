from django.urls import path,include
from .views import home, openrouter

app_name = 'frontend'

urlpatterns = [
    path('', home.home, name='home'),
    path('contact', home.contact, name='contact'),
    path('api/chat-token/', openrouter.get_chat_token, name='chat_token'),
]

