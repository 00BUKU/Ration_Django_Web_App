from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.home, name='home'), #**kwargs, key word argument
    path('about/', views.about, name='about'),
    path('recipes/', views.recipes_index, name='index'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name="detail"),
    path('recipes/<int:recipe_id>/favorite/', views.favorite_recipe, name="favorite_recipe"),
    path('recipes/<int:recipe_id>/unfavorite/', views.unfavorite_recipe, name="unfavorite_recipe"),
    path('recipes/<int:recipe_id>/delete_recipe', views.delete_recipe, name='delete_recipe'),
    path('recipes/<int:recipe_id>/add_review/', views.add_review, name='add_review'),
    path('recipes/<int:recipe_id>/update/', views.recipe_update, name='update'),
    path('recipes/<int:recipe_id>/remove_review/<int:review_id>/', views.remove_review, name='remove_review'),
    path('recipes/create/', views.recipe_create, name='recipe_create'),
    path('recipes/search/', views.recipes_search, name='recipes_search'),
    path('accounts/signup/', views.signup, name='signup'),
    path('members/<int:user_id>/profile/', views.profile_detail, name='profile_detail'),
    path('members/profile', views.my_profile, name='my_profile'),
    path('members/profile/update', views.profile_update, name="profile_update"),
    path('members/profile/change_password', views.change_password, name="change_password"),
    path('members/profile/<int:date>', views.meal_log, name='meal_log'),
    path('meals', views.meal_search, name='meal_search'),
    path('meals/<int:recipe_id>/create', views.meal_create, name='meal_create'),
    path('meals/delete/<int:meal_id>', views.meal_delete, name="meal_delete"),
    path('review/<int:review_id>/update_review/', views.update_review, name='update_review'),
]


urlpatterns += staticfiles_urlpatterns()