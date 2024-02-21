from . import views
from django.urls import path 

urlpatterns = [
    path('', views.home, name='home'),
    path('about_us', views.about_us, name='about_us'),
    path('price', views.price, name='price'),
    path('profile', views.profile, name='profile'),
    path('auth', views.auth, name='auth'),
    path('reg', views.reg, name='reg'),
    path('search', views.search, name='search'),
]