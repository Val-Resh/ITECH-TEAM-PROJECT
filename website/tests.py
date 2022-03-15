from django.test import TestCase
from website.models import *
import time

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
    
class UserBuyItemView(TestCase):
    def test_buy_item(self):
        user=User(username="username",password="password")
        monster = Monster(name="monster")
        user.monster = monster
        user.add_coins(1000)
        eff_des_list=['ATK','HP','EXP']
        for eff_des in range(len(eff_des_list)):
            item = Item(name="item", price=50, effect_description=eff_des,effect=10)
            coins = user.coins
            user.buy_item(item)
            self.assertEqual(user.coins, coins-item.price)
            if eff_des == 'ATK':
                self.asserfEqual(user.monster.attack,Monster.STARTING_ATTACK+10) 
            elif eff_des == 'HP':
                self.asserfEqual(user.monster.health,Monster.STARTING_HEALTH+10) 
            elif eff_des == 'EXP':
                self.asserfEqual(user.monster.exp,10)
        
        item = Item(name="item", price=50, effect_description=eff_des,effect=10)
        user.coins=60
        self.assertEqual(user.buy_item(item),"Buy an item successfully. Your monster stats were upgraded.")
        user.coins=50
        self.assertEqual(user.buy_item(item),"Buy an item successfully. Your monster stats were upgraded.")
        user.coins=20
        self.assertEqual(user.buy_item(item),"Insufficient coins.")

class AddUserToRoomTest(TestCase):
    
    def test_add_room(self):
        user = User(username="username", password="password")
        room = Room(name="room")
        self.assertEqual(user.add_room(room), "Added")
        room.USERS_IN_ROOM = 5
        self.assertEqual(user.add_room(room), "Full")

class UserExitRoomVie(TestCase):

    def test_exit_room(self):
        user = User(username="username", password="password")
        room = Room(name="room")
        self.assertEqual(user.exit_room(),"Not in room")
        user.add_room(room)
        print("calculate coins ...")
        time.sleep(60)
        user.exit_room()
        self.assertEqual(user.coins,1)
        self.assertEqual(user.room,None)
        self.assertEqual(room.USERS_IN_ROOM,0)


class ItemTest(TestCase):

    def test_create(self):
        item = Item(name="item", price=50, effect_description="something")
        self.assertIsNotNone(item.price)
        self.assertEqual(item.name, "item")

class BattleTest(TestCase):

    def test_battle(self):
        user = User(username="username1", password="password1")
        user2 = User(username="username2", password="password")
        monster = Monster(name="m")
        monster2 = Monster(name="c")
        user1coins = user.coins
        user2coins = user2.coins
        user.monster = monster
        user2.monster = monster2
        user.battle_user(user2)
        self.assertTrue((user1coins != user.coins) or (user2coins != user2.coins))
        