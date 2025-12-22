from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with first name, last name, username, email, and password'

    def handle(self, *args, **options):
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        username = input("Username: ").strip()
        email = input("Email address: ").strip()

        if not username:
            self.stderr.write("Error: Username is required.")
            return

        if User.objects.filter(username=username).exists():
            self.stderr.write(f"Error: A user with username '{username}' already exists.")
            return

        password = input("Password: ")
        password2 = input("Password confirmation: ")

        if password != password2:
            self.stderr.write("Error: Passwords do not match.")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully!"))