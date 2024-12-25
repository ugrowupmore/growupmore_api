# authuser/management/commands/cleanup_blacklisted_tokens.py

from django.core.management.base import BaseCommand
from authuser.models import (
    StudentBlacklistedToken,
    EmployeeBlacklistedToken,
    InstructorBlacklistedToken,
    InstituteBlacklistedToken,    
)
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Clean up blacklisted tokens older than 30 days.'

    def handle(self, *args, **options):
        cutoff_date = timezone.now() - timedelta(days=7)
        models_to_clean = [
            StudentBlacklistedToken,
            EmployeeBlacklistedToken,
            InstructorBlacklistedToken,
            InstituteBlacklistedToken,            
        ]

        for model in models_to_clean:
            deleted, _ = model.objects.filter(blacklisted_at__lt=cutoff_date).delete()
            self.stdout.write(f"Deleted {deleted} entries from {model.__name__}")
