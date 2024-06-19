from django.shortcuts import redirect
from gestor.models import Gestor
from gestor.forms import GestorForms
from utils.utils import capturate_paramns


class DadosGestoresAndFormulario:
    def __init__(self, login_type, id, status_gestor, gestor_id=None):
        self.login_type = login_type
        self.id = id
        self.status_gestor = status_gestor
        self.gestor_id = gestor_id


    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)


        elif self.login_type == 'Gerente':
            return redirect('painel_do_administrador', self.login_type, self.id)


        elif self.login_type == 'Gestor':
            return redirect('painel_do_administrador', self.login_type, self.id)


        elif self.login_type == "Administrador":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_gestores = Gestor.objects.filter(
                status__in=self.status_gestor
            )
            gestor = None
            if self.gestor_id == None:
                gestor_form = GestorForms()

            else:
                gestor = Gestor.objects.get(
                    id_random=self.gestor_id
                )
                gestor_form = GestorForms(
                    instance=gestor
                )

            return empresa, dados_gestores, gestor_form, gestor

        else:
            return redirect('logout', self.login_type, self.id)