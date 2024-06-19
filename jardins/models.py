from django.db import models
from unidadee.models import Localidade
from catalogoservico.models import CatalogoServicos
import random

# Create your models here.

# Função que cria um id randomico para identificar os objetos nos bancos de dados
# a funcao generate_id_random oarace varias vezes no código
# isolar a função gera um erro de referencia circular sabe - se Deus porque
def generate_id_random():
    while True:
        # Generate a random integer between 0 and 999999 inclusive
        random_int = random.randint(0, 999998)
        return random_int

class Jardins(models.Model):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )

    nome = models.CharField(
        max_length=30,
        blank=False,
        null=False
    )

    area = models.FloatField(
        null=False,
        blank=False
    )

    tipo_vegetacao = [
        ('Grama', 'Grama'),
        ('Mata nativa', 'Mata nativa'),
        ('Mata de eucalipto', 'Mata de eucalipto'),
        ('Bosque', 'Bosque'),
        ('Cerca viva', 'Cerca viva'),
        ('Bosque de plantio vivo', 'Bosque de plantio vivo'),
        ('Jardim', 'Jardim'),
        ('Palmeiras', 'Palmeiras'),
        ('Outros Pisos', 'Outros Pisos')
    ]

    vegetacao = models.CharField(
        max_length=100,
        default='',
        choices=tipo_vegetacao
    )

    tipo_terreno = [
        ('Talude', 'Talude'),
        ('Área plana concretada', 'Área plana concretada'),
        ('Área plana não concretada', 'Área plana não concretada'),
    ]

    terreno = models.CharField(
        max_length=100,
        default='',
        choices=tipo_terreno
    )

    servicos_na_area = models.ForeignKey(
        to=CatalogoServicos,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='servicooriginal'
    )

    unidade_jardim = models.ForeignKey(
        to=Localidade,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='localidadeoriginal'
    )

    status_options = [
        ('Mobilizado', 'Mobilizado'),
        ('Desmobilizado', 'Desmobilizado'),
        ('Desmobilizacao Permanente', 'Desmobilizacao Permanente')
    ]

    status = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=status_options,
        default='Mobilizado'
    )

    opcoes_periodicidade = [
        ('Mensal', 'Mensal'),
        ('Semanal', 'Semanal'),
        ('Quinzenal', 'Quinzenal'),
        ('Bimestral', 'Bimestral'),
        ('Semestral', 'Semestral'),
        ('Trimestral', 'Trimestral')
    ]

    periodicidade = models.CharField(
        max_length=100,
        default='',
        choices=opcoes_periodicidade,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('nome', 'unidade_jardim', 'vegetacao', 'terreno')

    def __str__(self):
        return f"{self.nome} | {self.unidade_jardim}"
