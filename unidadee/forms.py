from django import forms

from unidadee.models import Unidade, Localidade

# formulario de criação de novas unidades
class UnidadeForms(forms.ModelForm):
    # tratamento do campo unidade
    def clean_unidade(self):
        return self.cleaned_data['unidade'].strip().capitalize()

    class Meta:
        model = Unidade
        fields = ['unidade', 'link', ]

        labels = {
            'unidade': 'Unidade',
            'link':'Link do myMaps',
        }

        widgets = {
            'unidade': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'link': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


class LocalidadeForms(forms.ModelForm):
    def __init__(self, *args, unidade = None, **kwargs):
        super(LocalidadeForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if unidade is not None:
            self.fields['unidadeoriginial'].queryset = self.fields['unidadeoriginial'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                unidade = unidade
            )
        else:
            self.fields['unidadeoriginial'].queryset = self.fields['unidadeoriginial'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )
    #
    # def __init__(self, *args, **kwargs):
    #     super(LocalidadeForms, self).__init__(*args, **kwargs)
    #     # Excluir serviços com status 'Desmobilizado' do queryset
    #     self.fields['unidadeoriginial'].queryset = self.fields['unidadeoriginial'].queryset.exclude(status='Desmobilizado')

    def clean_nome(self):
        return self.cleaned_data['nome'].strip().capitalize()

    class Meta:
        model = Localidade
        fields = ['nome', 'unidadeoriginial', 'negocio']

        labels = {
            'nome': 'Nome',
            'unidadeoriginial': 'Unidade',
            'negocio': 'Tipo de negócio'
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'unidadeoriginial': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'negocio': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }