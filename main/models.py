from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

CURRENCIES = [
    ('RUB', 'руб.'),
    ('BYN', 'бел. руб.'),
    ('USD', 'долл.'),
    ('EUR', 'евро')
]

EDUCATION_DEGREES = [
    ('secondary', 'среднее'),
    ('secondary_special', 'среднее специальное'),
    ('unfinished_higher', 'неоконченное высшее'),
    ('higher', 'высшее'),
    ('bachelor', 'бакалавр'),
    ('master', 'магистр'),
    ('candidate_science', 'кандидат наук'),
    ('doctor_sciense', 'доктор наук'),
]


class Person(models.Model):
    first_name = models.CharField('Имя', max_length=50)
    first_name_eng = models.CharField('Name', max_length=50, blank=True)

    last_name = models.CharField('Фамилия', max_length=50)
    last_name_eng = models.CharField('Last name', max_length=50, blank=True)

    patronymic = models.CharField('Отчество', max_length=50)
    patronymic_eng = models.CharField('Patronymic', max_length=50, blank=True)

    birthday = models.DateField('Дата рождения')

    phonenumber = PhoneNumberField('Номер телефона (основной)')
    phonenumber_extra = PhoneNumberField(
        'Номер телефона (дополнительный)',
        blank=True
    )
    email = models.EmailField('E-mail', blank=True)
    github = models.URLField('GitHub', blank=True)
    main_social_media = models.URLField(
        'Main social media account',
        blank=True
    )
    extra_social_media = models.URLField(
        'Extra social media account',
        blank=True
    )
    personal_site = models.URLField('Personal site', blank=True)

    location = models.CharField('Город проживания', max_length=50)
    want_to_relocate = models.BooleanField('Готов к переезду')

    education = models.CharField(
        'Образование',
        choices=EDUCATION_DEGREES,
        max_length=50
    )

    def get_age(self):
        today = datetime.now().date()
        if (
            (today.month < self.birthday.month) or
            (
                today.month == self.birthday.month and
                today.day <= self.birthday.day
            )
        ):
            return today.year - self.birthday.year - 1
        else:
            return today.year - self.birthday.year

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def initials(self):
        return f'{self.last_name} {self.first_name[0]}. {self.patronymic[0]}.'


class Resume(models.Model):
    title = models.CharField('Название', max_length=50)
    person = models.ForeignKey(
        'Person',
        verbose_name='Соискатель',
        related_name='resumes',
        on_delete=models.PROTECT
    )

    desired_position = models.CharField('Желаемая должность', max_length=50)
    desired_salary_amount = models.SmallIntegerField('Желаемая зарплата')
    desired_salary_currensy = models.CharField(
        'Валюта',
        max_length=10,
        choices=CURRENCIES
    )

    soft_skills = models.ManyToManyField(
        'SoftSkill',
        verbose_name='Софт скиллы',
        related_name='persons'
    )
    hard_skills = models.ManyToManyField(
        'HardSkill',
        verbose_name='Хард скиллы',
        related_name='persons'
    )

    def get_places_of_work(self):
        return self.person.places_of_work.order_by('-started_at')

    def __str__(self):
        return f'[{self.person.initials()}]: {self.title}'


class PlaceOfWork(models.Model):
    person = models.ForeignKey(
        'Person',
        verbose_name='Соискатель',
        related_name='places_of_work',
        on_delete=models.PROTECT
    )
    company = models.CharField('Компания', max_length=50)
    post = models.CharField('Должность', max_length=50)
    location = models.CharField('Город (страна)', max_length=50)
    started_at = models.DateField('Начало работы')
    finished_at = models.DateField('Окончание работы', blank=True, null=True)
    responsibilities = models.TextField('Обязанности')
    achievements = models.TextField('Достижения', blank=True)
    retire_reasons = models.TextField('Причина увольнения', blank=True)

    def get_work_duration(self):
        if self.finished_at:
            return self.finished_at - self.started_at
        else:
            return datetime.now().date() - self.started_at

    def __str__(self):
        return (
            f'[{self.person}]: {self.company} ({self.started_at} - '
            f'{self.finished_at if self.finished_at else "наст. время"})'
        )


class SoftSkill(models.Model):
    title = models.CharField('Софт-скилл', max_length=50)

    def __str__(self):
        return self.title


class HardSkill(models.Model):
    title = models.CharField('Хард-скилл', max_length=50)

    def __str__(self):
        return self.title


class Recomendation(models.Model):
    person = models.ForeignKey(
        'Person',
        verbose_name='Соискатель',
        related_name='recomendations',
        on_delete=models.PROTECT
    )
    resume = models.ManyToManyField(
        'Resume',
        verbose_name='Резюме',
        related_name='recomendations',
        blank=True
    )
    recommender = models.CharField('Рекомендатель', max_length=100)
    company = models.CharField('Компания', max_length=50)
    post = models.CharField('Должность', max_length=50)

    def __str__(self):
        return f'{self.recommender} ({self.company}, {self.post})'


class HigherEducation(models.Model):
    person = models.ForeignKey(
        'Person',
        verbose_name='Соискатель',
        related_name='higher_education',
        on_delete=models.PROTECT
    )
    institution = models.CharField('Учебное заведение', max_length=200)
    specialization = models.CharField('Специальность', max_length=50)
    started_at = models.SmallIntegerField(
        'Год начала обучения',
        validators=[
            RegexValidator(r'^[0-9]{4}$')
        ],
        help_text='Введите год в формате YYYY (напр. 2012)'
    )
    finished_at = models.SmallIntegerField(
        'Год окончания обучения (напр. 2012)',
        validators=[
            RegexValidator(r'^[0-9]{4}$')
        ],
        help_text='Введите год в формате YYYY (напр. 2012)',
        blank=True
    )

    def __str__(self):
        return f'{self.person.initials()} - {self.institution} ({self.finished_at})'


class Course(models.Model):
    pass


class Language(models.Model):
    pass


class Photo(models.Model):
    person = models.ForeignKey(
        'Person',
        verbose_name='Соискатель',
        related_name='photos',
        on_delete=models.CASCADE
    )
    index = models.SmallIntegerField(
        'Порядковый номер (UNIQUE ONLY)',
        default=0
    )
    image = models.ImageField(
        'Фотография',
        upload_to='images'
    )

    class Meta:
        ordering = ['index', ]


class Visitor(models.Model):
    telegram_id = models.SmallIntegerField('TG_id')
    first_visit = models.DateTimeField(
        'added at',
        auto_now_add=True,
        editable=False
    )