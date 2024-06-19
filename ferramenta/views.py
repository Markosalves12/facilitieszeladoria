from django.shortcuts import render, redirect
from django.db.models import Q
from ferramenta.forms import (CatalogoFerramentasForms, FerramentaDisponivelForms,
                              ManutencaoFerramentasForms)

from ferramenta.models import (FerramentaDisponivel, CatalogoFerramentas,
                               ManutencaoFerramentas)

from utils.utils import paginate
from ferramenta.utils import (DadosCatalogoFerramentaAndFormulario,
                              DadosFerramentasAndFormulario)

from utils.utils import block_view
from django.contrib import messages
from utils.utils import alterar_status, colect_dados, DadosDisponiveisHandler, capturate_paramns, editar_item

# Create your views here.
# consultar os comentarios no app de equipamentos
# comentarios similar ou iguais
def disponibilidade_ferramentas(request):
    login_type = request.session['login_type']
    id = request.session['login_id']

    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa = ''
    if request.session['login_type'] == 'Administrador':
        dados_ferramentas = colect_dados(
                FerramentaDisponivel,
                vida_util_campo= 'catalogo_ferramenta__vida_util_meses',
        ).filter(
            Q(data_desmobilizacao__isnull=True) |
            Q(data_desmobilizacao=None),
        )

    elif request.session['login_type'] == 'Gestor':
        empresa = capturate_paramns(login_type=login_type, id=id, type='empresa')
        dados_ferramentas = colect_dados(
                FerramentaDisponivel,
                vida_util_campo= 'catalogo_ferramenta__vida_util_meses',
                empresa=empresa
        ).filter(
            Q(data_desmobilizacao__isnull=True) |
            Q(data_desmobilizacao=None),
            empresa=empresa
        )

    elif login_type == 'Gerente':
        empresa = capturate_paramns(login_type=login_type, id=id, type='empresa')
        dados_ferramentas = colect_dados(
                FerramentaDisponivel,
                vida_util_campo= 'catalogo_ferramenta__vida_util_meses',
                empresa=empresa
        ).filter(
            Q(data_desmobilizacao__isnull=True) |
            Q(data_desmobilizacao=None),
            empresa=empresa
        )

    elif login_type == 'Colaborador':
        empresa = capturate_paramns(login_type=login_type, id=id, type='empresa')
        dados_ferramentas = colect_dados(
                FerramentaDisponivel,
                vida_util_campo= 'catalogo_ferramenta__vida_util_meses',
                empresa=empresa
        ).filter(
            Q(data_desmobilizacao__isnull=True) |
            Q(data_desmobilizacao=None),
            empresa=empresa
        )

    ferramentas_disponiveis = dados_ferramentas.count()

    ferramentas_disponiveis_novos = dados_ferramentas.filter(diferenca_dias__lt=30).count()

    ferramentas_disponiveis_semi_novos = dados_ferramentas.filter(diferenca_dias__lte=30, diferenca_dias__gt=80).count()

    ferramentas_disponiveis_velhos = dados_ferramentas.filter(diferenca_dias__gte=80).count()

    elementos_paginados = paginate(request=request, data_objects=dados_ferramentas, per_page=10)

    if ferramentas_disponiveis == 0:
        carteira_ferramentas = {
            'ferramentas_disponiveis': 0,
            'ferramentas_disponiveis_novos': 0,
            'ferramentas_disponiveis_novos_percent': 0,
            'ferramentas_disponiveis_semi_novos': 0,
            'ferramentas_disponiveis_semi_novos_percent': 0,
            'ferramentas_disponiveis_velhos': 0,
            'ferramentas_disponiveis_velhos_percent': 0
        }
    else:
        carteira_ferramentas = {
            'ferramentas_disponiveis': ferramentas_disponiveis,
            'ferramentas_disponiveis_novos': ferramentas_disponiveis_novos,
            'ferramentas_disponiveis_novos_percent': (ferramentas_disponiveis_novos / ferramentas_disponiveis) * 100,
            'ferramentas_disponiveis_semi_novos': ferramentas_disponiveis_semi_novos,
            'ferramentas_disponiveis_semi_novos_percent': (
                                                                  ferramentas_disponiveis_semi_novos / ferramentas_disponiveis) * 100,
            'ferramentas_disponiveis_velhos': ferramentas_disponiveis_velhos,
            'ferramentas_disponiveis_velhos_percent': (ferramentas_disponiveis_velhos / ferramentas_disponiveis) * 100,
        }

    return render(request, 'ferramentas/disponibilidade_ferramentas.html',
                  {'elementos_paginados': elementos_paginados,
                   'carteira_ferramentas': carteira_ferramentas, 'empresa': empresa})

