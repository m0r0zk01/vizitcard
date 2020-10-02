from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, logout, login, get_user
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Q
from vizitcard.settings import EMAIL_HOST_USER, TOKEN_LIFETIME
from app.models import User, Token
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status


def get_context(request):
    return {
        'user': request.user
    }


def index(request):
    return render(request, 'index.html', context=get_context(request))


@api_view(['POST'])
def register(request):
    username = request.POST['username']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    email = request.POST['email']
    errors = {'username': [], 'password': [], 'email': [], 'confirm': []}
    if User.objects.filter(username=username).count():
        errors['username'].append('Имя занято')
    if User.objects.filter(email=email).count():
        errors['email'].append('Почта занята')
    if not (5 <= len(username) <= 20):
        errors['username'].append('Длина имени от 5 до 20 плиз')
    if not (8 <= len(password) <= 30):
        errors['password'].append('Длина пароля от 8 до 30 плиз')
    if password != confirm_password:
        errors['confirm'].append('Пароли не совпадают')

    for i in errors.items():
        if len(i[1]):
            return Response(errors, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_active = False
    user.save()
    print('saved')

    token = Token.objects.create(user=user, token_type="activation")
    text = f'Hey, this is vizitcard bot! Go to this link: 127.0.0.1:8000/activate/{token.token} to activate your account'
    send_mail('vizitcard', '', None, [email], html_message=text)
    token.save()

    return Response(b'', status=200)


def validate_user(request, token):
    try:
        token_obj = Token.objects.get(token=token, token_type='activation')
    except Token.DoesNotExist:
        return HttpResponse('Wrong token')
    if token_obj.creation_date + timedelta(days=TOKEN_LIFETIME) > timezone.now():
        user = token_obj.user
        user.is_active = True
        user.save()
    token_obj.delete()
    return redirect('/')


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            user = None
        token = Token.objects.create(token_type='forgot_password', user=user)
        text = f'Hey, you requested password change! Go to this link: 127.0.0.1:8000/forgot_password/{token.token} to activate your account'
        send_mail('vizitcard', '', None, [user.email], html_message=text)
        token.save()
    return render(request, 'forgot_password.html')


def new_password(request, token):
    try:
        token_obj = Token.objects.get(token=token, token_type='forgot_password')
    except Token.DoesNotExist:
        return HttpResponse('Неправильный токен')
    if token_obj.creation_date + timedelta(days=TOKEN_LIFETIME) < timezone.now():
        token_obj.delete()
        return HttpResponse('Время жизни токена закончилось')
    if request.method == 'GET':
        return render(request, 'new_password.html')
    elif request.method == 'POST':
        password = request.POST['password']
        confirm = request.POST['confirm']
        user = token_obj.user
        if password != confirm:
            return HttpResponse('Пароли не совпадают')
        user.set_password(password)
        user.save()
        token_obj.delete()
        return redirect('/')


@api_view(['POST'])
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            return Response('Пользователь не активирован, пожалуйста, проверить почту и перейдите по ссылке из нашего письма', status=400)
    else:
        return Response('Неправильное имя пользователя или пароль', status=400)
    return Response(b'', status=200)


@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')


def profile(request):
    if request.method == 'POST':
        pass
    return render(request, 'profile.html', get_context(request))
