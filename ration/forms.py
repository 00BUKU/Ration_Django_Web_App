from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, Ingredient, Amount, MEALS
import datetime

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2",] 

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=((1,1),(2,2),(3,3),(4,4),(5,5)))
    comment = forms.CharField(max_length=250)
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    daily_calorie = forms.FloatField(min_value=0)
    daily_carbohydrate = forms.FloatField(min_value=0)
    daily_fat = forms.FloatField(min_value=0)
    daily_protein = forms.FloatField(min_value=0)

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CreateRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    summary = forms.CharField(widget=forms.Textarea,max_length=500)
    directions = forms.CharField(widget=forms.Textarea)
    cooking_minutes = forms.IntegerField(min_value=0)
    preparation_minutes = forms.IntegerField(min_value=0)
    servings = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        super(CreateRecipeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class MealForm(forms.Form):
    servings = forms.FloatField(min_value=0, initial=1.0)
    date = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"), initial=datetime.date.today)
    meal = forms.ChoiceField(choices=MEALS)

    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    