from django.test import TestCase
from website.models import *

class UserTest(TestCase):

    def test_attributes(self):
        user = User(username="username", password="password")
        self.assertEqual(user.username, "username")
        self.assertEqual(user.password, "password")

    def test_add_coins(self):
        user = User(username="username", password="password")
        self.assertEqual(user.coins, 0)
        user.add_coins(100)
        self.assertEqual(user.coins, 100)
        user.add_coins(10000000)
        self.assertEqual(user.coins, user.MAX_COINS)
        user.coins = 0
        user.add_coins(-1000)
        self.assertEqual(user.coins, 0)

class MonsterTest(TestCase):
    
    def test_default_values(self):
        monster = Monster(name="monster")
        expected = ["monster", Monster.STARTING_LEVEL, Monster.STARTING_HEALTH, Monster.STARTING_ATTACK, 0]
        testing = [monster.name, monster.level, monster.health, monster.attack, monster.exp]
        for i in range(len(expected)):
            self.assertEqual(testing[i], expected[i])
    
    def test_level_up(self):
        monster = Monster(name="monster")
        monster.exp = Monster.MAX_EXP
        monster.level_up()
        expected = ["monster", Monster.STARTING_LEVEL+1, Monster.STARTING_HEALTH+100, Monster.STARTING_ATTACK+20, 0]
        testing = [monster.name, monster.level, monster.health, monster.attack, monster.exp]
        for i in range(len(expected)):
            self.assertEqual(testing[i], expected[i])

class GiveUserMonsterTest(TestCase):

    def test_give_monster(self):
        user = User(username="username", password="password")
        monster = Monster(name="monster")
        monsterTwo = Monster(name="monsterTwo")
        user.monster = monster
        self.assertTrue(user.monster == monster)

class AddUserToRoomTest(TestCase):
    
    def test_add_room(self):
        user = User(username="username", password="password")
        room = Room(name="room")
        self.assertEqual(user.add_room(room), "Added")
        room.USERS_IN_ROOM = 5
        self.assertEqual(user.add_room(room), "Full")

class ItemTest(TestCase):

    def test_create(self):
        item = Item(name="item", price=50, effect_description="something")
        self.assertIsNotNone(item.price)
        self.assertEqual(item.name, "item")