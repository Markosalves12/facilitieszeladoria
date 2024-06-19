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

class CatalogoServicos(models.Model):
    # conluna principal usada como parametro de urls
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )

    # nome do serviço
    # ex:
    # capina quimica
    # roçada mecanizada
    # capina manual
    servico = models.CharField(
        max_length=60,
        blank=False,
        null=False
    )

    # a coluna status controla a disponibilidade do objeto no formularios espalhados pelo sistema
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

    # a coluna empresa faz o mapeamento dos serviços que empresa pratica
    empresa = models.ForeignKey(
        to=Empresa,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="catalogoservicoempresa"
    )

    # servico e empresa, funcionam como chave primaria
    # nao pode existir duplicatas para essa combinação
    class Meta:
        unique_together = ('servico', 'empresa',)

    def __str__(self):
        return f'{self.servico} | {self.empresa}'