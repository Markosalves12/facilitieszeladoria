# O arquivo context processor fornece parametos globais para ser usado
# No html sem precisar ser enviado pelas views
# Parametros globais de html

# não esquecer de aicionar o arquivo context processor no arquivo setting.py, na pasta raiz do
# django project


def classicate_login(request):
    # variável de sessão com o tipo de login
    # para validar os privilégios de administrador
    type = request.session.get('login_type', '')
    # variável de sessão com o nome do usuário logado
    nome = request.session.get('login_nome', '')
    # variável de sessão com o id que para controlar seus respectivos acessos no banco de dados
    id = request.session.get('login_id', '')
    # variável de ssessão que enditifica a empresa em que o usuário está alocado
    empresa = request.session.get('empresa', '')
    # variável de sessão que indentifica a unidade que o usuário atente
    # exceto administradores
    unidade = request.session.get('unidade', '')
    # variável de sessão que identifica o gestor imediato
    gestor = request.session.get('gestor', '')
    # variável de sessão que identifica o email do gestor
    emailgestor = request.session.get('emailgestor', '')
    emailuser = request.session.get('emailuser', '')

    update_password_code = request.session.get('update_password_code', '')
    new_password = request.session.get('new_password', '')
    email_update = request.session.get('email_update', '')

    # envio das variáveis
    return {'type': type,
            'nome': nome,
            'id': id,
            'temp': 'temp',
            'perm': 'perm',
            'empresa': empresa,
            'unidade': unidade,
            'gestor':gestor,
            'emailgestor':emailgestor,
            'emailuser': emailuser
            }