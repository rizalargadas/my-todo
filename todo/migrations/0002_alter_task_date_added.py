# Generated by Django 5.0.4 on 2024-04-29 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
