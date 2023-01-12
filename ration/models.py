from django.db import models
from django.db.models import Avg
from datetime import date
from django.urls import reverse 
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from django.core.validators import MaxValueValidator, MinValueValidator
import operator
import datetime

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    calorie = models.FloatField(validators=[MinValueValidator(0.0)])
    carbohydrate = models.FloatField(validators=[MinValueValidator(0.0)])
    fat = models.FloatField(validators=[MinValueValidator(0.0)])
    protein = models.FloatField(validators=[MinValueValidator(0.0)])
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Recipe(models.Model):
    title = models.CharField(max_length=50)
    summary = models.TextField(max_length=500)
    directions = models.TextField()
    cooking_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    preparation_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.CharField(null=True, blank=True, max_length=200)
    servings = models.IntegerField(validators=[MinValueValidator(1)])
    ingredient = models.ManyToManyField(Ingredient, through='Amount')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_added = models.DateTimeField(auto_now_add=True)

    def average_rating(self) -> float:
        return Review.objects.filter(recipe=self).aggregate(Avg("rating"))["rating__avg"] or 0

    def get_star_rating(self):
        return range(0, int(self.average_rating()))

    def calculate_nutrition(self):
        nutrient = {}
        for ingredient in Amount.objects.filter(recipe=self):
            for key, value in ingredient.ingredient.__dict__.items():
                if type(value) == float:
                    previous_amount = nutrient.get(key, 0)
                    size_multiplier = {
                        'S': 1/3 ,
                        'M': 1,
                        'L': 16,
                    }
                    nutrient[key] = previous_amount + value*ingredient.amount*size_multiplier.get(ingredient.size, 1)
        for key in nutrient:
            nutrient[key] /= self.servings 
        return nutrient

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'recipe_id': self.id})

SIZES = (
	('S', 'Teaspoon'),
	('M', 'Tablespoon'),
	('L', 'Cup'),
)

class Amount(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0.0)])
    size = models.CharField(
		max_length=1,
		# this will help us make a select menu when a form is created from this model
		choices=SIZES, 
		default=SIZES[1][0])

    def __str__(self):
        return f"{self.recipe}: {self.ingredient}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.CharField(null=True, blank=True, max_length=200)
    daily_calorie = models.FloatField(default=2000.0, validators=[MinValueValidator(0.0)])
    daily_carbohydrate = models.FloatField(default=300.0, validators=[MinValueValidator(0.0)])
    daily_fat = models.FloatField(default=65.0, validators=[MinValueValidator(0.0)])
    daily_protein = models.FloatField(default=50.0, validators=[MinValueValidator(0.0)])
    favorites = models.ManyToManyField(Recipe, blank=True)
    

    def __str__(self):
        return self.user.username

    def get_daily_nutrition(self, day, month, year):
        date = datetime.datetime(year, month, day)
        daily_meals = self.meal_set.filter(date=date)
        daily_nutrition = {}
        for meal in daily_meals:
            for nutrient, value in meal.recipe.calculate_nutrition().items():
                daily_nutrition[nutrient] = value + daily_nutrition.get(nutrient, 0)
    
    def fed_for_day(self, day, month, year):
        date = datetime.datetime(year, month, day)
        return self.meal_set.filter(date=date).count() >= len(MEALS) - 1

    @classmethod
    def count_favorites(cls):
        favorites = cls.favorites.through.objects.all()
        favorites_dictionary = {}
        for favorite in favorites:
            if favorite.recipe not in favorites_dictionary:
                favorites_dictionary[favorite.recipe] = 1
            else:
                favorites_dictionary[favorite.recipe] += 1
        return sorted(favorites_dictionary.items(), key=operator.itemgetter(1),reverse=True)[:3]

class Review(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    constraints = [
        models.UniqueConstraint(fields=['recipe', 'user'], name='unique_review_per_user')
    ]

MEALS = (
	('B', 'Breakfast'),
	('L', 'Lunch'),
	('D', 'Dinner'),
    ('S', 'Snack'),
)

class Meal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    servings = models.FloatField(validators=[MinValueValidator(0.0)])
    meal = models.CharField(
		max_length=1,
		choices=MEALS, 
		default=MEALS[0][0])
    date = models.DateField('Meal date')

    def __str__(self):
        return f"{self.get_meal_display()} of {self.servings} servings {self.recipe.title} on {self.date}"
    
    def calculate_nutrition(self):
        nutrition = self.recipe.calculate_nutrition()
        for key, value in nutrition.items():
            nutrition[key] = value*self.servings
        return nutrition
