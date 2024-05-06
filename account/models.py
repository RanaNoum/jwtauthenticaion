from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
import pycountry
from django.conf import settings  # Import settings to reference the AUTH_USER_MODEL
from tinymce.models import HTMLField
from django.db.models.signals import post_migrate
from django.dispatch import receiver



#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser,PermissionsMixin):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  
  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin
  
  def get_all_permissions(self, obj=None):
        if not self.is_active or self.is_anonymous:
            return set()
        if not hasattr(self, '_perm_cache'):
            self._perm_cache = set(super().get_all_permissions(obj))
        return self._perm_cache  





class Categorie(models.Model):
    
    name = models.CharField(max_length=255)
    blog_post_categories=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    image = models.ImageField(upload_to='events_images/', blank=True, null=True)
    registration_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.start_time > timezone.now()

    @property
    def duration(self):
        return self.end_time - self.start_time

    class Meta:
        ordering = ['start_time']


class Technologie(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='technology_images/', blank=True, null=True)  # New ImageField
    description = models.TextField()
    

class Industrie(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='industry_images/', blank=True, null=True)  # New ImageField
    description = models.TextField()    

class RatingChoices(models.IntegerChoices):
    ONE = 1, '1'
    TWO = 2, '2'
    THREE = 3, '3'
    FOUR = 4, '4'
    FIVE = 5, '5'

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_company = models.CharField(max_length=100)
    rating = models.IntegerField(choices=RatingChoices.choices)
    image = models.ImageField(upload_to='testimonial_images/', blank=True, null=True)
    content = models.TextField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_projects')
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE,related_name='Blog_post_categories')
    technologies = models.ForeignKey(Technologie, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('Active', 'Active'), ('Completed', 'Completed'), ('Paused', 'Paused')]
    )

    def __str__(self):
        return self.name

    @property
    def technology_used(self):
        return self.technologies

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='Service_images/', blank=True, null=True)  # New ImageField
    related_projects = models.ForeignKey(Project, on_delete=models.CASCADE)

class RoleChoices(models.TextChoices):
    ADMIN = 'Admin', 'Administrator'
    EDITOR = 'Editor', 'Editor'
    CONTRIBUTOR = 'Contributor', 'Contributor'
    GUEST = 'Guest', 'Guest'


class Author(models.Model):
    Select_author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    Author_image = models.ImageField(upload_to='Auther_images/', blank=True, null=True)  # New ImageField
    roles = models.CharField(max_length=50, choices=RoleChoices.choices, default=RoleChoices.CONTRIBUTOR)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username



class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # heading = models.TextField('Heading_Content',blank=True)  # Replaces models.TextField()
    content = models.TextField()
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    published_date = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # New ImageField

    def __str__(self):
        return self.title


class Comment(models.Model):
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    posted_date = models.DateTimeField()
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

class CompanyInformation(models.Model):
    about_us = models.TextField()
    mission = models.TextField()
    vision = models.TextField()
    # Assuming team members are separate for scalability
    contact = models.IntegerField()

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team_member_images/', blank=True, null=True)  # New ImageField
    social_media_links = models.CharField(max_length=255)






class ContactInquirie(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    received_date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)





class ServiceType(models.Model):
    choice_name = models.TextField(max_length=50)
    


