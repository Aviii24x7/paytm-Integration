# Generated by Django 4.1.7 on 2023-07-04 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payApp', '0005_user_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='datetime',
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
