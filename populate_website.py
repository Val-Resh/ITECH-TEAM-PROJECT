
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech.settings')

import django
django.setup()

import random

from website.models import *

def populate():

    users = [
        {"username": "user1", "password": "password1"},
        {"username": "user2", "password": "password2"},
        {"username": "user3", "password": "password3"}, ]
    monsters = [{"name": "monster1"},
                {"name": "monster2"},
                {"name": "monster3"}]
    rooms = [{"name": "Natsukan Gym","image":"Natsukan_Gym.png"},
             {"name":"Navel Gym","image":"Navel_Gym.png"},
             {"name":"Trovita Gym","image":"Trovita_Gym.png"}]
    items = [
        {"name": "Grape", "price": 2, "effect_description": "HP", "effect": 10,"image":"Grape.png"},
        {"name": "Wepear Berry", "price": 5, "effect_description": "HP", "effect": 30,"image":"Wepear_Berry.png"},
        {"name": "Revive", "price": 10, "effect_description": "HP", "effect": 100,"image":"Revive.png"},
        {"name": "Potion", "price": 7, "effect_description": "ATK", "effect": 5,"image":"Potion.png"},
        {"name": "Hyper Potion", "price": 5,
            "effect_description": "ATK", "effect": 2,"image":"Hyper_Potion.png"},
        {"name": "Lucky Egg", "price": 1, "effect_description": "EXP", "effect": 10,"image":"Lucky_Egg.png"},
        {"name": "Icense", "price": 4, "effect_description": "EXP", "effect": 50,"image":"Icense.png"},
        {"name": "EXP Potion", "price": 10, "effect_description": "EXP", "effect": 150,"image":"EXP_Potion.png"},
    ]

    initialised_monsters = []
    initialised_rooms = []

    for monster in monsters:
        m = add_monster(monster["name"])
        initialised_monsters.append(m)
        print("monster {name} created".format(name=m.name))

    for room in rooms:
        r = add_room(room["name"],room["image"])
        initialised_rooms.append(r)
        print("room {name} created".format(name=r.name))

    for i in range(len(users)):
        user = users[i]
        u = add_user(user["username"], user["password"],
                     initialised_monsters[i], initialised_rooms[0])
        print("User with\n Username: {username}\n Monster: {monster}\n Coins: {coins}\n Room: {room}\n has been created!\n\n".
              format(username=u.username, monster=u.monster.name, coins=u.coins, room=u.room.name))

    for item in items:
        print(item)
        add_item(item["name"], item["image"],item["price"],
                 item["effect_description"], item["effect"])


def add_user(username, password, monster: Monster, room: Room):
    user = User.objects.get_or_create(username=username, password=password)[0]
    user.monster = monster
    user.coins = random.randrange(0, User.MAX_COINS)
    user.room = room
    user.save()
    return user


def add_monster(name):
    monster = Monster.objects.get_or_create(name=name)[0]
    monster.save()
    return monster


def add_room(name,image):
    room = Room.objects.get_or_create(name=name,image=image)[0]
    room.save()
    return room


def add_item(name, image,p=0, eff_des="", eff=0):
    item = Item.objects.get_or_create(
        name=name, image=image,price=p, effect_description=eff_des, effect=eff)[0]
    item.save()
    return item


if __name__ == "__main__":
    print("Starting website's populating script...")
    populate()
