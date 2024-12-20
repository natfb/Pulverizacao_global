# Generated by Django 5.1 on 2024-09-06 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_talhao_farm'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nome_Comercial', models.TextField()),
                ('grupo_Produto', models.TextField()),
                ('principio_Ativo', models.TextField()),
                ('dosagem', models.TextField()),
                ('taxa_Aplicacao', models.TextField()),
                ('observacoes', models.TextField()),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'db_table': 'product',
            },
        ),
    ]
