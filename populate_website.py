import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech.settings')

import django
django.setup()

from django.contrib.auth.models import User
from website.models import *
import random


def populate():

    monsters = [{'name': "Pikachu", 'picture': "/monster_images/Pikachu.png"},
                {'name': "Eevee", 'picture': "/monster_images/Eevee.png"},
                {'name': "Charmander", 'picture': "/monster_images/Charmander.png"}]

    items = [
        {"name": "Grape", "price": 2, "effect_description": "HP",
            "effect": 10, "picture": "/item_images/Grape.png"},
        {"name": "Wepear Berry", "price": 5, "effect_description": "HP",
            "effect": 30, "picture": "/item_images/Wepear_Berry.png"},
        {"name": "Revive", "price": 10, "effect_description": "HP",
            "effect": 100, "picture": "/item_images/Revive.png"},
        {"name": "Potion", "price": 7, "effect_description": "ATK",
            "effect": 5, "picture": "/item_images/Potion.png"},
        {"name": "Hyper Potion", "price": 5, "effect_description": "ATK",
            "effect": 2, "picture": "/item_images/Hyper_Potion.png"},
        {"name": "Lucky Egg", "price": 1, "effect_description": "EXP",
            "effect": 10, "picture": "/item_images/Lucky_Egg.png"},
        {"name": "Icense", "price": 4, "effect_description": "EXP",
            "effect": 50, "picture": "/item_images/Icense.png"},
        {"name": "EXP Potion", "price": 10, "effect_description": "EXP",
            "effect": 150, "picture": "/item_images/EXP_Potion.png"},
    ]

    initialised_monsters = []

    for item in items:
        print(item)
        add_item(item["name"], item["price"],
                 item["effect_description"], item["effect"], item['picture'])

    for monster in monsters:
        m = add_monster(monster["name"], monster["picture"])
        initialised_monsters.append(m)
        print("monster {name} created".format(name=m.name))


def add_monster(name, picture):
    monster = MonsterList.objects.get_or_create(name=name, picture=picture)[0]
    monster.save()
    return monster


def add_item(name, p=0, eff_des="", eff=0, pic=""):
    item = Item.objects.get_or_create(
        name=name, price=p, effect_description=eff_des, effect=eff, picture=pic)[0]
    item.save()
    return item


if __name__ == "__main__":
    print("Starting website's populating script...")
    populate()
