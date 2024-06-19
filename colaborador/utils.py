from django.shortcuts import redirect
from colaborador.models import Colaborador
from colaborador.forms import ColaboradorForms
from utils.utils import capturate_paramns


# classe usada para servir objetos na views de colaborador (app)
# essa view server
# dados, formulario, formulario previamente preenchidos e outros parametros uteis aos html
class DadosColaboradoresAndFormulario:
    def __init__(self, login_type, id, status_colaborador, colaborador_id=None):
        # dados usados para fazer as consultas
        self.login_type = login_type
        self.id = id
        self.status_colaborador = status_colaborador
        self.colaborador_id = colaborador_id


    def verify_login_type_and_return_objects(self):
        # colaboradores são proibidos de acessar essa rota e
        # são redirecioando para rota que lhe cabe
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)

        # para o login de administrador
        elif self.login_type == "Administrador":
            # capturate_paramns caputura os dois parametros principais para uso dos formularios
            # unidade em empresa
            # o valor type padrao e "undiade" que retorna a unidade
            unidade = capturate_paramns(
                login_type=self.login_type,
                id=self.id
            )
            # busca os dados desejados seguindo o status do colaborador
            # status_options = [
            #     ('Mobilizado', 'Mobilizado'),
            #     ('Desmobilizado', 'Desmobilizado'),
            #     ('Desmobilizacao Permanente', 'Desmobilizacao Permanente')
            # ]

            # para o login_type 'Administrador'
            dados_colaboradores = Colaborador.objects.filter(
                status__in=self.status_colaborador
            ).distinct()

            # predefinição da variável colaborador
            colaborador = None


            if self.colaborador_id == None:
                # caso o id do colaborador seja None type
                # retorna o formulario padrão para preenchimento do novos colaboradores
                colaborador_form = ColaboradorForms(
                    login_type=self.login_type,
                )
            else:
                # caso id do colaborador esteja preenchido
                # iedntifica a que colaborador o id pertence
                colaborador = Colaborador.objects.get(
                    # o id enviado precisa ser o id_random
                    id_random=self.colaborador_id
                )

                # caso id do colaborador esteja preenchido
                # retorna um formulario pre preenchido para ser editado
                # seguindo todas as regras de uso
                colaborador_form = ColaboradorForms(
                    instance=colaborador,
                    login_type=self.login_type,
                    unidade=unidade,
                    id_random=self.id
                )

            # return das variáveis
            return unidade, dados_colaboradores, colaborador_form, colaborador


        # para o login de gestor
        elif self.login_type == "Gestor":
            unidade = capturate_paramns(
                login_type=self.login_type,
                id=self.id
            )

            # para o login_type 'Administrador'
            # retorna se apenas os colaboradores
            # que estão debaixo da sua gestão
            # segundo status de busca
            dados_colaboradores = Colaborador.objects.filter(
                status__in = self.status_colaborador
            ).filter(
                gerente__gestor__id_random=self.id
            ).distinct()

            # predefinição do status de colaborador
            colaborador = None
            if self.colaborador_id == None:
                # caso o id do colaborador seja None type
                # retorna o formulario padrão para preenchimento do novos colaboradores
                # porem aplica se um filtro para que os menus suspensos funcionem do jeito certo

                # consultar nos comentarios dos formulario de colaborador
                colaborador_form = ColaboradorForms(
                    login_type=self.login_type,
                    unidade=unidade,
                    id_random=self.id
                )
            else:
                # caso id do colaborador esteja preenchido
                # iedntifica a que colaborador o id pertence
                colaborador = Colaborador.objects.get(
                    id_random=self.colaborador_id
                )

                # caso id do colaborador esteja preenchido
                # retorna um formulario pre preenchido para ser editado
                # seguindo todas as regras de uso
                # porem aplica se um filtro para que os menus suspensos funcionem do jeito certo

                # consultar nos comentarios dos formulario de colaborador
                colaborador_form = ColaboradorForms(
                    instance=colaborador,
                    login_type=self.login_type,
                    unidade=unidade,
                    id_random=self.id
                )


            return unidade, dados_colaboradores, colaborador_form, colaborador

        # consultar os comentários para o login "Gestor"
        elif self.login_type == "Gerente":
            unidade = capturate_paramns(
                login_type=self.login_type,
                id=self.id
            )
            dados_colaboradores = Colaborador.objects.filter(
                status__in=self.status_colaborador[0:1]
            ).filter(
                gerente__id_random=self.id
            ).distinct()

            colaborador = None
            if self.colaborador_id == None:
                colaborador_form = ColaboradorForms(
                    login_type=self.login_type,
                    unidade=unidade,
                    id_random=self.id
                )

            else:
                colaborador = Colaborador.objects.get(
                    id_random=self.colaborador_id
                )
                colaborador_form = ColaboradorForms(
                    instance=colaborador,
                    login_type=self.login_type,
                    unidade=unidade,
                    id_random=self.id
                )

            # return das variáveis
            return unidade, dados_colaboradores, colaborador_form, colaborador

        else:
            # qualquer erro força o logout do usuário
            return redirect('logout')

