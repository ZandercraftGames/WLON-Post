# Generated by Django 4.0.4 on 2022-05-24 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PostMaster', '0007_alter_tracking_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracking',
            name='package',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PostMaster.package'),
        ),
    ]