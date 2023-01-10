from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView
from django.http import HttpResponse
from .models import Recipe, Review, Profile, Amount, Ingredient

from .forms import RegisterForm, ReviewForm, CreateRecipeForm

def is_float(element: any) -> bool:
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


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
  is_reviewed = True
  if request.user.is_authenticated:
    is_reviewed = Review.objects.filter(recipe_id=recipe_id, user=request.user).exists()
  is_favorited = False
  try:
    Profile.objects.get(user=request.user).favorites.get(id=recipe_id)
    is_favorited = True
  except:
    pass
  return render(request, 'recipes/detail.html', {'recipe': recipe, 'ingredients': ingredients, 'reviews': reviews, 'review_form': review_form, 'is_reviewed': is_reviewed, 'is_favorited': is_favorited})

def recipes_search(request):
  if request.method == "POST":
    searched = request.POST['search']
    recipes = Recipe.objects.filter(title__icontains=searched)
    context = {'searched': searched, 'recipes': recipes}
    return render(request, 'recipes/search.html', context)
  else: 
    context = {}
    return render(request, 'recipes/search.html', context)

@login_required
def favorite_recipe(request, recipe_id):
  Profile.objects.get(user=request.user).favorites.add(recipe_id)
  return redirect('detail', recipe_id=recipe_id)

@login_required
def unfavorite_recipe(request, recipe_id):
  Profile.objects.get(user=request.user).favorites.remove(recipe_id)
  return redirect('detail', recipe_id=recipe_id)

@login_required
def recipe_create(request):
  if request.method == "POST":
    form = CreateRecipeForm(request.POST, request.FILES)
    print(request.POST)
    amountDict = {}
    for key, value in request.POST.items():
      print(key)
      if key.startswith('amount-') and is_float(value):
        print(key[7:])
        if Ingredient.objects.filter(id=key[7:]).exists():
          amountDict[key[7:]] = float(value)
    if form.is_valid():
      
      new_recipe = Recipe()
      for key, value in form.cleaned_data.items():
        setattr(new_recipe, key, value)
      new_recipe.user_id = request.user.id
      new_recipe.save()
      for key, value in amountDict.items():
        amount = Amount(recipe_id=new_recipe.id, ingredient_id=key, amount_tablespoons=value)
        amount.save()
      return redirect('detail', recipe_id=new_recipe.id)
    else:
      return redirect('recipe_create')
  else:
    form = CreateRecipeForm()
    ingredient_list = Ingredient.objects.all()
    return render(request, 'recipes/create.html', { 'form': form, 'ingredient_list': ingredient_list })

@login_required
def recipe_update(request, recipe_id):
  if request.method == "POST":
    pass
  else:
    recipe = Recipe.objects.get(id=recipe_id)
    data = {
      "title": recipe.title,
      "summary": recipe.summary,
      "directions": recipe.directions,
      "cooking_minutes": recipe.cooking_minutes,
      "preparation_minutes": recipe.preparation_minutes,
      "image": recipe.image,
      "servings": recipe.servings,
    }
    form = CreateRecipeForm(initial=data)
    ingredients = Amount.objects.filter(recipe_id=recipe_id)
    ingredient_list = Ingredient.objects.exclude(id__in = ingredients.values_list('ingredient_id'))
  context = {'recipe': recipe, 'form': form, 'ingredients': ingredients, 'ingredient_list': ingredient_list }
  return render(request, 'recipes/create.html', context)

@login_required
def add_review(request, recipe_id):
  form = ReviewForm(request.POST)

  if form.is_valid():
    new_review = form.save(commit=False)
    new_review.user_id = request.user.id
    new_review.recipe_id = recipe_id
    new_review.save()
  return redirect('detail', recipe_id=recipe_id)

# class ReviewUpdate(UpdateView):
#   model = Review
#   fields = ['rating', 'comment']

# class ReviewDelete(DeleteView):
#   model = Review
#   sucess_url = '/recipes/'
  
def remove_review(request, review_id, recipe_id):
  
  review=Review.objects.get(id=review_id)
  # if review.user_id == request.user.id:
  review.delete()
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

def profile_detail(request, user_id):
    profile = Profile.objects.get(user_id=user_id) 
    context = {'profile': profile}
    return render(request, 'registration/user_profile.html', context)