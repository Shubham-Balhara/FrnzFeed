# Generated by Django 2.0.2 on 2018-02-20 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0014_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='post_no',
            new_name='post',
        ),
    ]