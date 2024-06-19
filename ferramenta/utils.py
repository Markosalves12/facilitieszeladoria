from ferramenta.models import FerramentaDisponivel, CatalogoFerramentas
from ferramenta.forms import CatalogoFerramentasForms, FerramentaDisponivelForms, FerramentaDisponivel
from django.shortcuts import redirect
from utils.utils import colect_dados, capturate_paramns



class DadosCatalogoFerramentaAndFormulario:
    def __init__(self, login_type, ferramenta_catalogo_id, id, status):
        self.login_type = login_type
        self.ferramenta_catalogo_id = ferramenta_catalogo_id
        self.id = id
        self.status = status

    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)


        elif self.login_type == "Administrador":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_catalogo_ferramentas = CatalogoFerramentas.objects.filter(
                status__in = self.status
            )
            if self.ferramenta_catalogo_id is not None:
                ferramenta_catalogo = CatalogoFerramentas.objects.get(
                    id_random=self.ferramenta_catalogo_id
                )
                catalogo_ferramenta_form = CatalogoFerramentasForms(
                    instance=ferramenta_catalogo
                )

            else:
                ferramenta_catalogo = None
                catalogo_ferramenta_form = CatalogoFerramentasForms()

            return empresa, dados_catalogo_ferramentas, catalogo_ferramenta_form, ferramenta_catalogo


        elif self.login_type == "Gestor":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_catalogo_ferramentas = CatalogoFerramentas.objects.filter(
                status__in=self.status,
                empresa=empresa
            )
            if self.ferramenta_catalogo_id is not None:
                ferramenta_catalogo = CatalogoFerramentas.objects.get(
                    id_random=self.ferramenta_catalogo_id
                )
                catalogo_ferramenta_form = CatalogoFerramentasForms(
                    instance=ferramenta_catalogo,
                    empresa=empresa
                )
            else:
                ferramenta_catalogo = None
                catalogo_ferramenta_form = CatalogoFerramentasForms(
                    empresa=empresa
                )

            return empresa, dados_catalogo_ferramentas, catalogo_ferramenta_form, ferramenta_catalogo


        elif  self.login_type == "Gerente":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_catalogo_ferramentas = CatalogoFerramentas.objects.filter(
                status__in = self.status[0:1],
                empresa = empresa
            )
            if self.ferramenta_catalogo_id is not None:
                ferramenta_catalogo = CatalogoFerramentas.objects.get(
                    id_random=self.ferramenta_catalogo_id
                )
                catalogo_ferramenta_form = CatalogoFerramentasForms(
                    instance=ferramenta_catalogo,
                    empresa=empresa
                )
            else:
                ferramenta_catalogo = None
                catalogo_ferramenta_form = CatalogoFerramentasForms(
                    empresa=empresa
                )


            return empresa, dados_catalogo_ferramentas, catalogo_ferramenta_form, ferramenta_catalogo

        else:
            return redirect('logout', self.login_type, self.id)


class DadosFerramentasAndFormulario:
    def __init__(self, login_type, id, status):
        self.login_type = login_type
        self.id = id
        self.status = status

    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)


        elif self.login_type == "Administrador":
            empresa = capturate_paramns(login_type=self.login_type, id=self.id, type="empresa")
            dados_ferramentas_disponiveis = colect_dados(
                FerramentaDisponivel,
                vida_util_campo= 'catalogo_ferramenta__vida_util_meses',
            ).filter(
                status__in = self.status
            )
            ferramenta_disponivel_form = FerramentaDisponivelForms()

            return empresa, dados_ferramentas_disponiveis, ferramenta_disponivel_form


        elif self.login_type == "Gestor":
            empresa = capturate_paramns(login_type=self.login_type, id=self.id, type="empresa")
            dados_ferramentas_disponiveis = colect_dados(
                FerramentaDisponivel,
                vida_util_campo= 'catalogo_ferramenta__vida_util_meses',
                empresa=empresa
            ).filter(
                status__in=self.status
            )
            ferramenta_disponivel_form = FerramentaDisponivelForms(
                empresa=empresa,
            )

            return empresa, dados_ferramentas_disponiveis, ferramenta_disponivel_form


        elif self.login_type == 'Gerente':
            empresa = capturate_paramns(login_type=self.login_type, id=self.id, type="empresa")
            dados_ferramentas_disponiveis = colect_dados(
                FerramentaDisponivel,
                vida_util_campo= 'catalogo_ferramenta__vida_util_meses',
                empresa=empresa
            ).filter(
                empresa=empresa,
                status__in=self.status[0:1]
            )
            ferramenta_disponivel_form = FerramentaDisponivelForms(
                empresa=empresa,
            )

            return empresa, dados_ferramentas_disponiveis, ferramenta_disponivel_form

        else:
            return redirect('logout', self.login_type, self.id)