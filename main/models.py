from datetime import datetime
from inspect import stack

from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from string import ascii_letters
from random import choice


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
    nickname = models.CharField(
        'Никнейм',
        max_length=50,
        default=''.join(choice(ascii_letters) for _ in range(8)),
        unique=True
    )
    telegram_id = models.SmallIntegerField(
        'Telegram ID',
        default=0,
        unique=True
    )

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

    places_of_work = models.ManyToManyField(
        'PlaceOfWork',
        verbose_name='Опыт работы',
        related_name='resume'
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
    started_at = models.DateField('Начало работы', blank=True, null=True)
    finished_at = models.DateField('Окончание работы', blank=True, null=True)
    summary = models.CharField(
        'Суммарно проработал',
        help_text='заполнять если не заполнено начало и окончание',
        max_length=100,
        blank=True,
        null=True
    )
    responsibilities = models.TextField('Обязанности')
    achievements = models.TextField('Достижения', blank=True)
    
    retire_reasons = models.TextField('Причина увольнения', blank=True)

    def get_work_duration(self):
        if self.summary:
            return self.summary
        if self.finished_at:
            return (
                f'{self.started_at} - '
                f'{self.finished_at if self.finished_at else "наст. время"}'
            )
        else:
            return f'c {self.started_at}'

    def __str__(self):
        return (
            f'[{self.person}]: {self.company} ({self.started_at} - '
            f'{self.finished_at if self.finished_at else "наст. время"})'
        )


class SoftSkill(models.Model):
    person = models.ForeignKey(
        'Person',
        verbose_name='Соискатель',
        related_name='softskills',
        on_delete=models.PROTECT,
        null=True
    )
    title = models.CharField('Софт-скилл', max_length=50)
    description = models.TextField('Описание', null=True)

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
    department = models.CharField('Отделение', max_length=100, default='Дневное')
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
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.person.initials()} - {self.institution} ({self.finished_at})'

    def education_period(self):
        return f'c {self.started_at}{f" по {self.finished_at}" if self.finished_at else ""}'

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


class BiographyChapter(models.Model):
    person = models.ForeignKey(
        'Person',
        verbose_name='Соискатель',
        related_name='biography_chapters',
        on_delete=models.CASCADE
    )
    index = models.SmallIntegerField(
        'Порядковый номер (UNIQUE ONLY)',
        default=0
    )
    title = models.CharField('Название раздела', max_length=25)
    text = models.TextField('Текст')
    photo = models.ForeignKey(
        'Photo',
        verbose_name='Фотография',
        related_name='biography_chapter',
        on_delete=models.PROTECT,
        blank=True
    )

    def __str__(self):
        return f'{self.person.initials()} - {self.title} ({self.index})'

    class Meta:
        ordering = ['index', ]

class Project(models.Model):
    person = models.ForeignKey(
        'Person',
        verbose_name='Соискатель',
        related_name='projects',
        on_delete=models.CASCADE
    )
    title = models.CharField('Название проекта', max_length=25, unique=True)
    url = models.URLField('Ссылка на github', blank=True)
    short_description = models.TextField('Короткое описание', max_length=500)
    develop_stack = models.ManyToManyField(
        'HardSkill',
        verbose_name='Стек',
        related_name='projects'
    )
    finished = models.BooleanField('Проект завершен?', default=True)
    will_show = models.BooleanField('Показывать в подборке?', default=False)

    def get_stack(self):
        s

    def __str__(self):
        return f'{self.person.initials()} - {self.title}'

class ProjectImage(models.Model):
    project = models.ForeignKey(
        'Project',
        verbose_name='Проект',
        related_name='images',
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