# Generated by Django 4.0.4 on 2022-05-25 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PostMaster', '0009_package_has_tracking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='has_tracking',
            field=models.BooleanField(default=False, editable=False, verbose_name='No Tracking'),
        ),
    ]
