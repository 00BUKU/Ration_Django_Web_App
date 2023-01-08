from django.db import models
from django.db.models import Avg
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
    summary = models.TextField(max_length=500)
    directions = models.TextField()
    cooking_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    preparation_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to=None)
    servings = models.IntegerField(validators=[MinValueValidator(1)])
    ingredient = models.ManyToManyField(Ingredient, through='Amount')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def average_rating(self) -> float:
        return Review.objects.filter(recipe=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def calculate_nutrition(self):
        nutrient = {}
        for ingredient in Amount.objects.filter(recipe=self):
            for key, value in ingredient.ingredient.__dict__:
                if type(value) == float:
                    previous_amount = nutrient.get(key, 0)
                    nutrient[key] = previous_amount + value*ingredient.amount_tablespoons
        return nutrient

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'recipe_id': self.id})


        
    
class Amount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount_tablespoons = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"{self.recipe}: {self.ingredient}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=None)
    favorites = models.ManyToManyField(Recipe, blank=True)

    def __str__(self):
        return self.user.username

class Review(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    constraints = [
        models.UniqueConstraint(fields=['recipe', 'user'], name='unique_review_per_user')
    ]
    