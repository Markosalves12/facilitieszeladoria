from django import forms
from colaborador.models import Colaborador
from gerente.models import Gerente

# Formulario que recebe os dados de login dos usuários
class LoginForms(forms.Form):
    def clean_email(self):
        return self.cleaned_data['email'].strip().lower()


    email = forms.EmailField(
        label="Email de usuário",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@suzano.com.br"
            }
        )
    )

    senha = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Sua senha"
            }
        )
    )
    # Nota depois de editar a pagina de login os estilos foram buscados da cadastro


class UpdateLoginForms(forms.Form):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is not None:
            return self.cleaned_data['email'].strip().lower()
        else:
            pass

    email = forms.EmailField(
        label="Email de usuário",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@suzano.com.br"
            }
        )
    )
    Senha = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Sua senha"
            }
        )
    )
    Confirmacao_da_senha = forms.CharField(
        label="Confirmar senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Sua senha"
            }
        )
    )
    # Nota depois de editar a pagina de login os estilos foram buscados da cadastro

class InsertCodeForms(forms.Form):
    codigo = forms.CharField(
        label="Código de troca",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Thry679**%"
            }
        )
    )

# class AdministradorForms(forms.ModelForm):
#     class Meta:
#         model = Adminsitrador
#         fields = ['nome', 'email', ]
#
#         widgets = {
#             'nome': forms.TextInput(
#                 attrs={
#                     'class': 'form-control'
#                 }
#             ),
#             'email': forms.TextInput(
#                 attrs={
#                     'class': 'form-control'
#                 }
#             ),
#         }

# Formulário que valida a criação de novo colaboradores
class ColaboradorForms(forms.ModelForm):
    # Alteração do campo de seleção de gerente para um checkbox
    # Para permitir a seleção múltipla de gerentes para um mesmo colaborador
    gerente = forms.ModelMultipleChoiceField(
        queryset=Gerente.objects.all(),
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Gerentes imediatos',
        required=True  # Defina como True se a seleção de colaboradores for obrigatória
    )

    # Metodo para alterar o comportamento padrão do formulário
    # Parametro login_type, id, e unidade, alteram a disposição de objetos para preenchimento
    def __init__(self, *args, login_type=None, id_random=None, unidade=None, **kwargs):
        # O parametro de unidade, identifica a qual hierarquia aquele usuario
        # que está logado pertence
        super(ColaboradorForms, self).__init__(*args, **kwargs)
        # Os colaboradores só podem responder aos gerentes das suas unidades especificas
        # Em caso de unidade ser None todas as unidades passar a estar disponiveis para uso
        if unidade is not None and login_type != "Administrador":
            self.fields['gerente'].queryset = self.fields['gerente'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            ).filter(
                gestor__empresa__unidade = unidade
            )

        # Em caso de haver preenchemnto para unidade (unidade!=None)
        if login_type is not None and id is not None:
            # O administrador pode associar colaboradores a todas aos gerentes
            # De todas unidades
            if login_type == 'Administrador':
                self.fields['gerente'].queryset = self.fields['gerente'].queryset.exclude(
                    status__in=['Desmobilizado', 'Desmobilizacao Permanente']
                )

            elif login_type == 'Gestor':
                self.fields['gerente'].queryset = self.fields['gerente'].queryset.exclude(
                    status__in=['Desmobilizado', 'Desmobilizacao Permanente']
                ).filter(
                    gestor__id_random=id_random
                )

            elif login_type == 'Gerente':
                gerente = Gerente.objects.get(
                    id_random=id_random
                )
                gestor__id_random = gerente.gestor.id_random
                self.fields['gerente'].queryset = self.fields['gerente'].queryset.exclude(
                    status__in=['Desmobilizado', 'Desmobilizacao Permanente']
                ).filter(
                    gestor__id_random = gestor__id_random
                )

            else:
                self.fields['gerente'].queryset = self.fields['gerente'].queryset.exclude(
                    status__in=['Desmobilizado', 'Desmobilizacao Permanente']
                )

        else:
            self.fields['gerente'].queryset = self.fields['gerente'].queryset.exclude(
                status__in=['Desmobilizado', 'Desmobilizacao Permanente']
            )

    def clean_nome(self):
        return self.cleaned_data['nome'].strip().capitalize()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is not None:
            return self.cleaned_data['email'].strip().lower()
        else:
            pass

    def clean_funcao(self):
        return self.cleaned_data['funcao'].strip().capitalize()

    def clean_atividades(self):
        return self.cleaned_data['atividades'].strip().capitalize()


    class Meta:
        model = Colaborador
        fields = ['nome', 'email', 'funcao', 'atividades', 'gerente', ]

        labels = {
            'nome': 'Nome do colaborador',
            'email': 'Email de contado (opcional)',
            'funcao': 'Função principal',
            'atividades': 'Atividades principais',
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
            'atividades': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
