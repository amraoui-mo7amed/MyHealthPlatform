from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from user_auth.models import UserProfile

@receiver(post_save,sender=get_user_model())
def create_user_profile(sender,instance,created,**kwargs):
    if created and instance.is_superuser:
        print('Creating admin profile...')
        UserProfile.objects.get_or_create(
            user=instance,
            image='images/user-teal.png',
            notifications_count=0,
            role='ADMIN'  
        )