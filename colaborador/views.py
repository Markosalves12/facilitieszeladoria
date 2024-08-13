from django.contrib import auth
from django.shortcuts import render, redirect
from colaborador.models import Colaborador
from gestor.models import Gestor
from django.contrib.auth.hashers import check_password
from gerente.models import Gerente
from colaborador.forms import ColaboradorForms, LoginForms, UpdateLoginForms, InsertCodeForms
from utils.utils import paginate
from utils.utils import block_view
from django.utils.crypto import get_random_string
from django.contrib import messages
from colaborador.utils import DadosColaboradoresAndFormulario
from utils.utils import alterar_status, gerar_codigo_aleatorio
from django.contrib.auth.models import User
from send_password.send_notificafions import SendCodeUpdatePassword

# Create your views here.


# Função que controla o login de usuário
# Validação de senhas
def login(request):
    login_form = LoginForms()
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():

            email = form['email'].value()
            senha = form['senha'].value()

            # O login funciona por uma espécie de tentativa e erro
            # pelo django não saber lidar com mais de uma tabela de usuário
            # e para controlar os privilégios de administrador
            # adotou-se a estratégia de tres tabelas de usuários
            try:
                # O primeira try verifica a tabela padrão do django
                # se existir
                # redireciona pro painel com os acessos permitidos
                # controle de botões, links e menus feitos diretamente no HTML
                usuario = User.objects.get(
                    email=email
                )

                usuario = auth.authenticate(
                    request,
                    username=usuario,
                    password=senha,
                )

                # Se o usuário existir cria variáveis de sessão especificas
                # que são enviadas via parametros de URL e controlam as operações dentro das views
                if usuario is not None:
                    auth.login(request, usuario)
                    # variável de sessão com o nome do usuário logado
                    request.session['login_nome'] = f'{usuario.username}'
                    # variável de sessão com o tipo de login
                    # para validar os privilégios de administrador
                    request.session['login_type'] = 'Administrador'
                    # variável de sessão com o id que para controlar seus respectivos acessos no banco de dados
                    request.session['login_id'] = usuario.id
                    # variável de ssessão que enditifica a empresa em que o usuário está alocado
                    request.session['empresa'] = ''
                    # variável de sessão que indentifica a unidade que o usuário atente
                    # exceto administradores
                    request.session['unidade'] = ''
                    request.session['emailgestor'] = f'{usuario.email}'
                    request.session['emailuser'] = f'{usuario.email}'
                    # As variáveis de sessão são envias para o html via processadores de contexto
                    # context processor
                    # do APP colaborador

                    # usuario é redirecionado para a painel de controle direto
                    return redirect('painel_do_administrador')

            except:
                pass

            try:
                # se a primeira identificação falhar
                # valida-se pela tabela de gestores
                gestor = Gestor.objects.get(
                    email=email
                )
                # se o gestor existir
                if check_password(senha, gestor.senha) and gestor.status == "Mobilizado":
                    # login(request, gestor)
                    # variável de sessão com o nome do usuário logado
                    request.session['login_nome'] = gestor.nome
                    # variável de sessão com o tipo de login
                    # para validar os privilégios de administrador
                    request.session['login_type'] = 'Gestor'
                    # variável de sessão com o id que para controlar seus respectivos acessos no banco de dados
                    request.session['login_id'] = gestor.id_random
                    # variável de ssessão que enditifica a empresa em que o usuário está alocado
                    request.session['empresa'] = f'{str(gestor.empresa).split("|")[0].strip()}'
                    # variável de sessão que indentifica a unidade que o usuário atente
                    # exceto administradores
                    request.session['unidade'] = f'{gestor.empresa.unidade}'
                    # variável de sessão que identifica o gestor imediato
                    request.session['gestor'] = f''
                    # variável de sessão que identifica o email do gestor
                    request.session['emailgestor'] = f'{gestor.email}'
                    request.session['emailuser'] = f'{gestor.email}'
                    # usuario é redirecionado para a painel de controle direto
                    return redirect('painel_do_administrador')

            except:
                pass


            try:
                # se a primeira identificação falhar
                # valida-se pela tabela de gestores
                gerente = Gerente.objects.get(
                    email=email
                )
                # se o gerente existir
                if check_password(senha, gerente.senha) and gerente.status == "Mobilizado":
                    # login(request, gerente)
                    # variável de sessão com o nome do usuário logado
                    request.session['login_nome'] = gerente.nome
                    # variável de sessão com o tipo de login
                    # para validar os privilégios de administrador
                    request.session['login_type'] = 'Gerente'
                    # variável de sessão com o id que para controlar seus respectivos acessos no banco de dados
                    request.session['login_id'] = gerente.id_random
                    # variável de ssessão que enditifica a empresa em que o usuário está alocado
                    request.session['empresa'] = f'{str(gerente.gestor.empresa).split("|")[0].strip()}'
                    # variável de sessão que indentifica a unidade que o usuário atente
                    # exceto administradores
                    request.session['unidade'] = f'{gerente.gestor.empresa.unidade}'
                    # variável de sessão que identifica o gestor imediato
                    request.session['gestor'] = f'{gerente.gestor}'
                    # variável de sessão que identifica o email do gestor
                    request.session['emailgestor'] = f'{gerente.gestor.email}'
                    request.session['emailuser'] = f'{gerente.email}'

                    # usuario é redirecionado para a painel de controle direto
                    return redirect('painel_do_administrador')

            except:
                pass

        else:
            login_form = LoginForms()

    # Se nenhum login funcionar
    # o usuário permanece na página de login
    return render(request, 'accounts/login.html', {'login_form': login_form})



