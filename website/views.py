from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from website.forms import UserForm, RoomForm
from django.http import HttpResponse
from django.urls import reverse
from website.models import Room, Item, Monster, User
from django.views.decorators.http import *

from django.utils.decorators import method_decorator

from django.views import View

import re

MONSTER_LISTS = [{"index":0,"name": "Pikachu", "health": "100", "attack": "10","image":"Pikachu.png"},
                 {"index":1,"name": "Squirtle", "health": "110", "attack": "8","image":"Squirtle.png"},
                 {"index":2,"name": "Eevee", "health": "80", "attack": "12","image":"eevee.png"},
                 {"index":3,"name": "Charmander", "health": "90", "attack": "9","image":"Charmander.png"},
                 {"index":4,"name": "Bulbasaur", "health": "110", "attack": "10","image":"Bulbasaur.png"}]


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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                print(user)
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
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

    return render(request, 'room.html', {'room': room, 'users': users_in_room})


@login_required
def userprofile(request):
    username = request.user.username
    user = User.objects.get(username=username)
    return render(request, 'user-profile.html', {'monster': user.monster})


@login_required
def user_logout(request):
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

        return redirect(request.META['HTTP_REFERER'])


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

        message = user.exit_room()
        user.save()
        return HttpResponse(message)


class UserChooseMonsterView(View):
    @method_decorator(login_required)
    def get(self, request):
        username = request.user.username
        monster_id = request.GET['monster_index']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        m = MONSTER_LISTS[int(monster_id)]
        monster = Monster.objects.create(
            name=m['name'], level=1, exp=0, attack=m['attack'], health=m['health'],image=m['image'])
        user.monster = monster
        user.save()
        return redirect('/userprofile')


class UserBuyItemView(View):
    @method_decorator(login_required)
    def get(self, request):
        username = request.user.username
        item_id = request.GET['item_id']

        try:
            item = Item.objects.get(id=item_id)
        except User.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        # add coin to test
        # message = user.add_coins(100)
        message = user.buy_item(item)
        user.save()
        return HttpResponse(message)


def battle_user(request):
    opponent_id = request.body.decode('UTF-8').strip(" ")
    this_id = request.user.id

    this_user = User.objects.get(id=this_id)
    opponent_user = User.objects.get(id=opponent_id)
    
    winner = this_user.battle_user(opponent_user)
    winner.save()
    return HttpResponse(winner.username)
