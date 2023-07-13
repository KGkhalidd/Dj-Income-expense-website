from django.shortcuts import render
from django.views import View 
import json
from django.http import JsonResponse
from django.contrib.auth.models import User 
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import redirect


from django.urls import reverse
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
#force_bytes takes a Unicode string and returns a byte string, 
#while force_text takes a byte string and returns a Unicode string.
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
#They are often used in Django when encoding and decoding data for use in URLs 
# or other contexts where special characters must be avoided.
from django.contrib.sites.shortcuts import get_current_site
#used to retrieve the current site object that is associated with the current request.
#This function is often used when generating URLs or links that include the current site's domain or other information.

from .utils import token_generator


# Create your views here.

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters!'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'sorry username in use, choose another one'}, status=409)
        
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid!'}, status=400)
                    # 1-email : the name of the field in the User model 'in db'
                    # 2-email : the variable that holds the value extracted from the request
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'sorry email in use, choose another one'}, status=409)
        
        return JsonResponse({'email_valid': True})



class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        # messages.success(request, 'Success whatsapp success')
        # messages.warning(request, 'Success whatsapp warning')
        # messages.info(request, 'Success whatsapp info')
        # messages.error(request, 'Success whatsapp error')
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context={
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username):
            if not User.objects.filter(email=email):
                if len(password) < 6:
                    messages.error(request , 'Password too short! ')
                    return render(request,'authentication/register.html' , context)
                
                user= User.objects.create_user(username=username , email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                
                uidb64= urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link= reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                activate_url = 'http://'+domain+link

                email_subject= "Activate your account!"
                email_body= f"Hi {user.username}, " + 'Please use this link to verify your account\n'+activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "khaledgamal1345@gmail.com",
                    [user.email],
                )

                email.send(fail_silently=False )
                messages.success(request, 'Account created successfully!')
                return render(request, 'authentication/register.html')



        return render(request, 'authentication/register.html')



class VerificationView(View):
    def get(self,request, uidb64, token):

            
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
                
            
            
            if not token_generator.check_token(user, token):
                messages.warning(request,'User already activated')
                
            
            elif user.is_active:
                messages.warning(request,'User already activated')
                

            elif user is not None and token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Account activated successfully')
                
                
            else:
                messages.error(request, 'Activation link is invalid!')
                
            
        
            return redirect('login')
    



class LoginView(View):
    def get(self,request):
        return render(request, 'authentication/login.html')

