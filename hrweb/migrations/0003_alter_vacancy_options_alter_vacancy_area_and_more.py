# Generated by Django 5.0.3 on 2024-03-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrweb', '0002_vacancy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='area',
            field=models.CharField(max_length=255, verbose_name='Зона'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='employer',
            field=models.CharField(max_length=255, verbose_name='Работодатель'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary',
            field=models.CharField(max_length=100, verbose_name='Зарплата'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='url',
            field=models.URLField(verbose_name='Ссылка'),
        ),
    ]
