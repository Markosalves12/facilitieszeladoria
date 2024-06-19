from django.shortcuts import redirect
from gerente.models import Gerente
from gerente.forms import GerenteForms
from utils.utils import capturate_paramns


class DadosGerentesAndFormulario:
    def __init__(self, login_type, id, status_gerente, gerente_id=None):
        self.login_type = login_type
        self.id = id
        self.status_gerente = status_gerente
        self.gerente_id = gerente_id


    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)


        elif self.login_type == 'Gerente':
            return redirect('painel_do_administrador', self.login_type, self.id)


        elif self.login_type == "Administrador":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_gerentes = Gerente.objects.filter(
                status__in=self.status_gerente
            )
            gerente = None
            if self.gerente_id == None:
                gerente_form = GerenteForms()

            else:
                gerente = Gerente.objects.get(
                    id_random=self.gerente_id
                )
                gerente_form = GerenteForms(
                    instance=gerente
                )

            return empresa, dados_gerentes, gerente_form, gerente


        elif self.login_type == "Gestor":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_gerentes = Gerente.objects.filter(
                status__in=self.status_gerente[:1]
            ).filter(
                gestor__id_random = self.id
            )
            gerente = None

            if self.gerente_id == None:
                gerente_form = GerenteForms(
                    gestor__id_random=self.id
                )
            else:
                gerente = Gerente.objects.get(
                    id_random=self.gerente_id
                )
                gerente_form = GerenteForms(
                    instance=gerente,
                    gestor__id_random=self.id
                )

            return empresa, dados_gerentes, gerente_form, gerente

        else:
            return redirect('logout', self.login_type, self.id)