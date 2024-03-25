from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from enum import Enum
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
class User(AbstractBaseUser):
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








class CategoryType(Enum):
    PROJECT = "project"
    BLOG_POST = "blog_post"
    # Add more categories as needed

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=[(tag.name, tag.value) for tag in CategoryType])

    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_company = models.CharField(max_length=100)
    content = models.TextField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE)



class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    images = models.JSONField(default=list)  # Array of image URLs
    link = models.URLField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    class Status(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        COMPLETED = 'Completed', 'Completed'
        PAUSED = 'Paused', 'Paused'
        
    status = models.CharField(max_length=20, choices=Status.choices)
    
    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon_image = models.URLField()
    related_projects = models.ManyToManyField(Project)

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_date = models.DateTimeField()
    author = models.ForeignKey('Auther', on_delete=models.CASCADE)
    # Assuming comments are separate for scalability
    # comments = models.ManyToManyField('Comment')

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
    # team_members = models.ManyToManyField('TeamMember')
    # contact = EmbeddedField(ContactInfo)

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.URLField()
    social_media_links = models.JSONField(default=dict)

class Auther(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    roles = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ContactInquiry(models.Model):
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


