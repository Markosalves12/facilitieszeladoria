from django.shortcuts import render, redirect
from django.db.models import F, Q, ExpressionWrapper, IntegerField, DurationField
from django.db.models.functions import Now, TruncDate
from servico.forms import ServicosForms, FatoServicoForm
from servico.models import Servicos, FatoServico
from catalogoservico.models import CatalogoServicos
from catalogoservico.forms import CatalogoServicosForms
from servico.utils import DadosCatalogoServicosAndFormulario
from utils.utils import paginate
from colaborador.models import Colaborador
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
from utils.utils import block_view, alterar_status, capturate_paramns, formatar_atributos
from send_password.send_password import (SendNotificationNewServiceToColaborador,
                                         SendNotificationServiceCanceled)

# Create your views here.

# view dedicada ao colaborador
# para que o mesmo veja e edite seus ultimos serviços prestados
# OBS: login de colaborador esta desabilitado
def servicos_concluidos(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        dados = Servicos.objects.filter(
            Q(colaboradores_escalados__id=id) &
            ~Q(status__in=['Agendado', 'Em andamento'])
        ).order_by('-data_inicio')[:10]

    else:
        dados = Servicos.objects.filter(
            Q(colaboradores_escalados__gerente__id=id) &
            ~Q(status__in=['Agendado', 'Em andamento'])
        ).order_by('-data_inicio')[:30]

    return render(request, 'servicos/servicos_concluidos.html', {'dados': dados})

# view dedicada ao colaborador ve os ultimos agendamentos em seu nome
# OBS: login de colaborador esta desabilitado
def servicos_agendados(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    # bloco de códigos, reservado para identificar o status do agendamento
    # agendado
    # proximo
    # atrasado
    if login_type == 'Colaborador':
        dados = Servicos.objects.annotate(
            data_atual=TruncDate(Now()),
            status_agendamento=ExpressionWrapper(
                F('data_inicio') - F('data_atual'),
                output_field=IntegerField()
            ) / (3600 * 24 * 1000000)
        ).filter(
            Q(colaboradores_escalados__id=id)
        ).exclude(
            # excui se os servicos concluidos ou cancelados
            status__in=['Cancelado', 'Concluido']
        )
    # bloco de códigos, reservado para identificar o status do agendamento
    # agendado
    # proximo
    # atrasado
    else:
        dados = Servicos.objects.annotate(
            data_atual=TruncDate(Now()),
            status_agendamento=ExpressionWrapper(
                F('data_inicio') - F('data_atual'),
                output_field=IntegerField()
            ) / (3600 * 24 * 1000000)
        ).filter(
            Q(colaboradores_escalados__gerente__id=id)
        ).exclude(
            status__in=['Cancelado', 'Concluido']
        )

    # Contagem total de linhas da tabela
    agendamentos = dados.filter(status='Agendado').count()

    # Contagem de linhas da tabela com status "Em andamento"
    em_andamento = dados.filter(status='Em andamento').count()

    # Contagem de linhas da tabela onde a data atual é maior que data_inicio
    atrasados = dados.filter(data_inicio__lt=timezone.datetime.now().date()).count()

    # Contagem de linhas da tabela onde a diferença entre data_inicio e data_atual é menor ou igual a 21 dias
    proximos = dados.filter(
        data_inicio__lte=F('data_atual') + timedelta(days=7)
    ).exclude(
        status="Em andamento"
    ).count()

    return render(request, 'servicos/servicos_agendados.html',
                  {'dados': dados,
                   'agendamentos': agendamentos,
                   'em_andamento': em_andamento,
                   'atrasados': atrasados,
                   'proximos': proximos})

# view dedicada para o colaborador preencher os serviços agendados para ele mesmo
def iniciar_servico(request, servico_id, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == "Administrador":
        return redirect('servicos', login_type, id)

    elif login_type == "Gestor":
        return redirect('servicos', login_type, id)

    elif login_type == "Gerente":
        return redirect('servicos', login_type, id)


    elif login_type == "Colaborador":
        colaborador = Colaborador.objects.get(id=id)
        gerente = colaborador.gerente
        servico_agendado = Servicos.objects.get(id=servico_id)
        servico_agendado_form = FatoServicoForm(gerente_id=gerente.id)


    if request.method == 'POST':
        form = FatoServicoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['servico'].id)
            servico = Servicos.objects.get(id=form.cleaned_data['servico'].id)
            servico.status = "Em andamento"
            servico.save()
            form.save()

            return redirect('servicos_agendados', login_type, id)

        if login_type == 'Colaborador':
            return redirect('servicos_agendados', id)

        return redirect('servicos')

    return render(request, 'servicos/iniciar_servico.html',
                  {'servico_agendado_form': servico_agendado_form,
                          'servico_agendado': servico_agendado,
                          'servico_id': servico_id})


# catalogo de serviços q a empresa presta na unidade
def catalogo_de_servicos(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    empresa, dados_catalogo_servicos, catalogo_servicos_form, servico_catalogo = DadosCatalogoServicosAndFormulario(
        login_type=login_type,
        id=id,
        status_servico=['Mobilizado']
    ).verify_login_type_and_return_objects()

    elementos_paginados = paginate(
        request=request,
        data_objects=dados_catalogo_servicos,
        per_page=5
    )

    if request.method == 'POST':
        form = CatalogoServicosForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Serviço {form.cleaned_data['servico']} criado com sucesso")
            return redirect('catalogo_de_servicos', login_type, id)

        messages.error(request, "Algo deu errado")

    return render(request, 'controle/servicos/catalogo/catalogo_de_servicos.html', {
        'elementos_paginados': elementos_paginados,
        'catalogo_servicos_form': catalogo_servicos_form,
        'empresa': empresa
    })

def editar_catalogo_de_servicos(request, login_type, servico_catalogo_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    unidade, dados_catalogo_servicos, catalogo_servicos_form, servico_catalogo = DadosCatalogoServicosAndFormulario(
        login_type=login_type,
        id=id,
        status_servico=['Desmobilizado', 'Desmobilizacao Permanente'],
        servico_catalogo_id=servico_catalogo_id
    ).verify_login_type_and_return_objects()

    if request.method == 'POST':
        form = CatalogoServicosForms(request.POST, instance=servico_catalogo)
        if form.is_valid():
            form.save()
            messages.success(request, f"Serviço {form.cleaned_data['servico']} editado com sucesso")
            return redirect('catalogo_de_servicos', login_type, id)

    return render(request, 'controle/servicos/catalogo/editar_catalogo_de_servicos.html',
                  {'catalogo_servicos_form': catalogo_servicos_form,
                   'servico_catalogo_id': servico_catalogo_id,
                   'servico_catalogo': servico_catalogo})

def desmobilizar_servico_do_catalogo(request, login_type, servico_catalogo_id, id, desm):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    alterar_status(request=request, model=CatalogoServicos, object_id=servico_catalogo_id, desm=desm)

    return redirect('catalogo_de_servicos', login_type, id)

def catalogo_de_servicos_desmobilizados(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    unidade, dados_catalogo_servicos, catalogo_servicos_form, servico_catalogo = DadosCatalogoServicosAndFormulario(
        login_type=login_type,
        id=id,
        status_servico=['Desmobilizado', 'Desmobilizacao Permanente']
    ).verify_login_type_and_return_objects()

    return render(request, 'controle/servicos/catalogo/catalogo_de_servicos_desmobilizados.html', {
        'dados_catalogo_servicos': dados_catalogo_servicos,
        'unidade': unidade
    })

def reabilitar_servico_do_catalogo(request, login_type, servico_catalogo_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    alterar_status(request=request, model=CatalogoServicos, object_id=servico_catalogo_id)


    return redirect('catalogo_de_servicos_desmobilizados', login_type, id)

def servicos(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    empresa = capturate_paramns(login_type=login_type, id=id, type='empresa')

    if login_type == 'Colaborador':
        filter_query = Q(colaboradores_escalados__id_random=id)

    elif login_type == 'Gerente':
        filter_query = Q(colaboradores_escalados__gerente__id_random=id)

    elif login_type == 'Gestor':
        filter_query = Q(colaboradores_escalados__gerente__gestor__id_random=id)

    else:
        filter_query = Q()


    # Filtrar e anotar os dados de serviços
    dados_servicos = (
        Servicos.objects.filter(status__in=['Agendado', 'Em andamento'])
        .annotate(
            data_atual=TruncDate(Now()),
            status_agendamento=ExpressionWrapper(
                F('data_inicio') - F('data_atual'),
                output_field=IntegerField()
            ) / (3600 * 24 * 1000000)
        )
        .filter(filter_query)
        .order_by('-data_inicio')
        .distinct()
    )

    # Contagem total de linhas da tabela
    agendamentos = dados_servicos.filter(status='Agendado').count()

    # Contagem de linhas da tabela com status "Em andamento"
    em_andamento = dados_servicos.filter(status='Em andamento').count()

    # Contagem de linhas da tabela onde a data atual é maior que data_inicio
    atrasados = dados_servicos.filter(data_inicio__lt=timezone.now().date()).count()

    # Contagem de linhas da tabela onde a diferença entre data_inicio e data_atual é menor ou igual a 21 dias
    one_day = ExpressionWrapper(F('data_atual') + timedelta(days=1), output_field=DurationField())
    seven_days = ExpressionWrapper(F('data_atual') + timedelta(days=7), output_field=DurationField())

    # Usar as expressões para filtrar os dados
    proximos = dados_servicos.filter(
        data_inicio__gte=one_day,
        data_inicio__lte=seven_days
    ).exclude(
        status="Em andamento"
    ).count()


    elementos_paginados = paginate(
        request=request,
        data_objects=dados_servicos,
        per_page=10
    )

    return render(request, 'controle/servicos/servicos/servicos.html',
                  {
                   'elementos_paginados': elementos_paginados,
                   'agendamentos': agendamentos,
                   'em_andamento': em_andamento,
                   'atrasados': atrasados,
                   'proximos': proximos,
                   'empresa': empresa
                   })

def solicitar_servico(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    unidade = capturate_paramns(login_type=login_type, id=id)
    empresa = capturate_paramns(login_type=login_type, id=id, type="empresa")

    if login_type == "Administrador":
        # unidade = capturate_paramns(login_type=login_type, id=id)
        servicos_forms = ServicosForms()

    elif login_type == 'Gestor':
        # unidade = capturate_paramns(login_type=login_type, id=id)
        # empresa = capturate_paramns(login_type=login_type, id=id, type="empresa")
        servicos_forms = ServicosForms(
            login_type=login_type,
            id_random=id,
            unidade=unidade,
            empresa=empresa
        )

    elif login_type == 'Gerente':
        servicos_forms = ServicosForms(
            id_random=id,
            unidade=unidade,
            login_type=login_type,
            empresa=empresa
        )

    elif login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)


    if request.method == 'POST':
        form = ServicosForms(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            colaboradores_escalados = form.cleaned_data['colaboradores_escalados']
            data_inicio = form.cleaned_data['data_inicio']
            # caso o campo de email co colaborador esteja preenchido
            # é disparado uma notificação com o agendamento
            for colaborador in colaboradores_escalados:
                # if Servicos.objects.filter(colaboradores_escalados__id_random=colaborador.id_random, data_inicio=data_inicio, status='Agendado'):
                #     messages.error(request, f'Já existe um serviços para {colaborador} em {data_inicio}')
                #     return redirect(solicitar_servico, login_type, id)

                email = Colaborador.objects.get(
                    id_random=colaborador.id_random
                ).email

                nome = Colaborador.objects.get(
                    nome=colaborador
                ).nome

                servicos = list()
                servicos_escalados = form.cleaned_data['servicos_escalados']
                for servico_cat in servicos_escalados:
                    servicos.append(
                        CatalogoServicos.objects.get(
                            id_random=servico_cat.id_random
                        ).servico
                    )
                try:
                    if email is not None:
                        SendNotificationNewServiceToColaborador(para=email, area=form.cleaned_data['area'].nome,
                                                                colaborador_nome=nome,
                                                                area_total=form.cleaned_data['area'].area,
                                                                localidade=form.cleaned_data['area'].unidade_jardim,
                                                                servicos=', '.join(servicos),
                                                                data_inicio=form.cleaned_data['data_inicio'],
                                                                descricao=form.cleaned_data['descricao_servico'],
                                                                ).send_email()
                        messages.success(request, f"Notificação de serviço enviada para {colaborador}")
                    else:
                        messages.error(request,  f"{colaborador} não tem email cadastrado")
                except:
                    messages.error(request, f"Algo deu errado")

            form.save()
            messages.success(request, f"Serviços agendado com sucesso")
            return redirect('servicos', login_type, id)
        messages.error(request, "Algo deu errado")


    return render(request, 'controle/servicos/servicos/solicitar_servico.html',
                  {
                      'servicos_forms': servicos_forms,
                      'unidade': unidade
                  })

def editar_servico_agendado(request, login_type, servico_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )
    if block == True:
        return redirect('logout')


    if login_type == "Administrador":
        unidade = ''
        servico_agendado = Servicos.objects.get(
            id_random=servico_id
        )
        servico_agendado_form = ServicosForms(
            instance=servico_agendado
        )


    elif login_type == "Colaborador":
        return redirect('servicos_agendados', login_type, id)


    elif login_type == "Gestor" or login_type == "Gerente":
        unidade = capturate_paramns(
            login_type=login_type,
            id=id
        )
        empresa = capturate_paramns(
            login_type=login_type,
            id=id,
            type='empresa'
        )

        servico_agendado = Servicos.objects.get(
            id_random=servico_id
        )
        servico_agendado_form = ServicosForms(
            instance=servico_agendado,
            login_type=login_type,
            id_random=id,
            unidade=unidade,
            empresa=empresa,
        )

    if request.method == 'POST':
        form = ServicosForms(
            request.POST,
            request.FILES,
            instance=servico_agendado
        )

        if form.is_valid():
            try:
                form.save()
                messages.success(request, f"Serviços {form.cleaned_data['descricao_servico']} editado com sucesso")

            except:
                pass

            return redirect('servicos', login_type, id)
        messages.error(request, "Algo deu errado")

    return render(request, 'controle/servicos/servicos/editar_servico_agendado.html',
                  {'servico_agendado_form': servico_agendado_form,
                   'servico_id': servico_id,
                   'servico_agendado': servico_agendado})

def cancelar_servico_agendado(request, login_type, servico_id, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    servico_agendado = Servicos.objects.get(
        id_random=servico_id
    )
    servico_agendado.status = "Cancelado"

    colaboradores_escalados = servico_agendado.colaboradores_escalados.all()
    for colaborador in colaboradores_escalados:
        email = Colaborador.objects.get(
            nome=colaborador
        ).email

        nome = Colaborador.objects.get(
            nome=colaborador
        ).nome

        # servicos = list()
        # servicos_escalados = servico_agendado.servicos_escalados.all()
        # for servico in servicos_escalados:
        #     servicos.append(CatalogoServicos.objects.get(servico=servico).servico)

        servicos = formatar_atributos(
            queryset=servico_agendado.servicos_escalados.all(),
            atributo='servico'
        )
        try:
            if email is not None:
                SendNotificationServiceCanceled(para=email, area=servico_agendado.area.nome,
                                                        colaborador_nome=nome,
                                                        area_total=servico_agendado.area.area,
                                                        localidade=servico_agendado.area.unidade_jardim,
                                                        servicos=servicos,
                                                        data_inicio=servico_agendado.data_inicio,
                                                        descricao=servico_agendado.descricao_servico,
                                                        ).send_email()
                messages.success(request, f"Notificação de cancelamento enviada para {colaborador}")
            else:
                messages.error(request,  f"{colaborador} não tem email cadastrado")
        except:
            messages.error(f"Algo deu errado")

    messages.success(request, f"Serviço cancelado com sucesso")
    servico_agendado.save()

    return redirect('servicos', login_type, id)


######################################

# função não está em uso

# def servicos_em_andamento(request, login_type, id):
#     block = block_view(request, login_type=login_type, id=id)
#     if block == True:
#         return redirect('logout')
#
#     servicos_em_andamentos = FatoServico.objects.all()
#     servicos_em_andamento_form = FatoServicoForm()
#
#     if request.method == 'POST':
#         form = FatoServicoForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#     return render(request, 'controle/servicos/servicos/servicos_em_andamentos.html',
#                   {'servicos_em_andamentos': servicos_em_andamentos,
#                    'servicos_em_andamento_form': servicos_em_andamento_form})

#########################################################

def execucao_de_servicos(request, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    servicos_em_andamento = FatoServico.objects.annotate(
        tempo_na_area = ExpressionWrapper(
            F('data_hora_retorno_area')-F('data_hora_chegada_na_area'),
            output_field=DurationField()
        ),
    ).filter(
        Q(servico__status="Em andamento") &
        (
                Q(servico__colaboradores_escalados__gerente__id_random=id) |
                Q(servico__colaboradores_escalados__gerente__gestor__id_random=id)
        )
    ).distinct(

    )

    elementos_paginados = paginate(
        request=request,
        data_objects=servicos_em_andamento,
        per_page=10
    )

    return render(request, 'controle/servicos/servicos/execucao_de_servicos.html',
                  {'elementos_paginados': elementos_paginados})

def executar_servico(request, login_type, id):
    block = block_view(request, login_type=login_type, id=id)
    if block == True:
        return redirect('logout')

    if login_type == 'Administrador':
        servicos_form = FatoServicoForm(

        )

    elif login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    else:
        empresa = capturate_paramns(login_type=login_type, id=id, type='empresa')
        servicos_form = FatoServicoForm(
            id=id,
            login_type=login_type,
            empresa=empresa
        )

    if request.method == 'POST':
        form = FatoServicoForm(request.POST)
        if form.is_valid():
            servico = Servicos.objects.get(
                id_random=form.cleaned_data['servico'].id_random
            )
            # na execucao do servico o servicos e identificado automaticamente como
            # em andamento
            servico.status = "Em andamento"
            servico.save()
            form.save()

            messages.success(request, f"Serviços realizado com sucesso")
            return redirect('execucao_de_servicos', login_type, id)
        messages.error(request, f"Algo deu errado")


    return render(request, 'controle/servicos/servicos/executar_servico.html',
                  {'servicos_form': servicos_form})


# função que altera o status do serviços para 'Concluido'
def concluir_servico(request, servico_id, login_type, id):
    block = block_view(
        request,
        login_type=login_type,
        id=id
    )

    if block == True:
        return redirect('logout')

    if login_type == 'Colaborador':
        return redirect('servicos_agendados', login_type, id)

    # captura o objeto que vai ser modificado
    servico_agendado = Servicos.objects.get(
        id_random=servico_id
    )
    # na conclusão do serviço, o campo data_conclusao é preenchido com data atual do sistema
    servico_agendado.status = "Concluido"
    servico_agendado.data_conclusao = timezone.now().date()
    servico_agendado.save()

    messages.success(request, f"Serviço finalizado com sucesso")
    return redirect('servicos', login_type, id)