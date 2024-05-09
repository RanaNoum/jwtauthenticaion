from django.contrib import admin
from account.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Categorie, Event,  ServiceType, Case, Career, Technologie, Industrie, Update, Testimonial, Project, Service, BlogPost, Comment, CompanyInformation, TeamMember, Author, ContactInquirie, PricingEstimate, QuestionsAnswer, Industries_we_serve
from .forms import BlogPostForm,CaseForm
from tinymce.widgets import TinyMCE
from django.db import models  # This import is necessary for models.TextField




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


# class CaseAdmin(admin.ModelAdmin):
#     list_display = ('case_number', 'title', 'featured_image', 'technologies', 'industries', 'country', 'status', 'priority', 'assigned_to', 'created_by', 'service_type','created_date')
#     list_filter = ('status', 'priority', 'created_date')
#     search_fields = ('title', 'description', 'case_number')
#     date_hierarchy = 'created_date'
@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['choice_name']
    


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    form = CaseForm
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
    list_display = ('title', 'status', 'priority', 'get_service_type', 'industries', 'get_technologies', 'created_by')
    search_fields = ('title', 'description')
    list_filter = ('status', 'priority', 'created_by', 'content')

    # def get_industries(self, obj):
    #     return ", ".join([industry.name for industry in obj.industries.all()])
    # get_industries.short_description = 'Industries'

    def get_service_type(self, obj):
        return ", ".join([service_types.choice_name for service_types in obj.service_type.all()])
    get_service_type.short_description = 'ServiceType'


    def get_technologies(self, obj):
        return ", ".join([technology.name for technology in obj.technologies.all()])
    get_technologies.short_description = 'Technologies'



@admin.register(Technologie)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'description')


@admin.register(Industrie)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'description')


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
    form = BlogPostForm
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }
    
    list_display = ('id', 'title', 'description', 'category', 'published_date', 'author', 'image')
    list_filter = ('category', 'author')
    search_fields = ('title', 'content')

    # def get_content(self, obj):
    #     return obj.content[:60] + '...' if len(obj.heading) > 60 else obj.heading
    # get_content.short_description = 'Content'



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
    list_display = ['Select_author', 'username', 'email', 'Author_image', 'roles', 'created_at', 'updated_at']
    search_fields = ['username', 'email']


@admin.register(ContactInquirie)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'message', 'received_date', 'status')
    list_filter = ['status']
    search_fields = ['name', 'email']


# @admin.register(PricingEstimate)
# class PricingEstimateAdmin(admin.ModelAdmin):
#     list_display = ['service_type', 'contact_information', 'submitted_on', 'total_estimated_cost', 'status', 'file']
#     list_filter = ['service_type', 'complexity', 'status', 'submitted_on']
#     search_fields = ['client_information', 'feature_set']
#     date_hierarchy = 'submitted_on'


from django.contrib import admin

from .models import PricingEstimate

@admin.register(PricingEstimate)
class PricingEstimateAdmin(admin.ModelAdmin):
    list_display = ['contact_name', 'platform', 'stage', 'need_investor', 'total_estimated_cost', 'status', 'file']
    list_filter = ['stage', 'platform', 'need_investor', 'status']
    search_fields = ['contact_name', 'contact_email']



# class FeatureInline(admin.TabularInline):
#     model = PricingEstimate.additional_features.through
#     extra = 1  # How many rows to show



# @admin.register(PricingEstimate)
# class PricingEstimateAdmin(admin.ModelAdmin):
#     list_display = ('contact_name', 'platform', 'stage', 'need_investor', 'total_estimated_cost', 'status', 'submitted_on', 'file')
#     list_filter = ('platform', 'stage', 'need_investor', 'status')
#     search_fields = ('contact_name', 'contact_email')
#     inlines = [FeatureInline]
#     fieldsets = (
#         ('Client Information', {
#             'fields': ('contact_name', 'contact_email')
#         }),
#         ('Project Details', {
#             'fields': ('stage', 'platform', 'need_investor', 'screen_range', 'estimated_hours', 'hourly_rate', 'additional_costs', 'total_estimated_cost', 'status')
#         }),
#         ('Additional Features', {
#             'fields': ('additional_features',)
#         }),
#     )
#     readonly_fields = ('submitted_on',)
    
#     def save_model(self, request, obj, form, change):
#         super().save_model(request, obj, form, change)
#         # Custom save logic or post-processing after save can be added here

#     def save_formset(self, request, form, formset, change):
#         super().save_formset(request, form, formset, change)
#         # Custom save logic for inline forms







@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'content','category', 'image']
    search_fields = ['title', 'content']
    list_filter = ['category']





@admin.register(QuestionsAnswer)
class QuestionsAnswerAdmin(admin.ModelAdmin):
  list_display = ('Question', 'Answer')  # Fields to display in admin list view



@admin.register(Industries_we_serve)
class CompaniesWeServeAdmin(admin.ModelAdmin):
    list_display = ['name', 'technologies']
    search_fields = ['name', 'technologies']