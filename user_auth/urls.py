from django.urls import path,include
from . import views

app_name = 'user_auth'

urlpatterns = [
    # auth 
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('register/', views.register_view, name='register'),
    path('activate-email/', views.activate_email, name='activate_email'),
    path('password-reset-confirmation/<str:token>/', views.password_reset_confirmation, name='password_reset_confirm'),


]
