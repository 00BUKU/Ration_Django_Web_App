from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, Ingredient, Amount

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2",] 

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class CreateRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    summary = forms.CharField(widget=forms.Textarea,max_length=500)
    directions = forms.CharField(widget=forms.Textarea)
    cooking_minutes = forms.IntegerField(min_value=0)
    preparation_minutes = forms.IntegerField(min_value=0)
    image = forms.ImageField(required=False)
    servings = forms.IntegerField(min_value=1)


    