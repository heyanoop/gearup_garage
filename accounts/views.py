from django.shortcuts import render, redirect, HttpResponse
from .forms import UserRegistration
from accounts.models import account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from user_dashboard.views import validate_password_complexity

# Create your views here.
def register(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            username = email.split("@")[0]
            if not validate_password_complexity(password):
                messages.error(request, 'New password must contain at least 8 characters, including at least one letter, one number, and one special character')
                return redirect('register')
            
            user = account.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.phone_number = phone_number
            user.save()
            
            # user activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_mail.html',{
                'user'  : user,
                'domain': current_site,
                'uid'   : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
                    
            messages.success(request, 'Activation link has been sent to mail, please verify to finish registration process')
            return redirect('register')
    
    else:
        form = UserRegistration()
    context = {
        'form' : form
        }
    return render (request, 'accounts/register.html', context)

def login(request):
   
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            if user.is_admin:   
                auth.login(request, user)
                return redirect('admin_dash')
            else:
                auth.login(request, user)
                return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    return render(request, 'accounts/login.html')


@login_required(login_url= login  )
def logout(request):
    auth.logout(request)
    messages.success(request, "You are Logged out")
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been verifed, Welcome to gearup garage ')
        return redirect('login')
    else:
        messages.error(request, 'invalid activation link, please try again')
        return redirect('register')
    
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if account.objects.filter(email=email).exists():
            user = account.objects.get(email__iexact=email)
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset link has been sent to your email')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist in the database')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please Reset Your Password")
        return redirect('reset_password')
    else:
        messages.error(request, "The link is expired")
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        if not validate_password_complexity(password):
            messages.error(request, 'New password must contain at least 8 characters, including at least one letter, one number, and one special character')
            return redirect('reset_password')
            
        if password == confirm_password:
            uid = request.session.get('uid')
            user = account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'password does not match')
            return redirect('reset_password')
    else:       
        return render(request, 'accounts/reset_password.html')
    
    
    
