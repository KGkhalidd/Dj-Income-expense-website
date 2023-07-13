from django.urls import path
from .views import RegistrationView, UsernameValidationView, EmailValidationView, VerificationView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', RegistrationView.as_view() , name='register'),
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()) , name='validate-username'),
    path('validate_email/', csrf_exempt(EmailValidationView.as_view()) , name='validate-email'),
    path('activate/<uidb64>/<token>', csrf_exempt(VerificationView.as_view()) , name='activate'),
    
]