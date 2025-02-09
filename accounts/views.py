from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from .models import User , OTP
from django.contrib.auth import authenticate, login , logout
import random 
# for otp send
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.db import IntegrityError
from django.conf import settings
import os
from blogs.models import Blog


def home(request):
    if request.user.is_authenticated:  # Corrected spelling
        blogs = Blog.objects.all()
        return render(request, 'accounts/home.html' , {'blogs' : blogs})
    else:
        return redirect('loginuser')
    
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'accounts/login.html')

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            otp_code = random.randint(100000 , 999999)
            try :
                 if otp_code is not None :
                    otp_object = OTP.objects.create(
                         user = user,
                         code = otp_code
                     )
                    # print(otp_object)
                    print(user)
                    print(otp_code)
                    # print(user.first_name)
                    subject = "🔐 Your One-Time Password (OTP) for Login"
                    # Render email HTML content
                    html_message = render_to_string('accounts/otp_email.html', {'user': user, 'otp_code': otp_code})
                    plain_message = strip_tags(html_message)

                    # send_mail( "🔐 Your One-Time Password (OTP) for Login" , otp_code, 'abhaynaravday123@gmail.com', ["abhaynarvade2@gmail.com"])
                    send_mail(
                        subject,
                        plain_message,  # Text version (for email clients that don’t support HTML)
                        'abhaynaravday123@gmail.com',  # Sender's email
                        [user.email],  # Receiver's email
                        html_message=html_message,  # HTML version
                        fail_silently=False,
                    )
                    request.session['otp_user_id'] = str(user.id)
                    return redirect('OTP_Verify')
                     
            except Exception as e :
                return HttpResponse(f'exception occure {e}')  # Replace 'dashboard' with your actual URL name



            # Log the user in
            # login(request, user)

            # Redirect to a success page or dashboard

        else:
            return HttpResponse(f"login post")
        

def register(request):
    if request.method == 'GET':
        return render(request, 'accounts/register.html')

    elif request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            mobileno = request.POST['mobileno']
            email = request.POST['email']
            profile_image = request.FILES.get('profile_image')

            # Initialize error dictionary
            error = {}

            # Validation checks for required fields
            if not username:
                error['username'] = 'Username is required'
            if not mobileno:
                error['mobileno'] = 'Mobile number is required'
            elif not mobileno.isdigit() or len(mobileno) != 10:
                error['mobileno'] = 'Mobile number must be 10 digits'
            if not password:
                error['password'] = 'Password is required'
            if not email:
                error['email'] = 'Email is required'

            # If there are validation errors, return them to the template
            if error:
                return render(request, 'accounts/register.html', {'error': error})

            # Create the user object (only if there are no validation errors)
            try:
                if profile_image:
                    user = User.objects.create(
                        username=username,
                        password=make_password(password),
                        mobileno=mobileno,
                        email=email,
                        profile_image=profile_image
                    )
                else:
                    user = User.objects.create(
                        username=username,
                        password=make_password(password),
                        mobileno=mobileno,
                        email=email
                    )
                # Save the user object to the database
                user.save()
                return redirect('loginuser')

            # Handle unique constraint errors
            except IntegrityError as e:
                if profile_image and profile_image.name:
                    file_path = os.path.join(settings.MEDIA_ROOT, 'profile_images', profile_image.name)
                    print(file_path)
                    if os.path.exists(file_path):
                        print("File exists. Proceeding to delete.")
                        try:
                            os.unlink(file_path)
                            print("File deleted successfully.")
                        except Exception as e:
                            print(f"Error deleting file: {e}")
                    else:
                        print("File does not exist.")
                if 'UNIQUE constraint failed' in str(e):
                    if 'mobileno' in str(e):
                        error['mobileno'] = 'Mobile number is already registered'
                    if 'email' in str(e):
                        error['email'] = 'Email is already registered'
                return render(request, 'accounts/register.html', {'error': error})

        except Exception as e:
            return HttpResponse(f'An exception occurred: {e}')


def OTP_Verify(request) :
    if request.method =="GET":
        return render(request , 'accounts/otp.html')
    elif request.method =="POST":

        otp =  request.POST.get('otp')
        user_id =  request.session.get('otp_user_id')
        if not user_id :
            return HttpResponse ('session Expire . Please Try Again')
        
        try :
            user = User.objects.get(id = user_id)
            otp_object = OTP.objects.filter(user=user, code = otp , is_used = False).first()
            if otp_object :
                otp_object.is_used = True
                otp_object.save()
                login(request , user)
                del request.session['otp_user_id']
                return redirect('home')
        except Exception as e :
                return HttpResponse('Invalid Credentials Try again ')


        
    return HttpResponse('OTP_Verify')


def logoutuser(request):
    logout(request)
    return redirect('home')


def profile(request):
    if request.user.is_authenticated:  # Corrected spelling
        return render(request, 'accounts/profile.html', {'user': request.user})
    else:
        return redirect('loginuser')