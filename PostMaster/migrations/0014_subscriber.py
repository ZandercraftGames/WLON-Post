# Generated by Django 4.0.4 on 2022-05-28 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PostMaster', '0013_alter_nation_options_alter_package_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=16, verbose_name="Subscriber's Username")),
                ('UUID', models.UUIDField(verbose_name="Subscriber's UUID")),
                ('email', models.EmailField(max_length=254, verbose_name="Subscriber's Email")),
            ],
            options={
                'verbose_name': 'Subscriber',
                'verbose_name_plural': 'Subscribers',
            },
        ),
    ]
