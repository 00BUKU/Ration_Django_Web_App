from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fileds = ["username", "password1", "password2", "first_name", "last_name", "email",] 