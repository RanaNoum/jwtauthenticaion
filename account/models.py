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
    description = models.TextField()
    technology_used=models.TextField()

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
        return self.technologies.technology_used

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='Service_images/', blank=True, null=True)  # New ImageField
    related_projects = models.ForeignKey(Project, on_delete=models.CASCADE)


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    # heading = models.CharField()
    heading = HTMLField('Heading_Content',blank=True)  # Replaces models.TextField()
    content = models.TextField()
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    published_date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_blogposts')
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

class RoleChoices(models.TextChoices):
    ADMIN = 'Admin', 'Administrator'
    EDITOR = 'Editor', 'Editor'
    CONTRIBUTOR = 'Contributor', 'Contributor'
    GUEST = 'Guest', 'Guest'


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    Author_image = models.ImageField(upload_to='Auther_images/', blank=True, null=True)  # New ImageField
    roles = models.CharField(max_length=50, choices=RoleChoices.choices, default=RoleChoices.CONTRIBUTOR)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


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



COUNTRY_CHOICES = [(country.alpha_2, country.name) for country in pycountry.countries]

class Case(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
        ('on_hold', 'On Hold')
    ]
    SERVICE_TYPE_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile App Development'),
        ('software', 'Software Development'),
    ]
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    service_type = models.CharField(max_length=100, choices=SERVICE_TYPE_CHOICES)
    technologies = models.ForeignKey(Technologie, on_delete=models.CASCADE)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True, null=True)
    country_image = models.ImageField(upload_to='case/', blank=True, null=True)
    case_number = models.CharField(max_length=120, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')
    assigned_to = models.ForeignKey(User, related_name='assigned_cases', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, related_name='created_cases', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.case_number} - {self.title}"

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
    discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Discounts applied")
    total_estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Automatically calculated total cost")
    client_information = models.CharField(max_length=255, help_text="Information about the client")
    submitted_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, default='pending', help_text="Status of the estimate")

    def save(self, *args, **kwargs):
        # Calculate total estimated cost
        self.total_estimated_cost = (self.estimated_hours * self.hourly_rate) + self.additional_costs - self.discounts
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service_type} for {self.client_information} on {self.submitted_on.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = 'Pricing Estimate'
        verbose_name_plural = 'Pricing Estimates'
        ordering = ['-submitted_on']



class Update(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='updates/', blank=True, null=True)
    category = models.TextField(max_length=255)

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

