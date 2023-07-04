# Generated by Django 4.1.7 on 2023-07-01 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=54)),
                ('phone', models.CharField(max_length=13)),
                ('amount', models.IntegerField()),
            ],
        ),
    ]
