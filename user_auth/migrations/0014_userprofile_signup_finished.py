# Generated by Django 5.1.3 on 2025-03-03 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0013_userprofile_main_diploma'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='signup_finished',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
