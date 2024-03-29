from . import views
from django.urls import path 

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us', views.about_us, name='about_us'),
    path('price', views.price, name='price'),
    path('profile', views.profile, name='profile_page'),
    path('auth', views.auth, name='auth_page'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('search', views.search, name='search'),
]