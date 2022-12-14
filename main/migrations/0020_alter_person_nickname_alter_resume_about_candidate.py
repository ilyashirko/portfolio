# Generated by Django 4.1.1 on 2022-10-20 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_person_nickname_alter_resume_about_candidate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nickname',
            field=models.CharField(default='iXUwIOIy', max_length=50, unique=True, verbose_name='Никнейм'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='about_candidate',
            field=models.TextField(blank=True, verbose_name='Коротко о себе'),
        ),
    ]