# Que funçãoq estabelece o logout
def logout(request):
    # Limpar variáveis de sessão ao fazer logout


    # consite em limpar todas as variáveis de sessão
    # para impedir que o usário continue manipulando o software
    auth.logout(request)
    nome = get_random_string(10)
    type = get_random_string(10)
    id = get_random_string(10)

    # as variáveis são reinstanciadas para o controle da sessão ser mais dificil de interceptar
    request.session['login_nome'] = nome
    request.session['login_type'] = type
    request.session['login_id'] = id


    # Redirecionar para a página de login
    return redirect('login')


#######################################################


# Função que faz a atualização do login e senha do usuário
def resgister(request):
    form = UpdateLoginForms()

    if request.method == 'POST':
        formupdate = UpdateLoginForms(request.POST)
        if formupdate.is_valid():
            # coletando os dados ndo fomulário
            email = formupdate.cleaned_data['email']
            senha1 = formupdate.cleaned_data['Senha']
            senha2 = formupdate.cleaned_data['Confirmacao_da_senha']

            # verificando se as senhas são iguais
            if senha1 != senha2:
                messages.error(request, "As senha devem ser iguais")
                return redirect('resgister')

            request.session['update_password_code'] = gerar_codigo_aleatorio()
            request.session['new_password'] = senha1
            request.session['email_update'] = email

            # SendCodeUpdatePassword(
            #     code=request.session['update_password_code'],
            #     para=formupdate.cleaned_data['email'],
            #     colaborador_nome=None,
            # )

            # a troca funciona com um sistema de tentativa e erro
            # caso o email exista na tabela user faz se a troca
            try:
                administrador = User.objects.get(
                    email=email
                )
                request.session['login_type'] = 'Administrador'

                SendCodeUpdatePassword(
                    code=request.session.get('update_password_code', ''),
                    para=formupdate.cleaned_data['email'],
                    colaborador_nome=administrador.username,
                ).send_email()

                return redirect('insert_code')

                # administrador.password = senha1
                # messages.success(request, "Senha atualizada com seucesso")
                # return redirect('login')

            except:
                pass

            # caso o email exista na tabela gestores faz se a troca
            try:
                gestor = Gestor.objects.get(
                    email=email
                )

                # o usuario precisa estar mobilizado no time
                if gestor.status == "Mobilizado":
                    request.session['login_type'] = 'Gestor'

                    SendCodeUpdatePassword(
                        code=request.session.get('update_password_code', ''),
                        para=formupdate.cleaned_data['email'],
                        colaborador_nome=gestor.nome,
                    ).send_email()

                    return redirect('insert_code')
                else:
                    return redirect('login')

                # gestor.senha = senha1
                # gestor.save()
                # messages.success(request, "Senha atualizada com seucesso")
                # return redirect('login')

            except:
                pass

            # caso o email exista na tabela gerentes faz se a troca
            try:
                gerente = Gerente.objects.get(
                    email=email
                )
                # o usuario precisa estar mobilizado no time
                if gerente.status == "Mobilizado":
                    request.session['login_type'] = 'Gerente'

                    SendCodeUpdatePassword(
                        code=request.session.get('update_password_code', ''),
                        para=formupdate.cleaned_data['email'],
                        colaborador_nome=gerente.nome,
                    ).send_email()

                    return redirect('insert_code')

                else:
                    return redirect('login')

                # gerente.senha = senha1
                # gerente.save()
                # messages.success(request, "Senha atualizada com seucesso")
                # return redirect('login')

            except:
                pass

            # caso não exista no sistema retorna se uma mensagem de erro
            messages.error(request, f'Email {email} não encontrado')
            return redirect('resgister')

        # caso nada de certo retorna uma mensagem de erro
        messages.error(request, 'Algo deu errado')
    return render(request, 'accounts/register.html',
                  {'form': form})


