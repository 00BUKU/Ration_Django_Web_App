from django.urls import path

from . import views


urlpatterns = [
    # localhost: 8000 (the catcollector.urls is '')
    path('', views.home, name='home'), #**kwargs, key word argument
    # path('about/', views.about, name='about'),
    # path('recipes/', views.recipes_index, name='index'),
    # path('recipes/<int:recipes_id>/', views.recipes_detail, name="detail"),
   
]