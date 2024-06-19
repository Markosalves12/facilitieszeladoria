from django.shortcuts import render, redirect
from django.db.models import Q
from equipamento.forms import CatalogoEquipamentosForms, ManutencaoEquipamentosForm, EquipamentoDisponivelForm
from equipamento.models import EquipamentoDisponivel, CatalogoEquipamentos, ManutencaoEquipamentos
from utils.utils import paginate
from equipamento.utils import (DadosCatalogoEquipamentoAndFormulario,
                               DadosEquipamentosAndFormulario)
from utils.utils import block_view
from django.contrib import messages
from utils.utils import alterar_status, colect_dados, DadosDisponiveisHandler, capturate_paramns, editar_item


# função que identifica a disponibilidade de equipamentos
# da respectoiva empresa que o usuario faz parte
def disponibilidade_equipamentos(request):
    # os parametros d elogin são enviados direto na view, por um bug ocasionando no menu lateral
    # corrigir numa versão futura
    login_type = request.session['login_type']
    id = request.session['login_id']

    # função que identifca e bloqueia o login
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect("logout")

    # o administrador pode ver todos os equipamentos
    if login_type == "Administrador":
        empresa = capturate_paramns(
            login_type=login_type,
            id=id,
            type="empresa"
        )
        # função que coleta os dados dos respectivos catalogos
        # equipamento e ferramenta
        dados_equipamentos = colect_dados(
            EquipamentoDisponivel,
            vida_util_campo= 'catalogo_equipamento__vida_util_meses',
        ).filter(
            Q(data_desmobilizacao__isnull=True) |
            Q(data_desmobilizacao=None),
        )

    # gestores e gerentes podem visualizar apenas equipamentos ativos
    elif login_type == 'Gestor':
        empresa = capturate_paramns(
            login_type=login_type,
            id=id,
            type="empresa"
        )

        dados_equipamentos = colect_dados(
            EquipamentoDisponivel,
            vida_util_campo='catalogo_equipamento__vida_util_meses',
            empresa=empresa
        ).filter(
            Q(data_desmobilizacao__isnull=True) |
            Q(data_desmobilizacao=None),
            empresa=empresa
        )

    elif login_type == 'Gerente':
        empresa = capturate_paramns(
            login_type=login_type,
            id=id,
            type="empresa"
        )

        dados_equipamentos = colect_dados(
            EquipamentoDisponivel,
            vida_util_campo='catalogo_equipamento__vida_util_meses',
            empresa=empresa
        ).filter(
            Q(data_desmobilizacao__isnull=True) |
            Q(data_desmobilizacao=None),
            empresa=empresa
        )

    elif login_type == 'Colaborador':
        empresa = capturate_paramns(
            login_type=login_type,
            id=id,
            type="empresa"
        )

        dados_equipamentos = colect_dados(
            EquipamentoDisponivel,
            vida_util_campo= 'catalogo_equipamento__vida_util_meses',
            empresa=empresa
        ).filter(
            Q(data_desmobilizacao__isnull=True) |
            Q(data_desmobilizacao=None),
            empresa=empresa
        )

    # quantidade de equipamentos
    equipamentos_disponiveis = dados_equipamentos.count()
    # equipamentos novos
    # que cumpriram menos de 30% da vida ultil estiamda
    equipamentos_disponiveis_novos = dados_equipamentos.filter(diferenca_dias__lt=30).count()
    # equipamentos seminovos
    # que cumpriram entre 30 e 80% da vida util
    equipamentos_disponiveis_semi_novos = dados_equipamentos.filter(diferenca_dias__lte=30, diferenca_dias__gt=80).count()
    # equioemntos na envelhecidos
    equipamentos_disponiveis_velhos = dados_equipamentos.filter(diferenca_dias__gte=80).count()
    # paginação dos elementos na view
    elementos_paginados = paginate(request=request, data_objects=dados_equipamentos, per_page=10)

    # caso não haja equipamentos disponiveis, os valores retornados são zerados
    if equipamentos_disponiveis == 0:
        carteira_equipamentos = {
            'equipamentos_disponiveis': 0,
            'equipamentos_disponiveis_novos': 0,
            'equipamentos_disponiveis_novos_percent': 0,
            'equipamentos_disponiveis_semi_novos': 0,
            'equipamentos_disponiveis_semi_novos_percent': 0,
            'equipamentos_disponiveis_velhos': 0,
            'equipamentos_disponiveis_velhos_percent': 0,
        }
    else:
        carteira_equipamentos = {
            'equipamentos_disponiveis': equipamentos_disponiveis,
            'equipamentos_disponiveis_novos': equipamentos_disponiveis_novos,
            'equipamentos_disponiveis_novos_percent': (equipamentos_disponiveis_novos / equipamentos_disponiveis) * 100,
            'equipamentos_disponiveis_semi_novos': equipamentos_disponiveis_semi_novos,
            'equipamentos_disponiveis_semi_novos_percent': (equipamentos_disponiveis_semi_novos / equipamentos_disponiveis) * 100,
            'equipamentos_disponiveis_velhos': equipamentos_disponiveis_velhos,
            'equipamentos_disponiveis_velhos_percent': (equipamentos_disponiveis_velhos / equipamentos_disponiveis) * 100,
        }

    return render(request, 'equipamentos/disponibilidade_equipamentos.html',
                  {
                    'elementos_paginados': elementos_paginados,
                    'carteira_equipamentos': carteira_equipamentos,
                    'empresa': empresa
                  })

