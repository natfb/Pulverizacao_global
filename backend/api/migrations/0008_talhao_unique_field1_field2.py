# Generated by Django 5.1 on 2024-08-22 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_farm_id_talhao_farm'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='talhao',
            constraint=models.UniqueConstraint(fields=('farm', 'id_talhao'), name='unique_field1_field2'),
        ),
    ]
