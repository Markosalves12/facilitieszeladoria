from django.core.mail import send_mail
from setup.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class SendEmail:
    def __init__(self, para, nome, de=EMAIL_HOST_USER, cargo=str(), senha=str()):
        self.de = de
        self.para = para
        self.nome = nome
        self.cargo = cargo
        self.senha = senha


    def send_email(self):
        html_content = render_to_string(
            template_name='notifications/add_to_sistem.html',
            context={
                'email': self.para,
                'nome': self.nome,
                'cargo': self.cargo,
                'senha': self.senha,
            }
        )
        text_contex = strip_tags(html_content)

        send_mail(
            'Sistema de jardinagem',
            text_contex,
            self.de,
            [self.para],
            html_message=html_content,
        )


class SendNotificationNewServiceToColaborador:
    def __init__(self, para, colaborador_nome, area, area_total, localidade,
                 servicos, data_inicio, descricao, de=EMAIL_HOST_USER):

        self.de = de
        self.para = para
        self.area = area
        self.colaborador_nome = colaborador_nome
        self.area_total = area_total
        self.localidade = localidade
        self.servicos = servicos
        self.data_inicio = data_inicio
        self.descricao = descricao


    def send_email(self):
        html_content = render_to_string(
            template_name='notifications/new_service.html',
            context={
                'colaborador_nome': self.colaborador_nome,
                'area_total': self.area_total,
                'area': self.area,
                'localidade': self.localidade,
                'data_inicio': self.data_inicio,
                'descricao': self.descricao,
                'servicos': self.servicos
            }
        )
        text_contex = strip_tags(html_content)

        send_mail(
            'Novo servico',
            text_contex,
            self.de,
            [self.para],
            html_message=html_content,
        )



class SendNotificationServiceCanceled:
    def __init__(self, para, colaborador_nome, area, area_total, localidade,
                 servicos, data_inicio, descricao, de=EMAIL_HOST_USER):
        self.de = de
        self.para = para
        self.area = area
        self.colaborador_nome = colaborador_nome
        self.area_total = area_total
        self.localidade = localidade
        self.servicos = servicos
        self.data_inicio = data_inicio
        self.descricao = descricao

    def send_email(self):
        html_content = render_to_string(
            template_name='notifications/canceled_service.html',
            context={
                'colaborador_nome': self.colaborador_nome,
                'area_total': self.area_total,
                'area': self.area,
                'localidade': self.localidade,
                'data_inicio': self.data_inicio,
                'descricao': self.descricao,
                'servicos': self.servicos
            }
        )
        text_contex = strip_tags(html_content)

        send_mail(
            'Serviço cancelado',
            text_contex,
            self.de,
            [self.para],
            html_message=html_content,
        )



class SendCodeUpdatePassword:
    def __init__(self, para, code, colaborador_nome, de=EMAIL_HOST_USER):
        self.code = code
        self.de = de
        self.para = para
        self.colaborador_nome = colaborador_nome

    def send_email(self):
        html_content = render_to_string(
            template_name='notifications/update_password.html',
            context={
                'para': self.para,
                'code': self.code,
                'colaborador_nome': self.colaborador_nome,
            }
        )
        text_contex = strip_tags(html_content)

        send_mail(
            'Atualização de senha',
            text_contex,
            self.de,
            [self.para],
            html_message=html_content,
        )