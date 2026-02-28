from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = "admin" # Өзіңіз қалаған логин
        email = "admin@example.com"
        password = "your_secure_password" # Өзіңіз қалаған пароль
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write("Superuser created!")
        else:
            self.stdout.write("Superuser already exists.")