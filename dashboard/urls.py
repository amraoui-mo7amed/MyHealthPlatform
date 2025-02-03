
from django.urls import path,include
from .views import dashbaord, user, notifications
app_name = 'dash'

urlpatterns = [

    path('home/',dashbaord.home,name='home'),
    # User
    path('users/', user.list_users, name='list_users'),
    path('user/',user.UserProfile,name='user-profile'),
    path('users/details/<int:pk>',user.userDetails,name='user-details'),
    path('users/edit/',user.EditUserProfile,name='edit-user-profile'),
    path('users/delete/<int:pk>', user.delete_user, name='delete_user'),
    path('users/approve-user/<int:pk>/', user.approve_user, name='approve_user'),
    path('pending/', user.pending_view, name='pending'),
    # notifications
    path('reset-notifications/',notifications.reset_notifications_count,name='reset-notifications'),
]

