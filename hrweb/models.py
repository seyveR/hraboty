from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Добавляем необязательные поля
    phone = models.CharField(max_length=15, blank=True)
    subscription_status = models.IntegerField(default=0)

    # Добавляем поле для определения статуса администратора
    is_admin = models.BooleanField(default=False)

    # Решаем проблему с обратными связями
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )

    def __str__(self):
        return self.username