COUNTRY_CHOICES = [(country.name, country.name) for country in pycountry.countries]
class Case(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
        ('on_hold', 'On Hold')
    ]

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to='case_featured_images/', blank=True, null=True)
    content = models.TextField()
    service_type = models.ManyToManyField(ServiceType, blank=True)
    industries = models.ForeignKey(Industrie, on_delete=models.CASCADE)
    technologies = models.ManyToManyField(Technologie, blank=True)
    country = models.CharField(max_length=255, choices=COUNTRY_CHOICES, blank=True, null=True)
    country_image = models.ImageField(upload_to='case_country_images/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')
    created_by = models.ForeignKey(User, related_name='created_cases', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ['-created_date']




class Career(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_type = models.CharField(max_length=10, choices=JOB_TYPES, default='full_time')
    posted_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField()

    def __str__(self):
        return f"{self.title} ({self.job_type})"

    class Meta:
        verbose_name = 'Career'
        verbose_name_plural = 'Careers'
        ordering = ['-posted_date']




from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from mimetypes import guess_type
from django.core.mail.message import EmailMessage
import threading

class PricingEstimate(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile App Development'),
        ('software', 'Software Development'),
    ]
    COMPLEXITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    service_type = models.CharField(max_length=100, choices=SERVICE_TYPE_CHOICES)
    feature_set = models.TextField(help_text="Detailed description of the requested features")
    complexity = models.CharField(max_length=10, choices=COMPLEXITY_CHOICES)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, help_text="Estimated hours to complete the project")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Hourly rate for the service")
    additional_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Additional costs")
    total_estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Automatically calculated total cost")
    Name = models.CharField(max_length=50, help_text="Name")
    contact_information = models.EmailField(max_length=255, verbose_name="Contact Information")
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending', help_text="Status of the estimate")
    
    # Add a file upload field
    file = models.FileField(upload_to='pricing_files/', blank=True, null=True)
lock = threading.Lock()


@receiver(post_save, sender=PricingEstimate)
def send_email_on_new_estimate(sender, instance, created, **kwargs):
    if created:
        subject = 'Confirmation Email'
        client_message = f"""
            Dear {instance.Name},

            Thank you for approaching us for services.
            
            
            I have received your service needs. 
            We appreciate your interest in our services.
            Our team will review your request and
            contact you as soon as possible to discuss further
            details.
            
            
            And you have filled this information.
            
            Service Type: {instance.service_type}
            Feature Set: {instance.feature_set}
            Complexity: {instance.complexity}
            Estimated Hours: {instance.estimated_hours}
            Hourly Rate: {instance.hourly_rate}
            Additional Costs: {instance.additional_costs}
            Name: {instance.Name}
            Total Estimated Cost: {instance.total_estimated_cost}
            Contact Information: {instance.contact_information}
           
            


            We look forward to serving you soon.
           
            Best regards,
            [Labvers Software Company]
        """
        company_message = f"""
            Dear Admin:

            New Client is approaching.
            Kindly review the information.

            
            "Client information Details"

    
            Service Type: {instance.service_type}
            Feature Set: {instance.feature_set}
            Complexity: {instance.complexity}
            Estimated Hours: {instance.estimated_hours}
            Hourly Rate: {instance.hourly_rate}
            Additional Costs: {instance.additional_costs}
            Name: {instance.Name}
            Total Estimated Cost: {instance.total_estimated_cost}
            Contact Information: {instance.contact_information}
            This is all client information.

            


            Kindly also review the client's file
            which is mentioned below.
        """
        from_email = 'info@labverse.co'
        client_email = [instance.contact_information]
        company_email = ['cost@labverse.co']

        with lock:
            # Send personalized message to the client
            client_email_message = EmailMessage(subject, client_message, from_email, client_email)
            if instance.file:
                file_attachment = instance.file.file
                mimetype, _ = guess_type(file_attachment.name)
                client_email_message.attach(file_attachment.name, file_attachment.read(), mimetype)
            client_email_message.send()

            # Send only relevant information to the company, no personalization
            company_email_message = EmailMessage(subject, company_message, from_email, company_email)
            if instance.file:
                file_attachment = instance.file.file  # This line is redundant if file is already attached above, just illustrating
                mimetype, _ = guess_type(file_attachment.name)
                company_email_message.attach(file_attachment.name, file_attachment.read(), mimetype)
            company_email_message.send()



# @receiver(post_save, sender=PricingEstimate)
# def send_email_on_new_estimate(sender, instance, created, **kwargs):
#     if created:
#         subject = 'New Pricing Estimate Received'
#         client_message = f"""
#             Dear {instance.Name},
#             Thank you for approaching us for services. I have received your service needs. We appreciate your interest for our services.
#             Our team will review your request and contact you as soon as possible to discuss further details.
#             And you have filled this information.
#             Please find the details of your estimate below:
#             Service Type: {instance.service_type}
#             Feature Set: {instance.feature_set}
#             Complexity: {instance.complexity}
#             Estimated Hours: {instance.estimated_hours}
#             Hourly Rate: {instance.hourly_rate}
#             Additional Costs: {instance.additional_costs}
#             Name: {instance.Name}
#             Total Estimated Cost: {instance.total_estimated_cost}
#             Contact Information: {instance.contact_information}
#             We look forward to serving you soon.
#             Best regards,
#             [Labverse]
#         """
#         company_message = f"""
#             Service Type: {instance.service_type}
#             Feature Set: {instance.feature_set}
#             Complexity: {instance.complexity}
#             Estimated Hours: {instance.estimated_hours}
#             Hourly Rate: {instance.hourly_rate}
#             Additional Costs: {instance.additional_costs}
#             Name: {instance.Name}
#             Total Estimated Cost: {instance.total_estimated_cost}
#             Contact Information: {instance.contact_information}
#         """
#         from_email = '18251598-111@uog.edu.pk'
#         recipient_list = [instance.contact_information, 'usman.latif.raw@gmail.com']  # Add company email here

#         with lock:
#             if instance.file:
#                 file_attachment = instance.file.file
#                 mimetype, _ = guess_type(file_attachment.name)
#                 email = EmailMessage(subject, client_message, from_email, recipient_list)
#                 email.attach(file_attachment.name, file_attachment.read(), mimetype)
#                 email.send()
#             else:
#                 email = EmailMessage(subject, client_message, from_email, [instance.contact_information])
#                 email.attach_alternative(company_message, 'text/plain')
#                 email.send()
                
#                 # Send only field information and file attachment to company email
#                 email = EmailMessage(subject, company_message, from_email, ['usman.latif.raw@gmail.com'])
#                 email.attach(file_attachment.name, file_attachment.read(), mimetype)
#                 email.send()






# @receiver(post_save, sender=PricingEstimate)
# def send_email_on_new_estimate(sender, instance, created, **kwargs):
#     if created:
#         subject = 'Confirmation Email from Labverse'
#         client_message = f"""
#             Dear {instance.Name},
#             Thank you for approaching us for services. I have received your service needs. We appreciate your interest for our services.
#             Our team will review your request and contact you as soon as possible to discuss further details.
#             And you have filled this information.
#             Please find the details of your estimate below:
#             Service Type: {instance.service_type}
#             Feature Set: {instance.feature_set}
#             Complexity: {instance.complexity}
#             Estimated Hours: {instance.estimated_hours}
#             Hourly Rate: {instance.hourly_rate}
#             Additional Costs: {instance.additional_costs}
#             Name: {instance.Name}
#             Total Estimated Cost: {instance.total_estimated_cost}
#             Contact Information: {instance.contact_information}
#             We look forward to serving you soon.
#             Best regards,
#             [Labverse]
#         """
#         company_message = f"""
#             Service Type: {instance.service_type}
#             Feature Set: {instance.feature_set}
#             Complexity: {instance.complexity}
#             Estimated Hours: {instance.estimated_hours}
#             Hourly Rate: {instance.hourly_rate}
#             Additional Costs: {instance.additional_costs}
#             Name: {instance.Name}
#             Total Estimated Cost: {instance.total_estimated_cost}
#             Contact Information: {instance.contact_information}
#         """
#         from_email = '18251598-111@uog.edu.pk'
#         recipient_list = [instance.contact_information, 'usman.latif.raw@gmail.com']  # Add company email here

#         with lock:
#             if instance.file:
#                 file_attachment = instance.file.file
#                 mimetype, _ = guess_type(file_attachment.name)
#                 email = EmailMessage(subject, client_message, from_email, recipient_list)
#                 email.attach(file_attachment.name, file_attachment.read(), mimetype)
#                 email.send()
#             else:
#                 email = EmailMessage(subject, client_message, from_email, [instance.contact_information])
#                 email.attach_alternative(company_message, 'text/plain')
#                 email.send()
                
#                 # Send file attachment to company email
#                 email = EmailMessage(subject, company_message, from_email, ['usman.latif.raw@gmail.com'])
#                 if instance.file:
#                     file_attachment = instance.file.file
#                     mimetype, _ = guess_type(file_attachment.name)
#                     email.attach(file_attachment.name, file_attachment.read(), mimetype)
#                 email.send()




# @receiver(post_save, sender=PricingEstimate)
# def send_email_on_new_estimate(sender, instance, created, **kwargs):
#     if created:
#         subject = 'New Pricing Estimate Received'
#         client_message = f"""
#             Dear {instance.Name},
#             Thank you for approaching us for services. 
#             I have received your  service needs. We appreciate your interest for our services.
#             Our team will review your request and contact you as soon as possible to discuss further details.
#             And you have filled this information.
#             Please find the details of your estimate below:
#             Service Type: {instance.service_type}
#             Feature Set: {instance.feature_set}
#             Complexity: {instance.complexity}
#             Estimated Hours: {instance.estimated_hours}
#             Hourly Rate: {instance.hourly_rate}
#             Additional Costs: {instance.additional_costs}
#             Name: {instance.Name}
#             Total Estimated Cost: {instance.total_estimated_cost}
#             Contact Information: {instance.contact_information}
#             We look forward to serving you soon.
#             Best regards,
#             [Labverse]
#         """
#         company_message = f"""
#             Service Type: {instance.service_type}
#             Feature Set: {instance.feature_set}
#             Complexity: {instance.complexity}
#             Estimated Hours: {instance.estimated_hours}
#             Hourly Rate: {instance.hourly_rate}
#             Additional Costs: {instance.additional_costs}
#             Name: {instance.Name}
#             Total Estimated Cost: {instance.total_estimated_cost}
#             Contact Information: {instance.contact_information}
#         """
#         from_email = '18251598-111@uog.edu.pk'
#         recipient_list = [instance.contact_information, 'company_email@example.com']  # Add company email here
#         with lock:
#             if instance.file:
#                 file_attachment = instance.file.file
#                 mimetype, _ = guess_type(file_attachment.name)
#                 email = EmailMessage(subject, client_message, from_email, recipient_list)
#                 email.attach(file_attachment.name, file_attachment.read(), mimetype)
#                 email.send()
#             else:
#                 email = EmailMessage(subject, client_message, from_email, [instance.contact_information])
#                 email.attach_alternative(company_message, 'text/plain')
#                 email.send()





# @receiver(post_save, sender=PricingEstimate)
# def send_email_on_new_estimate(sender, instance, created, **kwargs):
#     if created:
#         subject = 'New Pricing Estimate Received'
#         message = f"""
#         Dear {instance.contact_information},

#             Thank you for approaching us for services.
#             I have recerived your needs. We appreciate your interest in our services.
#             Our team will review your request and contact you as soon as possible to discuss further details.
            
#             And you have filled this information.
#             Please find the details of your estimate below:
#             Service Type: {instance.service_type}
#             Feature Set: {instance.feature_set}
#             Complexity: {instance.complexity}
#             Estimated Hours: {instance.estimated_hours}
#             Hourly Rate: {instance.hourly_rate}
#             Additional Costs: {instance.additional_costs}
#             Discounts: {instance.Name}
#             Total Estimated Cost: {instance.total_estimated_cost}
#             Contact Information: {instance.contact_information}


#          We look forward to serving you soon.

#             Best regards,
#             [Labverse]



#         """
#         from_email = '18251598-111@uog.edu.pk'
#         recipient_list = [instance.contact_information]
#         with lock:
#             if instance.file:
#                 file_attachment = instance.file.file
#                 mimetype, _ = guess_type(file_attachment.name)
#                 email = EmailMessage(subject, message, from_email, recipient_list)
#                 email.attach(file_attachment.name, file_attachment.read(), mimetype)
#                 email.send()
#             else:
#                 send_mail(subject, message, from_email, recipient_list)







class Update(models.Model):
    COMPLEXITY_CHOICES = [
        ('expert', 'Expert'),
        ('service', 'Service'),
     
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='updates/', blank=True, null=True)
    category = models.TextField(max_length=255, choices = COMPLEXITY_CHOICES)

    def __str__(self):
        return self.title
    

class QuestionsAnswer(models.Model):
    Question = models.TextField(verbose_name="Question")
    Answer = models.TextField(verbose_name="Answer")

    def __str__(self):
        return f"Question: {self.Question} | Answer: {self.Answer}"
    

# Predefined QnA data
DEFAULT_QNA_DATA = [
    {
        "Question": "What services do you offer?",
        "Answer": "We offer a variety of services including web development, app development, and digital marketing."
    },
    {
        "Question": "How can I contact customer support?",
        "Answer": "You can reach our customer support at support@example.com."
    },
    {
        "Question": "Where is your company located?",
        "Answer": "Our main office is located in New York City."
    },
    {
        "Question": "Do you offer international shipping?",
        "Answer": "Yes, we offer shipping to numerous countries around the globe."
    },
    {
        "Question": "What are your operating hours?",
        "Answer": "We operate from 9 AM to 5 PM on weekdays."
    }
]

@receiver(post_migrate)
def populate_qna(sender, **kwargs):
    if sender.name == 'account':  # Replace 'your_app_name' with the name of your app
        for item in DEFAULT_QNA_DATA:
            QuestionsAnswer.objects.get_or_create(Question=item["Question"], defaults={'Answer': item["Answer"]})






class Industries_we_serve(models.Model):
    name = models.CharField(max_length=255)
    description = HTMLField('Write description here', blank=True)
    features_overview = models.TextField()
    image = models.ImageField(upload_to='Project_weServed_images/')
    technologies = models.CharField(max_length=255)

    def __str__(self):
        return self.name