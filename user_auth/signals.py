from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from user_auth.models import UserProfile, OTP
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import random
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@receiver(post_save,sender=get_user_model())
def create_user_profile(sender,instance,created,**kwargs):
    """
    Signal receiver to create a UserProfile when a new superuser is created.
    
    Args:
        sender: The model class sending the signal
        instance: The actual instance being saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    # Check if a new user is created and if it's a superuser
    if created and instance.is_superuser:
        print('Creating admin profile...')
        # Create a UserProfile with default admin settings
        UserProfile.objects.get_or_create(
            user=instance,  # Link to the user instance
            image='images/user-teal.png',  # Default admin image
            notifications_count=0,  # Initialize notification count
            role='ADMIN',  # Set role as ADMIN
            email_confirmed=True,  # Mark email as confirmed
        )

@receiver(post_save, sender=get_user_model())
def send_otp_on_user_creation(sender, instance, created, **kwargs):
    """
    Signal receiver to generate and send OTP when a new user is registered.
    """
    if created and not instance.is_superuser:
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        expires_at = timezone.now() + timedelta(minutes=15)

        # Render the email template with context
        email_body = render_to_string('emails/email_activation.html', {
            'user': instance,
            'activation_link': f'http://localhost:8000/activate-email/?token={otp_code}',
            'expiration_hours': 0.25  # 15 minutes in hours
        })
                
        otp = OTP.objects.create(
            user=instance,
            code=otp_code,
            expires_at=expires_at
        )
        otp.save()
        print(otp.user,otp.code)
        send_mail(
            'Account Activation',  # Email subject
            strip_tags(email_body),  # Plain text version
            'myhealthypartner0@gmail.com',
            [instance.email],
            html_message=email_body  # HTML version
        )
            