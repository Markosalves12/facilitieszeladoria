from django.db import models
from equipamento.models import EquipamentoDisponivel
from ferramenta.models import FerramentaDisponivel
from colaborador.models import Colaborador
from catalogoservico.models import CatalogoServicos
from jardins.models import Jardins
from materiais.models import Materiais
import random
from utils.utils import resize_image


# Create your models here.

# Função que cria um id randomico para identificar os objetos nos bancos de dados
# a funcao generate_id_random oarace varias vezes no código
# isolar a função gera um erro de referencia circular sabe - se Deus porque
def generate_id_random():
    while True:
        # Generate a random integer between 0 and 999999 inclusive
        random_int = random.randint(0, 999998)
        return random_int


# model de agendamento de novos servicos
class Servicos(models.Model):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )

    servicos_escalados = models.ManyToManyField(
        to=CatalogoServicos,
        blank=False,
        null=False,
        related_name="catalogoservicooriginal",
    )

    descricao_servico = models.TextField(
        max_length = 100,
        blank=False,
        null=False,
    )

    data_inicio = models.DateField(
        blank=False,
        null=False,
    )

    colaboradores_escalados = models.ManyToManyField(
        to=Colaborador,
        blank=False,
        null=False,
        related_name="colaboradoresoriginais",
    )

    area = models.ForeignKey(
        to=Jardins,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='areaoriginais'
    )

    status_options = [
        ('Agendado', 'Agendado'),
        ('Cancelado', 'Cancelado'),
        ('Em andamento', 'Em andamento'),
        ('Concluido', 'Concluido')
    ]
    status = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=status_options,
        default='Agendado'
    )

    foto_inicio = models.ImageField(
        upload_to="media/%Y/%m/%d/",
        blank=True,
        max_length=500
    )

    foto = models.ImageField(
        upload_to="media/%Y/%m/%d/",
        blank=True,
        max_length=500
    )

    data_conclusao = models.DateField(
        blank=True,
        null=True
    )

    prest_options = [
        ('Regular', 'Regular'),
        ('Extra', 'Extra'),
        ('Outros', 'Outros'),
    ]
    tipo_servico = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=prest_options,
        default='Regular'
    )

    # função que trata as imagens enviadas
    # para padronizar a largura da imagem
    # antes de salvar no banco de imagens
    def save(self, *args, **kwargs):
        # Redimensiona as imagens se necessário antes de salvar
        if self.foto_inicio:
            self.foto_inicio = resize_image(self.foto_inicio)
        if self.foto:
            self.foto = resize_image(self.foto)
        super(Servicos, self).save(*args, **kwargs)


    def __str__(self):
        colaboradores_nomes = ", ".join(colaborador.nome for colaborador in self.colaboradores_escalados.all())
        return f"{self.descricao_servico} | {self.data_inicio} | {colaboradores_nomes} "


# model de acompanhamento de servicos por colaborador
class FatoServico(models.Model):
    servico = models.ForeignKey(
        to=Servicos,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="servicooriginal"
    )


    data_hora_chegada_na_area = models.DateTimeField(
        blank=False,
        null=False
    )

    equipamentos_usados = models.ForeignKey(
        to=EquipamentoDisponivel,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="equipamentodisponiveloriginal"
    )


    ferramentas_usados = models.ForeignKey(
        to=FerramentaDisponivel,
        default='',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="ferramentadisponiveloriginal"
    )


    data_hora_retorno_area = models.DateTimeField(
        blank=False,
        null=False
    )

    material_usado = models.ForeignKey(
        to=Materiais,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='materiaisusados'
    )

    servico_aplicado = models.ForeignKey(
        to=CatalogoServicos,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    quantidade = models.FloatField(
        blank=True,
        null=True
    )

    tipo_options = [
        ('Proprio', 'Proprio'),
        ('Terceirizado', 'Terceirizado'),
    ]

    tipo = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=tipo_options,
        default='Proprio'
    )

    colaborador = models.ForeignKey(
        to=Colaborador,
        blank=False,
        null=True,
        on_delete=models.CASCADE,
        related_name='colaboradorservico'
    )