from django.db import models
from django.contrib.auth.models import User

class Notifications(models.Model):
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    title        = models.TextField(max_length=1200,verbose_name='Notfication Title')
    text        = models.TextField(max_length=1200,verbose_name='Notification Content')
    create_at   = models.DateTimeField(auto_now_add=True,verbose_name='Date Created')

    class Meta:
        ordering = ['-create_at']

