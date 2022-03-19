from tokenize import blank_re
from django.test import TestCase
from django.contrib.auth.models import User
from website.models import *
import time

# test about class Users


class UsersTest(TestCase):
    # user's attributes test
    def test_attributes(self):
        user = User(username="username", password="password")
        self.assertEqual(user.username, "username")
        self.assertEqual(user.password, "password")
    # user's method add_coins() test

    def test_add_coins(self):
        user = User(username="username", password="password")
        userinfo = Users(user)
        self.assertEqual(userinfo.coins, 0)
        userinfo.add_coins(100)
        self.assertEqual(userinfo.coins, 100)
        userinfo.add_coins(10000000)
        self.assertEqual(userinfo.coins, userinfo.MAX_COINS)
        userinfo.coins = 0
        userinfo.add_coins(-1000)
        self.assertEqual(userinfo.coins, 0)

# test about class Monster


class MonsterTest(TestCase):
    # monster's attributes test
    def test_default_values(self):
        monster = Monster(name="monster")
        expected = ["monster", Monster.STARTING_LEVEL,
                    Monster.STARTING_HEALTH, Monster.STARTING_ATTACK, 0]
        testing = [monster.name, monster.level,
                   monster.health, monster.attack, monster.exp]
        for i in range(len(expected)):
            self.assertEqual(testing[i], expected[i])
    # monster's method level_up() test

    def test_level_up(self):
        monster = Monster(name="monster")
        monster.exp = Monster.MAX_EXP
        monster.level_up()
        expected = ["monster", Monster.STARTING_LEVEL+1,
                    Monster.STARTING_HEALTH+10, Monster.STARTING_ATTACK+5, 0]
        testing = [monster.name, monster.level,
                   monster.health, monster.attack, monster.exp]
        for i in range(len(expected)):
            self.assertEqual(testing[i], expected[i])
    # monster's method battle() test

    def test_battle(self):
        monster = Monster(name="monster", health=50, attack=10)
        monster2 = Monster(name="opponent", health=50, attack=5)
        result = monster.battle(monster2)
        if monster.health > 0:
            self.assertTrue(result)
        else:
            self.assertFalse(result)

# test about user choose a monster


class GiveUserMonsterTest(TestCase):

    def test_give_monster(self):
        user = Users()
        monster = Monster(name="monster")
        monsterTwo = Monster(name="monsterTwo")
        user.monster = monster
        self.assertTrue(user.monster == monster)

# test about user buy item


class UserBuyItemView(TestCase):
    def test_buy_item(self):
        user = Users()
        monster = Monster(name="monster")
        user.monster = monster
        user.add_coins(1000)
        # item's effect description test
        eff_des_list = ['ATK', 'HP', 'EXP']
        for eff_des in range(len(eff_des_list)):
            item = Item(name="item", price=50,
                        effect_description=eff_des, effect=10)
            coins = user.coins
            user.buy_item(item)
            self.assertEqual(user.coins, coins-item.price)
            if eff_des == 'ATK':
                self.asserfEqual(user.monster.attack,
                                 Monster.STARTING_ATTACK+10)
            elif eff_des == 'HP':
                self.asserfEqual(user.monster.health,
                                 Monster.STARTING_HEALTH+10)
            elif eff_des == 'EXP':
                self.asserfEqual(user.monster.exp, 10)
        # coins and price test
        item = Item(name="item", price=50,
                    effect_description=eff_des, effect=10)
        user.coins = 60
        self.assertEqual(user.buy_item(
            item), "Buy an item successfully. Your monster stats were upgraded.")
        user.coins = 50
        self.assertEqual(user.buy_item(
            item), "Buy an item successfully. Your monster stats were upgraded.")
        user.coins = 20
        self.assertEqual(user.buy_item(item), "Insufficient coins.")

# test user join a room


class AddUserToRoomTest(TestCase):
    # user's methond add_room() test
    def test_add_room(self):
        user = Users()
        room = Room(name="room")
        self.assertEqual(user.add_room(room), "Added")
        room.USERS_IN_ROOM = 5
        self.assertEqual(user.add_room(room), "Full")

# test user exit a room


class UserExitRoomVie(TestCase):
    # user's method exit_room() test
    def test_exit_room(self):
        user = Users()
        room = Room(name="room")
        self.assertEqual(user.exit_room(), "Not in room")
        user.add_room(room)
        print("calculate coins ...")
        time.sleep(61)
        user.exit_room()
        self.assertEqual(user.coins, 1)
        self.assertEqual(user.room, None)
        self.assertEqual(room.USERS_IN_ROOM, 0)

# test about class Item


class ItemTest(TestCase):
    # test item's attributes
    def test_create(self):
        item = Item(name="item", price=50, effect_description="something")
        self.assertIsNotNone(item.price)
        self.assertEqual(item.name, "item")

# test about Battle


class BattleTest(TestCase):
    # user's method battle_user() test
    def test_battle(self):
        user = Users()
        user2 = Users()
        monster = Monster(name="m")
        monster2 = Monster(name="c")
        user1coins = user.coins
        user2coins = user2.coins
        user.monster = monster
        user2.monster = monster2
        user.battle_user(user2)
        self.assertTrue((user1coins != user.coins)
                        or (user2coins != user2.coins))
