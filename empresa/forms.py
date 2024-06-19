from django import forms

from empresa.models import Empresa


# formulario de criação de novas emporesas
# cada empresa pode atender uma ou mais empresas
class EmpresaForms(forms.ModelForm):
    # o parametro unidade_id serve para travar a criação de unidades
    # desmobilizadas
    def __init__(self, *args, unidade_id = None, **kwargs):
        super(EmpresaForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if unidade_id is not None:
            self.fields['unidade'].queryset = self.fields['unidade'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                unidade_id = unidade_id
            )
        else:
            self.fields['unidade'].queryset = self.fields['unidade'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    #funções para tratar os inputs enviados pel usuario

    # tratamento da variavel nome
    def clean_nome(self):
        return self.cleaned_data['nome'].strip().capitalize()

    # tratamento da razão social
    def clean_razao_social(self):
        return self.cleaned_data['razao_social'].strip().capitalize()

    # tratamento do cnpj
    def clean_cnpj(self):
        return self.cleaned_data['cnpj'].strip().capitalize()

    # liberação dos campos
    class Meta:
        model = Empresa
        fields = ['nome', 'razao_social', 'cnpj', 'unidade', 'tipo_empresa']

        # labels que identificam o formulario na tela
        labels = {
            'nome': 'Nome da empresa',
            'razao_social': 'Razão social',
            'cnpj': 'CNPJ',
            'unidade': 'Unidade que atende',
            'tipo_empresa': 'Tipo de empresa'
        }

        # widgets do formulario

        # o campo de status é controlado automaticamente pelos
        # cruds administrativo
        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'razao_social': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'cnpj': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'unidade': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'tipo_empresa': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            )
        }