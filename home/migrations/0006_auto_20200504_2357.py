# Generated by Django 3.0.5 on 2020-05-04 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20200504_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfieldsforaccount',
            name='field_type',
            field=models.CharField(choices=[('password', 'Password'), ('text', 'Text'), ('email', 'Email'), ('number', 'Number')], max_length=100),
        ),
    ]
