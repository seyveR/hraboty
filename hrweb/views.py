from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileUpdateForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Vacancy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, CharField, Value
from django.db.models.functions import Lower
from django.core.files.base import ContentFile
import base64
from django.contrib.auth.hashers import check_password
import re
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from babel.dates import format_date


def home(request): 
    user = request.user
    decoded_image = None
    if user.is_authenticated and hasattr(user, 'avatar'):
        decoded_image = user.avatar

    context = {'user': user, 'decoded_image': decoded_image}
    return render(request, 'home.html', context)


def about_us(request): 
    user = request.user
    decoded_image = None
    if user.is_authenticated and hasattr(user, 'avatar'):
        decoded_image = user.avatar

    context = {'user': user, 'decoded_image': decoded_image}
    return render(request, 'aboutus.html', context)

def price(request): 
    user = request.user
    decoded_image = None
    if user.is_authenticated and hasattr(user, 'avatar'):
        decoded_image = user.avatar

    context = {'user': user, 'decoded_image': decoded_image}
    return render(request, 'price.html', context)

def search(request):
    query = request.GET.get('search')
    vacancies_list = Vacancy.objects.all()

    # Текстовый запрос
    if query and query.strip(): 
        vacancies_list = vacancies_list.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(area__icontains=query)
        )

    # Фильтр по зп
    income_level = request.GET.get('income_level')
    min_salary = income_level

    if income_level:
        if income_level == '0':
            pass
        else:
            vacancies_list = vacancies_list.filter(salary_min__gte=min_salary)


    # Фильтр по графику 
    schedule = request.GET.getlist("schedule[]")
    print(schedule)
    if schedule:
        vacancies_list = vacancies_list.filter(schedule__in=schedule)

    # Фильтр по региону
    all_areas = Vacancy.objects.values_list('area', flat=True).distinct()
    selected_region = request.GET.getlist("area[]")
    if selected_region:
        vacancies_list = vacancies_list.filter(area__in=selected_region)

    # Фильтрация по дате
    check_date = request.GET.getlist("check_date[]")
    today = date.today()
    yesterday = today - timedelta(days=1)
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_3_months_ago = today - relativedelta(months=3)

    if 'today' in check_date:
        vacancies_list = vacancies_list.filter(date=today)
    elif 'yesterday' in check_date:
        vacancies_list = vacancies_list.filter(date=yesterday)
    elif 'this_week' in check_date:
        vacancies_list = vacancies_list.filter(date__range=[start_of_week, today])
    elif 'this_month' in check_date:
        vacancies_list = vacancies_list.filter(date__range=[start_of_month, today])
    elif 'last_3_months' in check_date:
        vacancies_list = vacancies_list.filter(date__gte=start_of_3_months_ago)

    # Вывод даты для юзера
    
    for vacancy in vacancies_list:
        if vacancy.date == today:
            vacancy.date_display = "Сегодня"
        elif vacancy.date == yesterday:
            vacancy.date_display = "Вчера"
        else:
            vacancy.date_display = format_date(vacancy.date, format='d MMMM', locale='ru_RU')


    # Пагинация 
    paginator = Paginator(vacancies_list, 100) 
    page = request.GET.get('page')
    try:
        vacancies = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        vacancies = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        vacancies = paginator.page(page)

    first_page_number = 1
    total_pages = paginator.num_pages
    previous_page_number = vacancies.previous_page_number() if vacancies.has_previous() else None
    next_page_number = vacancies.next_page_number() if vacancies.has_next() else None
    show_first_page_link = vacancies.number > 2
    show_last_page_link = vacancies.number < vacancies.paginator.num_pages - 1
    

    # Аутентификация юзера для отображения аватара
    user = request.user
    decoded_image = None
    if user.is_authenticated and hasattr(user, 'avatar'):
        decoded_image = user.avatar

    return render(request, 'search.html', {'selected_region': selected_region, 'all_areas': all_areas, 'user': user, 'decoded_image': decoded_image, 'vacancies': vacancies, 'search_query': query, 'selected_region': selected_region, 'first_page_number': first_page_number, 'total_pages': total_pages, 'previous_page_number': previous_page_number, 'next_page_number': next_page_number, 'show_first_page_link': show_first_page_link, 'show_last_page_link': show_last_page_link})


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
            if 'avatar' in request.FILES:
                image_file = request.FILES['avatar']
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                user.avatar = encoded_image
                user.save()
                print("Изображение успешно сохранено в базе данных.")
            else:
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
        elif 'delete_avatar' in request.POST: 
            # Удаление изображения из базы данных
            user.avatar = None
            user.save()
            return redirect('profile_page')

    decoded_image = None
    if user.avatar:
        try:
            decoded_image = user.avatar
        except:
            print("Ошибка при декодировании изображения")


    context = {'user': user, 'authenticated': True, 'profile_form': profile_form, 'password_form': password_form, 'decoded_image': decoded_image}
    return render(request, 'profile.html', context)




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