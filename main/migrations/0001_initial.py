# Generated by Django 4.1.1 on 2022-09-15 12:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='HardSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Хард-скилл')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('first_name_eng', models.CharField(blank=True, max_length=50, verbose_name='Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('last_name_eng', models.CharField(blank=True, max_length=50, verbose_name='Last name')),
                ('patronymic', models.CharField(max_length=50, verbose_name='Отчество')),
                ('patronymic_eng', models.CharField(blank=True, max_length=50, verbose_name='Patronymic')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Номер телефона (основной)')),
                ('phonenumber_extra', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Номер телефона (дополнительный)')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('github', models.URLField(blank=True, verbose_name='GitHub')),
                ('main_social_media', models.URLField(blank=True, verbose_name='Main social media account')),
                ('extra_social_media', models.URLField(blank=True, verbose_name='Extra social media account')),
                ('personal_site', models.URLField(blank=True, verbose_name='Personal site')),
                ('location', models.CharField(max_length=50, verbose_name='Город проживания')),
                ('want_to_relocate', models.BooleanField(verbose_name='Готов к переезду')),
                ('education', models.CharField(choices=[('secondary', 'среднее'), ('secondary_special', 'среднее специальное'), ('unfinished_higher', 'неоконченное высшее'), ('higher', 'высшее'), ('bachelor', 'бакалавр'), ('master', 'магистр'), ('candidate_science', 'кандидат наук'), ('doctor_sciense', 'доктор наук')], max_length=50, verbose_name='Образование')),
            ],
        ),
        migrations.CreateModel(
            name='SoftSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Софт-скилл')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('desired_position', models.CharField(max_length=50, verbose_name='Желаемая должность')),
                ('desired_salary_amount', models.SmallIntegerField(verbose_name='Желаемая зарплата')),
                ('desired_salary_currensy', models.CharField(choices=[('RUB', 'руб.'), ('BYN', 'бел. руб.'), ('USD', 'долл.'), ('EUR', 'евро')], max_length=10, verbose_name='Валюта')),
                ('hard_skills', models.ManyToManyField(related_name='persons', to='main.hardskill', verbose_name='Хард скиллы')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='resumes', to='main.person', verbose_name='Соискатель')),
                ('soft_skills', models.ManyToManyField(related_name='persons', to='main.softskill', verbose_name='Софт скиллы')),
            ],
        ),
        migrations.CreateModel(
            name='Recomendations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommender', models.CharField(max_length=100, verbose_name='Рекомендатель')),
                ('company', models.CharField(max_length=50, verbose_name='Компания')),
                ('post', models.CharField(max_length=50, verbose_name='Должность')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recomendations', to='main.person', verbose_name='Соискатель')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceOfWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=50, verbose_name='Компания')),
                ('post', models.CharField(max_length=50, verbose_name='Должность')),
                ('location', models.CharField(max_length=50, verbose_name='Город (страна)')),
                ('started_at', models.DateField(verbose_name='Начало работы')),
                ('finished_at', models.DateField(blank=True, null=True, verbose_name='Окончание работы')),
                ('responsibilities', models.TextField(verbose_name='Обязанности')),
                ('achievements', models.TextField(blank=True, verbose_name='Достижения')),
                ('retire_reasons', models.TextField(blank=True, verbose_name='Причина увольнения')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='places_of_work', to='main.person', verbose_name='Соискатель')),
            ],
        ),
        migrations.CreateModel(
            name='HigherEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=200, verbose_name='Учебное заведение')),
                ('specialization', models.CharField(max_length=50, verbose_name='Специальность')),
                ('started_at', models.SmallIntegerField(help_text='Введите год в формате YYYY (напр. 2012)', validators=[django.core.validators.RegexValidator('^[0-9]{4}$')], verbose_name='Год начала обучения')),
                ('finished_at', models.SmallIntegerField(blank=True, help_text='Введите год в формате YYYY (напр. 2012)', validators=[django.core.validators.RegexValidator('^[0-9]{4}$')], verbose_name='Год окончания обучения (напр. 2012)')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='higher_education', to='main.person', verbose_name='Соискатель')),
            ],
        ),
    ]
