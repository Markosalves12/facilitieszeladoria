from django import forms

from gerente.models import Gerente

class GerenteForms(forms.ModelForm):
    def __init__(self, *args, gestor__id_random = None,**kwargs):
        super(GerenteForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if gestor__id_random is not None:
            self.fields['gestor'].queryset = self.fields['gestor'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                id_random = gestor__id_random
            )
        else:
            self.fields['gestor'].queryset = self.fields['gestor'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    def clean_nome(self):
        return self.cleaned_data['nome'].strip().capitalize()

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_funcao(self):
        return self.cleaned_data['funcao'].strip().capitalize()


    class Meta:
        model = Gerente
        fields = ['nome', 'email', 'funcao', 'gestor']

        labels = {
            'nome': 'Nome do gerente',
            'email': 'Email de contado',
            'funcao': 'Função principal',
            'gestor': 'Gestor emediato',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'funcao': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'gestor': forms.Select(
                attrs={
                    'class': 'form-control '
                }
            )
        }
