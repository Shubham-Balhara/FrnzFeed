# Generated by Django 2.0.2 on 2018-08-06 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0016_auto_20180221_0019'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('ch_name', models.CharField(max_length=1000)),
            ],
        ),
    ]