from django import forms
from django.contrib.auth.models import User
from website.models import Users, Room


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email', )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('picture', )


class RoomForm(forms.ModelForm):
    name = forms.CharField(max_length=Room.MAX_NAME_LENGTH, help_text="Room Name")

    class Meta:
        model = Room
        fields = ('name', )