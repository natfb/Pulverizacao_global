# Generated by Django 5.1 on 2024-10-04 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_alter_guia_aplicacao_supervisor_cod_aplicacao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]