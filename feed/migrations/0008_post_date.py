# Generated by Django 2.0.2 on 2018-02-19 13:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0007_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
