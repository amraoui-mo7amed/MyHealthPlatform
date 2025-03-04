from django.db import migrations

def populate_illness(apps, schema_editor):
    Illness = apps.get_model('patient', 'Illness')
    illnesses = ['DIABETES', 'OBESITY']
    
    for illness in illnesses:
        Illness.objects.get_or_create(name=illness)

class Migration(migrations.Migration):
    dependencies = [
        ('patient', '0001_initial'),  # Changed from 'previous_migration' to '0001_initial'
    ]

    operations = [
        migrations.RunPython(populate_illness),
    ]