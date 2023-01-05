from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Recipe, Review, Profile

def index(request):
    return HttpResponse("Hello, world. You're at the ration index.")