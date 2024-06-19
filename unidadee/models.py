from django.db import models
import random


# Função que cria um id randomico para identificar os objetos nos bancos de dados
# a funcao generate_id_random oarace varias vezes no código
# isolar a função gera um erro de referencia circular sabe - se Deus porque
def generate_id_random():
    while True:
        # Generate a random integer between 0 and 999999 inclusive
        random_int = random.randint(0, 999998)
        return random_int


# Função que cria um id randomico para identificar os objetos nos bancos de dados
# a funcao generate_id_random oarace varias vezes no código
# isolar a função gera um erro de referencia circular sabe - se Deus porque
def generate_id_random_localidade():
    while True:
        # Generate a random integer between 0 and 999999 inclusive
        random_int = random.randint(0, 999998)
        return random_int


# Create your models here.
class Unidade(models.Model):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )

    unidade = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )

    link = models.CharField(
        max_length=150,
        blank=False,
        null=False
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

    def __str__(self):
        return self.unidade


class Localidade(models.Model):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random_localidade
    )

    nome = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    unidadeoriginial = models.ForeignKey(
        to=Unidade,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="unidadeoriginal"
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

    negocio_options = [
        ('Industrial', 'Industrial'),
        ('Florestal', 'Florestal'),
        ('Outros', 'Outros')
    ]

    negocio = models.CharField(
        max_length=60,
        blank=True,
        null=True,
        choices=negocio_options,
        default='Industrial'
    )

    class Meta:
        unique_together = ('nome', 'unidadeoriginial', 'negocio')

    def __str__(self):
        return f"{self.unidadeoriginial} | {self.nome} | {self.negocio}"
