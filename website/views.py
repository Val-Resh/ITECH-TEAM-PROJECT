from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from website.forms import UserForm, RoomForm
from django.http import HttpResponse
from django.urls import reverse
from website.models import Room, Item, Monster, User

from django.utils.decorators import method_decorator

from django.views import View

MONSTER_LISTS = [{"index": 0, "name": "Pika", "health": "100", "attack": "10"},
                 {"index": 1, "name": "Liza", "health": "120", "attack": "8"},
                 {"index": 2, "name": "Eevee", "health": "80", "attack": "12"}]


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


@login_required
def monster(request):
    return render(request, 'monster.html', {'monsters': MONSTER_LISTS})


@login_required
def room(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        room = None
        # return redirect(reverse('room', kwargs={'room_name_slug': room_name_slug}))

    try:
        users_in_room = User.objects.filter(room=room)
    except User.DoesNotExist:
        users_in_room = None
    print(users_in_room)

    return render(request, 'room.html', {'room': room, 'users': users_in_room})


@login_required
def userprofile(request):
    username = request.user.username
    user = User.objects.get(username=username)
    return render(request, 'user-profile.html', {'monster': user.monster})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('index'))


#
class UserJoinRoomView(View):
    @method_decorator(login_required)
    def get(self, request):
        username = request.user.username
        room_name = request.GET['room_name']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        user.add_room(room)
        user.save()
        return HttpResponse(room)


class UserExitRoomView(View):
    @method_decorator(login_required)
    def get(self, request):
        username = request.user.username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        user.exit_room()
        user.save()
        return HttpResponse(user.room)


class UserChooseMonsterView(View):
    @method_decorator(login_required)
    def get(self, request):
        username = request.user.username
        monster_id = request.GET['monster_index']
        print(monster_id)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        m = MONSTER_LISTS[int(monster_id)]
        print(m)
        monster = Monster.objects.create(
            name=m['name'], level=1, exp=0, attack=m['attack'], health=m['health'])

        user.monster = monster
        user.save()
        print('monster', user.monster)
        return HttpResponse(user)
