from django.shortcuts import redirect
from catalogoservico.models import CatalogoServicos
from catalogoservico.forms import CatalogoServicosForms
from utils.utils import capturate_paramns



class DadosCatalogoServicosAndFormulario:
    def __init__(self, login_type, id, status_servico, servico_catalogo_id=None):
        self.login_type = login_type
        self.id = id
        self.status_servico = status_servico
        self.servico_catalogo_id = servico_catalogo_id


    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)

        elif self.login_type == "Administrador":
            unidade = capturate_paramns(
                login_type=self.login_type,
                id=self.id
            )
            dados_catalogo_servicos = CatalogoServicos.objects.filter(
                status__in=self.status_servico
            )
            servico_catalogo = None
            if self.servico_catalogo_id == None:
                catalogo_servicos_form = CatalogoServicosForms(

                )
            else:
                servico_catalogo = CatalogoServicos.objects.get(
                    id_random=self.servico_catalogo_id
                )
                catalogo_servicos_form = CatalogoServicosForms(
                    instance=servico_catalogo
                )

            return unidade, dados_catalogo_servicos, catalogo_servicos_form, servico_catalogo


        elif self.login_type == "Gestor":
            empresa = capturate_paramns(login_type=self.login_type,
                                        id=self.id,
                                        type="empresa")
            dados_catalogo_servicos = CatalogoServicos.objects.filter(
                status__in=self.status_servico
            ).filter(
                empresa=empresa
            )
            servico_catalogo = None
            if self.servico_catalogo_id == None:
                catalogo_servicos_form = CatalogoServicosForms(
                    empresa=empresa
                )
            else:
                servico_catalogo = CatalogoServicos.objects.get(
                    id_random=self.servico_catalogo_id
                )
                catalogo_servicos_form = CatalogoServicosForms(
                    instance=servico_catalogo,
                    empresa=empresa
                )

            return empresa, dados_catalogo_servicos, catalogo_servicos_form, servico_catalogo


        elif self.login_type == "Gerente":
            empresa = capturate_paramns(
                login_type=self.login_type,
                id=self.id,
                type="empresa"
            )
            dados_catalogo_servicos = CatalogoServicos.objects.filter(
                status__in=self.status_servico[0:1]
            ).filter(
                empresa=empresa
            )
            servico_catalogo = None
            if self.servico_catalogo_id == None:
                catalogo_servicos_form = CatalogoServicosForms(
                    empresa=empresa
                )
            else:
                servico_catalogo = CatalogoServicos.objects.get(
                    id_random=self.servico_catalogo_id
                )
                catalogo_servicos_form = CatalogoServicosForms(
                    instance=servico_catalogo,
                    empresa=empresa
                )

            return empresa, dados_catalogo_servicos, catalogo_servicos_form, servico_catalogo


        elif self.login_type == 'Colaborador':
            return redirect('servicos_agendados', self.login_type, self.id)


        else:
            return redirect('logout', self.login_type, self.id)
