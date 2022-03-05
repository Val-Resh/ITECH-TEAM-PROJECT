from django.contrib import admin

from website.models import User, Room, Item

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Item)
