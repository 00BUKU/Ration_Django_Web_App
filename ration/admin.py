from django.contrib import admin


# Register your models here.
from .models import Recipe, Ingredient, Amount, Review, Profile, Meal

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Amount)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(Meal)