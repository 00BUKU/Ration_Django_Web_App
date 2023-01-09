from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'), #**kwargs, key word argument
    path('about/', views.about, name='about'),
    path('recipes/', views.recipes_index, name='index'),
    path('recipes/<int:recipe_id>/', views.recipes_detail, name="detail"),
    path('recipes/<int:recipe_id>/favorite/', views.favorite_recipe, name="favorite_recipe"),
    path('recipes/<int:recipe_id>/unfavorite/', views.unfavorite_recipe, name="unfavorite_recipe"),
    path('recipes/<int:recipe_id>/add_review/', views.add_review, name='add_review'),
    # path('recipes/<int:pk>/update/', views.ReviewUpdate.as_view(), name='reviews_update'),
    path('recipes/<int:recipe_id>/remove_review/<int:review_id>/', views.remove_review, name='remove_review'),
    path('recipes/create/', views.recipe_create, name='recipe_create'),
    path('recipes/search/', views.recipes_search, name='recipes_search'),
    path('accounts/signup/', views.signup, name='signup'),
    path('members/<int:user_id>/profile/', views.profile_detail, name='profile_detail')
]