from django.shortcuts import render, redirect
from jardins.models import Jardins
from jardins.forms import JardimForms
from utils.utils import paginate
from django.db.models import Q
from utils.utils import block_view
from django.contrib import messages
from jardins.utils import DadosJardinsAndFormulario
from utils.utils import alterar_status

# Create your views here.
def areas_verdes(request, unidade, link):
    login_type = request.session['login_type']
    id = request.session['login_id']

    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    return render(request, 'areas_verdes/areas_verdes.html',
                  {'unidade': unidade, 'link': link})


def areas(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    unidade, dados_areas, area_form = DadosJardinsAndFormulario(
        login_type=login_type,
        id=id,
        status_jardin=['Mobilizado'],
        status_unidade=['Mobilizado'],
        status_localidade=['Mobilizado'],
        delimiter="|"
    ).verify_login_type_and_return_objects()

    dados_areas = dados_areas.exclude(
            Q(status='Desmobilizado') |
            Q(status='Desmobilizacao Permanente') |
            Q(unidade_jardim__unidadeoriginial__status='Desmobilizado') |
            Q(unidade_jardim__unidadeoriginial__status='Desmobilizacao Permanente') |
            Q(unidade_jardim__status='Desmobilizado') |
            Q(unidade_jardim__status='Desmobilizacao Permanente')
    )

    elementos_paginados = paginate(request=request, data_objects=dados_areas)

    if request.method == 'POST':
        form = JardimForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Area verde {form.cleaned_data['nome']} cadastrada com sucesso")
            return redirect('areas', login_type, id)
        messages.error(request, f"Algo deu errado verifique as entradas")

    return render(request, 'controle/unidades/areas_verdes/areas.html', {
        'area_form': area_form,
        'elementos_paginados': elementos_paginados,
        'unidade': unidade})

def editar_area(request, login_type, area_id, id):
    print("Editar area")
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    print("A view nao foi bloqueada")

    area = Jardins.objects.get(
        id_random=area_id
    )

    unidade, dados_areas, area_form = DadosJardinsAndFormulario(
        login_type=login_type,
        id=id,
        status_jardin=['Mobilizado'],
        status_unidade=['Mobilizado'],
        status_localidade=['Mobilizado'],
        area_id=area_id,
        delimiter="|"
    ).verify_login_type_and_return_objects()

    if request.method == 'POST':
        form = JardimForms(
            request.POST,
            instance=area,
        )
        if form.is_valid():
            form.save()

            messages.success(request, f"Area verde {form.cleaned_data['nome']} editada com sucesso")
            return redirect('areas', login_type, id)
        messages.error(request, f"Algo deu errado verifique as entradas")

    return render(request, 'controle/unidades/areas_verdes/editar_area.html',
                  {'area_form': area_form, 'area_id': area_id})

def desmobilizar_area(request, login_type, area_id, id, desm):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(request=request, model=Jardins, object_id=area_id, desm=desm)

    return redirect('areas', login_type, id)

def areas_desmobilizadas(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    unidade, dados_areas, area_form = DadosJardinsAndFormulario(
        login_type=login_type,
        id=id,
        status_jardin=['Desmobilizado', 'Desmobilizacao Permanente'],
        status_unidade=['Desmobilizado', 'Desmobilizacao Permanente'],
        status_localidade=['Desmobilizado', 'Desmobilizacao Permanente'],
        delimiter= "|"
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_areas)

    return render(request, 'controle/unidades/areas_verdes/areas_desmobilizadas.html',{
                      'area_form': area_form,
                      'elementos_paginados':elementos_paginados,
                      'unidade': unidade
    })


def reabilitar_area(request, login_type, area_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    alterar_status(request=request, model=Jardins, object_id=area_id, desm='mob')

    return redirect('areas_desmobilizadas', login_type, id)
