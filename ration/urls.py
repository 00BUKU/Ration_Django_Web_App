from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'), #**kwargs, key word argument
    path('about/', views.about, name='about'),
    path('recipes/', views.recipes_index, name='index'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name="detail"),
    path('accounts/signup', views.signup, name='signup'),
    path('recipes/create/', views.RecipeCreate.as_view(), name='recipe_create'),
]