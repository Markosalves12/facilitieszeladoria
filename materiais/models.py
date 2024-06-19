from django.db import models
from empresa.models import Empresa
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

class Materiais(models.Model):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )


    material = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    categoria_options = [
        ('Fertilizante','Fertilizante'),
        ('pesticida', 'pesticida'),
        ('Formicida', 'Formicida'),
        ('Adubos', 'Adubos'),
        ('Herbicida', 'Herbicida'),
        ('Fungicida', 'Fungicida'),
        ('Inseticida', 'Inseticida'),
        # ('Micronutrientes', 'Micronutrientes'),
        ('Condicionadores de Solo', 'Condicionadores de Solo'),
        ('Inoculantes', 'Inoculantes'),
        ('Mulching', 'Mulching'),
        ('Anti - caracóis e lesmas', 'Anti - caracóis e lesmas'),
        ('Bioestimulantes', 'Bioestimulantes'),
        ('Adjuvantes', 'Adjuvantes'),
    ]
    categoria = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        choices=categoria_options,
        default=''
    )

    consumo_options = [
        ('Sache','Sache'),
        ('KG', 'KG'),
        ('Refil', 'Refil'),
        ('Litros', 'Litros'),
        ('Pacote', 'Pacote'),
        ('Barra', 'Barra'),
        ('Galões ', 'Galões '),
        ('Peças', 'Peças'),
        ('Unidades', 'Unidades'),
        ('Potes', 'Potes'),
        ('Tubos', 'Tubos'),
        ('Fardos', 'Fardos'),
        ('Sacos', 'Sacos'),
    ]
    consumo = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=consumo_options,
        default=''
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

    empresa = models.ForeignKey(
        to=Empresa,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        unique_together = ('material', 'categoria', 'consumo', 'empresa', )


    def __str__(self):
        return f'{self.material} | {self.categoria} | {self.consumo} | {self.empresa}'