def insert_code(request):
    login_form = InsertCodeForms()
    if request.method == "POST":
        form = InsertCodeForms(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            if codigo == request.session.get('update_password_code', ''):
                if request.session.get('login_type', '') == "Administrador":
                    administrador = User.objects.get(
                        email=request.session.get('email_update', '')
                    )
                    administrador.password = request.session.get('new_password', '')

                elif request.session.get('login_type', '') == "Gestor":
                    gestor = Gestor.objects.get(
                        email=request.session.get('email_update', '')
                    )
                    gestor.senha = request.session.get('new_password', '')


                elif request.session.get('login_type', '') == "Gerente":
                    gerente = Gerente.objects.get(
                        email=request.session.get('email_update', '')
                    )
                    gerente.senha = request.session.get('new_password', '')

                messages.success(
                    request=request,
                    message="senha atualizada com sucesso"
                )

                return redirect('login')

            messages.error(
                request=request,
                message="algo deu errado"
            )

    return render(
        request=request,
        template_name='accounts/insert_code.html',
        context={
            'login_form': login_form
        }
    )


# View que controla o painel do administrador nos 3 niveis
# administrador, gestor, gerente
def painel_do_administrador(request):
    # variavel de sessão que identifica o tipo de login
    # variavel de sessão que idnetifica o id do usuário
    login_type = request.session['login_type']
    id = request.session['login_id']

    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        # Força o retorno para a página de login
        return redirect('logout')

    # renderiza o template html
    return render(request, 'controle/camadas/painel_do_administrador.html')


def colaboradores(request, login_type, id):
    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        # Força o retorno para a página de login
        return redirect('logout')

    # Classe que captura e rotorna os dados que o login tem permissão de acessar
    # DadosColaboradoresAndFormulario -- controlado por essa classe

    # dica -- o arquivo utils dos apps, coloboradores, equipamentos(catalago),
    # ferramentas(catalogo), servicos(catalogo), empresas
    # materiais(catalogo), tem classes identicas para fazer esse controle fazer a ptimização futura
    # simplificando as classes

    unidade, dados_colaboradores, colaborador_form, colaborador = DadosColaboradoresAndFormulario(
        login_type=login_type,
        id=id,
        status_colaborador=['Mobilizado'],
    ).verify_login_type_and_return_objects()

    # Função que padroniza o metodo de paginação dos elementos nas páginas
    elementos_paginados = paginate(
        request=request,
        data_objects=dados_colaboradores
    )

    # Checagem do formulário enviado no tamplete
    if request.method == 'POST':
        form = ColaboradorForms(request.POST)
        if form.is_valid():
            # Caso o fomulário seja válido retorno uma mensagem de sucesso
            messages.success(request, f"Colaborador(a) {form.cleaned_data['nome'].strip().capitalize()} criado(a) com sucesso")
            form.save()
            return redirect('colaboradores', login_type, id)

        # Caso o fomulário seja invalido retorno uma mensagem de erro
        messages.error(request, f"Algo deu errado, nome ou email já existem")

    return render(request, 'controle/colaboradores/colaboradores.html', {
        'colaborador_form': colaborador_form,
        'elementos_paginados': elementos_paginados
    })

def editar_colaborador(request, login_type, colaborador_id, id):
    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    # Classe que captura e rotorna os dados que o login tem permissão de acessar
    # DadosColaboradoresAndFormulario -- controlado por essa classe

    # dica -- o arquivo utils dos apps, coloboradores, equipamentos(catalago),
    # ferramentas(catalogo), servicos(catalogo), empresas
    # materiais(catalogo), tem classes identicas para fazer esse controle fazer a ptimização futura
    # simplificando as classes

    unidade, dados_colaboradores, colaborador_form, colaborador = DadosColaboradoresAndFormulario(
        login_type=login_type,
        id=id,
        status_colaborador=['Mobilizado'],
        colaborador_id=colaborador_id
    ).verify_login_type_and_return_objects()

    # Checagem do formulário enviado no tamplete
    if request.method == 'POST':
        form = ColaboradorForms(request.POST, instance=colaborador)
        if form.is_valid():
            # Obter os dados limpos do formulário
            # Aplica um capitalize no campo de nome
            # Aplica um lower nos demais compos

            # Caso o fomulário seja válido retorno uma mensagem de sucesso
            form.save()
            messages.success(request, f"Colaborador(a) {form.cleaned_data['nome']} editado(a) com sucesso")
            return redirect('colaboradores', login_type, id)

        # Caso o fomulário seja invalido retorno uma mensagem de erro
        messages.error(request, f"Algo deu errado, nome ou email já existem")

    return render(request, 'controle/colaboradores/editar_colaborador.html',
                  {'colaborador_form': colaborador_form, 'colaborador_id': colaborador_id})


def desmobilizar_colaborador(request, login_type, colaborador_id, id, desm):
    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    # Função que cumpre o papel de alterar o status dos models
    # essa função é aplicada no models --> catalogoferramentas, catalogoequipamentos,
    # catalogoservicos, colaboradores, gerentes
    # OBS -- avaliar em quais models essa função se aplica
    alterar_status(
        request=request,
        model=Colaborador,
        object_id=colaborador_id,
        desm=desm
    )

    # Redireciona para a pagina de colaboradores habilitados e receberem novos serviços
    return redirect('colaboradores', login_type, id)

def colaboradores_desmobilizados(request, login_type, id):
    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('login')


    # Classe que captura e rotorna os dados que o login tem permissão de acessar
    # DadosColaboradoresAndFormulario -- controlado por essa classe

    # dica -- o arquivo utils dos apps, coloboradores, equipamentos(catalago),
    # ferramentas(catalogo), servicos(catalogo), empresas
    # materiais(catalogo), tem classes identicas para fazer esse controle fazer a ptimização futura
    # simplificando as classes

    unidade, dados_colaboradores, colaborador_form, colaborador = DadosColaboradoresAndFormulario(
        login_type=login_type,
        id=id,
        status_colaborador=['Desmobilizado', 'Desmobilizacao Permanente'],
    ).verify_login_type_and_return_objects()

    # Função que padroniza o metodo de paginação dos elementos nas páginas
    elementos_paginados = paginate(
        request=request,
        data_objects=dados_colaboradores
    )

    return render(request, 'controle/colaboradores/colaboradores_desmobilizados.html', {
        'elementos_paginados': elementos_paginados
    })

def reabilitar_colaborador(request, login_type, colaborador_id, id):
    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    # Função que cumpre o papel de alterar o status dos models
    # essa função é aplicada no models --> catalogoferramentas, catalogoequipamentos,
    # catalogoservicos, colaboradores, gerentes, empresas
    # OBS -- avaliar em quais models essa função se aplica
    alterar_status(
        request=request,
        model=Colaborador,
        object_id=colaborador_id
    )

    # Redireciona para a pagina de colaboradores desmobilizados e receberem novos serviços
    return redirect('colaboradores_desmobilizados', login_type, id)
