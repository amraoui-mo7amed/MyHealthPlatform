from django.core.management.base import BaseCommand
from patient.models import Illness, ILLNESS_CHOICES

class Command(BaseCommand):
    help = 'Initialize all illness types in the database'

    def handle(self, *args, **kwargs):
        for illness_code, illness_name in ILLNESS_CHOICES:
            Illness.objects.get_or_create(
                name=illness_code,
                defaults={'name': illness_code}
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created {illness_name}')) 