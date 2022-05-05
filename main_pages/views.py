from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.admin import site


def index(request):
    return render(request, 'base.html')


def about(request):
    return render(request, 'main_pages/about.html')
