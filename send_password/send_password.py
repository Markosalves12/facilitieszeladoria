from send_password.dados import senha_smtp, email_smtp
import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendEmail:
    def __init__(self, para, nome, de=email_smtp, cargo=str(), senha=str(), senha_ = senha_smtp):
        self.de = de
        self.para = para
        self.nome = nome
        self.cargo = cargo
        self.senha = senha
        self.senha_ = senha_

    def create_mensagem(self):

        html = f"""<!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facilities Suzano - Jardinagem</title>
        </head>
        <body>
            <div style="text-align: center;">
                 <p style="font-size: 25px; color: #003366; font-family: Arial, sans-serif; font-weight: bold;">Facilities Suzano</p>
            </div>
            <div style="margin-top: 20px; text-align: center;">
                <h2 style="font-size: 18px; color: #000; font-family: Arial, sans-serif;">{self.para} | '{self.nome}'adicionado como {self.cargo} ao sistema de Jardinagem, senha de acesso</h2>
                <p style="font-size: 25px; color: #003366; font-family: Arial, sans-serif; font-weight: bold;">{self.senha}</p>
            </div>
        </body>
        </html>"""

        return html

    def send_email(self):
        mensagem = MIMEMultipart()
        mensagem['Subject'] = "Facilities Suzano - Jardinagem"
        mensagem['From'] = self.de
        mensagem['To'] = self.para
        mensagem['Body'] = self.create_mensagem()
        mensagem.attach(MIMEText(mensagem['Body'], 'html'))


        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=contexto) as servidor:
            servidor.login(mensagem['From'], password=self.senha_)
            servidor.sendmail(
                mensagem['From'], mensagem['To'], mensagem.as_string()
            )


class SendNotificationNewServiceToColaborador:
    def __init__(self, para, colaborador_nome, area, area_total, localidade,
                 servicos, data_inicio, descricao, de=email_smtp, senha_ = senha_smtp):
        self.de = de
        self.senha_ = senha_
        self.para = para
        self.area = area
        self.colaborador_nome = colaborador_nome
        self.area_total = area_total
        self.localidade = localidade
        self.servicos = servicos
        self.data_inicio = data_inicio
        self.descricao = descricao

    def create_mensagem(self):

        html = f"""<!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facilities Suzano - Jardinagem</title>
        </head>
        <body>
            <div style="text-align: center;">
                 <p style="font-size: 25px; color: #003366; font-family: Arial, sans-serif; font-weight: bold;">Facilities Suzano jardinagem</p>
            </div>
            <div style="margin-top: 20px; text-align: left;">
                <p style="font-size: 18px; color: #000; font-family: Arial, sans-serif;">
                    Novo serviço atribuido a {self.colaborador_nome}<br>
                    {self.descricao}<br>
                    Serviço de {self.servicos} na área {self.area}{self.localidade}, inicio em {self.data_inicio}<br>
                    <br>
                    resumo da atividade:<br>
                    area: {self.area}<br>
                    area M^2: {self.area_total}<br>
                    localidade: {self.localidade}<br>
                    servicos: {self.servicos}<br>
                    inicio: {self.data_inicio}<br>
                <p>
            </div>
        </body>
        </html>"""

        return html

    def send_email(self):
        mensagem = MIMEMultipart()
        mensagem['Subject'] = "Serviço agendado"
        mensagem['From'] = self.de
        mensagem['To'] = self.para
        mensagem['Body'] = self.create_mensagem()
        mensagem.attach(MIMEText(mensagem['Body'], 'html'))


        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=contexto) as servidor:
            servidor.login(mensagem['From'], password=self.senha_)
            servidor.sendmail(
                mensagem['From'], mensagem['To'], mensagem.as_string()
            )


class SendNotificationServiceCanceled:
    def __init__(self, para, colaborador_nome, area, area_total, localidade,
                 servicos, data_inicio, descricao, de=email_smtp, senha_=senha_smtp):
        self.de = de
        self.senha_ = senha_
        self.para = para
        self.area = area
        self.colaborador_nome = colaborador_nome
        self.area_total = area_total
        self.localidade = localidade
        self.servicos = servicos
        self.data_inicio = data_inicio
        self.descricao = descricao

    def create_mensagem(self):
        html = f"""<!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facilities Suzano - Jardinagem</title>
        </head>
        <body>
            <div style="text-align: center;">
                 <p style="font-size: 25px; color: #003366; font-family: Arial, sans-serif; font-weight: bold;">Facilities Suzano - Jardinagem</p>
            </div>
            <div style="margin-top: 20px; text-align: left;">
                <p style="font-size: 18px; color: #000; font-family: Arial, sans-serif;">
                    serviço atribuido a {self.colaborador_nome}<br><br>
                    {self.descricao}<br><br>
                    Cancelado<br>
                    Serviço de {self.servicos} na área {self.area}{self.localidade}, inicio em {self.data_inicio}<br>
                    <br>
                    resumo da atividade:<br>
                    area: {self.area}<br>
                    area M^2: {self.area_total}<br>
                    localidade: {self.localidade}<br>
                    servicos: {self.servicos}<br>
                    inicio: {self.data_inicio}<br>
                <p>
            </div>
        </body>
        </html>"""

        return html

    def send_email(self):
        mensagem = MIMEMultipart()
        mensagem['Subject'] = "Serviço cancelado"
        mensagem['From'] = self.de
        mensagem['To'] = self.para
        mensagem['Body'] = self.create_mensagem()
        mensagem.attach(MIMEText(mensagem['Body'], 'html'))

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=contexto) as servidor:
            servidor.login(mensagem['From'], password=self.senha_)
            servidor.sendmail(
                mensagem['From'], mensagem['To'], mensagem.as_string()
            )


class SendCodeUpdatePassword:
    def __init__(self, para, code, colaborador_nome , de=email_smtp, senha_=senha_smtp):
        self.code = code
        self.de = de
        self.senha_ = senha_
        self.para = para
        self.colaborador_nome = colaborador_nome

    def create_mensagem(self):
        html = f"""<!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facilities Suzano - Jardinagem</title>
        </head>
        <body>
            <div style="text-align: center;">
                 <p style="font-size: 25px; color: #003366; font-family: Arial, sans-serif; font-weight: bold;">Facilities Suzano - Jardinagem</p>
            </div>
            <div style="margin-top: 20px; text-align: left;">
                <p style="font-size: 18px; color: #000; font-family: Arial, sans-serif;">
                    Alteração de senha {self.para}<br><br>
                    código de alteração de senha {self.code}<br>
                    <br>
                <p>
            </div>
        </body>
        </html>"""

        return html

    def send_email(self):
        mensagem = MIMEMultipart()
        mensagem['Subject'] = "Serviço cancelado"
        mensagem['From'] = self.de
        mensagem['To'] = self.para
        mensagem['Body'] = self.create_mensagem()
        mensagem.attach(MIMEText(mensagem['Body'], 'html'))

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL(host='smtp.gmail.com', port=465, context=contexto) as servidor:
            servidor.login(mensagem['From'], password=self.senha_)
            servidor.sendmail(
                mensagem['From'], mensagem['To'], mensagem.as_string()
            )