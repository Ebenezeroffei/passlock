# Generated by Django 3.0.5 on 2020-04-30 22:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0003_auto_20200430_2031'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DefaultAccount',
            new_name='Account',
        ),
        migrations.RenameModel(
            old_name='CustomFieldsForDefaultAccount',
            new_name='CustomFieldsForAccount',
        ),
        migrations.RenameField(
            model_name='customfieldsforaccount',
            old_name='default_account',
            new_name='account',
        ),
    ]