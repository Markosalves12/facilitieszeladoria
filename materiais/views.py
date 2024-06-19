from django.shortcuts import render, redirect
from materiais.models import Materiais
from materiais.forms import MaterialForms
from utils.utils import paginate
from utils.utils import block_view
from django.contrib import messages
from materiais.utils import DadosMateriaisAndFormulario
from utils.utils import alterar_status

# Create your views here.
def materiais(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa, dados_materiais, material_form, material = DadosMateriaisAndFormulario(
        login_type=login_type, id=id, status_material=['Mobilizado']
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_materiais)

    if request.method == 'POST':
        form = MaterialForms(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, f"Material {form.cleaned_data['material']} criado com sucesso")
            return redirect('materiais', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/materiais/materiais.html',
                  {'elementos_paginados': elementos_paginados,
                   'material_form': material_form,
                   'empresa': empresa})

def editar_material(request, login_type, material_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    unidade, dados_materiais, material_form, material = DadosMateriaisAndFormulario(
        login_type=login_type, id=id, status_material=['Mobilizado'], material_id=material_id
    ).verify_login_type_and_return_objects()


    if request.method == 'POST':
        form = MaterialForms(request.POST, instance=material)
        if form.is_valid():
            form.save()

            messages.success(request, f"Material {form.cleaned_data['material']} editado com sucesso")
            return redirect('materiais', login_type, id)
        messages.error(request, f"Algo deu errado")

    return render(request, 'controle/materiais/editar_material.html',
                  {'material_form': material_form, 'material_id': material_id})

def desmobilizar_material(request, login_type, material_id, id, desm):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    alterar_status(request=request, model=Materiais, object_id=material_id, desm=desm)

    return redirect('materiais', login_type, id)

def materiais_desmobilizados(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    empresa, dados_materiais, material_form, material = DadosMateriaisAndFormulario(
        login_type=login_type, id=id, status_material=['Desmobilizado', 'Desmobilizacao Permanente'],
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(request=request, data_objects=dados_materiais)

    return render(request, 'controle/materiais/materiais_desmobilizados.html',
                  {'elementos_paginados': elementos_paginados,
                   'empresa': empresa})

def reabilitar_material(request, login_type, material_id, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    alterar_status(request=request, model=Materiais, object_id=material_id)

    return redirect('materiais_desmobilizados', login_type, id)