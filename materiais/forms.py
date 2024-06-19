from django import forms
from materiais.models import Materiais

class MaterialForms(forms.ModelForm):
    def __init__(self, *args, empresa=None, **kwargs):
        super(MaterialForms, self).__init__(*args, **kwargs)
        if empresa is not None:
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                id = empresa.id
            )

        else:
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    def clean_material(self):
        return self.cleaned_data['material'].strip().capitalize()

    class Meta:
        model = Materiais
        fields = ['material', 'categoria', 'consumo', 'empresa', ]

        labels = {
            'material': 'Nome o material',
            'categoria': 'Categoria',
            'consumo': 'Forma de consumo',
            'empresa': 'Empresa operadora',
        }

        widgets = {
            'material': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'consumo': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'empresa': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                }
            )
        }