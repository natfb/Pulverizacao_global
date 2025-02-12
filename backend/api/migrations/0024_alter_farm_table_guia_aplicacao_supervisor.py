# Generated by Django 5.1 on 2024-09-16 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_alter_pilot_table_alter_usuario_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='farm',
            table='farm',
        ),
        migrations.CreateModel(
            name='Guia_aplicacao_supervisor',
            fields=[
                ('cod_aplicacao', models.IntegerField(max_length=50, primary_key=True, serialize=False)),
                ('data', models.DateField(auto_now_add=True)),
                ('cultura', models.CharField(choices=[('', 'Escolha a cultura'), ('Algodão', 'Algodão'), ('Cana-de-açucar', 'Cana-de-açucar'), ('Milho', 'Milho'), ('Pasto', 'Pasto'), ('Soja', 'Soja')], max_length=50)),
                ('area_aplicacao', models.FloatField()),
                ('dosagem', models.FloatField()),
                ('id_responsavel_global', models.CharField(max_length=100)),
                ('realizado', models.BooleanField(default=False)),
                ('id_fazenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.farm')),
                ('id_produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
    ]
