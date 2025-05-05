
from django.urls import path,include
from .views import dashbaord, user, notifications, contact, nutrition
app_name = 'dash'

urlpatterns = [

    path('home/',dashbaord.home,name='home'),
    # charts 
    path('api/chart-data/', dashbaord.get_chart_data, name='chart_data'),

    # User
    path('users/', user.list_users, name='list_users'),
    path('user/',user.UserProfile,name='user-profile'),
    path('users/details/<int:pk>',user.userDetails,name='user-details'),
    path('users/edit/',user.EditUserProfile,name='edit-user-profile'),
    path('users/delete/<int:pk>', user.delete_user, name='delete_user'),
    path('users/approve-user/<int:pk>/', user.approve_user, name='approve_user'),
    path('pending/', user.pending_view, name='pending'),
    # Contacts 
    path('contacts/', contact.contact_list_view, name='contacts-list'),
    # nutrition 
    path('nutrition/', nutrition.list, name='nutritions-list'),

    # notifications
    path('reset-notifications/',notifications.reset_notifications_count,name='reset-notifications'),

]

