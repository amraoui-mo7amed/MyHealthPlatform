# Generated by Django 5.1.3 on 2025-03-04 19:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_alter_dietrequest_diabetes_alter_dietrequest_obesity'),
    ]

    operations = [
        migrations.AddField(
            model_name='dietrequest',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 3, 4, 19, 55, 43, 833521, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
