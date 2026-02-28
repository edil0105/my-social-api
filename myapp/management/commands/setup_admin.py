from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Admin пайдаланушысын құру немесе паролін жаңарту'

    def handle(self, *args, **options):
        username = "admin"
        password = "your_password_here" # Осы жерге пароліңді жаз
        email = "admin@example.com"
        
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Пайдаланушы '{username}' сәтті құрылды!"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Пайдаланушы '{username}' мәліметтері жаңартылды!"))