from django.shortcuts import render, redirect
from empresa.models import Empresa
from empresa.forms import EmpresaForms
from utils.utils import paginate
from utils.utils import block_view
from django.contrib import messages
from utils.utils import capturate_paramns, alterar_status
from empresa.utils import DadosEmpresasAndFormulario


# Create your views here.
def empresas(request, login_type, id):
    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    # Classe que captura e rotorna os dados que o login tem permissão de acessar
    # DadosEmpresasAndFormulario -- controlado por essa classe

    # dica -- o arquivo utils dos apps, coloboradores, equipamentos(catalago),
    # ferramentas(catalogo), servicos(catalogo), empresas,
    # materiais(catalogo), tem classes identicas para fazer esse controle fazer a ptimização futura
    # simplificando as classes

    unidade, empresa, dados_empresas, empresa_form = DadosEmpresasAndFormulario(
        login_type=login_type,
        id=id,
        status_empresa=['Mobilizado']
    ).verify_login_type_and_return_objects()

    # Função que padroniza o metodo de paginação dos elementos nas páginas
    elementos_paginados = paginate(
        request=request,
        data_objects=dados_empresas
    )

    # Validação do formulário
    if request.method == 'POST':
        form = EmpresaForms(request.POST)
        if form.is_valid():
            form.save()
            # caso o formulário seja valido é aplicado no banco de dados
            # e retorna uma mensagem de sucesso
            messages.success(request, f"Empresa {form.cleaned_data['nome']} criada com sucesso")
            return redirect('empresas', login_type, id)
        # caso o formulario seja invalido retorna uma mensagem de erro
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/empresa/empresas.html', {
        'empresa_form': empresa_form,
        'elementos_paginados': elementos_paginados,
        'unidade': unidade
    })

# função para editar uma empresa especifica
def editar_empresa(request, login_type, empresa_id, id):
    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    # Classe que captura e rotorna os dados que o login tem permissão de acessar
    # DadosEmpresasAndFormulario -- controlado por essa classe

    # dica -- o arquivo utils dos apps, coloboradores, equipamentos(catalago),
    # ferramentas(catalogo), servicos(catalogo), empresas,
    # materiais(catalogo), tem classes identicas para fazer esse controle fazer a ptimização futura
    # simplificando as classes

    unidade, empresa, dados_empresas, empresa_form = DadosEmpresasAndFormulario(
        login_type=login_type,
        id=id,
        status_empresa=['Mobilizado'],
        empresa_id=empresa_id
    ).verify_login_type_and_return_objects()

    # validação do formulario enviado na view
    if request.method == 'POST':
        form = EmpresaForms(request.POST, instance=empresa)
        if form.is_valid():
            form.save()

            # caso o formulario seja valido, o objeto do banco de dados e alterado
            messages.success(request, f"Empresa {form.cleaned_data['nome']} editada com sucesso")
            return redirect('empresas', login_type, id)
        # caso contrario retorna uma mensagem de erro
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/empresa/editar_empresa.html',
                  {'empresa_form': empresa_form,'empresa_id': empresa_id})


# função que altera o status de uma empresa
#     status_options = [
#         ('Mobilizado', 'Mobilizado'),
#         ('Desmobilizado', 'Desmobilizado'),
#         ('Desmobilizacao Permanente', 'Desmobilizacao Permanente')
#     ]

def desmobilizar_empresa(request, login_type, empresa_id, id, desm):
    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Administrador' or login_type == 'Gestor':
        empresa = Empresa.objects.get(id_random=empresa_id)

    # logins de gerente e colaborador nao podem alterar o status das unidades
    # porem as empresas ainda nao entao habilitas no painel do gestor

    elif login_type == 'Gerente':
        return redirect('painel_do_administrador', login_type, id)

    elif login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    # Função que cumpre o papel de alterar o status dos models
    # essa função é aplicada no models --> catalogoferramentas, catalogoequipamentos,
    # catalogoservicos, colaboradores, gerentes, empresas
    # OBS -- avaliar em quais models essa função se aplica

    alterar_status(
        request=request,
        model=Empresa,
        object_id=empresa_id,
        desm=desm
    )

    return redirect('empresas', login_type, id)


def empresas_desmobilizadas(request, login_type, id):
    # Função que bloqueia a view em caso das variáveis de sessão terem sido alteradas no logout
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    # Classe que captura e rotorna os dados que o login tem permissão de acessar
    # DadosEmpresasAndFormulario -- controlado por essa classe

    # dica -- o arquivo utils dos apps, coloboradores, equipamentos(catalago),
    # ferramentas(catalogo), servicos(catalogo), empresas,
    # materiais(catalogo), tem classes identicas para fazer esse controle fazer a ptimização futura
    # simplificando as classes

    unidade, empresa, dados_empresas, empresa_form = DadosEmpresasAndFormulario(
        login_type=login_type,
        id=id,
        status_empresa=['Desmobilizado', 'Desmobilizacao Permanente'],
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_empresas)

    return render(request, 'controle/empresa/empresas_desmobilizadas.html', {
        'empresa_form': empresa_form,
        'elementos_paginados': elementos_paginados,
        'unidade': unidade
    })

# função que altera o status de uma empresa
#     status_options = [
#         ('Mobilizado', 'Mobilizado'),
#         ('Desmobilizado', 'Desmobilizado'),
#         ('Desmobilizacao Permanente', 'Desmobilizacao Permanente')
#     ]
def reabilitar_empresa(request, login_type, empresa_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Gerente':
        return redirect('painel_do_administrador', login_type, id)

    elif login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    # Função que cumpre o papel de alterar o status dos models
    # essa função é aplicada no models --> catalogoferramentas, catalogoequipamentos,
    # catalogoservicos, colaboradores, gerentes, empresas
    # OBS -- avaliar em quais models essa função se aplica

    alterar_status(
        request=request,
        model=Empresa,
        object_id=empresa_id,
    )

    return redirect('empresas_desmobilizadas', login_type, id)
