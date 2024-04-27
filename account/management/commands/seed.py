# from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model
# from account.models import Categorie, Technologie
# # seed.py
# from django.core.management.base import BaseCommand
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class Command(BaseCommand):
#     help = 'Seeds the database with initial data'

#     def handle(self, *args, **kwargs):
#         admin_email = 'admin@example.com'
#         admin_password = 'password'
#         tc_agreement = True  # Assuming this is a terms and conditions agreement field

#         if not User.objects.filter(email=admin_email).exists():
#             User.objects.create_superuser(
#                 email=admin_email,
#                 name='Admin Name',
#                 password=admin_password,
#                 tc=tc_agreement  # Make sure to include this argument
#             )
#             self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        
        
#         categories = ['Category 1', 'Category 2', 'Category 3']
#         for category_name in categories:
#             Categorie.objects.get_or_create(name=category_name)
#         self.stdout.write(self.style.SUCCESS(f'Successfully added {len(categories)} categories'))

#         # Seed Technology data
#         technologies = ['Technology 1', 'Technology 2', 'Technology 3']
#         for tech_name in technologies:
#             Technologie.objects.get_or_create(name=tech_name, description=f"{tech_name} description")
#         self.stdout.write(self.style.SUCCESS(f'Successfully added {len(technologies)} technologies'))


from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
import os
from account.models import Categorie,Technologie

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
                tc=tc_agreement  # Ensure this field is appropriate for your user model
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        
        # Seed Category data
        categories = ['Category 1', 'Category 2', 'Category 3']
        for category_name in categories:
            Categorie.objects.get_or_create(name=category_name)
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(categories)} categories'))

        # Seed Technology data with optional images
        technologies = [
            {'name': 'Technology 1', 'description': 'Description of Technology 1', 'image': None},
            {'name': 'Technology 2', 'description': 'Description of Technology 2', 'image': None},
            {'name': 'Technology 3', 'description': 'Description of Technology 3', 'image': None},
        ]
        for tech in technologies:
            tech_obj, created = Technologie.objects.get_or_create(
                name=tech['name'],
                description=tech['description']
            )
            if tech['image'] and created:  # Only add image if it exists and the tech was newly created
                image_path = os.path.join('path/to/seed_images', tech['image'])
                with open(image_path, 'rb') as image_file:
                    tech_obj.technology_image.save(tech['image'], File(image_file), save=True)

        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(technologies)} technologies'))
