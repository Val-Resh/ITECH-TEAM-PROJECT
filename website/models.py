from django.db import models
from django.core.validators import *

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

    name = models.CharField(max_length = MAX_NAME_LENGTH)
    level = models.IntegerField(default=STARTING_LEVEL, validators=[MaxValueValidator(MAX_LEVEL),
                                           MinValueValidator(STARTING_LEVEL)])
    health = models.IntegerField(default=STARTING_HEALTH, validators=[MaxValueValidator(MAX_HP),
                                           MinValueValidator(0)])
    attack = models.IntegerField(default = STARTING_ATTACK, validators=[MaxValueValidator(MAX_AP),
                                           MinValueValidator(STARTING_ATTACK)])
    exp = models.IntegerField(default = 0, validators=[MaxValueValidator(MAX_EXP),
                                           MinValueValidator(0)])

    #method to level up a monster.
    def level_up(self):
        if self.level < self.MAX_LEVEL and self.exp == self.MAX_EXP:
            self.level += 1
            self.health += 100
            self.attack += 20
            self.exp = 0  


class User(models.Model):
    MAX_COINS = 1000
    MAX_PASSWORD_LENGTH = 30
    MAX_USERNAME_LENGTH = 30
    MAX_WINS = 15

    username = models.CharField(max_length = MAX_USERNAME_LENGTH)
    password = models.CharField(max_length = MAX_PASSWORD_LENGTH)
    wins = models.IntegerField(default = 0, validators=[MaxValueValidator(MAX_WINS),
                                           MinValueValidator(0)])
    monster = models.OneToOneField(Monster, on_delete=models.SET_NULL, default = None, null=True)
    coins = models.IntegerField(default = 0, validators=[MaxValueValidator(MAX_COINS),
                                           MinValueValidator(0)])

    #method to add coins to a User.
    def add_coins(self, coin_amount):
        if coin_amount > 0:
            self.coins = self.MAX_COINS if coin_amount > self.MAX_COINS \
                            else self.coins + coin_amount
