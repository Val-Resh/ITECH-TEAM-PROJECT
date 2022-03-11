from django.db import models
from django.conf import settings
from django.core.validators import *
from django.contrib.auth.models import AbstractUser
import random

# Create your models here.


class Monster(models.Model):
    MAX_NAME_LENGTH = 30
    MAX_LEVEL = 5
    MAX_HP = 500
    MAX_AP = 100
    MAX_EXP = 1000
    STARTING_HEALTH = MAX_HP / MAX_LEVEL
    STARTING_LEVEL = MAX_LEVEL / MAX_LEVEL
    STARTING_ATTACK = MAX_AP / MAX_LEVEL

    name = models.CharField(max_length=MAX_NAME_LENGTH)
    level = models.IntegerField(default=STARTING_LEVEL, validators=[MaxValueValidator(MAX_LEVEL),
                                                                    MinValueValidator(STARTING_LEVEL)])
    health = models.IntegerField(default=STARTING_HEALTH, validators=[MaxValueValidator(MAX_HP),
                                                                      MinValueValidator(0)])
    attack = models.IntegerField(default=STARTING_ATTACK, validators=[MaxValueValidator(MAX_AP),
                                                                      MinValueValidator(STARTING_ATTACK)])
    exp = models.IntegerField(default=0, validators=[MaxValueValidator(MAX_EXP),
                                                     MinValueValidator(0)])

    # method to level up a monster.
    def level_up(self):
        if self.level < self.MAX_LEVEL and self.exp >= self.MAX_EXP:
            self.level += 1
            self.health += 100
            self.attack += 20
            self.exp = 0

    # battles an opponent monster.
    # returns true if won, false otherwise.
    def battle(self, monster):
        monster1_health = self.health
        monster2_health = monster.health

        while(monster1_health > 0 or monster2_health > 0):
            monster2_health -= random.randrange(
                round(self.attack/3), self.attack)
            if(monster2_health <= 0):
                break
            monster1_health -= random.randrange(
                round(monster.attack/3), monster.attack)

        return True if monster1_health > 0 else False


class Room(models.Model):
    MAX_USERS = 5
    MAX_NAME_LENGTH = 30
    USERS_IN_ROOM = 0

    name = models.CharField(unique=True, max_length=MAX_NAME_LENGTH)


class Item(models.Model):
    MAX_NAME_LENGTH = 30
    MAX_PRICE = 500
    MAX_EFFECT_DESCRIPTION = 30

    name = models.CharField(unique=True, max_length=MAX_NAME_LENGTH)
    price = models.IntegerField(validators=[MaxValueValidator(MAX_PRICE,
                                            MinValueValidator(0))])
    effect_description = models.CharField(
        null=False, max_length=MAX_EFFECT_DESCRIPTION)
    effect = models.IntegerField(null=False)


class User(AbstractUser):
    MAX_COINS = 1000
    MAX_PASSWORD_LENGTH = 30
    MAX_USERNAME_LENGTH = 30
    MAX_WINS = 15

    username = models.CharField(unique=True, max_length=MAX_USERNAME_LENGTH)
    password = models.CharField(max_length=MAX_PASSWORD_LENGTH)
    wins = models.IntegerField(default=0, validators=[MaxValueValidator(MAX_WINS),
                                                      MinValueValidator(0)])
    monster = models.OneToOneField(
        Monster, on_delete=models.SET_NULL, default=None, null=True)
    coins = models.IntegerField(default=0, validators=[MaxValueValidator(MAX_COINS),
                                                       MinValueValidator(0)])
    room = models.ForeignKey(
        Room, null=True, on_delete=models.SET_NULL, default=None)

    class Meta:
        app_label = 'website'

    # method to add a room.
    def add_room(self, room: Room):
        if room.USERS_IN_ROOM < room.MAX_USERS:
            self.room = room
            room.USERS_IN_ROOM += 1
            return "Added"
        else:
            return "Full"

    def exit_room(self):
        if self.room:
            room = self.room
            room.USERS_IN_ROOM -= 1
            self.room = None
            return "Removed"
        else:
            return "Not in room"

    # method to add coins to a User.
    def add_coins(self, coin_amount):
        if coin_amount > 0:
            self.coins = self.MAX_COINS if coin_amount > self.MAX_COINS \
                else self.coins + coin_amount
        return "Added"

    # battle against another user:
    def battle_user(self, opponent):
        result = self.monster.battle(opponent.monster)
        if result is True:
            self.add_coins(100)
            return self
        else:
            opponent.add_coins(100)
            return opponent

    def buy_item(self, item: Item):
        if item.price <= self.coins:
            eff = item.effect_description
            amount = item.effect
            if eff == 'ATK':
                self.monster.attack += amount
            elif eff == 'HP':
                self.monster.health += amount
            elif eff == 'EXP':
                self.monster.exp += amount
                self.monster.level_up()

            self.coins -= item.price
            self.monster.save()

            return "Buy an item successfully. Your monster stats were upgraded."
        else:
            return "Insufficient coins."
