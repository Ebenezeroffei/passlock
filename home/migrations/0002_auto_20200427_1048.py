# Generated by Django 3.0.5 on 2020-04-27 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defaultaccount',
            name='username',
        ),
        migrations.AddField(
            model_name='defaultaccount',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
    ]
