from django import forms

from gestor.models import Gestor

class GestorForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GestorForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
            status__in=['Desmobilizado', 'Desmobilizacao Permanente']
        )

    def clean_nome(self):
        return self.cleaned_data['nome'].strip().capitalize()

    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()

    def clean_funcao(self):
        return self.cleaned_data['funcao'].strip().capitalize()


    class Meta:
        model = Gestor
        fields = ['nome', 'email', 'funcao', 'empresa']

        labels = {
            'nome': 'Nome do gestor',
            'email': 'Email de contado',
            'funcao': 'Função principal',
            'empresa': 'Empresa',
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
            'empresa': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }