# Generated by Django 4.0.5 on 2022-08-14 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20)),
                ('mobile', models.IntegerField()),
                ('mail', models.EmailField(max_length=254)),
                ('about', models.TextField()),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
