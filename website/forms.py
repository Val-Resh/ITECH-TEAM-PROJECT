from django import forms
# from django.contrib.auth.models import User
from website.models import Room
from website.models import User


class RoomForm(forms.ModelForm):
    name = forms.CharField(max_length=Room.MAX_NAME_LENGTH,
                           help_text="Room name")

    class Meta:
        model = Room
        fields = ('name',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

# class UserAppForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ('username', 'password')
