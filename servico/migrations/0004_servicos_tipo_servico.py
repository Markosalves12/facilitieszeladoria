# Generated by Django 5.0.6 on 2024-06-10 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("servico", "0003_servicos_foto_inicio"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicos",
            name="tipo_servico",
            field=models.CharField(
                choices=[
                    ("Agendado", "Agendado"),
                    ("Cancelado", "Cancelado"),
                    ("Em andamento", "Em andamento"),
                    ("Concluido", "Concluido"),
                ],
                default="Regular",
                max_length=60,
            ),
        ),
    ]
