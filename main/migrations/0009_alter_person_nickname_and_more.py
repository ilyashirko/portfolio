# Generated by Django 4.1.1 on 2022-09-17 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_project_alter_biographychapter_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nickname',
            field=models.CharField(default='bjaIopbY', max_length=50, unique=True, verbose_name='Никнейм'),
        ),
        migrations.AlterField(
            model_name='project',
            name='short_description',
            field=models.TextField(max_length=200, verbose_name='Короткое описание'),
        ),
    ]
