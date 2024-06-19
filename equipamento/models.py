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

class CatalogoEquipamentos(models.Model):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )

    nome = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    marca = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    vida_util_meses = models.IntegerField()

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
        related_name='empresacatalogoequipamento'
    )

    class Meta:
        unique_together = ('nome', 'marca', 'empresa', )

    def __str__(self):
        return f"{self.nome} | {self.marca} | {self.empresa}"


class EquipamentoDisponivel(models.Model):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )

    data_aquisicao = models.DateField(
        blank=False,
        null=False
    )

    data_desmobilizacao = models.DateField(
        null=True,
        blank=True
    )

    matricula = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )

    catalogo_equipamento = models.ForeignKey(
        to=CatalogoEquipamentos,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="catalogoequipamentooriginal"
    )

    empresa = models.ForeignKey(
        to=Empresa,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='empresaequipamentoorigem'
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

    tipo_options = [
        ('Próprio', 'Próprio'),
        ('Terceirizado', 'Terceirizado'),
    ]

    tipo = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=tipo_options,
        default=''
    )


    def __str__(self):
        return f"{self.catalogo_equipamento} | {self.matricula} | {self.empresa} | {self.tipo}"


class ManutencaoEquipamentos(models.Model):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )

    data_hora_inicio = models.DateTimeField(
        blank=False,
        null=False
    )

    data_hora_fim = models.DateTimeField()

    descricao_servico = models.TextField()

    descricao_motivo = models.TextField()

    equipamento = models.ForeignKey(
        to=EquipamentoDisponivel,
        on_delete=models.CASCADE
    )

    opcoes_manutencoes = [
        ('Preventiva', 'Preventiva'),
        ('Corretiva', 'Corretiva'),
        ('Detectiva', 'Detectiva'),
        ('Proativa', 'Proativa'),
        ('De Oportunidade', 'De Oportunidade'),
        ('Planejada', 'Planejada'),
        ('Autônoma', 'Autônoma'),
        ('Condicional', 'Condicional'),
        ('De Emergência', 'De Emergência'),
        ('De Rotina', 'De Rotina'),
    ]

    tipo_manutencao = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=opcoes_manutencoes,
        default=''
    )
