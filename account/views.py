# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
# from django.contrib.auth import authenticate
# from account.renderers import UserRenderer
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.permissions import IsAuthenticated

# # Generate Token Manually
# def get_tokens_for_user(user):
#   refresh = RefreshToken.for_user(user)
#   return {
#       'refresh': str(refresh),
#       'access': str(refresh.access_token),
#   }

# class UserRegistrationView(APIView):
#   renderer_classes = [UserRenderer]
#   def post(self, request, format=None):
#     serializer = UserRegistrationSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.save()
#     token = get_tokens_for_user(user)
#     return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

# class UserLoginView(APIView):
#   renderer_classes = [UserRenderer]
#   def post(self, request, format=None):
#     serializer = UserLoginSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.data.get('email')
#     password = serializer.data.get('password')
#     user = authenticate(email=email, password=password)
#     if user is not None:
#       token = get_tokens_for_user(user)
#       return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
#     else:
#       return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

# class UserProfileView(APIView):
#   renderer_classes = [UserRenderer]
#   permission_classes = [IsAuthenticated]
#   def get(self, request, format=None):
#     serializer = UserProfileSerializer(request.user)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# class UserChangePasswordView(APIView):
#   renderer_classes = [UserRenderer]
#   permission_classes = [IsAuthenticated]
#   def post(self, request, format=None):
#     serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
#     serializer.is_valid(raise_exception=True)
#     return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

# class SendPasswordResetEmailView(APIView):
#   renderer_classes = [UserRenderer]
#   def post(self, request, format=None):
#     serializer = SendPasswordResetEmailSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

# class UserPasswordResetView(APIView):
#   renderer_classes = [UserRenderer]
#   def post(self, request, uid, token, format=None):
#     serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
#     serializer.is_valid(raise_exception=True)
#     return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)



from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Project, Service, BlogPost, CompanyInformation, ContactInquiry, User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets
from .models import Category, Technology, Testimonial, Project, Service, BlogPost, Comment, CompanyInformation, TeamMember, Auther, ContactInquiry
from .serializers import CategorySerializer, TechnologySerializer, TestimonialSerializer, ProjectSerializer, ServiceSerializer, BlogPostSerializer, CommentSerializer, CompanyInformationSerializer, TeamMemberSerializer, AutherSerializer, ContactInquirySerializer



# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

# @login_required
# def admin_dashboard(request):
#     if request.user.is_authenticated and request.user.is_admin:
#         # Implement logic to retrieve dashboard data
#         return render(request, 'admin_dashboard.html', context={'data': data})  # Replace 'admin_dashboard.html' with your actual template name
#     else:
#         messages.error(request, 'You are not authorized to access this page.')
#         return redirect('admin_login')
    
# @login_required
# def admin_dashboard(request):
#     if request.user.is_authenticated and request.user.is_admin:
#         # Implement logic to retrieve dashboard data
#         data = {}  # Placeholder for dashboard data
#         return render(request, 'admin_dashboard.html', context={'data': data})  # Replace 'admin_dashboard.html' with your actual template name
#     else:
#         messages.error(request, 'You are not authorized to access this page.')
#         return redirect('admin_login')



# @csrf_exempt
# def admin_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(email=email, password=password)
#         if user is not None and user.is_admin:
#             login(request, user)
#             return redirect('admin_dashboard')
#         else:
#             messages.error(request, 'Invalid email or password.')
#     return render(request, 'admin_login.html')  # Replace 'admin_login.html' with your actual template name

# @login_required
# def admin_logout(request):
#     logout(request)
#     return redirect('admin_login')

# # Projects Showcase
# def get_all_projects(request):
#     projects = Project.objects.all()
#     data = [{'id': project.id, 'name': project.name, 'description': project.description} for project in projects]
#     return JsonResponse(data, safe=False)

# def get_project_details(request, project_id):
#     project = get_object_or_404(Project, id=project_id)
#     data = {
#         'id': project.id,
#         'name': project.name,
#         'description': project.description,
#         'categories': [category.name for category in project.categories.all()],
#         'images': project.images,
#         'technologies_used': [technology.name for technology in project.technologies_used.all()],
#         'client_testimonials': [testimonial.id for testimonial in project.client_testimonials.all()],
#         'link': project.link,
#         'start_date': project.start_date,
#         'end_date': project.end_date,
#         'status': project.status,
#     }
#     return JsonResponse(data)

# # Services Offered
# def get_all_services(request):
#     services = Service.objects.all()
#     data = [{'id': service.id, 'name': service.name, 'description': service.description} for service in services]
#     return JsonResponse(data, safe=False)

# # Blog/News Section
# def get_all_posts(request):
#     posts = BlogPost.objects.all()
#     data = [{'id': post.id, 'title': post.title, 'content': post.content} for post in posts]
#     return JsonResponse(data, safe=False)

# # Company Information
# def get_company_info(request):
#     company_info = CompanyInformation.objects.first()
#     data = {
#         'about_us': company_info.about_us,
#         'mission': company_info.mission,
#         'vision': company_info.vision,
#         # Add other fields as needed
#     }
#     return JsonResponse(data)

# # Contact Form
# @csrf_exempt
# def submit_contact_form(request):
#     if request.method == 'POST':
#         # Handle form submission
#         return JsonResponse({'message': 'Contact form submitted successfully.'})
#     else:
#         return JsonResponse({'error': 'Only POST requests are allowed for this endpoint.'}, status=405)

# # User Management (for Admins)
# @staff_member_required
# def list_all_users(request):
#     users = User.objects.all()
#     data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
#     return JsonResponse(data, safe=False)




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CompanyInformationViewSet(viewsets.ModelViewSet):
    queryset = CompanyInformation.objects.all()
    serializer_class = CompanyInformationSerializer

class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

class AutherViewSet(viewsets.ModelViewSet):
    queryset = Auther.objects.all()
    serializer_class = AutherSerializer

class ContactInquiryViewSet(viewsets.ModelViewSet):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
