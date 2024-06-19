from django.shortcuts import redirect
from django.db.models import Q
from unidadee.models import Localidade, Unidade
from unidadee.forms import LocalidadeForms, UnidadeForms
from utils.utils import capturate_paramns


class DadosLocalidadesAndFormulario:
    def __init__(self,login_type, id, status_localidade, status_unidade, localidade_id=None, delimiter = "&"):
        self.login_type = login_type
        self.id = id
        self.status_localidade = status_localidade
        self.status_unidade = status_unidade
        self.delimiter = delimiter
        self.localidade_id = localidade_id


    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)


        elif self.login_type == "Administrador":
            unidade = capturate_paramns(
                login_type=self.login_type,
                id=self.id
            )
            if self.delimiter == "&":
                dados_localidades = Localidade.objects.filter(
                    Q(status__in=self.status_localidade) &
                    Q(unidadeoriginial__status__in=self.status_unidade)
                )
            else:
                dados_localidades = Localidade.objects.filter(
                    Q(status__in=self.status_localidade) |
                    Q(unidadeoriginial__status__in=self.status_unidade)
                )

            localidade = None
            if self.localidade_id is not None:
                localidade = Localidade.objects.get(id_random = self.localidade_id)
                localidade_form = LocalidadeForms(
                    instance=localidade
                )
            else:
                localidade_form = LocalidadeForms(

                )

            return dados_localidades, localidade_form, unidade, localidade


        elif self.login_type == "Gestor":
            unidade = capturate_paramns(
                login_type=self.login_type,
                id=self.id
            )

            if self.delimiter == "&":
                dados_localidades = Localidade.objects.filter(
                    Q(status__in=self.status_localidade) &
                    Q(unidadeoriginial__status__in = self.status_unidade)
                ).filter(
                    Q(unidadeoriginial__unidade=unidade)
                )
            else:
                dados_localidades = Localidade.objects.filter(
                    Q(status__in=self.status_localidade) |
                    Q(unidadeoriginial__status__in = self.status_unidade)
                ).filter(
                    Q(unidadeoriginial__unidade=unidade)
                )

            localidade = None
            if self.localidade_id is not None:
                localidade = Localidade.objects.get(
                    id_random=self.localidade_id
                )

                localidade_form = LocalidadeForms(
                    instance=localidade,
                    unidade=unidade
                )
            else:
                localidade_form = LocalidadeForms(
                    unidade=unidade
                )

            return dados_localidades, localidade_form, unidade, localidade

        elif self.login_type == "Gerente":
            unidade = capturate_paramns(
                login_type=self.login_type,
                id=self.id
            )

            if self.delimiter == "&":
                dados_localidades = Localidade.objects.filter(
                    Q(status__in=self.status_localidade[0:1]) &
                    Q(unidadeoriginial__status__in = self.status_unidade)
                ).filter(
                    Q(unidadeoriginial__unidade=unidade)
                )
            else:
                dados_localidades = Localidade.objects.filter(
                    Q(status__in=self.status_localidade[0:1]) |
                    Q(unidadeoriginial__status__in = self.status_unidade)
                ).filter(
                    Q(unidadeoriginial__unidade=unidade)
                )

            localidade = None
            if self.localidade_id is not None:
                localidade = Localidade.objects.get(
                    id_random=self.localidade_id
                )
                localidade_form = LocalidadeForms(
                    instance=localidade,
                    unidade=unidade
                )
            else:
                localidade_form = LocalidadeForms(
                    unidade=unidade
                )

            return dados_localidades, localidade_form, unidade, localidade

        elif self.login_type == 'Colaborador':
            return redirect('servicos_agendados', self.login_type, self.id)


class DadosUnidadesAndFormulario:
    def __init__(self, login_type, id, status_unidade, unidade_id=None):
        self.login_type = login_type
        self.id = id
        self.status_unidade = status_unidade
        self.unidade_id = unidade_id


    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)


        elif self.login_type == 'Gerente':
            return redirect('painel_do_administrador', self.login_type, self.id)


        elif self.login_type == 'Gestor':
            return redirect('painel_do_administrador', self.login_type, self.id)


        elif self.login_type == "Administrador":
            dados_unidades = Unidade.objects.filter(
                status__in=self.status_unidade
            )
            unidade = None
            if self.unidade_id == None:
                unidade_form = UnidadeForms()

            else:
                unidade = Unidade.objects.get(
                    id_random=self.unidade_id
                )
                unidade_form = UnidadeForms(
                    instance=unidade
                )

            return dados_unidades, unidade_form, unidade

        else:
            return redirect('logout', self.login_type, self.id)