# view do catalogo de equipamentos
def catalogo_de_equipamentos(request, login_type, id):
    # função que identifica o login e bloqueia a view
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    # Classe que captura e rotorna os dados que o login tem permissão de acessar
    # DadosCatalogoEquipamentoAndFormulario -- controlado por essa classe

    # dica -- o arquivo utils dos apps, coloboradores, equipamentos(catalago),
    # ferramentas(catalogo), servicos(catalogo), empresas,
    # materiais(catalogo), tem classes identicas para fazer esse controle fazer a ptimização futura
    # simplificando as classes

    empresa, dados_catalogo_equipamentos, catalogo_equipamentos_form, equipamento_catalogo = DadosCatalogoEquipamentoAndFormulario(
        login_type=login_type,
        equipamento_catalogo_id = None,
        id=id,
        status=['Mobilizado']
    ).verify_login_type_and_return_objects()

    # função que padroniza a paginação dos elementos na pagina
    elementos_paginados = paginate(
        request=request,
        data_objects=dados_catalogo_equipamentos,
        per_page=20
    )

    # bloco de codigo que valida o formulario enviado na view
    if request.method == 'POST':
        form = CatalogoEquipamentosForms(request.POST)
        if form.is_valid():
            form.save()
            # caso o formulario seja valido retorna uma mensagem de sucesso
            messages.success(
                request,
                f"Equipamento {form.cleaned_data['nome']} adicionado com sucesso"
            )

            return redirect(
                'catalogo_de_equipamentos',
                login_type,
                id)
        # caso o formulario seja valido retorna uma mensagem de erro
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/equipamentos/catalogo/catalogo_de_equipamentos.html', {
        'catalogo_equipamentos_form': catalogo_equipamentos_form,
        'elementos_paginados': elementos_paginados,
        'empresa': empresa
    })

# view que edita o catalogo de equipamentos
def editar_catalogo_de_equipamentos(request, login_type, equipamento_catalogo_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )
    if block == True:
        return redirect('logout')


    unidade, dados_catalogo_equipamentos, catalogo_equipamentos_form, equipamento_catalogo = DadosCatalogoEquipamentoAndFormulario(
        login_type=login_type,
        equipamento_catalogo_id = equipamento_catalogo_id,
        id=id,
        status=['Mobilizado']
    ).verify_login_type_and_return_objects()


    if request.method == 'POST':
        form = CatalogoEquipamentosForms(
            request.POST,
            instance=equipamento_catalogo
        )

        if form.is_valid():
            form.save()
            messages.success(request, f"Equipamento {form.cleaned_data['nome']} editado com sucesso")
            return redirect('catalogo_de_equipamentos', login_type, id)
        messages.error(request, f"Algo deu errado")

    return render(request, 'controle/equipamentos/catalogo/editar_catalogo_de_equipamentos.html',
                  {'catalogo_equipamentos_form': catalogo_equipamentos_form,
                   'equipamento_catalogo_id': equipamento_catalogo_id
                   })


def desmobilizar_equipamento_do_catalogo(request, login_type, equipamento_catalogo_id, id, desm):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(request=request, model=CatalogoEquipamentos, object_id=equipamento_catalogo_id, desm=desm)

    return redirect('catalogo_de_equipamentos', login_type, id)


