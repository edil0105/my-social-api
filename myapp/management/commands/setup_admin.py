from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        username = "admin"
        password = "edil0909" # Жаңа пароль қойыңыз
        
        user = User.objects.filter(username=username).first()
        if user:
            user.set_password(password)
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(f"User {username} updated successfully!")
        else:
            User.objects.create_superuser(username, "admin@example.com", password)
            self.stdout.write("New superuser created!")