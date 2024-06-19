from equipamento.models import EquipamentoDisponivel, CatalogoEquipamentos
from equipamento.forms import CatalogoEquipamentosForms, EquipamentoDisponivelForm
from utils.utils import capturate_paramns, colect_dados
from django.shortcuts import redirect


class DadosCatalogoEquipamentoAndFormulario:
    def __init__(self, login_type, id, status, equipamento_catalogo_id = None):
        self.login_type = login_type
        self.equipamento_catalogo_id = equipamento_catalogo_id
        self.id = id
        self.status = status

    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)


        elif self.login_type == "Administrador":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_catalogo_equipamentos = CatalogoEquipamentos.objects.filter(
                status__in = self.status
            )
            if self.equipamento_catalogo_id is not None:
                equipamento_catalogo = CatalogoEquipamentos.objects.get(
                    id_random=self.equipamento_catalogo_id
                )
                catalogo_equipamentos_form = CatalogoEquipamentosForms(
                    instance=equipamento_catalogo
                )
            else:
                equipamento_catalogo = None
                catalogo_equipamentos_form = CatalogoEquipamentosForms(

                )

            return empresa, dados_catalogo_equipamentos, catalogo_equipamentos_form, equipamento_catalogo


        elif self.login_type == "Gestor":
            # unidade = capturate_paramns(self.login_type, self.id)
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_catalogo_equipamentos = CatalogoEquipamentos.objects.filter(
                status__in=self.status,
                empresa = empresa
            )
            if self.equipamento_catalogo_id is not None:
                equipamento_catalogo = CatalogoEquipamentos.objects.get(
                    id_random=self.equipamento_catalogo_id
                )
                catalogo_equipamentos_form = CatalogoEquipamentosForms(
                    instance=equipamento_catalogo,
                    empresa=empresa
                )
            else:
                equipamento_catalogo = None
                catalogo_equipamentos_form = CatalogoEquipamentosForms(
                    empresa=empresa
                )

            return empresa, dados_catalogo_equipamentos, catalogo_equipamentos_form, equipamento_catalogo


        elif  self.login_type == "Gerente":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_catalogo_equipamentos = CatalogoEquipamentos.objects.filter(
                status__in = self.status[0:1],
                empresa = empresa
            )
            if self.equipamento_catalogo_id is not None:
                equipamento_catalogo = CatalogoEquipamentos.objects.get(
                    id_random=self.equipamento_catalogo_id
                )
                catalogo_equipamentos_form = CatalogoEquipamentosForms(
                    instance=equipamento_catalogo,
                    empresa=empresa
                )
            else:
                equipamento_catalogo = None
                catalogo_equipamentos_form = CatalogoEquipamentosForms(
                    empresa=empresa
                )


            return empresa, dados_catalogo_equipamentos, catalogo_equipamentos_form, equipamento_catalogo

        else:
            return redirect('logout', self.login_type, self.id)


class DadosEquipamentosAndFormulario:
    def __init__(self, login_type, id, status):
        self.login_type = login_type
        self.id = id
        self.status = status

    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)


        elif self.login_type == "Administrador":
            empresa = capturate_paramns(login_type=self.login_type, id=self.id, type="empresa")
            dados_equipamentos_disponiveis = colect_dados(
                EquipamentoDisponivel,
                vida_util_campo= 'catalogo_equipamento__vida_util_meses',
                ).filter(
                status__in = self.status
            )
            equipamento_disponivel_form = EquipamentoDisponivelForm()

            return empresa, dados_equipamentos_disponiveis, equipamento_disponivel_form


        elif self.login_type == "Gestor":
            empresa = capturate_paramns(login_type=self.login_type, id=self.id, type="empresa")
            dados_equipamentos_disponiveis = colect_dados(
                EquipamentoDisponivel,
                vida_util_campo= 'catalogo_equipamento__vida_util_meses',
                empresa = empresa
                ).filter(
                status__in=self.status
            )
            equipamento_disponivel_form = EquipamentoDisponivelForm(
                empresa=empresa,
            )

            return empresa, dados_equipamentos_disponiveis, equipamento_disponivel_form


        elif self.login_type == 'Gerente':
            empresa = capturate_paramns(login_type=self.login_type, id=self.id, type="empresa")
            dados_equipamentos_disponiveis = colect_dados(
                EquipamentoDisponivel,
                vida_util_campo= 'catalogo_equipamento__vida_util_meses',
                empresa = empresa
            ).filter(
                empresa=empresa,
                status__in=self.status[0:1]
            )
            equipamento_disponivel_form = EquipamentoDisponivelForm(
                empresa=empresa,
            )

            return empresa, dados_equipamentos_disponiveis, equipamento_disponivel_form


        elif self.login_type == 'Colaborador':
            return redirect('servicos_agendados', self.login_type, self.id)


        else:
            return redirect('logout', self.login_type, self.id)


