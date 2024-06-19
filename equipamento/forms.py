from django import forms
from equipamento.models import ManutencaoEquipamentos, EquipamentoDisponivel, CatalogoEquipamentos

# formulario de criação de novos equipamentos no catalogo
# cada empresa tem seu proprio catalogo
class CatalogoEquipamentosForms(forms.ModelForm):
    def __init__(self, *args, empresa = None, **kwargs):
        super(CatalogoEquipamentosForms, self).__init__(*args, **kwargs)
        # caso o parametro empresa seja preenchido
        # o menu libera apenas a empresa da hierarqui que o usuario se encontra

        # as empresas desmobilizadas somem dos menus
        if empresa is not None:
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                id_random=empresa.id_random
            )
        else:
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    #funções para tratar os inputs enviados pel usuario

    # tratamento da variavel nome
    def clean_nome(self):
        return self.cleaned_data['nome'].strip().capitalize()

    # tratamento da variavel marca
    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if marca is not None:
            return self.cleaned_data['marca'].strip().capitalize()
        else:
            pass

    # liberação dos campos
    class Meta:
        model = CatalogoEquipamentos
        fields = ["nome", "marca", "vida_util_meses", "empresa", ]

        # labels que identificam o formulario na tela
        labels = {
            'nome': 'Nome do equipamento',
            'marca': 'Marca do equipamento',
            'vida_util_meses': 'Vida útil expectável em meses',
            'empresa': 'Empresa operadora',
        }

        # widgets do formulario

        # o campo de status é controlado automaticamente pelos
        # cruds administrativo
        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ex: Motosserra"
                }
            ),
            "marca": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ex: toyama"
                }
            ),
            "vida_util_meses": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ex: 15"
                }
            ),
            "empresa": forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                }
            )
        }

# formulario de criação de novos equipamentos
# cada empresa tem seu proprio arsenal de equipamentos

class EquipamentoDisponivelForm(forms.ModelForm):
    def __init__(self, *args, empresa = None, **kwargs):
        super(EquipamentoDisponivelForm, self).__init__(*args, **kwargs)
        # caso o parametro empresa seja preenchido
        # o menu libera apenas a empresa da hierarqui que o usuario se encontra

        # Excluir serviços com status 'Desmobilizado' do queryset
        if empresa is not None:
            self.fields['catalogo_equipamento'].queryset = self.fields['catalogo_equipamento'].queryset.filter(
                empresa = empresa
            ).exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

        if empresa is not None:
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.filter(
                id = empresa.id
            ).exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

        else:
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    def clean_matricula(self):
        return self.cleaned_data['matricula'].strip().upper()


    class Meta:
        model = EquipamentoDisponivel
        fields = ['data_aquisicao', 'data_desmobilizacao', 'matricula',
                  'catalogo_equipamento', 'empresa', 'tipo']

        labels = {
            'data_aquisicao': 'Data de aquisição',
            'data_desmobilizacao': 'Data de desmobilização',
            'matricula': 'Matrícula do equipamento',
            'catalogo_ferramenta': 'Cátalogo ferramenta',
            'empresa': 'Empresa operadora',
            'tipo':'Tipo de equipamento'
        }

        widgets = {
            'data_aquisicao': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),
            'data_desmobilizacao': forms.DateInput(
                format='%d/%m/%Y',
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),
            'matricula': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Matricula do equipamento'
                }
            ),
            'catalogo_equipamento': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),
            'empresa': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
            'tipo': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
        }

class ManutencaoEquipamentosForm(forms.ModelForm):
    def __init__(self, *args, equipamento_id = None, **kwargs):
        super(ManutencaoEquipamentosForm, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if equipamento_id is not None:
            self.fields['equipamento'].queryset = self.fields['equipamento'].queryset.filter(
                id_random=equipamento_id
            )
        else:
            self.fields['equipamento'].queryset = self.fields['equipamento'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    def clean_motivo(self):
        return self.cleaned_data['descricao_motivo'].strip().capitalize()

    def clean_descricao(self):
        return self.cleaned_data['descricao_servico'].strip().capitalize()

    class Meta:
        model = ManutencaoEquipamentos
        fields = ['data_hora_inicio', 'data_hora_fim', 'descricao_servico',
                  'descricao_motivo', 'equipamento', 'tipo_manutencao']

        labels = {
            'data_hora_inicio': 'Data e hora de envio para manutenção DD/MM/AAAA HH:MM',
            'data_hora_fim': 'Data e hora de retorno da manutenção DD/MM/AAAA HH:MM',
            'descricao_servico': 'Descrição so serviço prestado',
            'equipamento': 'Equipamento enviado para manutenção',
            'tipo_manutencao': 'Tipo de serviço prestado',
        }

        widgets = {
            'data_hora_inicio': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),
            'data_hora_fim': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),
            'descricao_servico': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Digite a descrição do serviço aqui'
                }
            ),
            'descricao_motivo': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Digite a descrição do motivo aqui'
                }
            ),
            'equipamento': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
            'tipo_manutencao': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg'
                }
            ),
        }