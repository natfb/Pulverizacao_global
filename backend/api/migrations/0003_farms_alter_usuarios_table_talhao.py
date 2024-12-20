# Generated by Django 5.1 on 2024-08-21 23:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_pilots_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Farms',
            fields=[
                ('id_farm', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=80)),
                ('owner', models.TextField()),
                ('city', models.TextField()),
                ('state', models.TextField()),
            ],
            options={
                'db_table': 'farms',
            },
        ),
        migrations.AlterModelTable(
            name='usuarios',
            table='users',
        ),
        migrations.CreateModel(
            name='Talhao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_talhao', models.BigIntegerField()),
                ('area', models.FloatField()),
                ('cultura', models.TextField()),
                ('technician', models.TextField()),
                ('id_farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.farms')),
            ],
            options={
                'db_table': 'talhao',
            },
        ),
    ]