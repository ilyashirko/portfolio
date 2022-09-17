# Generated by Django 4.1.1 on 2022-09-17 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_person_telegram_id_alter_person_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25, unique=True, verbose_name='Название проекта')),
                ('url', models.URLField(blank=True, verbose_name='Ссылка на github')),
                ('short_description', models.CharField(max_length=200, verbose_name='Короткое описание')),
                ('develop_stack', models.ManyToManyField(related_name='Стек', to='main.hardskill', verbose_name='projects')),
            ],
        ),
        migrations.AlterField(
            model_name='biographychapter',
            name='photo',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='biography_chapter', to='main.photo', verbose_name='Фотография'),
        ),
        migrations.AlterField(
            model_name='person',
            name='nickname',
            field=models.CharField(default='AkLkOrVC', max_length=50, unique=True, verbose_name='Никнейм'),
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.SmallIntegerField(default=0, verbose_name='Порядковый номер (UNIQUE ONLY)')),
                ('image', models.ImageField(upload_to='images', verbose_name='Фотография')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.project', verbose_name='Проект')),
            ],
            options={
                'ordering': ['index'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='main.person', verbose_name='Соискатель'),
        ),
    ]
