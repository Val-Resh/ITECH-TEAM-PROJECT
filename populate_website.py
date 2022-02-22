import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itech.settings')
django.setup()

from website.models import *

def populate():

	users = [
		{"username" : "user1", "password" : "password1"},
		{"username": "user2", "password": "password2"},
		{"username": "user3", "password": "password3"},]
	monsters = [{"name": "monster1"}, 
			 {"name": "monster2"},
			{"name": "monster3"}]
	rooms = [{"name" : "room"}]

	initialised_monsters = []
	initialised_rooms = []

	for monster in monsters:
		m = add_monster(monster["name"])
		initialised_monsters.append(m)
		print("monster {name} created".format(name=m.name))

	for room in rooms:
		r = add_room(room["name"])
		initialised_rooms.append(r)
		print("room {name} created".format(name=r.name))

	for i in range(len(users)):
		user = users[i]
		u = add_user(user["username"],user["password"],initialised_monsters[i], initialised_rooms[0])
		print("User with\n Username: {username}\n Monster: {monster}\n Coins: {coins}\n Room: {room}\n has been created!\n\n".
		format(username=u.username, monster=u.monster.name, coins=u.coins, room=u.room.name))



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

def add_room(name):
	room = Room.objects.get_or_create(name=name)[0]
	room.save()
	return room
	
if __name__ == "__main__":
	print("Starting website's populating script...")
	populate()


	