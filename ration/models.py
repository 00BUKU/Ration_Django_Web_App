from django.db import models
from datetime import date
from django.urls import reverse 
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    calorie = models.FloatField(validators=[MinValueValidator(0.0)])
    carbohydrate = models.FloatField(validators=[MinValueValidator(0.0)])
    fat = models.FloatField(validators=[MinValueValidator(0.0)])
    protein = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    directions = models.TextField()
    cooking_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    preparation_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to=None)
    servings = models.IntegerField(validators=[MinValueValidator(1)])
    ingredient = models.ManyToManyField(Ingredient, through='Amount')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
    
class Amount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount_teaspoons = models.FloatField(validators=[MinValueValidator(0.0)])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=None)
    favorites = models.ManyToManyField(Recipe)

class Review(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    