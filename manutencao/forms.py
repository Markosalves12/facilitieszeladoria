from django import forms

from manutencao.models import Manutencao

class ManutencaoForms(forms.ModelForm):
    def __init__(self, *args, unidade=None, **kwargs):
        super(ManutencaoForms, self).__init__(*args, **kwargs)
        if unidade is not None:
            self.fields['unidade'].queryset = self.fields['unidade'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                unidade = unidade
            )

        else:
            self.fields['unidade'].queryset = self.fields['unidade'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    class Meta:
        model = Manutencao
        fields = ["tipo_manutencao", "unidade"]

        widgets = {
            "tipo_manutencao": forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            "unidade": forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                }
            )
        }