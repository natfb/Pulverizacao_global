# Generated by Django 5.1 on 2024-10-01 23:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_alter_guia_aplicacao_piloto_id_aplicacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guia_aplicacao_supervisor',
            name='cod_aplicacao',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        
    ]