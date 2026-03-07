from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = "admin"
        password = "edil0505" # Осы жерге жаңа пароль жазыңыз
        
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.is_active = True  # Токен алу үшін осы өте маңызды!
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        if created:
            self.stdout.write(f"Жаңа пайдаланушы '{username}' құрылды!")
        else:
            self.stdout.write(f"Пайдаланушы '{username}' деректері жаңартылды!")