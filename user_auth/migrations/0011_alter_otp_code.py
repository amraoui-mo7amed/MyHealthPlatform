# Generated by Django 5.1.3 on 2025-02-03 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0010_rename_certeficate_serial_userprofile_certificate_serial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
