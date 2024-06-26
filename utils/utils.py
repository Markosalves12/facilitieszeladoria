from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect
from gestor.models import Gestor
from gerente.models import Gerente
from django.contrib import messages
from colaborador.models import Colaborador
from django.shortcuts import get_object_or_404
from django.db.models.functions import Coalesce, ExtractDay
from django.db.models import ExpressionWrapper, F, IntegerField, DurationField, FloatField
from django.utils import timezone
from django.core.files.base import ContentFile
import random
from PIL import Image
from io import BytesIO
import os
import secrets
import string




def gerar_codigo_aleatorio(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(
        secrets.choice(caracteres) for i in range(tamanho)
    )
    return codigo


def resize_image(image, max_width=620):
    # Dicionário de mapeamento de extensões para formatos Pillow
    EXTENSION_TO_FORMAT = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.gif': 'GIF',
        '.bmp': 'BMP',
        '.tiff': 'TIFF',
        '.webp': 'WEBP'
    }

    # Abre a imagem usando Pillow
    img = Image.open(image)

    # Verifica a extensão do arquivo
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in EXTENSION_TO_FORMAT:
        raise ValueError(f"Unsupported file extension: {ext}")

    # Calcula a nova dimensão se a largura for maior que max_width
    if img.width > max_width:
        aspect_ratio = img.height / img.width
        new_width = max_width
        new_height = int(new_width * aspect_ratio)
        img = img.resize((new_width, new_height), Image.LANCZOS)

    # Salva a imagem redimensionada no formato correto
    img_io = BytesIO()
    img_format = EXTENSION_TO_FORMAT[ext]
    img.save(img_io, format=img_format)
    return ContentFile(img_io.getvalue(), image.name)


def generate_id_random():
    while True:
        # Generate a random integer between 0 and 999999 inclusive
        random_int = random.randint(0, 999998)
        return random_int


def paginate(request, data_objects, per_page=10):
    paginator = Paginator(data_objects, per_page=per_page)
    page_number = request.GET.get('page')

    try:
        elementos_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        # Se o número da página não for um número inteiro, retorne a primeira página
        elementos_paginados = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo (por exemplo, 9999), retorne a última página de resultados
        elementos_paginados = paginator.page(paginator.num_pages)

    return elementos_paginados


def block_view(request, login_type, id):
    # Verifique se o usuário está autenticado
    if request.session.get('login_type', '') == login_type and request.session.get('login_id', '') == id:
        if login_type == "Administrador":
            return False

        elif login_type == "Gestor":
            gestor = Gestor.objects.get(id_random=id)
            if gestor.status == "Mobilizado":
                return False
            return True
        elif login_type == "Gerente":
            gerente = Gerente.objects.get(id_random=id)
            if gerente.status == "Mobilizado":
                return False
            return True
    else:
        # O usuário não está autenticado, redirecione para a página de login
        return True


def capturate_paramns(login_type, id, type="unidade"):
    if type == "unidade":
        if login_type == "Administrador":
            unidade = ""
            return unidade

        elif login_type == "Gestor":
            gestor = Gestor.objects.get(
                id_random=id
            )
            unidade = gestor.empresa.unidade
            return unidade

        elif login_type == "Gerente":
            gerente = Gerente.objects.get(
                id_random=id
            )
            unidade = gerente.gestor.empresa.unidade
            return unidade

        elif login_type == "Colaborador":
            return redirect('servicos_agendados', login_type, id)

    elif type == "empresa":
        if login_type == "Administrador":
            empresa = ""
            return empresa

        elif login_type == "Gestor":
            gestor = Gestor.objects.get(
                id_random=id
            )
            empresa = gestor.empresa
            return empresa

        elif login_type == "Gerente":
            gerente = Gerente.objects.get(
                id_random=id
            )
            empresa = gerente.gestor.empresa
            return empresa

        elif login_type == "Colaborador":
            colaborador = Colaborador.objects.get(
                id_random=id
            )
            empresa = colaborador.gerente.gestor.empresa
            return empresa

        else:
            return redirect('servicos_agendados', login_type, id)

def capturate_object(model, object_id):
    return get_object_or_404(model, id_random=object_id)


def alterar_status(request, model, object_id, desm='mob', data = None):
    obj = capturate_object(model, object_id)

    if desm == 'temp':
        if data != None:
            if obj.data_desmobilizacao == None or obj.data_desmobilizacao == '':
                obj.data_desmobilizacao = timezone.now().date()

        obj.status = "Desmobilizado"
        messages.success(request, f"{model.__name__} {obj} desmobilizado(a) com sucesso")

    elif desm == 'perm':
        if data != None:
            if obj.data_desmobilizacao == None or obj.data_desmobilizacao == '':
                obj.data_desmobilizacao = timezone.now().date()

        obj.status = "Desmobilizacao Permanente"
        messages.success(request, f"{model.__name__} {obj} desmobilizado(a) permanentemente com sucesso")

    elif desm == 'mob':
        if data != None:
            if obj.data_desmobilizacao != None or obj.data_desmobilizacao != '':
                obj.data_desmobilizacao = None

        obj.status = "Mobilizado"
        messages.success(request, f"{model.__name__} {obj} Reabilitado(a) com sucesso")

    obj.save()




