# Generated by Django 4.1.1 on 2022-09-17 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_project_finished_project_will_show_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nickname',
            field=models.CharField(default='kFHrlfMb', max_length=50, unique=True, verbose_name='Никнейм'),
        ),
    ]
