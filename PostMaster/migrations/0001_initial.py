# Generated by Django 4.0.4 on 2022-05-24 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_id', models.UUIDField()),
                ('receiving_date', models.DateTimeField(verbose_name='date received')),
                ('return_address', models.CharField(max_length=200, verbose_name='address to return package to')),
                ('delivery_address', models.CharField(max_length=200, verbose_name='address to send package to')),
                ('from_nation', models.CharField(max_length=50, verbose_name='sent from nation')),
                ('to_nation', models.CharField(max_length=50, verbose_name='sent to this nation')),
            ],
        ),
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_code', models.UUIDField()),
                ('status', models.CharField(choices=[('PS', 'Pre-Shipment'), ('RX', 'Received'), ('TF', 'In Transit (Domestic)'), ('ID', 'In Transit to Distribution Centre'), ('IW', 'At Distribution Centre'), ('IN', 'In Transit to Nation'), ('DF', 'Delivered')], default='PS', max_length=2)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PostMaster.package')),
            ],
        ),
    ]
