# Generated by Django 5.1 on 2024-09-05 01:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_talhao_unique_field1_field2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talhao',
            name='farm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.farms'),
        ),
    ]