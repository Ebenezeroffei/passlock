# Generated by Django 3.0.5 on 2020-05-04 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20200430_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfieldsforaccount',
            name='field_type',
            field=models.CharField(choices=[('Password', 'Password'), ('Text', 'Text'), ('Email', 'Email'), ('Number', 'Number')], max_length=100),
        ),
    ]