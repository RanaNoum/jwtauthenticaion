from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework.views import APIView
from account.serializers import UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
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
from .models import Project, Service, BlogPost, CompanyInformation, ContactInquirie, User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets
from .models import Categorie, Technologie, QuestionsAnswer, Industrie, ServiceType,Case, Career, Update, PricingEstimate, Testimonial, Project, Service, BlogPost, Comment, CompanyInformation, TeamMember, Author, ContactInquirie, Event, Industries_we_serve
from .serializers import CategorySerializer, UpdateSerializer, TechnologySerializer, IndustrySerializer,  ServiceTypeSerializer, CaseSerializer, CareerSerializer, PricingEstimateSerializer, TestimonialSerializer, ProjectSerializer, EventSerializer, ServiceSerializer, BlogPostSerializer, CommentSerializer, CompanyInformationSerializer, TeamMemberSerializer, AuthorSerializer, ContactInquirySerializer, QuestionsAnswerSerializer, IndustriesWeServeSerializer
from .permissions import IsGetRequestOrAdmin
from django.contrib.auth import authenticate
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# class CustomTokenObtainPairView(views.APIView):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get("username", "")
#         password = request.data.get("password", "")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             })
#         return Response(status=status.HTTP_401_UNAUTHORIZED)


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

# class SendPasswordResetEmailView(APIView):
#     renderer_classes = [UserRenderer]
#     def post(self, request, format=None):
#         serializer = SendPasswordResetEmailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)




class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technologie.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industrie.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class CompanyInformationViewSet(viewsets.ModelViewSet):
    queryset = CompanyInformation.objects.all()
    serializer_class = CompanyInformationSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

class ContactInquiryViewSet(viewsets.ModelViewSet):
    queryset = ContactInquirie.objects.all()
    serializer_class = ContactInquirySerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission


class ServicetypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned cases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     queryset = self.queryset
    #     username = self.request.query_params.get('username')
    #     if username is not None:
    #         queryset = queryset.filter(created_by__username=username)
    #     return queryset    


class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission


class PricingEstimateViewSet(viewsets.ModelViewSet):
    queryset = PricingEstimate.objects.all()
    serializer_class = PricingEstimateSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission



class UpdateViewSet(viewsets.ModelViewSet):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission


class QuestionsAnswerViewSet(viewsets.ModelViewSet):
  queryset = QuestionsAnswer.objects.all()
  serializer_class = QuestionsAnswerSerializer  # Use your created serializer
  permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission



class IndustriesWeServeViewSet(viewsets.ModelViewSet):
    queryset = Industries_we_serve.objects.all()
    serializer_class = IndustriesWeServeSerializer
    permission_classes = [IsGetRequestOrAdmin]  # Apply the custom permission





# class AdminCreateAPIView(views.APIView):
#     permission_classes = [AllowAny]  # Consider tightening this to more secure permissions

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         email = request.data.get("email")
#         if not all([username, email, password]):
#             return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(username=username).exists():
#             return Response({"error": "This username is already taken."}, status=status.HTTP_409_CONFLICT)

#         user = User.objects.create_superuser(username=username, email=email, password=password)
#         return Response({"success": f"Admin user {username} created successfully."}, status=status.HTTP_201_CREATED)

# from django.contrib.auth import get_user_model
# from rest_framework import views, status
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny

# User = get_user_model()

# class AdminCreateAPIView(views.APIView):
#     permission_classes = [AllowAny]  # Consider using more restrictive permissions in production

#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")
#         name = request.data.get("name")  # Assuming 'name' might also be used as a display name

#         if not all([email, password]):
#             return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             return Response({"error": "This email is already used."}, status=status.HTTP_409_CONFLICT)

#         user = User.objects.create_superuser(email=email, password=password, name=name)  # Ensure your create_superuser method supports these fields
#         return Response({"success": f"Admin user with email {email} created successfully."}, status=status.HTTP_201_CREATED)


# class AdminCreateAPIView(views.APIView):
#     permission_classes = [AllowAny]  # Ensure you have the appropriate permissions in production

#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")
#         name = request.data.get("name")  # Assuming 'name' is also a required field
#         tc = request.data.get("tc")  # Retrieve the tc value from request data

