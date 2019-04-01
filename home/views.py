from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse

# Create your views here.


def indexview(request):
    return render(request, 'index.html')


def signinview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username= username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dashboard'))
                else:
                    login(request, user)
                    return HttpResponseRedirect(reverse('prog_dash'))
            else:
                messages.error(request, 'Username and password did not matched')
        except:
            pass
    return render(request, 'signin.html')


def signupview(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_active_email.html', {
                'registration': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            mess = "A Verification link sent to your Email Please confirm the link to register..."
            return render(request, 'index.html', {'register':mess})
    else:
        form = UserSignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return HttpResponse("invalid...", user)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        mess = "Email activation success. Please Login..."
        return render(request, 'index.html', {'activated':mess})
    else:
        return HttpResponse('Activation link is invalid!')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('indexview'))
