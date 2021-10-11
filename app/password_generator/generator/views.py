from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.
def home(request):
    return render(request, 'generator/home.html', {'password':'huig667'})
def password(request):

    characters = list('abcdefghjiklmnopqrstuvwxyz')
    if request.GET.get('uppercase'):
        characters.extend(list('ABCDEFGHIKLMNOPQRSTUVWXYZ'))
    if request.GET.get('special'):
        characters.extend(list('?#<>&@=%!()+§/'))
    if request.GET.get('numbers'):
        characters.extend(list('0123456789'))

    length = int(request.GET.get('length', 12))
    thepassword = ''
    for x in range(length):
            thepassword += random.choice(characters)
    return render(request, 'generator/password.html', {'password':thepassword})
def about_page(request):
    return render(request, 'generator/about.html')
