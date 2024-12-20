# Generated by Django 5.1 on 2024-11-14 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_guia_aplicacao_piloto_observacao_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guia_aplicacao_supervisor',
            old_name='id_produto',
            new_name='id_receita',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='dosagem',
            new_name='dosagem_recomendada',
        ),
        migrations.RemoveField(
            model_name='guia_aplicacao_supervisor',
            name='dosagem',
        ),
        migrations.RemoveField(
            model_name='product',
            name='taxa_aplicacao',
        ),
        migrations.CreateModel(
            name='Receita',
            fields=[
                ('id_receita', models.AutoField(primary_key=True, serialize=False)),
                ('dosagem', models.FloatField()),
                ('taxa_aplicacao', models.FloatField()),
                ('id_produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
            options={
                'db_table': 'receita',
            },
        ),
        migrations.DeleteModel(
            name='Foto_telemetria',
        ),
    ]
