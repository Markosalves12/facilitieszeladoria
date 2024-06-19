from django.shortcuts import render, redirect
from manutencao.models import Manutencao
from manutencao.forms import ManutencaoForms
from utils.utils import paginate
from utils.utils import block_view
from django.contrib import messages
from gerente.models import Gerente
from gestor.models import Gestor
# Create your views here.

def catalogo_de_manutencao(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    if login_type == "Administrador":
        unidade = ""
        dados_catalogo_manutencao = Manutencao.objects.exclude(
            status__in=['Desmobilizado', 'Desmobilizacao Permanente']
        )
        catalogo_manutencao_form = ManutencaoForms()

    elif login_type == "Gestor":
        gestor = Gestor.objects.get(id=id)
        unidade = gestor.empresa.unidade
        dados_catalogo_manutencao = Manutencao.objects.exclude(
            status__in=['Desmobilizado', 'Desmobilizacao Permanente']
        ).filter(
            unidade=unidade
        )
        catalogo_manutencao_form = ManutencaoForms(
            unidade=unidade
        )

    elif login_type == "Gerente":
        gerente = Gerente.objects.get(id=id)
        unidade = gerente.gestor.empresa.unidade
        dados_catalogo_manutencao = Manutencao.objects.exclude(
            status__in=['Desmobilizado', 'Desmobilizacao Permanente']
        ).filter(
            unidade=unidade
        )
        catalogo_manutencao_form = ManutencaoForms(
            unidade=unidade
        )

    else:
        return redirect("logout", login_type, id)


    elementos_paginados = paginate(request=request, data_objects=dados_catalogo_manutencao)

    if request.method == 'POST':
        form = ManutencaoForms(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f"Manutenção {form.cleaned_data['tipo_manutencao']} criada com sucesso")
            return redirect('catalogo_de_manutencao', login_type, id)

    return render(request, 'controle/manutencao/manutencao/catalogo_de_manutencao.html', {
        'catalogo_manutencao_form': catalogo_manutencao_form,
        'elementos_paginados': elementos_paginados,
        'unidade': unidade

    })

def editar_manutencao(request, login_type, manutencao_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    manutencao = Manutencao.objects.get(id=manutencao_id)
    manutencao_form = ManutencaoForms(instance=manutencao)

    if request.method == 'POST':
        form = ManutencaoForms(request.POST, instance=manutencao)
        if form.is_valid():
            form.save()

            messages.success(request, f"Manutenção {form.cleaned_data['tipo_manutencao']} editado com sucesso")
            return redirect('catalogo_de_manutencao', login_type, id)

    return render(request, 'controle/manutencao/manutencao/editar_manutencao.html',
                  {'manutencao_form': manutencao_form, 'manutencao_id': manutencao_id})

def desmobilizar_manutencao(request, login_type, manutencao_id, id, desm):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    manutencao_catalogo = Manutencao.objects.get(id=manutencao_id)

    if desm == "temp":
        manutencao_catalogo.status = "Desmobilizado"
        messages.success(request, f"Manutenção {manutencao_catalogo.tipo_manutencao} desmobilizado com sucesso")
    elif desm == "perm":
        manutencao_catalogo.status = "Desmobilizacao Permanente"
        messages.success(request, f"Manutenção {manutencao_catalogo.tipo_manutencao} desmobilizado permanentemente com sucesso")
    manutencao_catalogo.save()


    return redirect('catalogo_de_manutencao', login_type, id)

def manutencoes_desmobilizadas(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    elif login_type == "Administrador":
        unidadee = ""
        dados_catalogo_manutencao = Manutencao.objects.filter(
            status__in=['Desmobilizado', 'Desmobilizacao Permanente']
        )

    elif login_type == "Gestor":
        gestor = Gestor.objects.get(id=id)
        unidade = gestor.empresa.unidade
        dados_catalogo_manutencao = Manutencao.objects.filter(
            status__in=['Desmobilizado', 'Desmobilizacao Permanente']
        ).filter(
            unidade = unidade
        )

    elif login_type == "Gerente":
        gerente = Gerente.objects.get(id=id)
        unidade = gerente.gestor.empresa.unidade
        dados_catalogo_manutencao = Manutencao.objects.filter(
            status__in=['Desmobilizado', 'Desmobilizacao Permanente']
        ).filter(
            unidade = unidade
        )

    elementos_paginados = paginate(request=request, data_objects=dados_catalogo_manutencao)

    return render(request, 'controle/manutencao/manutencao/manutencoes_desmobilizadas.html', {
        'elementos_paginados': elementos_paginados,
        'unidade':unidade
    })

def reabilitar_manutencao(request, login_type, manutencao_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    manutencao_catalogo = Manutencao.objects.get(id=manutencao_id)
    manutencao_catalogo.status = "Mobilizado"
    manutencao_catalogo.save()

    messages.success(request, f"Manutenção {manutencao_catalogo.tipo_manutencao} reabilitada com sucesso")
    return redirect('manutencoes_desmobilizadas', login_type, id)

