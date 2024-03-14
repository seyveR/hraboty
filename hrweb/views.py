from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


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
    user = request.user  # Получаем текущего аутентифицированного пользователя
    context = {'user': user}
    return render(request, 'profile.html', context)

def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Используйте правильное имя поля
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Успешный вход")
            return redirect('profile_page')
        else:
            print("Ошибка входа")
    return render(request, 'auth.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Дополнительные действия после успешной регистрации
            return redirect('auth_page')
    else:
        form = UserRegistrationForm()
    return render(request, 'reg.html', {'form': form})