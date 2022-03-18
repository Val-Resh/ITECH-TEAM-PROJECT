"""itech URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('userprofile/', views.userprofile, name='user-profile'),
    path('monster_list/', views.monster_list, name='monster_list'),
    path('shop/', views.shop, name='shop'),
    path('room/<room_name>/', views.room, name='room'),
    path('create_room/', views.index, name='create_room'),
    path('battle/', views.battle, name='battle'),

    # AJAX
    path('choose_monster/', views.UserChooseMonsterView.as_view(), name='choose_monster'),
    path('buy_item/', views.UserBuyItemView.as_view(), name='buy_item'),
    path('join_room/', views.UserJoinRoomView.as_view(), name='join_room'),
    path('exit_room/', views.UserExitRoomView.as_view(), name='exit_room'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
