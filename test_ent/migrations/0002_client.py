# Generated by Django 3.1.1 on 2020-09-17 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_ent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=80)),
                ('city', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
