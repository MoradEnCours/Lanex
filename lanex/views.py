from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context_dict = {'message': 'Index'}
    return render(request, 'lanex/index.html', context=context_dict)

def about(request):
    context_dict = {'message': 'About'}
    return render(request, 'lanex/about.html', context=context_dict)

def userpage(request):
    context_dict = {'message': 'User Page'}
    return render(request, 'lanex/user.html', context=context_dict)

def explore(request):
    context_dict = {'message': 'Explore'}
    return render(request, 'lanex/explore.html', context=context_dict)