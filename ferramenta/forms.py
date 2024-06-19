from django import forms
from ferramenta.models import ManutencaoFerramentas, FerramentaDisponivel, CatalogoFerramentas

# formulario de preenchimento
class CatalogoFerramentasForms(forms.ModelForm):
    def __init__(self, *args, empresa=None, **kwargs):
        super(CatalogoFerramentasForms, self).__init__(*args, **kwargs)
        # caso o parametro empresa esteja preenchida retorna apenas as empresas
        # disponiveis para aquele login
        if empresa is not None:
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                id_random=empresa.id_random
            )
        else:
            # caso o parametro empresa nao esteja preenchido retorna todas as empresas
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )
    # tratamento aplicado ao campo nome
    def clean_nome(self):
        return self.cleaned_data['nome'].strip().capitalize()

    # tratamento aplicado ao campo marca
    def clean_marca(self):
        marca = self.cleaned_data.get('marca')
        if marca is not None:
            return self.cleaned_data['marca'].strip().capitalize()
        else:
            pass


    class Meta:
        model = CatalogoFerramentas
        # liberação dos campos
        fields = ["nome", "marca", "vida_util_meses", "empresa", ]

        labels = {
            'nome': 'Nome da ferramenta',
            'marca': 'Marca da ferramenta',
            'vida_util_meses': 'Vida útil expectável',
            'empresa': 'Empresa operadora',
        }

        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ex: Tesoura de Poda"
                }
            ),
            "marca": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "ex: Toyama"
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


# formulario de criação de novas ferramentas
class FerramentaDisponivelForms(forms.ModelForm):
    def __init__(self, *args, empresa=None,  **kwargs):
        super(FerramentaDisponivelForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if empresa is not None:
                # manten se no formulario apenas ferramentas do catalogo da
                # empresa que o o login esta inserido
                self.fields['catalogo_ferramenta'].queryset = self.fields['catalogo_ferramenta'].queryset.filter(
                    empresa=empresa
                ).exclude(
                    # exclui se equipamentos ja desmobilizados do catálogo
                    status__in=['Desmobilizado', 'Desmobilizacao Permanente']
                )

        if empresa is not None:
            # excluise do query set empresas desmobilizadas
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                id_random=empresa.id_random
            )

        else:
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    # tratamento do campo matricula
    def clean_matricula(self):
        return self.cleaned_data['matricula'].strip().upper()


    class Meta:
        model = FerramentaDisponivel
        # campos liberados para o autor
        fields = ['data_aquisicao', 'data_desmobilizacao', 'matricula',
                  'catalogo_ferramenta', 'empresa', 'tipo']

        labels = {
            'data_aquisicao': 'Data de aquisição',
            'data_desmobilizacao': 'Data de desmobilização',
            'matricula': 'Matrícula da ferramenta',
            'catalogo_ferramenta': 'Cátalogo ferramenta',
            'empresa': 'Empresa operadora',
            'tipo': 'Tipo de ferramenta'
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
                    'placeholder': 'Matricula da ferramenta'
                }
            ),
            'catalogo_ferramenta': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                    'placeholder': 'Digite a descrição do motivo aqui'
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

# formulario de preenchimento de manutenção de ferramentas
class ManutencaoFerramentasForms(forms.ModelForm):
    def __init__(self, *args, ferramenta_id = None, **kwargs):
        super(ManutencaoFerramentasForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if ferramenta_id is not None:
            self.fields['ferramenta'].queryset = self.fields['ferramenta'].queryset.filter(
                id_random=ferramenta_id
            )
        else:
            self.fields['ferramenta'].queryset = self.fields['ferramenta'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    # tratamento do campo motivo
    def clean_motivo(self):
        return self.cleaned_data['descricao_motivo'].strip().capitalize()
    # tratamento do campo descricao
    def clean_descricao(self):
        return self.cleaned_data['descricao_servico'].strip().capitalize()


    class Meta:
        model = ManutencaoFerramentas
        # liberação dos campos
        fields = ['data_hora_inicio', 'data_hora_fim', 'descricao_servico',
                  'descricao_motivo', 'ferramenta', 'tipo_manutencao']

        labels = {
            'data_hora_inicio': 'Data e hora de envio para manutenção DD/MM/AAAA HH:MM',
            'data_hora_fim': 'Data e hora de retorno da manutenção DD/MM/AAAA HH:MM',
            'descricao_servico': 'Descrição so serviço prestado',
            'ferramenta': 'Ferramenta enviado para manutenção',
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
            'ferramenta': forms.Select(
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