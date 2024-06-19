from django import forms
from catalogoservico.models import CatalogoServicos

class CatalogoServicosForms(forms.ModelForm):
    # parametrização do fomulario de colaborador
    # cada empresa cadastrada no sistema recebe um catalogo proprio de serviços
    # o parametro empresa, serve para o usuario logado
    # criar serviços exclusivos para a empresa que está alocado
    def __init__(self, *args, empresa=None, **kwargs):
        super(CatalogoServicosForms, self).__init__(*args, **kwargs)
        if empresa is not None:
            # pelo parametro empresa, os menus flutuantes do formulario django
            # são alterados
            # não se pode criar serviços para empresas desmobilizadas e/ou que o usuario nao atenda
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                # excluise empresas desmibilizadas
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                # todos os filtros estão em função de id_random
                # para diminuir a previsibilidades das rotas
                id_random = empresa.id_random
            )
        else:
            # apenas o administrador pode adicionar serviços para todas as empresas
            self.fields['empresa'].queryset = self.fields['empresa'].queryset.exclude(
                # excluise empresas desmibilizadas
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    # trata o dado 'servico' inputado pelo usuário
    def clean_servico(self):
        return self.cleaned_data['servico'].strip().capitalize()


    class Meta:
        model = CatalogoServicos
        fields = ['servico', 'empresa', ]

        widgets = {
            'servico' : forms.TextInput(
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