from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def shop(request):
    return render(request, 'shop.html')

def userprofile(request):
    return render(request, 'User profile.html')

def room(request):
    return render(request, 'room.html')