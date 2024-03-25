from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TechnologyViewSet, TestimonialViewSet, ProjectViewSet,
    ServiceViewSet, BlogPostViewSet, CommentViewSet, CompanyInformationViewSet,
    TeamMemberViewSet, AutherViewSet, ContactInquiryViewSet
)
from account.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView, UserPasswordResetView
# get_all_projects,get_all_posts,get_all_services,get_company_info,get_project_details,
# list_all_users,admin_dashboard,admin_login,admin_logout,submit_contact_form
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),



    # URLs Endpoints




    # # Projects Showcase
    # path('projects/', get_all_projects, name='get_all_projects'),
    # path('projects/<int:project_id>/', get_project_details, name='get_project_details'),
    # # Services Offered
    # path('services/', get_all_services, name='get_all_services'),
    # # Blog/News Section
    # path('posts/', get_all_posts, name='get_all_posts'),
    # # Company Information
    # path('company-info/', get_company_info, name='get_company_info'),
    # # Contact Form
    # path('contact/', submit_contact_form, name='submit_contact_form'),
    # # Authentication & Admin Panel
    # path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    # path('auth/login/', admin_login, name='admin_login'),
    # path('auth/logout/', admin_logout, name='admin_logout'),
    # # User Management (for Admins)
    # path('admin/users/', list_all_users, name='list_all_users'),


]



# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'technologies', TechnologyViewSet, basename='technology')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'blogposts', BlogPostViewSet, basename='blogpost')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'companyinformation', CompanyInformationViewSet, basename='companyinformation')
router.register(r'teammembers', TeamMemberViewSet, basename='teammember')
router.register(r'authers', AutherViewSet, basename='auther')
router.register(r'contactinquiries', ContactInquiryViewSet, basename='contactinquiry')

urlpatterns = [
    path('api/', include(router.urls)),
]
