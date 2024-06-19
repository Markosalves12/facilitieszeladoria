from django.shortcuts import redirect
from materiais.models import Materiais
from materiais.forms import MaterialForms
from utils.utils import capturate_paramns


class DadosMateriaisAndFormulario:
    def __init__(self, login_type, id, status_material, material_id=None):
        self.login_type = login_type
        self.id = id
        self.status_material = status_material
        self.material_id = material_id


    def verify_login_type_and_return_objects(self):
        if self.login_type == "Colaborador":
            return redirect("servicos_agendados", self.login_type, self.id)

        elif self.login_type == "Administrador":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_materiais = Materiais.objects.filter(
                status__in=self.status_material
            )
            material = None
            if self.material_id == None:
                material_form = MaterialForms()
            else:
                material = Materiais.objects.get(
                    id_random=self.material_id
                )
                material_form = MaterialForms(
                    instance=material
                )

            return empresa, dados_materiais, material_form, material


        elif self.login_type == "Gestor":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_materiais = Materiais.objects.filter(
                status__in=self.status_material
            ).filter(
                empresa=empresa
            )
            material = None
            if self.material_id == None:
                material_form = MaterialForms(
                    empresa=empresa
                )
            else:
                material = Materiais.objects.get(
                    id_random=self.material_id
                )
                material_form = MaterialForms(
                    instance=material,
                    empresa=empresa
                )

            return empresa, dados_materiais, material_form, material

        elif self.login_type == "Gerente":
            empresa = capturate_paramns(self.login_type, self.id, type="empresa")
            dados_materiais = Materiais.objects.filter(
                status__in=self.status_material[0:1]
            ).filter(
                empresa = empresa
            )
            material = None
            if self.material_id == None:
                material_form = MaterialForms(
                    empresa=empresa
                )
            else:
                material = Materiais.objects.get(
                    id_random=self.material_id
                )
                material_form = MaterialForms(
                    instance=material,
                    empresa=empresa
                )

            return empresa, dados_materiais, material_form, material


        elif self.login_type == 'Colaborador':
            return redirect('servicos_agendados', self.login_type, self.id)


        else:
            return redirect('logout', self.login_type, self.id)