def catalogo_de_ferramentas(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa, dados_catalogo_ferramentas, catalogo_ferramentas_form, ferramenta_catalogo = DadosCatalogoFerramentaAndFormulario(
        login_type=login_type,
        ferramenta_catalogo_id = None,
        id=id,
        status=['Mobilizado']
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_catalogo_ferramentas)

    if request.method == 'POST':
        form = CatalogoFerramentasForms(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f"Ferramenta {form.cleaned_data['nome']} adicionado com sucesso")
            return redirect('catalogo_de_ferramentas', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/ferramentas/catalogo/catalogo_de_ferramentas.html', {
        'elementos_paginados': elementos_paginados,
        'catalogo_ferramentas_form': catalogo_ferramentas_form,
        'empresa': empresa,
    })

def editar_catalogo_de_ferramentas(request, login_type, ferramenta_catalogo_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    unidade, dados_catalogo_ferramentas, catalogo_ferramentas_form, ferramenta_catalogo = DadosCatalogoFerramentaAndFormulario(
        login_type=login_type,
        ferramenta_catalogo_id = ferramenta_catalogo_id,
        id=id,
        status=['Mobilizado']
    ).verify_login_type_and_return_objects()

    if request.method == 'POST':
        form = CatalogoFerramentasForms(request.POST, instance=ferramenta_catalogo)
        if form.is_valid():
            form.save()

            messages.success(request, f"Ferramenta {form.cleaned_data['nome']} editado com sucesso")
            return redirect('catalogo_de_ferramentas', login_type, id)
        messages.error(request, "Algo de errado")

    return render(request, 'controle/ferramentas/catalogo/editar_catalogo_de_ferramentas.html',
                  {'catalogo_ferramentas_form': catalogo_ferramentas_form,
                   'ferramenta_catalogo_id': ferramenta_catalogo_id})

def desmobilizar_ferramenta_do_catalogo(request, login_type, ferramenta_catalogo_id, id, desm):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(request=request, model=CatalogoFerramentas, object_id=ferramenta_catalogo_id, desm=desm)

    return redirect('catalogo_de_ferramentas', login_type, id)

def catalogo_de_ferramentas_desmobilizadas(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa, dados_catalogo_ferramentas, catalogo_ferramentas_form, ferramenta = DadosCatalogoFerramentaAndFormulario(
        login_type=login_type,
        ferramenta_catalogo_id = None,
        id=id,
        status=['Desmobilizado', 'Desmobilizacao Permanente']
    ).verify_login_type_and_return_objects()

    catalogo_ferramentas_form = CatalogoFerramentasForms()
    elementos_paginados = paginate(request=request, data_objects=dados_catalogo_ferramentas)

    return render(request, 'controle/ferramentas/catalogo/catalogo_de_ferramentas_desmobilizadas.html', {
        'elementos_paginados': elementos_paginados,
        'catalogo_ferramentas_form': catalogo_ferramentas_form,
        'empresa': empresa
    })

def reabilitar_ferramenta_do_catalogo(request, login_type, ferramenta_catalogo_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(request=request, model=CatalogoFerramentas, object_id=ferramenta_catalogo_id)

    return redirect('catalogo_de_ferramentas_desmobilizadas', login_type, id)

def ferramentas_disponiveis(request,login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    empresa, dados_ferramentas_disponiveis, ferramenta_disponivel_form = DadosFerramentasAndFormulario(
        login_type=login_type,
        id=id,
        status=['Mobilizado']
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(
        request=request,
        data_objects=dados_ferramentas_disponiveis
    )

    if request.method == 'POST':
        form = FerramentaDisponivelForms(request.POST)
        if form.is_valid():
            if form.cleaned_data['data_desmobilizacao'] == '' or form.cleaned_data['data_desmobilizacao'] == None:
                form.save()
            else:
                form.instance.status = 'Desmobilizado'
                form.save()

            messages.success(request, f"Ferramenta {form.cleaned_data['catalogo_ferramenta']} criado(a) com sucesso")
            return redirect('ferramentas_disponiveis', login_type, id)
        messages.error(request, f"Algo deu errado")


    return render(request, 'controle/ferramentas/disponibilidade/ferramentas_disponiveis.html', {
        'ferramenta_disponivel_form': ferramenta_disponivel_form,
        'elementos_paginados': elementos_paginados,
        'empresa': empresa
    })

def editar_ferramenta_disponivel(request, login_type, ferramenta_disponivel_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')


    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    ferramenta_disponivel, empresa, ferramenta_disponivel_form = editar_item(
        id=ferramenta_disponivel_id,
        model=FerramentaDisponivel,
        form_class=FerramentaDisponivelForms
    )

    if request.method == 'POST':
        form = FerramentaDisponivelForms(request.POST, instance=ferramenta_disponivel)
        if form.is_valid():
            if form.cleaned_data['data_desmobilizacao'] == '' or form.cleaned_data['data_desmobilizacao'] == None:
                form.instance.status = 'Mobilizado'
                form.save()
            else:
                form.instance.status = 'Desmobilizado'
                form.save()

            messages.success(request, f"Ferramenta {form.cleaned_data['catalogo_ferramenta']} editada com sucesso")
            return redirect('ferramentas_disponiveis', login_type, id)
        messages.error(request, 'Algo deu errado')

    return render(request, 'controle/ferramentas/disponibilidade/editar_ferramenta_disponivel.html',
                  {'ferramenta_disponivel_form': ferramenta_disponivel_form,
                   'ferramenta_disponivel_id': ferramenta_disponivel_id})

def ferramentas_desmobilizadas(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa, dados_ferramentas_desmobilizados, ferramenta_desmobilizado_form = DadosFerramentasAndFormulario(
        login_type=login_type,
        id=id,
        status=['Desmobilizado', 'Desmobilizacao Permanente']
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_ferramentas_desmobilizados)

    return render(request, 'controle/ferramentas/desmobilizados/ferramentas_desmobilizadas.html', {
        'ferramenta_desmobilizado_form': ferramenta_desmobilizado_form,
        'elementos_paginados': elementos_paginados,
        'empresa':empresa
    })

def editar_ferramenta_desmobilizada(request, login_type, ferramenta_desmobilizado_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)


    ferramenta_desmobilizado, empresa, ferramenta_desmobilizado_form = editar_item(
        id=ferramenta_desmobilizado_id,
        model=FerramentaDisponivel,
        form_class=FerramentaDisponivelForms
    )

    if request.method == 'POST':
        form = FerramentaDisponivelForms(
            request.POST,
            instance=ferramenta_desmobilizado
        )
        if form.is_valid():
            if form.cleaned_data['data_desmobilizacao'] == '' or form.cleaned_data['data_desmobilizacao'] == None:
                form.instance.status = 'Mobilizado'
                form.save()
            else:
                form.save()

            messages.success(request, f"Ferramenta {form.cleaned_data['catalogo_ferramenta']} edita com sucesso")
            return redirect('ferramentas_desmobilizadas', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/ferramentas/desmobilizados/editar_ferramenta_desmobilizado.html',
                  {'ferramenta_desmobilizado_form': ferramenta_desmobilizado_form,
                   'ferramenta_desmobilizado_id': ferramenta_desmobilizado_id})

def manutencao_de_ferramentas(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    dados_ferramentas_disponiveis, empresa, ferramenta_disponivel_form = DadosDisponiveisHandler(
        login_type=login_type,
        id=id,
        model=FerramentaDisponivel,
        form_cls=FerramentaDisponivelForms,
        vida_util_campo="catalogo_ferramenta__vida_util_meses"
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_ferramentas_disponiveis, per_page=10)

    if request.method == 'POST':
        form = FerramentaDisponivelForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Ferramenta {form.cleaned_data['catalogo_ferramenta']} criada com sucesso")
            return redirect('manutencao_de_ferramentas', login_type, id)

    return render(request, 'controle/manutencao/ferramentas/manutencao_de_ferramentas.html', {
        'elementos_paginados': elementos_paginados,
        'ferramenta_disponivel_form': ferramenta_disponivel_form,
        'empresa': empresa
    })

def cadastro_manutencao_ferramenta(request, login_type, ferramenta_disponivel_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    ferramenta_disponivel = FerramentaDisponivel.objects.get(
        id_random=ferramenta_disponivel_id
    )
    manutencao_ferramenta_form = ManutencaoFerramentasForms(
        initial={'ferramenta': ferramenta_disponivel},
        ferramenta_id=ferramenta_disponivel_id
    )

    if request.method == 'POST':
        form = ManutencaoFerramentasForms(
            request.POST,
            ferramenta_id=ferramenta_disponivel_id
        )
        if form.is_valid():
            form.save()
            messages.success(request, f"Manutenção aplicada com sucesso")
            return redirect('manutencao_de_ferramentas', login_type, id)

    return render(request, 'controle/manutencao/ferramentas/cadastro_manutencao_ferramenta.html',
                  {'manutencao_ferramenta_form': manutencao_ferramenta_form,
                   'ferramenta_disponivel_id': ferramenta_disponivel_id,
                   'ferramenta_disponivel': ferramenta_disponivel})

def historico_de_manutencao_ferramenta(request, login_type, ferramenta_disponivel_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    ferramenta_disponivel = FerramentaDisponivel.objects.get(
        id_random=ferramenta_disponivel_id
    )
    dados_historico_de_manutencao = ManutencaoFerramentas.objects.filter(
        ferramenta__id_random=ferramenta_disponivel_id
    )

    elementos_paginados = paginate(request=request, data_objects=dados_historico_de_manutencao, per_page=10)


    return render(request, 'controle/manutencao/ferramentas/historico_de_manutencao_ferramenta.html',
                  {'elementos_paginados': elementos_paginados,
                   'ferramenta_disponivel': ferramenta_disponivel})

def desmobilizar_ferramenta_disponivel(request, login_type, ferramenta_disponivel_id, id, desm):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(
        request=request,
        model=FerramentaDisponivel,
        object_id=ferramenta_disponivel_id,
        desm=desm,
        data='data_desmobilizacao'
    )

    return redirect('ferramentas_disponiveis', login_type, id)

def reabilitar_ferramenta_desmobilizado(request, login_type,
                                        ferramenta_desmobilizado_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(
        request=request,
        model=FerramentaDisponivel,
        object_id=ferramenta_desmobilizado_id,
        data='data_desmobilizacao'
    )

    return redirect('ferramentas_desmobilizadas', login_type, id)

def editar_manutencao_ferramenta(request, login_type, manutencao_ferramenta_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    manutencao = ManutencaoFerramentas.objects.get(
        id_random=manutencao_ferramenta_id
    )
    manutencao_ferramenta_form = ManutencaoFerramentasForms(
        instance=manutencao,
        ferramenta_id=manutencao.ferramenta.id_random
    )

    if request.method == 'POST':
        form = ManutencaoFerramentasForms(
            request.POST,
            instance=manutencao,
        )
        print(form)
        if form.is_valid():
            form.save()

            messages.success(request, "Manutenção editada com sucesso")
            return redirect('historico_de_manutencao_ferramenta', login_type, manutencao.ferramenta.id_random, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/manutencao/ferramentas/editar_manutencao_ferramenta.html',
                  {'manutencao_ferramenta_form': manutencao_ferramenta_form,
                   'manutencao_ferramenta_id': manutencao_ferramenta_id})

def deletar_manutencao_do_historico(request, login_type, manutencao_ferramenta_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    manutencao = ManutencaoFerramentas.objects.get(
        id_random=manutencao_ferramenta_id
    )
    id_manutencao = manutencao.ferramenta.id_random
    manutencao.delete()
    messages.success(request, f"Manutenção removida do histórico")
    return redirect('historico_de_manutencao_ferramenta', login_type, id_manutencao, id)