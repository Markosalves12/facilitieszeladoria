from django import forms
from dashboards.models import FiltroTable, FiltroTableManutencao


class FiltroTableForms(forms.ModelForm):
    class Meta:
        model = FiltroTable
        fields = ['datastart', 'datafim', 'empresa','unidade',
                  'localidade', ]

        # labels que identificam o formulario na tela
        labels = {
            'datastart': 'Data de inicio',
            'datafim': 'Data final',
            'empresa': 'Empresa',
            'unidade': 'Unidade',
            'localidade': 'Localidade',
        }

        widgets = {
            'datastart': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
            ),
            'datafim': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
            ),
            'empresa': forms.Select(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
            ),
            'unidade': forms.Select(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
            ),
            'localidade': forms.Select(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super(FiltroTableForms, self).__init__(*args, **kwargs)
        self.fields['localidade'].queryset = self.fields['localidade'].queryset.order_by('nome')


class FiltroTableManutencaoForms(forms.ModelForm):
    class Meta:
        model = FiltroTableManutencao
        fields = ['datastart', 'datafim', 'unidade',
                  'empresa', 'tipo_manutencao']

        # labels que identificam o formulario na tela
        labels = {
            'datastart': 'Data de inicio',
            'datafim': 'Data final',
            'unidade': 'Unidade',
            'empresa': 'Empresa',
            'tipo_manutencao': 'Tipo de manutenção'
        }

        widgets = {
            'datastart': forms.DateInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
            ),
            'datafim': forms.DateInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
            ),
            'unidade': forms.Select(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
            ),
            'empresa': forms.Select(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
            ),
            'tipo_manutencao': forms.Select(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
            ),
        }