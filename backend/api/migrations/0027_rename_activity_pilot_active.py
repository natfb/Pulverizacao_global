# Generated by Django 5.1 on 2024-09-18 00:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_guia_aplicacao_supervisor_talhao'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pilot',
            old_name='activity',
            new_name='active',
        ),
    ]
