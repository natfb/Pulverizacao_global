# Generated by Django 5.1 on 2024-09-13 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_aeronave_rename_pilots_pilot_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Farms',
            new_name='Farm',
        ),
    ]