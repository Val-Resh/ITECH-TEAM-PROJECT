from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from website.forms import UserForm, RoomForm
from django.http import HttpResponse
from django.urls import reverse
from website.models import Room, Item


def index(request):
    form = RoomForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/')
        else:
            print(form.errors)

    room_list = Room.objects.order_by('-name')[:4]
    return render(request, 'index.html', {'form': form, 'rooms': room_list})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>'] # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        print(username, password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                print(user)
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return render(request, 'login.html', {
                'login_message': 'Enter the username and password incorrectly', })

    else:
        return render(request, 'login.html')


def register(request):
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':

        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return redirect('/login')
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request, 'register.html', context={'user_form': user_form})


@login_required
def shop(request):
    item_list = Item.objects.order_by('-name')
    return render(request, 'shop.html', {'items': item_list})


@ login_required
def room(request):
    return render(request, 'room.html')


@ login_required
def userprofile(request):
    return render(request, 'user-profile.html')


@ login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('index'))
