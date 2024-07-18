from django.db import models
from gestor.models import Gestor
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
# from send_password.send_password import SendEmail

from send_password.send_notificafions import SendEmail

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from utils.models import GerenteManager
import random


# Função que cria um id randomico para identificar os objetos nos bancos de dados
# a funcao generate_id_random oarace varias vezes no código
# isolar a função gera um erro de referencia circular sabe - se Deus porque
def generate_id_random():
    while True:
        # Generate a random integer between 0 and 999999 inclusive
        random_int = random.randint(0, 999998)
        return random_int


class Gerente(AbstractBaseUser, PermissionsMixin):
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
    gestor = models.ForeignKey(
        to=Gestor,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='gestororigem'
    )

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

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='gerente_set',  # Renomeia o acessor reverso
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='gerente_permissions_set',  # Renomeia o acessor reverso
        blank=True,
    )

    objects = GerenteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'funcao', 'gestor']

    def __str__(self):
        return self.nome

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

        super(Gerente, self).save(*args, **kwargs)

    # função dispara a senha por email caso o campo senha esteja em braco
    # nesse caso isso é ativado nos formularios html
    # pelo admin do django pode se criar alterar manualemnte
    def save(self, *args, **kwargs):
        if not self.pk and not self.senha:
            random_password = get_random_string(
                length=12
            )

            SendEmail(
                para=self.email,
                nome=self.nome,
                cargo='gerente',
                senha=random_password,
            ).send_email()

            self.senha = make_password(random_password)

        else:
            self.senha = make_password(self.senha)

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)

    @property
    def is_staff(self):
        return self.is_active