# Generated by Django 4.1.3 on 2022-11-03 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_basic',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='is_income',
            field=models.BooleanField(default=False),
        ),
    ]
