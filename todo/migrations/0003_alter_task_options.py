# Generated by Django 5.0.4 on 2024-04-29 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_task_date_added'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['date_added']},
        ),
    ]
