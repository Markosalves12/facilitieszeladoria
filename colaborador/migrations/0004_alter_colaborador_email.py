# Generated by Django 5.0.6 on 2024-05-26 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("colaborador", "0003_remove_colaborador_gerente_colaborador_gerente"),
    ]

    operations = [
        migrations.AlterField(
            model_name="colaborador",
            name="email",
            field=models.EmailField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
