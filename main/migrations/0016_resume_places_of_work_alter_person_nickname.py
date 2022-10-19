# Generated by Django 4.1.1 on 2022-10-19 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_highereducation_finished_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='places_of_work',
            field=models.ManyToManyField(related_name='resume', to='main.placeofwork', verbose_name='Опыт работы'),
        ),
        migrations.AlterField(
            model_name='person',
            name='nickname',
            field=models.CharField(default='nqBvUYCo', max_length=50, unique=True, verbose_name='Никнейм'),
        ),
    ]