def catalogo_de_equipamentos_desmobilizados(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    unidade, dados_catalogo_equipamentos, catalogo_equipamentos_form, equipamento_catalogo = DadosCatalogoEquipamentoAndFormulario(
        login_type=login_type,
        equipamento_catalogo_id = None,
        id=id,
        status=['Desmobilizado', 'Desmobilizacao Permanente']
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_catalogo_equipamentos)

    return render(request, 'controle/equipamentos/catalogo/catalogo_de_equipamentos_desmobilizados.html', {
        'elementos_paginados':elementos_paginados,
        'unidade': unidade
    })


def reabilitar_equipamento_do_catalogo(request, login_type, equipamento_catalogo_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(request=request, model=CatalogoEquipamentos, object_id=equipamento_catalogo_id)

    return redirect('catalogo_de_equipamentos_desmobilizados', login_type, id)


def equipamentos_disponiveis(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    empresa, dados_equipamentos_disponiveis, equipamento_disponivel_form = DadosEquipamentosAndFormulario(
        login_type=login_type,
        id=id,
        status=['Mobilizado']
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(
        request=request,
        data_objects=dados_equipamentos_disponiveis
    )


    if request.method == 'POST':
        form = EquipamentoDisponivelForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['data_desmobilizacao'] == '' or form.cleaned_data['data_desmobilizacao'] == None:
                form.instance.status = 'Mobilizado'
                form.save()
            else:
                form.instance.status = 'Desmobilizado'
                form.save()

            messages.success(request, f"Equipamento {form.cleaned_data['catalogo_equipamento']} criado(a) com sucesso")
            return redirect('equipamentos_disponiveis', login_type, id)
        messages.error(request, f"Algo deu errado")

    return render(request, 'controle/equipamentos/disponibilidade/equipamentos_disponiveis.html', {
        'equipamento_disponivel_form': equipamento_disponivel_form,
        'elementos_paginados': elementos_paginados,
        'empresa': empresa,
    })


def editar_equipamento_disponivel(request, login_type, equipamento_disponivel_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    equipamento_disponivel, empresa, equipamento_disponivel_form = editar_item(
        id=equipamento_disponivel_id,
        model=EquipamentoDisponivel,
        form_class=EquipamentoDisponivelForm
    )

    if request.method == 'POST':
        form = EquipamentoDisponivelForm(request.POST, instance=equipamento_disponivel)
        if form.is_valid():
            if form.cleaned_data['data_desmobilizacao'] == '' or form.cleaned_data['data_desmobilizacao'] == None:
                form.instance.status = 'Mobilizado'
                form.save()
            else:
                form.instance.status = 'Desmobilizado'
                form.save()

            messages.success(request, f"Equipamento {form.cleaned_data['catalogo_equipamento']} editado com sucesso")
            return redirect('equipamentos_disponiveis', login_type, id)
        messages.error(request, f"Algo deu errado")


    return render(request, 'controle/equipamentos/disponibilidade/editar_equipamento_disponivel.html',
                  {'equipamento_disponivel_form': equipamento_disponivel_form,
                   'equipamento_disponivel_id': equipamento_disponivel_id})


def equipamentos_desmobilizados(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    empresa, dados_equipamentos_disponiveis, equipamento_disponivel_form = DadosEquipamentosAndFormulario(
        login_type=login_type,
        id=id,
        status=['Desmobilizado', 'Desmobilizacao Permanente']
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(
        request=request,
        data_objects=dados_equipamentos_disponiveis
    )

    return render(request, 'controle/equipamentos/desmobilizados/equipamentos_desmobilizados.html', {
        'equipamento_desmobilizado_form': equipamento_disponivel_form,
        'elementos_paginados': elementos_paginados,
        'empresa': empresa,
    })


def editar_equipamento_desmobilizado(request, login_type, equipamento_desmobilizado_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)


    equipamento_desmobilizado, empresa, equipamento_desmobilizado_form = editar_item(
        id=equipamento_desmobilizado_id,
        model=EquipamentoDisponivel,
        form_class=EquipamentoDisponivelForm
    )


    if request.method == 'POST':
        form = EquipamentoDisponivelForm(request.POST, instance=equipamento_desmobilizado)
        if form.is_valid():
            if form.cleaned_data['data_desmobilizacao'] == '' or form.cleaned_data['data_desmobilizacao'] == None:
                form.instance.status = 'Mobilizado'
                form.save()
            else:
                form.save()

            messages.success(request, f"Equipamento {form.cleaned_data['catalogo_equipamento']} editado com sucesso")
            return redirect('equipamentos_desmobilizados', login_type, id)
        messages.error(request, 'Algo deu errado')

    return render(request, 'controle/equipamentos/desmobilizados/editar_equipamento_desmobilizado.html',
                  {'equipamento_desmobilizado_form': equipamento_desmobilizado_form,
                   'equipamento_desmobilizado_id': equipamento_desmobilizado_id})



def manutencao_de_equipamentos(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    dados_equipamentos_disponiveis, empresa, equipamento_disponivel_form = DadosDisponiveisHandler(
        login_type=login_type,
        id=id,
        model=EquipamentoDisponivel,
        form_cls=EquipamentoDisponivelForm,
        vida_util_campo="catalogo_equipamento__vida_util_meses"
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_equipamentos_disponiveis)

    if request.method == 'POST':
        form = EquipamentoDisponivelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Equipamento {form.cleaned_data['catalogo_equipamento']} criado com sucesso")
            return redirect('manutencao_de_equipamentos', login_type, id)

    return render(request, 'controle/manutencao/equipamentos/manutencao_de_equipamentos.html', {
        'equipamento_disponivel_form': equipamento_disponivel_form,
        'elementos_paginados': elementos_paginados,
        'empresa': empresa
    })


def cadastro_manutencao_equipamento(request, login_type, equipamento_disponivel_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    equipamento_disponivel = EquipamentoDisponivel.objects.get(
        id_random=equipamento_disponivel_id
    )
    manutencao_equipaemnto_form = ManutencaoEquipamentosForm(
        initial={'equipamento': equipamento_disponivel},
        equipamento_id=equipamento_disponivel_id
    )

    if request.method == 'POST':
        form = ManutencaoEquipamentosForm(
            request.POST,
            equipamento_id=equipamento_disponivel_id
        )
        if form.is_valid():
            form.save()
            messages.success(request, f"Manutenção aplicada com sucesso")
            return redirect('manutencao_de_equipamentos', login_type, id)

    return render(request, 'controle/manutencao/equipamentos/cadastro_manutencao_equipamento.html',
                  {'manutencao_equipaemnto_form': manutencao_equipaemnto_form,
                   'equipamento_disponivel_id': equipamento_disponivel_id,
                   'equipamento_disponivel': equipamento_disponivel})


def historico_de_manutencao_equipamento(request, login_type, equipamento_disponivel_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    equipamento_disponivel = EquipamentoDisponivel.objects.get(
        id_random=equipamento_disponivel_id
    )
    dados_historico_de_manutencao = ManutencaoEquipamentos.objects.filter(
        equipamento__id_random=equipamento_disponivel_id
    )

    elementos_paginados = paginate(request=request, data_objects=dados_historico_de_manutencao)

    return render(request, 'controle/manutencao/equipamentos/historico_de_manutencao_equipamento.html',
                  {'equipamento_disponivel': equipamento_disponivel,
                           'elementos_paginados': elementos_paginados})


def desmobilizar_equipamento_disponivel(request, login_type, equipamento_disponivel_id, id, desm):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(
        request=request,
        model=EquipamentoDisponivel,
        object_id=equipamento_disponivel_id,
        desm=desm,
        data='data_desmobilizacao'
    )

    return redirect('equipamentos_disponiveis', login_type, id)


def reabilitar_equipamento_desmobilizado(request, login_type, equipamento_desmobilizado_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(
        request=request,
        model=EquipamentoDisponivel,
        object_id=equipamento_desmobilizado_id,
        data='data_desmobilizacao'
    )

    return redirect('equipamentos_desmobilizados', login_type, id)

# view  que edita a manutenção aplicada
def editar_manutencao_equipamento(request, login_type, manutencao_equipamento_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    # resgata a manutenção do banco de dados
    manutencao = ManutencaoEquipamentos.objects.get(
        id_random=manutencao_equipamento_id
    )
    # instacia o formulario
    # e trava o equipamento que pode ser chamado
    # pra proteger os inputs
    manutencao_equipamento_form = ManutencaoEquipamentosForm(
        instance=manutencao,
        equipamento_id=manutencao.equipamento.id_random
    )

    # bloco de codigo acionado quando o formulario e enviado
    if request.method == 'POST':
        form = ManutencaoEquipamentosForm(
            request.POST,
            # substitui a instancia inicial no banco de dados
            instance=manutencao,
        )
        if form.is_valid():
            form.save()

            messages.success(request, "Manutenção editada com sucesso")
            return redirect('historico_de_manutencao_equipamento', login_type, manutencao.equipamento.id_random, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/manutencao/equipamentos/editar_manutencao_equipamento.html',
                  {'manutencao_equipamento_form': manutencao_equipamento_form,
                   'manutencao_equipamento_id': manutencao_equipamento_id})


# função que deleta a manutenção do historica
def deletar_manutencao_do_historico_equipamento(request, login_type, manutencao_equipamento_id, id):
    # função que identifica o login e bloqueia a view
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    # localiza qual linha do banco de dados deve ser deletada
    manutencao = ManutencaoEquipamentos.objects.get(
        id_random=manutencao_equipamento_id
    )
    # nova caputura de dados antes retorna a view de historico de manutenção
    id_manutencao = manutencao.equipamento.id_rando
    manutencao.delete()
    messages.success(request, f"Manutenção removida do histórico")
    return redirect('historico_de_manutencao_equipamento', login_type, id_manutencao, id)
