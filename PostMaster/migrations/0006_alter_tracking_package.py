# Generated by Django 4.0.4 on 2022-05-24 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PostMaster', '0005_alter_nation_code_alter_nation_leader_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracking',
            name='package',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='PostMaster.package'),
        ),
    ]