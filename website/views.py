from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def shop(request):
    return render(request, 'shop.html')


def room(request):
    return render(request, 'room.html')


def userprofile(request):
    return render(request, 'user-profile.html')