#         if not all([email, password, tc]):
#             return Response({"error": "Email, password, and tc are required."}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             return Response({"error": "This email is already used."}, status=status.HTTP_409_CONFLICT)

#         user = User.objects.create_superuser(email=email, password=password, name=name, tc=tc)  # Pass the tc field here
#         return Response({"success": f"Admin user {email} created successfully."}, status=status.HTTP_201_CREATED)




# from rest_framework.permissions import IsAdminUser
# User = get_user_model()

# class AdminChangePasswordAPIView(views.APIView):
#     permission_classes = [IsAdminUser]

#     def post(self, request):
#         username = request.data.get("username")
#         new_password = request.data.get("new_password")
#         if not all([username, new_password]):
#             return Response({"error": "Both username and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(username=username)
#             user.set_password(new_password)
#             user.save()
#             return Response({"success": "Password updated successfully."}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


# class AdminChangePasswordAPIView(views.APIView):
#     # permission_classes = [IsAdminUser]
#     permission_classes = [AllowAny]  # Not recommended for sensitive operations

#     def post(self, request):
#         email = request.data.get("email")
#         new_password = request.data.get("new_password")

#         if not all([email, new_password]):
#             return Response({"error": "Email and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)  # Use email to identify the user
#             user.set_password(new_password)
#             user.save()
#             return Response({"success": "Password updated successfully for email: " + email}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

# views.py
# from django.http import HttpResponse
# from .utils import send_email_via_smtp

# def send_test_email(request):
#     send_email_via_smtp(
#         '18251598-111@uog.edu.pk',
#         'Test Email',
#         'This is a test email from Django.'
#     )
#     return HttpResponse("Email sent successfully!")


# from django.core.mail import EmailMessage, get_connection


# from django.conf import settings

# def send_email(request):  
#    if request.method == "POST": 
#        with get_connection(  
#            host=settings.EMAIL_HOST, 
#      port=settings.EMAIL_PORT,  
#      username=settings.EMAIL_HOST_USER, 
#      password=settings.EMAIL_HOST_PASSWORD, 
#      use_tls=settings.EMAIL_USE_TLS  
#        ) as connection:  
#            subject = request.POST.get("subject")  
#            email_from = settings.EMAIL_HOST_USER  
#            recipient_list = [request.POST.get("email"), ]  
#            message = request.POST.get("message")  
#            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()  
 
#    return render(request, 'home.html')



# from django.core.mail import EmailMessage, get_connection
# from django.core.mail import *
# from django.views.generic.edit import CreateView
# from django.urls import reverse_lazy
# from .forms import PricingEstimateForm

# class PricingEstimateCreateView(CreateView):
#     model = PricingEstimate
#     form_class = PricingEstimateForm
#     template_name = 'pricing_estimate_form.html'  # Path to your template
#     success_url = reverse_lazy('create_pricing_estimate')

#     def form_valid(self, form):
#         # Here you can add additional logic if needed before saving the form
#         return super().form_valid(form)


# from django.shortcuts import render
# from django.core.mail import send_mail
# from .forms import PricingEstimateForm  # Make sure to import the correct form

# def pricing_estimate_view(request):
#     if request.method == 'POST':
#         form = PricingEstimateForm(request.POST)
#         if form.is_valid():
#             # Assuming the form saves the data to a model
#             estimate = form.save()

#             send_mail(
#                 'New Pricing Estimate Submitted',
#                 f'A new pricing estimate has been submitted by {estimate.contact_information}.',  # Adjust based on actual model fields
#                 '18251598-111@uog.edu.pk',
#                 ['noumanlatifm@gmail.com'],  # Adjust recipient as needed
#                 fail_silently=False,
#             )
#             return render(request, 'estimate_success.html')
#     else:
#         form = PricingEstimateForm()

#     return render(request, 'estimate.html', {'form': form})


# from django.shortcuts import redirect
# from .models import PricingEstimate
# from .utils import send_model_data_via_email

# def send_model_data_view(request):
#     my_instance = PricingEstimate.objects.get(id=1)
#     send_model_data_via_email(my_instance)
#     return redirect('success_page')

