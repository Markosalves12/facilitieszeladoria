# Generated by Django 5.0.6 on 2024-06-12 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("empresa", "0003_empresa_tipo_empresa"),
        ("unidadee", "0003_alter_localidade_negocio"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="empresa",
            unique_together={("cnpj", "unidade", "tipo_empresa")},
        ),
    ]
