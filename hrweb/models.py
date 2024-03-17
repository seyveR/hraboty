from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    subscription_status = models.IntegerField(default=0)

    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    def __str__(self):
        return self.username

class Vacancy(models.Model):
    name = models.CharField(max_length=255, verbose_name ='Название')
    employer = models.CharField(max_length=255, verbose_name ='Работодатель')
    url = models.URLField(verbose_name ='Ссылка')
    salary = models.CharField(max_length=100, verbose_name ='Зарплата')
    description = models.TextField(verbose_name ='Описание')
    area = models.CharField(max_length=255, verbose_name ='Зона')
    date = models.DateField(verbose_name ='Дата')
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'