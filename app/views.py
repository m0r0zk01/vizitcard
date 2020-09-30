from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from app.models import User


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
        user.save()
        return redirect('/')
    return HttpResponse('wrong request type')


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
