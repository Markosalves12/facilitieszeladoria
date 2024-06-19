from django.shortcuts import redirect
from jardins.models import Jardins
from jardins.forms import JardimForms
from utils.utils import capturate_paramns
from django.db.models import Q


class DadosJardinsAndFormulario:
    def __init__(self, login_type, id, status_jardin, status_localidade, status_unidade,
                 area_id=None,delimiter = "&"):
        self.login_type = login_type
        self.id = id
        self.status_jardin = status_jardin
        self.status_localidade = status_localidade
        self.status_unidade = status_unidade
        self.area_id = area_id
        self.delimiter = delimiter


    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)


        elif self.login_type == "Administrador":
            unidade = capturate_paramns(login_type=self.login_type, id=self.id)
            if self.delimiter == "&" and self.area_id is None:
                dados_areas = Jardins.objects.filter(
                    Q(status__in=self.status_jardin) &
                    Q(unidade_jardim__unidadeoriginial__status__in=self.status_unidade) &
                    Q(unidade_jardim__status__in=self.status_localidade)
                )
                area_form = JardimForms()

                return unidade, dados_areas, area_form

            elif self.area_id is not None:
                dados_areas = Jardins.objects.filter(
                    Q(status__in=self.status_jardin) &
                    Q(unidade_jardim__unidadeoriginial__status__in=self.status_unidade) &
                    Q(unidade_jardim__status__in=self.status_localidade)
                )
                area = Jardins.objects.get(
                    id_random=self.area_id
                )
                area_form = JardimForms(
                    instance=area,
                )

                return unidade, dados_areas, area_form

            else:
                dados_areas = Jardins.objects.filter(
                    Q(status__in=self.status_jardin) |
                    Q(unidade_jardim__unidadeoriginial__status__in=self.status_unidade) |
                    Q(unidade_jardim__status__in=self.status_localidade)
                )
                area_form = JardimForms()

                return unidade, dados_areas, area_form

        elif self.login_type == "Gestor":
            unidade = capturate_paramns(login_type=self.login_type, id=self.id)
            empresa = capturate_paramns(login_type=self.login_type, id=self.id, type='empresa')
            if self.delimiter == "&" and self.area_id is None:
                dados_areas = Jardins.objects.filter(
                    Q(status__in=self.status_jardin) &
                    Q(unidade_jardim__unidadeoriginial__status__in=self.status_unidade) &
                    Q(unidade_jardim__status__in=self.status_localidade)
                ).filter(
                    unidade_jardim__unidadeoriginial__unidade=unidade,
                )
                area_form = JardimForms(
                    unidade=unidade,
                    empresa=empresa
                )

                return unidade, dados_areas, area_form

            elif self.area_id is not None:
                dados_areas = Jardins.objects.filter(
                    Q(status__in=self.status_jardin) &
                    Q(unidade_jardim__unidadeoriginial__status__in=self.status_unidade) &
                    Q(unidade_jardim__status__in=self.status_localidade)
                )
                area = Jardins.objects.get(
                    id_random=self.area_id
                )
                area_form = JardimForms(
                    instance=area,
                    unidade=unidade,
                    empresa=empresa
                )

                return unidade, dados_areas, area_form

            else:
                dados_areas = Jardins.objects.filter(
                    Q(status__in=self.status_jardin) |
                    Q(unidade_jardim__unidadeoriginial__status__in=self.status_unidade) |
                    Q(unidade_jardim__status__in=self.status_localidade)
                ).filter(
                    unidade_jardim__unidadeoriginial__unidade=unidade,
                )
                area_form = JardimForms(
                    unidade=unidade,
                    empresa=empresa
                )

                return unidade, dados_areas, area_form

        elif self.login_type == "Gerente":
            unidade = capturate_paramns(login_type=self.login_type, id=self.id)
            empresa = capturate_paramns(login_type=self.login_type, id=self.id, type='empresa')
            if self.delimiter == "&" and self.area_id is None:
                dados_areas = Jardins.objects.filter(
                    Q(status__in=self.status_jardin[0:1]) &
                    Q(unidade_jardim__unidadeoriginial__status__in=self.status_unidade[0:1]) &
                    Q(unidade_jardim__status__in=self.status_localidade[0:1])
                ).filter(
                    unidade_jardim__unidadeoriginial__unidade=unidade,
                )
                area_form = JardimForms(
                    unidade=unidade,
                    empresa=empresa
                )

                return unidade, dados_areas, area_form

            elif self.area_id is not None:
                dados_areas = Jardins.objects.filter(
                    Q(status__in=self.status_jardin) &
                    Q(unidade_jardim__unidadeoriginial__status__in=self.status_unidade) &
                    Q(unidade_jardim__status__in=self.status_localidade)
                )
                area = Jardins.objects.get(
                    id_random=self.area_id
                )
                area_form = JardimForms(
                    instance=area,
                    unidade=unidade,
                    empresa=empresa
                )

                return unidade, dados_areas, area_form

            else:
                dados_areas = Jardins.objects.filter(
                    Q(status__in=self.status_jardin[0:1]) |
                    Q(unidade_jardim__unidadeoriginial__status__in=self.status_unidade[0:1]) |
                    Q(unidade_jardim__status__in=self.status_localidade[0:1])
                ).filter(
                    unidade_jardim__unidadeoriginial__unidade=unidade,
                )
                area_form = JardimForms(
                    unidade=unidade,
                    empresa=empresa
                )

                return unidade, dados_areas, area_form

        else:
            return redirect('logout')