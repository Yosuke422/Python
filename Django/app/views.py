
from django.shortcuts import render
from django.db.models import F


from .models import Question

def index(requests):
    return render(requests,'index.html')

# Create your views here.
