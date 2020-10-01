from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from vizitcard.settings import EMAIL_HOST_USER, TOKEN_LIFETIME
from app.models import User, Token
from datetime import datetime, timedelta


def get_context(request):
    return {
        'user': request.user
    }


def index(request):
    return render(request, 'index.html', context=get_context(request))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        user.save()

        token = Token.objects.create(user=user)
        print(token.token, token.user)
        text = f'Hey, this is vizitcard bot! Go to this link: 127.0.0.1:8000/activate/{token.token} to activate your account'
        send_mail('vizitcard', '', None, [email], html_message=text)
        token.save()

        return redirect('/')
    return HttpResponse('wrong request type')


def validate_user(request, token):
    token_obj = Token.objects.get(token=token)
    print(token_obj.creation_date + timedelta(days=TOKEN_LIFETIME), type(token_obj.creation_date + timedelta(days=TOKEN_LIFETIME)))
    print(datetime.today(), type(datetime.today()))
    if token_obj.creation_date + timedelta(days=TOKEN_LIFETIME) > timezone.now():
        user = token_obj.user
        user.is_active = True
        user.save()
    token_obj.delete()
    return redirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('/')
    return HttpResponse('wrong request type')


@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')
