# Generated by Django 5.0.2 on 2024-03-20 15:14


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrweb', '0006_merge_20240319_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='salary',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='salary_max',

            field=models.IntegerField(default=None, null=True, verbose_name='Зарплата max'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='salary_min',

            field=models.IntegerField(default=None, null=True, verbose_name='Зарплата min'),
        ),
    ]
