from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import *
from django.utils.decorators import method_decorator
from django.views import View
from website.models import Users, Monster, MonsterList, Item, Room
from website.forms import UserForm,  UserProfileForm
from website.forms import RoomForm


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

    room_list = Room.objects.order_by('-name')
    for i in range(len(room_list)):
        room_list[i].image_id = (i % 7)+1
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
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


@login_required
def user_logout(request):
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('index'))


@login_required
def userprofile(request):
    user = request.user
    userinfo = Users.objects.get(user=user)
    mon = userinfo.monster
    return render(request, 'user-profile.html', {'coins': userinfo.coins,
                                                 'wins': userinfo.wins,
                                                 'picture': userinfo.picture,
                                                 'mon': mon})


@login_required
def monster_list(request):
    monsters = MonsterList.objects.all()
    return render(request, 'monster.html', {'monsters': monsters})


@login_required
def shop(request):
    item_list = Item.objects.order_by('-name')
    user = request.user
    userinfo = Users.objects.get(user=user)
    mon = userinfo.monster
    return render(request, 'shop.html', {'items': item_list,
                                         'mon': mon})


@login_required
def room(request, room_name):

    try:
        user = request.user
        userinfo = Users.objects.get(user=user)
    except Users.DoseNotExist:
        return redirect('/login')

    try:
        mon = userinfo.monster
    except mon.DoseNotExist:
        mon = None

    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        return redirect('/')

    try:
        users_in_room = Users.objects.filter(room=room)
    except Users.DoesNotExist:
        users_in_room = None

    return render(request, 'room.html', {'room': room,
                                         'userinfo': userinfo,
                                         'mon': mon,
                                         'users': users_in_room})


@login_required
def battle(request):
    user = request.user
    userinfo = Users.objects.get(user=user)
    opponent_user_name = request.POST.get('opponent_user_name')
    opponent_user = User.objects.get(username=opponent_user_name)
    opponent_userinfo = Users.objects.get(user=opponent_user)

    winner = userinfo.battle_user(opponent_userinfo)
    winner.save()
    return render(request, 'battle.html', {'userinfo': userinfo,
                                           'opponent_userinfo': opponent_userinfo,
                                           'winner': winner.user.username})


#
class UserChooseMonsterView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        monster_index = request.GET['monster_index']
        try:
            userinfo = Users.objects.get(user=user)
        except Users.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        m = MonsterList.objects.get(id=monster_index)
        selected_monster = Monster.objects.create(
            name=m.name, picture=m.picture, level=m.level, health=m.health, attack=m.attack, exp=m.exp)
        userinfo.monster = selected_monster
        userinfo.save()
        return redirect('/userprofile')


class UserBuyItemView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        item_id = request.GET['item_id']

        try:
            item = Item.objects.get(id=item_id)
        except Users.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        try:
            userinfo = Users.objects.get(user=user)
        except Users.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        # add coin to test
        # userinfo.add_coins(100)

        message = userinfo.buy_item(item)
        userinfo.save()
        return HttpResponse(message)


class UserJoinRoomView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        room_name = request.GET['room_name']
        try:
            userinfo = Users.objects.get(user=user)
        except Users.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        userinfo.add_room(room)
        userinfo.save()

        return redirect(request.META['HTTP_REFERER'])


class UserExitRoomView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        try:
            userinfo = Users.objects.get(user=user)
        except Users.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        message = userinfo.exit_room()
        userinfo.save()
        return HttpResponse(message)
