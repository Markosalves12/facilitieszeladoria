from django.shortcuts import render, redirect
from gestor.models import Gestor
from gestor.forms import GestorForms
from utils.utils import paginate
from utils.utils import block_view
from django.contrib import messages
from utils.utils import alterar_status
from gestor.utils import DadosGestoresAndFormulario

# Create your views here.
def gestores(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa, dados_gestores, gestor_form, gestor = DadosGestoresAndFormulario(
        login_type=login_type,
        id=id,
        status_gestor=['Mobilizado'],
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_gestores)

    if request.method == 'POST':
        form = GestorForms(request.POST)
        if form.is_valid():
            if '@suzano.com' not in form.cleaned_data['email']:
                messages.error(request, f"Insira um email suzano")
                return redirect('gestores', login_type, id)

            try:
                form.save()
            except:
                messages.error(request, 'Servidor SMTP não respondeu, acione o administrador para criar um(a) gestor(a) manualmente')
                return redirect('gestores', login_type, id)

            messages.success(request, f"Gestor {form.cleaned_data['nome'].strip().capitalize()} criado com sucesso")
            return redirect('gestores', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/gestores/gestores.html', {
        'gestor_form': gestor_form,
        'elementos_paginados': elementos_paginados})

def editar_gestor(request, login_type, gestor_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    empresa, dados_gestores, gestor_form, gestor = DadosGestoresAndFormulario(
        login_type=login_type,
        id=id,
        status_gestor=['Mobilizado'],
        gestor_id=gestor_id
    ).verify_login_type_and_return_objects()

    if request.method == 'POST':
        form = GestorForms(request.POST, instance=gestor)
        if form.is_valid():
            if '@suzano.com' not in form.instance.email:
                messages.error(request, f"Insira um email suzano")
                return redirect('gestores', login_type, id)

            form.save()
            messages.success(request, f"Gestor {form.cleaned_data['nome']} editado com sucesso")
            return redirect('gestores', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/gestores/editar_gestor.html',
                  {'gestor_form': gestor_form, 'gestor_id': gestor_id})

def desmobilizar_gestor(request, login_type, gestor_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    alterar_status(request=request, model=Gestor, object_id=gestor_id, desm='temp')

    return redirect('gestores', login_type, id)

def gestores_desmobilizados(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    dados_gestores = Gestor.objects.filter(status='Desmobilizado')
    gestor_form = GestorForms()

    elementos_paginados = paginate(request=request, data_objects=dados_gestores)

    return render(request, 'controle/gestores/gestores_desmobilizados.html', {
        'gestor_form': gestor_form,
        'elementos_paginados': elementos_paginados})

def reabilitar_gestor(request, login_type, gestor_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    alterar_status(
        request=request,
        model=Gestor,
        object_id=gestor_id
    )

    return redirect('gestores_desmobilizados', login_type, id)
