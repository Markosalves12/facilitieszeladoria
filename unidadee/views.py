from django.shortcuts import render, redirect
from unidadee.models import Unidade, Localidade
from unidadee.forms import UnidadeForms, LocalidadeForms
from utils.utils import paginate
from utils.utils import block_view
from django.contrib import messages
from unidadee.utils import capturate_paramns, DadosLocalidadesAndFormulario, DadosUnidadesAndFormulario
from utils.utils import alterar_status
# Create your views here.


def unidades(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    dados_unidades, unidade_form, unidade = DadosUnidadesAndFormulario(
        login_type=login_type,
        id=id,
        status_unidade=['Mobilizado'],
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_unidades)

    if request.method == 'POST':
        form = UnidadeForms(request.POST)
        if form.is_valid():
            # Obter os dados limpos do formulário
            # Aplica um capitalize no campo de unidade
            # Aplica um lower nos demais compos
            form.cleaned_data['unidade'].strip().capitalize()
            form.save()
            messages.success(request, f"Unidade {form.cleaned_data['unidade']} cadastrada com sucesso")
            return redirect('unidades', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/unidades/unidades/unidades.html',
                  {'unidade_form': unidade_form,
                   'elementos_paginados': elementos_paginados})

def editar_unidade(request, login_type, unidade_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')


    dados_unidades, unidade_form, unidade = DadosUnidadesAndFormulario(
        login_type=login_type,
        id=id,
        status_unidade=['Mobilizado'],
        unidade_id=unidade_id
    ).verify_login_type_and_return_objects()

    if request.method == 'POST':
        form = UnidadeForms(request.POST, request.FILES, instance=unidade)
        if form.is_valid():
            form.save()

            messages.success(request, f"Unidade {form.cleaned_data['unidade']} editada com sucesso")
            return redirect('unidades', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/unidades/unidades/editar_unidade.html',
                  {'unidade_form': unidade_form, 'unidade_id': unidade_id})

def desmobilizar_unidade(request, login_type, unidade_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    alterar_status(
        request=request,
        model=Unidade,
        object_id=unidade_id,
        desm='temp'
    )


    return redirect('unidades', login_type, id)

def unidades_desmobilizadas(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    dados_unidades, unidade_form, unidade = DadosUnidadesAndFormulario(
        login_type=login_type,
        id=id,
        status_unidade=['Desmobilizado'],
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(
        request=request,
        data_objects=dados_unidades
    )

    return render(request, 'controle/unidades/unidades/unidades_desmobilizadas.html',
                  {'unidade_form': unidade_form,
                   'elementos_paginados': elementos_paginados})

def reabilitar_unidade(request, login_type, unidade_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    alterar_status(
        request=request,
        model=Unidade,
        object_id=unidade_id
    )

    return redirect('unidades_desmobilizadas', login_type, id)

def localidades(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    dados_localidades, localidade_form, unidade, localidade = DadosLocalidadesAndFormulario(
        login_type=login_type,
        id=id,
        status_localidade=['Mobilizado'],
        status_unidade=['Mobilizado'],
        delimiter="&",
        localidade_id=None
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(
        request=request,
        data_objects=dados_localidades
    )

    if request.method == 'POST':
        form = LocalidadeForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Localidade {form.cleaned_data['nome']} adicionada com sucesso")
            return redirect('localidades', login_type, id)

        messages.error(request, f"Algo deu errado")

    return render(request, 'controle/unidades/localidades/localidades.html', {
        'localidade_form': localidade_form,
        'elementos_paginados': elementos_paginados,
        'unidade': unidade})

def editar_localidade(request, login_type, localidade_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    dados_localidades, localidade_form, unidade, localidade = DadosLocalidadesAndFormulario(
        login_type=login_type,
        id=id,
        status_localidade=['Mobilizado'],
        status_unidade=['Mobilizado'],
        delimiter="&",
        localidade_id=localidade_id
    ).verify_login_type_and_return_objects()

    if request.method == 'POST':
        form = LocalidadeForms(request.POST, instance=localidade)
        if form.is_valid():
            form.save()

            messages.success(request, f"Localidade {form.cleaned_data['nome']} editada com sucesso")
            return redirect('localidades', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/unidades/localidades/editar_localidade.html',
                  {'localidade_form': localidade_form, 'localidade_id': localidade_id})

def desmobilizar_localidade(request, login_type, localidade_id, id, desm):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    alterar_status(
        request=request,
        model=Localidade,
        object_id=localidade_id,
        desm=desm
    )

    return redirect('localidades', login_type, id)

def localidades_desmobilizadas(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    dados_localidades, localidade_form, unidade, localidade = DadosLocalidadesAndFormulario(
        login_type = login_type,
        id = id,
        status_localidade = ["Desmobilizado", "Desmobilizacao Permanente"],
        status_unidade = ["Desmobilizado"],
        delimiter="|"
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(
        request=request,
        data_objects=dados_localidades
    )

    return render(request, 'controle/unidades/localidades/localidades_desmobilizadas.html', {
        'localidade_form': localidade_form,
        'elementos_paginados': elementos_paginados})

def reabilitar_localidade(request, login_type, localidade_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    alterar_status(
        request=request,
        model=Localidade,
        object_id=localidade_id
    )

    return redirect('localidades_desmobilizadas', login_type, id)

