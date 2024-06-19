from django.shortcuts import render, redirect
from gerente.models import Gerente
from gerente.forms import GerenteForms
from utils.utils import paginate
from utils.utils import block_view
from django.contrib import messages
from utils.utils import alterar_status
from gerente.utils import DadosGerentesAndFormulario

# Create your views here.
def gerentes(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa, dados_gerentes, gerente_form, gerente = DadosGerentesAndFormulario(
        login_type=login_type,
        id=id,
        status_gerente=['Mobilizado'],
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_gerentes)


    if request.method == 'POST':
        form = GerenteForms(request.POST)
        if form.is_valid():
            # if '@suzano.com' not in form.cleaned_data['email']:
            #     messages.error(request, f"Insira um email suzano")
            #     return redirect('gerentes', login_type, id)
            try:
                form.save()
            except:
                messages.error(request, 'Servidor SMTP não respondeu, acione o administrador para criar gerente manualmente')
                return redirect('gerentes', login_type, id)

            messages.success(request, f"Gerente {form.cleaned_data['nome']} criado(a) com sucesso")
            return redirect('gerentes', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/gerentes/gerentes.html', {
        'gerente_form': gerente_form,
        'elementos_paginados': elementos_paginados
    })

def editar_gerente(request, login_type, gerente_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa, dados_gerentes, gerente_form, gerente = DadosGerentesAndFormulario(
        login_type=login_type,
        id=id,
        status_gerente=['Mobilizado'],
        gerente_id=gerente_id
    ).verify_login_type_and_return_objects()

    if request.method == 'POST':
        form = GerenteForms(request.POST, instance=gerente)
        if form.is_valid():
            # if '@suzano.com' not in form.instance.email:
            #     messages.error(request, f"Insira um email suzano")
            #     return redirect('gerentes', login_type, id)

            form.save()
            messages.success(request, f"Gerente {form.cleaned_data['nome']} editado(a) com sucesso")
            return redirect('gerentes', login_type, id)
        messages.error(request, f"Algo deu errado")

    return render(request, 'controle/gerentes/editar_gerente.html',
                  {'gerente_form': gerente_form, 'gerente_id': gerente_id})

def gerentes_desmobilizados(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa, dados_gerentes, gerente_form, gerente = DadosGerentesAndFormulario(
        login_type=login_type,
        id=id,
        status_gerente=['Desmobilizado', 'Desmobilizacao Permanente'],
    ).verify_login_type_and_return_objects()


    elementos_paginados = paginate(request=request, data_objects=dados_gerentes)

    return render(request, 'controle/gerentes/gerentes_desmobilizados.html', {
        'gerente_form': gerente_form,
        'elementos_paginados': elementos_paginados
    })

def desmobilizar_gerente(request, login_type, gerente_id, id, desm):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    alterar_status(request=request, model=Gerente, object_id=gerente_id, desm=desm)

    return redirect('gerentes', login_type, id)

def reabilitar_gerente(request, login_type, gerente_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    alterar_status(request=request, model=Gerente, object_id=gerente_id)

    return redirect('gerentes_desmobilizados', login_type, id)