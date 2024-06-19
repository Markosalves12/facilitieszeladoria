from django.db import models
from unidadee.models import Unidade, Localidade
from empresa.models import Empresa

# Create your models here.
class FiltroTable(models.Model):
    datafim = models.DateField(
        blank=True,
        null=True
    )

    unidade = models.ForeignKey(
        to=Unidade,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='unidadefiltro'
    )

    empresa = models.ForeignKey(
        to=Empresa,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='unidadefiltro'
    )

    datastart = models.DateField(
        blank=True,
        null=True
    )

    localidade = models.ForeignKey(
        to=Localidade,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='localidadefiltro'
    )

    def __str__(self):
        return f"{self.datafim}, {self.datastart}"



class FiltroTableManutencao(models.Model):
    datafim = models.DateTimeField(
        blank=True,
        null=True
    )

    unidade = models.ForeignKey(
        to=Unidade,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='unidadefiltromanutencao'
    )

    datastart = models.DateTimeField(
        blank=True,
        null=True
    )

    empresa = models.ForeignKey(
        to=Empresa,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='empresafiltromanutencao'
    )

    status_options = [
        ('Mobilizado', 'Mobilizado'),
        ('Desmobilizado', 'Desmobilizado'),
        ('Desmobilizacao Permanente', 'Desmobilizacao Permanente')
    ]

    status = models.CharField(max_length=60, blank=True, null=True, choices=status_options, default='Mobilizado')

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

    tipo_manutencao = models.CharField(max_length=60, blank=True, null=True,
                                       choices=opcoes_manutencoes, default='')

    def __str__(self):
        return f"{self.datafim}, {self.datastart}"