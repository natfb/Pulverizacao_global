# Generated by Django 5.1 on 2024-11-14 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_rename_id_produto_guia_aplicacao_supervisor_id_receita_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guia_aplicacao_supervisor',
            name='id_receita',
        ),
    ]
