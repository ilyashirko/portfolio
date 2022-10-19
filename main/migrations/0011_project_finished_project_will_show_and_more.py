# Generated by Django 4.1.1 on 2022-09-17 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_person_nickname_alter_project_develop_stack'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='finished',
            field=models.BooleanField(default=True, verbose_name='Проект завершен?'),
        ),
        migrations.AddField(
            model_name='project',
            name='will_show',
            field=models.BooleanField(default=False, verbose_name='Показывать в подборке?'),
        ),
        migrations.AlterField(
            model_name='person',
            name='nickname',
            field=models.CharField(default='IcPTRxox', max_length=50, unique=True, verbose_name='Никнейм'),
        ),
        migrations.AlterField(
            model_name='project',
            name='short_description',
            field=models.TextField(max_length=500, verbose_name='Короткое описание'),
        ),
    ]
