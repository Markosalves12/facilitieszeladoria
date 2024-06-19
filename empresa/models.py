from django.db import models
from unidadee.models import Unidade
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

class Empresa(models.Model):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )

    nome = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
    )

    razao_social = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    cnpj = models.CharField(
        max_length=18,
        blank=False,
        null=False,
    )

    unidade = models.ForeignKey(
        to=Unidade,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='unidadeorigem'
    )

    tipo_options = [
        ('Jardinagem', 'Jardinagem'),
        ('Limpeza predial', 'Limpeza predial'),
    ]

    tipo_empresa = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=tipo_options,
        default='Jardinagem'
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

    class Meta:
        unique_together = ('cnpj', 'unidade', 'tipo_empresa')

    def __str__(self):
        return f"{self.nome} | {self.unidade} | {self.tipo_empresa}"