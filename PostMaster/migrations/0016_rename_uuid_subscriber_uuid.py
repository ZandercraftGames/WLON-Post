# Generated by Django 4.0.4 on 2022-05-28 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PostMaster', '0015_alter_subscriber_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscriber',
            old_name='UUID',
            new_name='uuid',
        ),
    ]