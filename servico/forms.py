from django import forms
from colaborador.models import Colaborador
from servico.models import Servicos, FatoServico
from catalogoservico.models import CatalogoServicos
from django.db.models import Q
from utils.utils import resize_image


class ServicosForms(forms.ModelForm):
    # alteração do widgets para permitir seleção multiplas via checkbox
    colaboradores_escalados = forms.ModelMultipleChoiceField(
        queryset=Colaborador.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Colaboradores destinados',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    # alteração do widgets para permitir seleção multiplas via checkbox
    servicos_escalados = forms.ModelMultipleChoiceField(
        queryset=CatalogoServicos.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Serviços aplicáveis',
        required=True  # Defina como True se a seleção de servicos for obrigatória
    )


    def __init__(self, *args, login_type=None, id_random=None, unidade=None, empresa=None, **kwargs):
        super(ServicosForms, self).__init__(*args, **kwargs)
        if id_random is not None:
            # disponibiliza os usuarios para a seleção segundo o login
            # gestores podem ver todos os colaboradores da carteira
            # gerentes podem ver apenas os seus colaboradores
            if login_type == 'Gerente':
                self.fields['colaboradores_escalados'].queryset = self.fields['colaboradores_escalados'].queryset.exclude(
                    status__in=['Desmobilizado', 'Desmobilizacao Permanente']
                ).filter(
                    gerente__id_random=id_random
                ).distinct(

                )

            elif login_type == 'Gestor':
                self.fields['colaboradores_escalados'].queryset = self.fields['colaboradores_escalados'].queryset.exclude(
                    status__in=['Desmobilizado', 'Desmobilizacao Permanente']
                ).filter(
                    gerente__gestor__id_random=id_random
                ).distinct(

                )

        else:
            # caso o login seja administrador
            self.fields['colaboradores_escalados'].queryset = self.fields['colaboradores_escalados'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).distinct(

            )

        # na seleção de áreas verdes existe um sistema de 3 travas
        # caso a area, unidade ou localidade tenha o status de
        # desmobilizado ou desmobilizacao permanente é excluido do query set
        if unidade is not None:
            self.fields['area'].queryset = self.fields['area'].queryset.exclude(
                Q(status='Desmobilizado') |
                Q(status='Desmobilizacao Permanente') |
                Q(unidade_jardim__unidadeoriginial__status = 'Desmobilizado') |
                Q(unidade_jardim__unidadeoriginial__status='Desmobilizacao Permanente') |
                Q(unidade_jardim__status = 'Desmobilizado') |
                Q(unidade_jardim__status='Desmobilizacao Permanente')
            ).filter(
                    unidade_jardim__unidadeoriginial__unidade = unidade,
            )
        else:
            self.fields['area'].queryset = self.fields['area'].queryset.exclude(
                Q(status='Desmobilizado') |
                Q(status='Desmobilizacao Permanente') |
                Q(unidade_jardim__unidadeoriginial__status = 'Desmobilizado') |
                Q(unidade_jardim__unidadeoriginial__status='Desmobilizacao Permanente') |
                Q(unidade_jardim__status = 'Desmobilizado') |
                Q(unidade_jardim__status='Desmobilizacao Permanente')
            )


        if empresa is not None:
            self.fields['servicos_escalados'].queryset = self.fields['servicos_escalados'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                    empresa=empresa,
            )
        else:
            self.fields['servicos_escalados'].queryset = self.fields['servicos_escalados'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    class Meta:
        model = Servicos
        fields = ['servicos_escalados', 'descricao_servico', 'data_inicio',
                  'colaboradores_escalados','area', 'foto_inicio', 'foto',
                  'tipo_servico']

        labels = {
            'descricao_servico': 'Descrição do serviço',
            'data_inicio': 'Iniciar em DD/MM/AAAA',
            'area': 'Área verde',
            'foto_inicio': 'Foto da área na solicitação',
            'foto': 'Foto do serviço finalizado',
            'tipo_servico': 'Tipo de serviço'
        }

        widgets = {
            'descricao_servico': forms.TextInput(attrs={'class': 'form-control'}),
            'data_inicio': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
            'foto_inicio': forms.FileInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'tipo_servico': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),
        }

    def clean_foto_inicio(self):
        foto_inicio = self.cleaned_data.get('foto_inicio')
        if foto_inicio:
            foto_inicio = resize_image(foto_inicio)
        return foto_inicio

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto:
            foto = resize_image(foto)
        return foto


class FatoServicoForm(forms.ModelForm):
    def __init__(self, *args, id = None, login_type = None, empresa = None, **kwargs):
        super(FatoServicoForm, self).__init__(*args, **kwargs)
        # Excluir serviços com status 'Concluído' ou 'Cancelado' do queryset
        if id is not None and login_type is not None:
            if login_type == 'Gerente':
                self.fields['servico'].queryset = self.fields['servico'].queryset.filter(
                    status__in=['Agendado', 'Em andamento']
                ).filter(
                    colaboradores_escalados__gerente__id_random=id
                ).distinct(

                )

                self.fields['colaborador'].queryset = self.fields['colaborador'].queryset.exclude(
                    status__in=['Desmobilizado', 'Desmobilizacao Permanente']
                ).filter(
                    gerente__id_random=id
                ).distinct(

                )


            elif login_type == 'Gestor':
                self.fields['servico'].queryset = self.fields['servico'].queryset.filter(
                    status__in=['Agendado', 'Em andamento']
                ).filter(
                    colaboradores_escalados__gerente__gestor__id_random=id
                ).distinct(

                )

                self.fields['colaborador'].queryset = self.fields['colaborador'].queryset.exclude(
                    status__in=['Desmobilizado', 'Desmobilizacao Permanente']
                ).filter(
                    gerente__gestor__id_random=id
                ).distinct(

                )
        else:
            self.fields['servico'].queryset = self.fields['servico'].queryset.filter(
                status__in=['Agendado', 'Em andamento']
            ).distinct(

            )

            self.fields['colaborador'].queryset = self.fields['colaborador'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).distinct(

            )


        if empresa is not None:
            self.fields['equipamentos_usados'].queryset = self.fields['equipamentos_usados'].queryset.filter(
                Q(data_desmobilizacao__isnull=True) |
                Q(data_desmobilizacao=None),
                empresa = empresa,
            )

            self.fields['material_usado'].queryset = self.fields['material_usado'].queryset.filter(
                status__in=['Mobilizado'],
                empresa = empresa
            )

            self.fields['ferramentas_usados'].queryset = self.fields['ferramentas_usados'].queryset.filter(
                Q(data_desmobilizacao__isnull=True) |
                Q(data_desmobilizacao=None),
                empresa = empresa
            )

            self.fields['servico_aplicado'].queryset = self.fields['servico_aplicado'].queryset.filter(
                empresa = empresa
            )


        else:
            self.fields['equipamentos_usados'].queryset = self.fields['equipamentos_usados'].queryset.filter(
                Q(data_desmobilizacao__isnull=True) |
                Q(data_desmobilizacao=None)
            )

            self.fields['material_usado'].queryset = self.fields['material_usado'].queryset.filter(
                status__in=['Mobilizado']
            )

            self.fields['ferramentas_usados'].queryset = self.fields['ferramentas_usados'].queryset.filter(
                Q(data_desmobilizacao__isnull=True) |
                Q(data_desmobilizacao=None)
            )

            self.fields['ferramentas_usados'].queryset = self.fields['ferramentas_usados'].queryset.filter(
            )



    class Meta:
        model = FatoServico
        fields = ["servico", "data_hora_chegada_na_area",
                    "equipamentos_usados", "ferramentas_usados", "data_hora_retorno_area",
                    "material_usado", "servico_aplicado", "quantidade", "colaborador", "tipo",
                    ]

        labels = {
            'servico': 'Descrição do serviço',
            'data_hora_chegada_na_area': 'Data de hora de chagada na área',
            'equipamentos_usados': 'Equipamento principal aplicado',
            'ferramentas_usados': 'Ferramenta principal aplicada (opcional)',
            'data_hora_retorno_area': 'Data de hora de retorno da área',
            'material_usado': 'Material principal aplicado',
            'servico_aplicado': 'Principal Servico',
            'quantidade': f'Quantidade de material aplicado',
            'colaborador': 'Colaborador',
            'tipo':'Origem do material',
        }


        widgets = {
            'servico': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'data_hora_chegada_na_area': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control form-control-lg',
                }
            ),

            'equipamentos_usados': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'ferramentas_usados': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'material_usado': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'quantidade': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'servico_aplicado': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'data_hora_retorno_area': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control form-control-lg',
                }
            ),

            'colaborador': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),

            'tipo': forms.Select(
                attrs={
                    'class': 'form-control form-control-lg',
                }
            ),
        }

