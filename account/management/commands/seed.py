from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from account.models import Category, Technology
# seed.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        admin_email = 'admin@example.com'
        admin_password = 'password'
        tc_agreement = True  # Assuming this is a terms and conditions agreement field

        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                name='Admin Name',
                password=admin_password,
                tc=tc_agreement  # Make sure to include this argument
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        
        
        categories = ['Category 1', 'Category 2', 'Category 3']
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(categories)} categories'))

        # Seed Technology data
        technologies = ['Technology 1', 'Technology 2', 'Technology 3']
        for tech_name in technologies:
            Technology.objects.get_or_create(name=tech_name, description=f"{tech_name} description")
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(technologies)} technologies'))
