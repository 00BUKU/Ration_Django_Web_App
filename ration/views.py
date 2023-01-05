from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
from .models import Recipe, Review, Profile
from .forms import RegisterForm

def index(request):
    return HttpResponse("Hello, world. You're at the ration index.")

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