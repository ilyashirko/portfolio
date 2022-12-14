# Generated by Django 4.1.1 on 2022-10-20 11:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_resume_advantages_resume_expectations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nickname',
            field=models.CharField(default='ayBrEInA', max_length=50, unique=True, verbose_name='Никнейм'),
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Достижение')),
                ('reached_at', models.SmallIntegerField(help_text='Введите год в формате YYYY (напр. 2012)', validators=[django.core.validators.RegexValidator('^[0-9]{4}$')], verbose_name='Год награждения')),
                ('company', models.CharField(max_length=100, verbose_name='Компания')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to='main.person', verbose_name='Соискатель')),
            ],
        ),
    ]
