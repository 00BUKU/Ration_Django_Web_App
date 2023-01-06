from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from .models import Recipe, Review, Profile
from .forms import RegisterForm
from .forms import ReviewForm

def home(request):
  return render(request, 'home.html')
 
def about(request):
 return render(request, 'about.html')

def recipes_index(request):
  recipes = Recipe.objects.all()
  return render(request, 'recipes/index.html', {'recipes': recipes})

def recipes_detail(request, recipe_id):
  recipe = Recipe.objects.get(id=recipe_id)
  reviews = Review.objects.filter(recipe_id=recipe_id)
  #Add a review
  review_form = ReviewForm()
  
  return render(request, 'recipes/detail.html', {'recipe': recipe, 'reviews': reviews, 'review_form': review_form})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = RegisterForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = RegisterForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def add_review(request, recipe_id):
  form = ReviewForm(request.POST)

  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.user_id = request.user.id
    new_review.recipe_id = recipe_id
    new_review.save()
  return redirect('detail', recipe_id=recipe_id)

  # def delete_review():