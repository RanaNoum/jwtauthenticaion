from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Categorie, Event, Case, Career, Technologie, Update, Testimonial, Project, Service, BlogPost, Comment, CompanyInformation, TeamMember, Author, ContactInquirie, PricingEstimate


class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'name', 'tc', 'is_admin')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('name', 'tc')}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
 
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'name', 'tc', 'password1', 'password2'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)





@admin.register(Categorie)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'blog_post_categories')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'organizer', 'location', 'is_upcoming')
    list_filter = ('start_time', 'end_time', 'organizer')
    search_fields = ('title', 'description', 'location') 

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_type', 'location', 'posted_date', 'closing_date')
    list_filter = ('job_type', 'location')
    search_fields = ('title', 'description')

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'title', 'technologies', 'country', 'status', 'priority', 'assigned_to', 'created_by', 'service_type','created_date')
    list_filter = ('status', 'priority', 'created_date')
    search_fields = ('title', 'description', 'case_number')
    date_hierarchy = 'created_date'


@admin.register(Technologie)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'technology_used')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'client_company', 'rating', 'image', 'content', 'project')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'link', 'user', 'category', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'category', 'user']
    search_fields = ['name', 'description']
    


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'image', 'related_projects')
    # filter_horizontal = ['related_projects']  # Allows selection of multiple projects.

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'category', 'published_date', 'user', 'image']
    list_filter = ['category', 'user']
    search_fields = ['title', 'content']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'author_email', 'content', 'posted_date', 'post')

@admin.register(CompanyInformation)
class CompanyInformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'about_us', 'mission', 'vision', 'contact')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role', 'bio', 'image', 'social_media_links')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'username', 'email', 'roles', 'created_at', 'updated_at']
    search_fields = ['username', 'email']


@admin.register(ContactInquirie)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'message', 'received_date', 'status')
    list_filter = ['status']
    search_fields = ['name', 'email']


@admin.register(PricingEstimate)
class PricingEstimateAdmin(admin.ModelAdmin):
    list_display = ['service_type', 'client_information', 'submitted_on', 'total_estimated_cost', 'status']
    list_filter = ['service_type', 'complexity', 'status', 'submitted_on']
    search_fields = ['client_information', 'feature_set']
    date_hierarchy = 'submitted_on'



@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'content','category', 'image']
    search_fields = ['title', 'content']
    list_filter = ['category']