from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from enum import Enum
from django.conf import settings  # Import settings to reference the AUTH_USER_MODEL
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










class Category(models.Model):
    
    name = models.CharField(max_length=255)
    blog_post_categories=models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technology_used=models.TextField()

class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_company = models.CharField(max_length=100)
    content = models.TextField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE)



# class Project(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
    
#     link = models.URLField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     technologies = models.ForeignKey(Technology, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
    
#     class Status(models.TextChoices):
#         ACTIVE = 'Active', 'Active'
#         COMPLETED = 'Completed', 'Completed'
#         PAUSED = 'Paused', 'Paused'
        
#     status = models.CharField(max_length=20, choices=Status.choices)
    
#     def __str__(self):
#         return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_projects')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='Blog_post_categories')
    technologies = models.ForeignKey(Technology, on_delete=models.CASCADE)
    # categories = models.ManyToManyField(Category, related_name='projects')  # Adjusted to ManyToManyField
    # technologies = models.ManyToManyField(Technology, related_name='projects')  # Adjusted to ManyToManyField
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
    icon_image = models.URLField()
    related_projects = models.ForeignKey(Project, on_delete=models.CASCADE)

# class BlogPost(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     published_date = models.DateTimeField()
#     author = models.ForeignKey('Author', on_delete=models.CASCADE)
    # Assuming comments are separate for scalability
    # comments = models.ManyToManyField('Comment')


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_blogposts')

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
    image = models.URLField()
    social_media_links = models.CharField(max_length=255)

# class Author(models.Model):
#     username = models.CharField(max_length=100)
#     email = models.EmailField()
    
#     roles = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

class RoleChoices(models.TextChoices):
    ADMIN = 'Admin', 'Administrator'
    EDITOR = 'Editor', 'Editor'
    CONTRIBUTOR = 'Contributor', 'Contributor'
    GUEST = 'Guest', 'Guest'


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()

    roles = models.CharField(max_length=50, choices=RoleChoices.choices, default=RoleChoices.CONTRIBUTOR)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


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


