from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import check_password
from send_password.send_password import SendEmail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from empresa.models import Empresa
from utils.models import GestorManager
import random
from django.core.exceptions import ValidationError

# Create your models here.


# Função que cria um id randomico para identificar os objetos nos bancos de dados
# a funcao generate_id_random oarace varias vezes no código
# isolar a função gera um erro de referencia circular sabe - se Deus porque
def generate_id_random():
    while True:
        # Generate a random integer between 0 and 999999 inclusive
        random_int = random.randint(0, 999998)
        return random_int

class Gestor(AbstractBaseUser, PermissionsMixin):
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )

    nome = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    funcao = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )
    senha = models.CharField(
        max_length=128,  # Alterado para suportar hashes de senha
        blank=True,
        null=True
    )

    empresa = models.ForeignKey(
        to=Empresa,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='empresaorigem'
    )

    # negocio_options = [
    #     ('Industrial', 'Industrial'),
    #     ('Florestal', 'Florestal'),
    #     ('Outros', 'Outros')
    # ]
    #
    # negocio = models.ManyToManyField(
    #     max_length=60,
    #     blank=True,
    #     null=True,
    #     choices=negocio_options,
    # )

    status_options = [
        ('Mobilizado', 'Mobilizado'),
        ('Desmobilizado', 'Desmobilizado'),
        ('Desmobilizacao Permanente', 'Desmobilizacao Permanente')
    ]
    status = models.CharField(
        max_length=60,
        blank=False,
        null=False,
        choices=status_options,
        default='Mobilizado'
    )

    is_active = models.BooleanField(
        default=True
    )
    is_admin = models.BooleanField(
        default=False
    )

    groups = models.ManyToManyField(
        Group,
        related_name='gestor_set',  # Renomeia o acessor reverso
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='gestor_permissions_set',  # Renomeia o acessor reverso
        blank=True,
    )

    objects = GestorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'funcao', 'gestor']

    def __str__(self):
        return self.nome


    # cria uma trava para que apenas emails suzanos atuem como gestores do sistema
    def clean(self):
        super().clean()
        # extensão de dominio de email suzano
        allowed_domain = 'suzano.com.br'
        if self.email:
            self.email = self.email.strip().lower()
            domain = self.email.split('@')[-1]
            if domain != allowed_domain:
                raise ValidationError(f'apenas emails {allowed_domain} podem ser cadastrados')

    # esse bloco de codigos pode ser reaproveitado
    # ele tbm aparece no model de gestor e gerente
    # corrigir futuramente
    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.strip().lower()

        if self.nome:
            self.nome = self.nome.strip().capitalize()

        if self.funcao:
            self.funcao = self.funcao.strip().capitalize()

        super(Gestor, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     self.full_clean()
    #     super(Gestor, self).save(*args, **kwargs)


    def save(self, *args, **kwargs):
        if not self.pk and not self.senha:
            random_password = get_random_string(
                length=12
            )
            SendEmail(para=self.email,
                      nome=self.nome,
                      cargo='gestor',
                      senha=random_password
                      ).send_email()
            self.senha = make_password(random_password)

        else:
            self.senha = make_password(self.senha)

        super().save(*args, **kwargs)


    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)

    @property
    def is_staff(self):
        return self.is_admin