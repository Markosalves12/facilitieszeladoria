from django import forms
from unidadee.models import Unidade, Localidade
from jardins.models import Jardins

class JardimForms(forms.ModelForm):
    def __init__(self, *args, unidade = None, empresa = None, **kwargs):
        super(JardimForms, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Desmobilizado' do queryset
        if unidade is not None:
            self.fields['unidade_jardim'].queryset = self.fields['unidade_jardim'].queryset.exclude(
                status='Desmobilizado'
            ).filter(
                unidadeoriginial__unidade = unidade
            )

        else:
            self.fields['unidade_jardim'].queryset = self.fields['unidade_jardim'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )


        if empresa is not None:
            self.fields['servicos_na_area'].queryset = self.fields['servicos_na_area'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                empresa = empresa
            )

        else:
            self.fields['servicos_na_area'].queryset = self.fields['servicos_na_area'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )




        # self.fields['unidade_jardim'].queryset = self.fields['unidade_jardim'].queryset.exclude(status='Desmobilizado')

    def clean_nome(self):
        return self.cleaned_data['nome'].strip().capitalize()

    class Meta:
        model = Jardins
        fields = ['nome', 'area', 'vegetacao', 'terreno', 'servicos_na_area', 'unidade_jardim', 'periodicidade']

        labels = {
            'nome': 'Nome da região',
            'area': 'Dimensão da área em M²',
            'vegetacao': 'Vegetação predominante',
            'terreno': 'Terreno predominante',
            'servicos_na_area': 'Serviço principal aplicado',
            'unidade_jardim': 'Localidade',
            'periodicidade': 'Periodicidade de retorno',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'area': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'vegetacao': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'terreno': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'servicos_na_area': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'unidade_jardim': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'periodicidade': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
        }