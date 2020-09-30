from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    pass


def login(request):
    pass
