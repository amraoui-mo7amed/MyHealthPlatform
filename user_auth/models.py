from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin'),
    ]
    
    birthdate = models.DateField(verbose_name='Birthdate',default='1999-01-01')
    user = models.OneToOneField(UserModel,on_delete=models.CASCADE,related_name='profile')
    image = models.ImageField(max_length=1200,upload_to='user/',verbose_name='User Image')
    notifications_count = models.IntegerField(default=0,verbose_name='User Notifications')
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='PATIENT', verbose_name='User Role')
    is_approved = models.BooleanField(default=True, verbose_name='Is Approved')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        if not self.pk and self.role == 'DOCTOR':
            self.is_approved = False
        super().save(*args, **kwargs)

