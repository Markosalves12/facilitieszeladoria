from django.shortcuts import redirect
from utils.utils import capturate_paramns
from empresa.models import Empresa
from empresa.forms import EmpresaForms

# classe usada para servir objetos na views de empresa (app)
# essa view server
# dados, formulario, formulario previamente preenchidos e outros parametros uteis aos html
class DadosEmpresasAndFormulario:
    def __init__(self, login_type, id, status_empresa, empresa_id=None):
        # dados usados para fazer as consultas
        self.login_type = login_type
        self.id = id
        self.status_empresa = status_empresa
        self.empresa_id = empresa_id


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
                self.login_type,
                self.id
            )
            empresa = capturate_paramns(
                self.login_type,
                self.id,
                type='empresa'
            )
            # busca os dados desejados seguindo o status do colaborador
            # status_options = [
            #     ('Mobilizado', 'Mobilizado'),
            #     ('Desmobilizado', 'Desmobilizado'),
            #     ('Desmobilizacao Permanente', 'Desmobilizacao Permanente')
            # ]

            dados_empresas = Empresa.objects.filter(
                status__in=self.status_empresa
            )

            # predefinição da variável empresa_form
            empresa_form = EmpresaForms()
            if self.empresa_id is not None:
                # caso o parametro empresa_id seja != None
                # retorna um formulario ja instanciado
                empresa = Empresa.objects.get(
                    id_random=self.empresa_id
                )
                empresa_form = EmpresaForms(
                    instance=empresa
                )

            # return das variáveis
            return unidade, empresa, dados_empresas, empresa_form

        # para o login de administrador

        #  Essa versão atual não deixa a visão das empresas liberada para os gestores
        # apenas o administrador pode ver nos cruds administrativos
        elif self.login_type == "Gestor":
            unidade = capturate_paramns(
                self.login_type,
                self.id
            )

            empresa = capturate_paramns(
                self.login_type,
                self.id,
                type='empresa'
            )

            dados_empresas = Empresa.objects.filter(
                status__in=self.status_empresa[0:1]
            ).filter(
                unidade=unidade
            )
            empresa_form = EmpresaForms(
                unidade_id=unidade.id
            )

            if self.empresa_id is not None:

                empresa_form = EmpresaForms(
                    instance=empresa,
                    unidade_id=unidade.id
                )

            return unidade, empresa, dados_empresas, empresa_form

        # gerentes são proibidos de acessar essa rota e
        # são redirecioando para rota que lhe cabe
        elif self.login_type == 'Gerente':
            return redirect('painel_do_administrador', self.login_type, self.id)

        # força o usuário a fezer logoutb da aplicação
        else:
            return redirect('logout', self.login_type, self.id)


