from django.shortcuts import render


def home(request): 
    return render(request, 'home.html')


def about_us(request): 
    return render(request, 'aboutus.html')

def price(request): 
    return render(request, 'price.html')

def search(request):
    return render(request, 'search.html')

def profile(request): 
    return render(request, 'profile.html')

def auth(request):
    return render(request, 'auth.html')

def reg(request):
    return render(request, 'reg.html')