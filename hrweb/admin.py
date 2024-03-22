from django.contrib import admin
from .models import CustomUser, Vacancy
from .forms import VacancyForm

admin.site.register(CustomUser)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display=('name', 'employer', 'url', 'salary_min', 'salary_max', 'description', 'area', 'date', 'schedule','role')
=======
    list_display=('name', 'employer', 'url', 'salary_min', 'salary_max', 'description', 'area', 'date', 'schedule')
>>>>>>> main
    form = VacancyForm
