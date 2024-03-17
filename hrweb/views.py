from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileUpdateForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.urls import reverse


def home(request): 
    return render(request, 'home.html')


def about_us(request): 
    return render(request, 'aboutus.html')

def price(request): 
    return render(request, 'price.html')

def search(request):
    return render(request, 'search.html')

@login_required
def profile(request):
    user = request.user
    profile_form = ProfileUpdateForm(initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'phone': user.phone
    })

    password_form = PasswordChangeForm()

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = ProfileUpdateForm(request.POST)
            if profile_form.is_valid():
                user.first_name = profile_form.cleaned_data['first_name']
                user.last_name = profile_form.cleaned_data['last_name']
                user.username = profile_form.cleaned_data['username']
                user.email = profile_form.cleaned_data['email']
                user.phone = profile_form.cleaned_data['phone']
                user.save()
                return redirect('profile_page')
        elif 'password_submit' in request.POST:
            password_form = PasswordChangeForm(request.POST)
            if password_form.is_valid():
                new_password = password_form.cleaned_data['newpass']
                old_password = password_form.cleaned_data['oldpass']
                repeat_password = password_form.cleaned_data['rnewpass']

                if new_password != repeat_password:
                    return HttpResponse("Пароли не совпадают")

                if not check_password(old_password, user.password):
                    return HttpResponse("Текущий пароль неверен")
                
                user.set_password(new_password)
                user.save()

                user = authenticate(request, username=user.username, password=new_password)
                if user is not None:
                    login(request, user)
                return redirect('profile_page')

    context = {'user': user, 'authenticated': True, 'profile_form': profile_form, 'password_form': password_form}
    return render(request, 'profile.html', context)

from django.contrib.auth.hashers import check_password


def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        custom_user = authenticate(request, username=username, password=password)
        if custom_user is not None:
            print("Успешный вход для пользователя:", username)
            login(request, custom_user)
            print(request.user.is_authenticated)
            print(request.user)
            return redirect('profile_page')
        else:
            error_message = "Неправильный пароль или логин"
            return render(request, 'auth.html', {'error_message': error_message})

    return render(request, 'auth.html')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth_page'))

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.password = make_password(form.cleaned_data['password'])  
            user.save()  
            
            return redirect('auth_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'reg.html', {'form': form})