def formatar_atributos(queryset, atributo):
    """
    Converte uma queryset em uma string de valores de um atributo específico, separados por vírgulas.

    :param queryset: Queryset de objetos de um modelo Django.
    :param atributo: O nome do atributo do modelo que deve ser extraído.
    :return: Uma string com os valores do atributo separados por vírgulas.
    """
    # Cria uma lista de valores do atributo especificado
    valores = [getattr(obj, atributo) for obj in queryset]

    # Junta os valores em uma única string, separada por vírgulas
    valores_texto = ", ".join(str(valor) for valor in valores)

    return valores_texto


# # Exemplo de uso para dado.servicos_escalados.all() e o campo 'servico'
# servicos_escalados = dado.servicos_escalados.all()
# texto_formatado = formatar_atributos(servicos_escalados, 'servico')
#
# # Exemplo de uso para outro modelo e campo
# outro_queryset = outro_modelo.objects.all()
# outro_texto_formatado = formatar_atributos(outro_queryset, 'outro_campo')


# .annotate(
#     data_atual=TruncDate(Now()),
#     timeagendamento=ExpressionWrapper(
#         F('data_inicio') - F('data_atual'),
#         output_field=DurationField()
#     ),
#     status_agendamento=ExpressionWrapper(
#         ExtractDay(F('data_inicio') - F('data_atual')),
#         output_field=IntegerField()
#     ),
# )

def colect_dados(modelo, vida_util_campo, empresa=None):
    data_atual = timezone.datetime.now().date()
    filtro_empresa = {} if empresa is None else {'empresa': empresa}

    dados = modelo.objects.annotate(
        data_desmobilizacao_coalesce=Coalesce('data_desmobilizacao', data_atual),
        tempooperacaco=ExpressionWrapper(
            F('data_desmobilizacao_coalesce') - F('data_aquisicao'),
            output_field=DurationField()
        ),
        diferenca_dias=ExpressionWrapper(
            (ExtractDay(F('data_aquisicao') - F('data_desmobilizacao_coalesce')) / (
                        F('vida_util_campo') * 30.44)) * 100,
            output_field=FloatField()
        ),
    ).filter(
        **filtro_empresa,
    )

    return dados


class DadosDisponiveisHandler:
    def __init__(self, login_type, id=None, model=None, form_cls=None, vida_util_campo=None):
        self.login_type = login_type
        self.id = id
        self.model = model
        self.form_cls = form_cls
        self.vida_util_campo = vida_util_campo

    def verify_login_type_and_return_objects(self):
        if self.login_type == 'Colaborador':
            return redirect('servicos_agendados', self.login_type, self.id)


        if self.login_type == 'Administrador':
            empresa = capturate_paramns(login_type=self.login_type, type='empresa', id=self.id)
            dados_disponiveis = colect_dados(self.model, self.vida_util_campo).filter(
                status__in=['Mobilizado']
            )

            return dados_disponiveis, empresa, self.form_cls

        elif self.login_type == 'Gestor':
            empresa = capturate_paramns(login_type=self.login_type, type='empresa', id=self.id)
            dados_disponiveis = colect_dados(self.model, self.vida_util_campo, empresa=empresa)
            dados_disponiveis = dados_disponiveis.filter(
                empresa_id=empresa.id
            ).filter(
                status__in=['Mobilizado']
            )

            return dados_disponiveis, empresa, self.form_cls(empresa=empresa)

        elif self.login_type == 'Gerente':
            empresa = capturate_paramns(login_type=self.login_type, type='empresa', id=self.id)
            dados_disponiveis = colect_dados(self.model, self.vida_util_campo, empresa=empresa)
            dados_disponiveis = dados_disponiveis.exclude(status__in=['Desmobilizado', 'Desmobilizacao Permanente'])
            dados_disponiveis = dados_disponiveis.filter(
                empresa_id=empresa.id
            ).filter(
                status__in=['Mobilizado']
            )

            return dados_disponiveis, empresa, self.form_cls(empresa=empresa)


def editar_item(id, model, form_class):
    item = model.objects.get(id_random=id)
    empresa = item.empresa
    item_form = form_class(instance=item, empresa=empresa)
    return item, empresa, item_form



# class DadosObjetosAndFormulario:
#     def __init__(self, login_type, id, status, obj_class, form_class, obj_id=None):
#         self.login_type = login_type
#         self.id = id
#         self.status = status
#         self.obj_class = obj_class
#         self.form_class = form_class
#         self.obj_id = obj_id
#
#     def verify_login_type_and_return_objects(self):
#         if self.login_type == "Colaborador":
#             return redirect("servicos_agendados", self.login_type, self.id)
#
#         unidade = None
#         if self.login_type in ["Administrador", "Gestor", "Gerente"]:
#             unidade = capturate_paramns(self.login_type, self.id)
#
#         if self.login_type == "Administrador":
#             dados_objetos = self.obj_class.objects.filter(status__in=self.status)
#         elif self.login_type == "Gestor":
#             dados_objetos = self.obj_class.objects.filter(status__in=self.status, unidade=unidade)
#         elif self.login_type == "Gerente":
#             dados_objetos = self.obj_class.objects.filter(status__in=self.status[0:1], unidade=unidade)
#         else:
#             return redirect('logout', self.login_type, self.id)
#
#         objeto = None
#         if self.obj_id is None:
#             form_objeto = self.form_class(unidade=unidade)
#         else:
#             objeto = self.obj_class.objects.get(id=self.obj_id)
#             form_objeto = self.form_class(instance=objeto, unidade=unidade)
#
#         return unidade, dados_objetos, form_objeto, objeto
#
