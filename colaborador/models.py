from django.db import models
from gerente.models import Gerente
import random
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from utils.models import ColaboradorManager
from send_password.send_password import SendEmail


# Create your models here
# class Adminsitrador(models.Model):
#     nome = models.CharField(max_length=100, blank=False, null=False,)
#     email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
#     senha = models.CharField(max_length=100, blank=True, null=True)
#     status_options = [
#         ('Mobilizado', 'Mobilizado'),
#         ('Desmobilizado', 'Desmobilizado'),
#         ('Desmobilizacao Permanente', 'Desmobilizacao Permanente')
#     ]
#     status = models.CharField(max_length=60, blank=False, null=False, choices=status_options, default='')
#
#
#     def save(self, *args, **kwargs):
#         if not self.pk:  # only if the object is being created, not updated
#             random_password = get_random_string(length=12)
#             SendEmail(para=self.email, cargo='administrador', senha=random_password).send_email()
#             self.senha = make_password(random_password)
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.nome



# Função que cria um id randomico para identificar os objetos nos bancos de dados
# a funcao generate_id_random oarace varias vezes no código
# isolar a função gera um erro de referencia circular sabe - se Deus porque
def generate_id_random():
    while True:
        # Generate a random integer between 0 and 999999 inclusive
        random_int = random.randint(0, 999998)
        return random_int

# modelo de colaborador
class Colaborador(AbstractBaseUser, PermissionsMixin):
    # conluna principal usada como parametro de urls
    id_random = models.IntegerField(
        unique=True,
        default=generate_id_random
    )
    # coluna que recebe o nome do colaborado
    nome = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
    )
    # email de contato do colaborador
    # opcional no contexto no projeto
    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )

    # função que o colaboradorn exerce no contexto
    funcao = models.CharField(
        max_length=100,
        blank=False,
        null=False
    )

    # atividades exercidas pelos colaboradores
    atividades = models.TextField()

##########################################

    # senhas removidas
    # login de colaborador removido do contexto suzano

    # senha = models.CharField(
    #     max_length=128,  # Alterado para suportar hashes de senha
    #     blank=True,
    #     null=True
    # )

###########################################

    # gerente imediato do colaborador
    gerente = models.ManyToManyField(
        to=Gerente,
        blank=False,
        null=False,
        related_name='gestororigem'
    )

    # a coluna status controla a disponibilidade do objeto no formularios espalhados pelo sistema
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

    # os colaboradores criados não tem acesso a rota admin do django
    # com privilégio de super usário
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


    # controle de permissões padrões dos colaboradores
    # permissão zeradas temporarioamente
    groups = models.ManyToManyField(
        Group,
        related_name='colaborador_set',  # Renomeia o acessor reverso
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='colaborador_permissions_set',  # Renomeia o acessor reverso
        blank=True,
    )

    # colaboiradores são objetos gerenciados por
    # ColaboradorManager
    objects = ColaboradorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'funcao', 'gestor']

    def __str__(self):
        return self.nome

    # def save(self, *args, **kwargs):
    #     if not self.pk and not self.senha:  # only if the object is being created and senha is not provided
    #         random_password = get_random_string(length=12)
    #         SendEmail(para=self.email,
    #                   nome=self.nome,
    #                   cargo='gerente',
    #                   senha=random_password
    #                   ).send_email()
    #         self.senha = make_password(random_password)
    #     super().save(*args, **kwargs)
    #
    # def check_password(self, raw_password):
    #     return check_password(raw_password, self.senha)



    @property
    def is_staff(self):
        return self.is_admin