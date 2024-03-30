from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    TechnologyViewSet,
    TestimonialViewSet,
    ProjectViewSet,
    ServiceViewSet,
    BlogPostViewSet,
    CommentViewSet,
    CompanyInformationViewSet,
    TeamMemberViewSet,
    AuthorViewSet,
    ContactInquiryViewSet,
    SendPasswordResetEmailView,
    UserChangePasswordView,
    UserLoginView,
    UserProfileView,
    UserRegistrationView,
    UserPasswordResetView,
)
app_name = 'account'

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
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'contactinquiries', ContactInquiryViewSet, basename='contactinquiry')

urlpatterns = [
    path('models/', include(router.urls)),  # Corrected path (empty string '')
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    
]
