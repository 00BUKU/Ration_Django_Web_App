from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from .models import Recipe, Review, Profile, Amount

from .forms import RegisterForm, ReviewForm

def home(request):
  return render(request, 'home.html')
 
def about(request):
 return render(request, 'about.html')

def recipes_index(request):
  recipes = Recipe.objects.all()
  return render(request, 'recipes/index.html', {'recipes': recipes})

def recipes_detail(request, recipe_id):
  recipe = Recipe.objects.get(id=recipe_id)
  ingredients = Amount.objects.filter(recipe_id=recipe_id)
  review_form = ReviewForm()
  reviews = Review.objects.filter(recipe_id=recipe_id)
  is_favorited = False
  try:
    Profile.objects.get(user=request.user).favorites.get(id=recipe_id)
    is_favorited = True
  except:
    pass
  return render(request, 'recipes/detail.html', {'recipe': recipe, 'ingredients': ingredients, 'reviews': reviews, 'review_form': review_form, 'is_favorited': is_favorited})

@login_required
def favorite_recipe(request, recipe_id):
  Profile.objects.get(user=request.user).favorites.add(recipe_id)
  return redirect('detail', recipe_id=recipe_id)

@login_required
def unfavorite_recipe(request, recipe_id):
  Profile.objects.get(user=request.user).favorites.remove(recipe_id)
  return redirect('detail', recipe_id=recipe_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = RegisterForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      profile = Profile(user=user)
      profile.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = RegisterForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class RecipeCreate(CreateView):
  model= Recipe
  fields = '__all__'
  def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)

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
  
