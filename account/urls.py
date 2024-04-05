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
router.register(r'categories', CategoryViewSet, basename='categorie')
router.register(r'technologies', TechnologyViewSet, basename='technologie')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'blogposts', BlogPostViewSet, basename='blogpost')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'companyinformation', CompanyInformationViewSet, basename='companyinformation')
router.register(r'teammembers', TeamMemberViewSet, basename='teammember')
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'contactinquiries', ContactInquiryViewSet, basename='contactinquirie')

urlpatterns = [
    path('lists/', include(router.urls)),  # Corrected path (empty string '')
    path('lists/projects/<int:pk>/', ProjectViewSet.as_view({'get': 'retrieve'}), name='project-detail'),
    path('lists/categories/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve'}), name='category-detail'),
    path('lists/technologies/<int:pk>/', TechnologyViewSet.as_view({'get': 'retrieve'}), name='technology-detail'),
    path('lists/testimonials/<int:pk>/', TestimonialViewSet.as_view({'get': 'retrieve'}), name='testimonial-detail'),
    path('lists/services/<int:pk>/', ServiceViewSet.as_view({'get': 'retrieve'}), name='service-detail'),
    path('lists/blogposts/<int:pk>/', BlogPostViewSet.as_view({'get': 'retrieve'}), name='blogpost-detail'),
    path('lists/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve'}), name='comment-detail'),
    path('lists/companyinformation/<int:pk>/', CompanyInformationViewSet.as_view({'get': 'retrieve'}), name='companyinformation-detail'),
    path('lists/teammembers/<int:pk>/', TeamMemberViewSet.as_view({'get': 'retrieve'}), name='teammember-detail'),
    path('lists/authors/<int:pk>/', AuthorViewSet.as_view({'get': 'retrieve'}), name='author-detail'),
    path('lists/contactinquiries/<int:pk>/', ContactInquiryViewSet.as_view({'get': 'retrieve'}), name='contactinquiry-detail'),
    # path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    
]
