from django.contrib.auth.models import BaseUserManager
from django.utils.crypto import get_random_string
import random
from send_password.send_password import SendEmail



def generate_id_random():
    while True:
        # Generate a random integer between 0 and 999999 inclusive
        random_int = random.randint(0, 999998)
        return random_int


class GerenteManager(BaseUserManager):
    def create_user(self, email, nome, funcao, senha=None, gestor=None, status='Mobilizado'):
        if not email:
            raise ValueError('O campo email deve ser preenchido')
        if not nome:
            raise ValueError('O campo nome deve ser preenchido')
        if not funcao:
            raise ValueError('O campo função deve ser preenchido')
        if not gestor:
            raise ValueError('O campo gestor deve ser preenchido')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nome=nome,
            funcao=funcao,
            gestor=gestor,
            status=status,
            id_random=generate_id_random()
        )

        if senha:
            user.set_password(senha)
        else:
            random_password = get_random_string(length=12)

            SendEmail(para=self.email,
                      nome=self.nome,
                      cargo='gerente',
                      senha=random_password
                      ).send_email()

            user.set_password(random_password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, funcao, senha, gestor):
        user = self.create_user(
            email=email,
            nome=nome,
            funcao=funcao,
            senha=senha,
            gestor=gestor,
            status='Mobilizado'
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user




class GestorManager(BaseUserManager):
    def create_user(self, email, nome, funcao, senha=None, empresa=None, status='Mobilizado'):
        if not email:
            raise ValueError('O campo email deve ser preenchido')
        if not nome:
            raise ValueError('O campo nome deve ser preenchido')
        if not funcao:
            raise ValueError('O campo função deve ser preenchido')
        if not empresa:
            raise ValueError('O campo empresa deve ser preenchido')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nome=nome,
            funcao=funcao,
            empresa=empresa,
            status=status,
            id_random=generate_id_random()
        )

        if senha:
            user.set_password(senha)
        else:
            random_password = get_random_string(length=12)

            SendEmail(para=self.email,
                      nome=self.nome,
                      cargo='gerente',
                      senha=random_password
                      ).send_email()

            user.set_password(random_password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, funcao, senha, empresa):
        user = self.create_user(
            email=email,
            nome=nome,
            funcao=funcao,
            senha=senha,
            empresa=empresa,
            status='Mobilizado'
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ColaboradorManager(BaseUserManager):
    def create_user(self, email, nome, funcao, senha=None, gerente=None, status='Mobilizado'):
        if not email:
            raise ValueError('O campo email deve ser preenchido')
        if not nome:
            raise ValueError('O campo nome deve ser preenchido')
        if not funcao:
            raise ValueError('O campo função deve ser preenchido')
        if not gerente:
            raise ValueError('O campo gerente deve ser preenchido')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            nome=nome,
            funcao=funcao,
            gerente=gerente,
            status=status,
            id_random=generate_id_random()
        )

        if senha:
            user.set_password(senha)
        else:
            random_password = get_random_string(length=12)

            SendEmail(para=self.email,
                      nome=self.nome,
                      cargo='colaborador',
                      senha=random_password
                      ).send_email()

            user.set_password(random_password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, funcao, senha, gerente):
        user = self.create_user(
            email=email,
            nome=nome,
            funcao=funcao,
            senha=senha,
            gerente=gerente,
            status='Mobilizado'
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
