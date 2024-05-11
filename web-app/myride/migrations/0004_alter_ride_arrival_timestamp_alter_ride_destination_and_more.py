# Generated by Django 4.0.1 on 2022-01-29 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myride', '0003_alter_user_name_alter_user_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='arrival_timestamp',
            field=models.DateTimeField(verbose_name='Arrival Time, format: YYYY-MM-DD HH:MM:SS or MM/DD/YY HH:MM'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='destination',
            field=models.CharField(max_length=100, verbose_name='Destination'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='num_passengers',
            field=models.IntegerField(verbose_name='Number of Passengers'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='special_req',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Special requests (optional)'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='vehicle_type',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Car type (optional)'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='max_passenger',
            field=models.IntegerField(verbose_name='Maximum passengers'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='plate_num',
            field=models.CharField(max_length=20, verbose_name='Plate number'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='special_info',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Special car info (optional)'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='type',
            field=models.CharField(max_length=20, verbose_name='Car type'),
        ),
    ]
