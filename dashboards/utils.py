from servico.models import FatoServico
from equipamento.models import ManutencaoEquipamentos
from ferramenta.models import ManutencaoFerramentas
from django.db.models import (ExpressionWrapper, F, CharField,
                              IntegerField, DurationField, DateField, DateTimeField
                              )

def colect_dados():
    # Adicione os dados do relatório ao arquivo Excel
    dados = FatoServico.objects.annotate(
        tipodeempresa=ExpressionWrapper(
            F('servico__colaboradores_escalados__gerente__gestor__empresa__tipo_empresa'),
            output_field=CharField()
        ),
        empresaprestadora=ExpressionWrapper(
            F('servico__colaboradores_escalados__gerente__gestor__empresa__nome'),
            output_field=CharField()
        ),
        id_agendamento = ExpressionWrapper(
            F('servico__id'),
            output_field=CharField()
        ),
        tipo_agendamento=ExpressionWrapper(
            F('servico__tipo_servico'),
            output_field=CharField()
        ),
        descricao_do_servico=ExpressionWrapper(
            F('servico__descricao_servico'),
            output_field=CharField()
        ),
        colaboradores_chamados = ExpressionWrapper(
            F('servico__colaboradores_escalados__nome'),
            output_field=CharField()
        ),
        servicos_solicitados=ExpressionWrapper(
            F('servico__servicos_escalados__servico'),
            output_field=CharField()
        ),
        data_de_inicio = ExpressionWrapper(
            F('servico__data_inicio'),
            output_field=CharField()
        ),
        data_de_conclusao=ExpressionWrapper(
            F('servico__data_conclusao'),
            output_field=CharField()
        ),
        antes=ExpressionWrapper(
            F('servico__foto_inicio'),
            output_field=CharField()
        ),
        depois=ExpressionWrapper(
            F('servico__foto'),
            output_field=CharField()
        ),
        equipamento_marca = ExpressionWrapper(
            F('equipamentos_usados__catalogo_equipamento__marca'),
            output_field=CharField()
        ),
        equipamento_catalogo=ExpressionWrapper(
            F('equipamentos_usados__catalogo_equipamento__nome'),
            output_field=CharField()
        ),
        equipamento_empresa = ExpressionWrapper(
            F('equipamentos_usados__empresa__nome'),
            output_field=CharField()
        ),
        tipo_equipamento = ExpressionWrapper(
            F('equipamentos_usados__tipo'),
            output_field=CharField()
        ),
        equipamento_id = ExpressionWrapper(
            F('equipamentos_usados__id'),
            output_field=CharField()
        ),
        vida_util_equipamento = ExpressionWrapper(
            F('equipamentos_usados__catalogo_equipamento__vida_util_meses'),
            output_field=IntegerField()
        ),
        data_aquisicao_equipamento=ExpressionWrapper(
            F('equipamentos_usados__data_aquisicao'),
            output_field=DateField()
        ),
        data_desmobilizacao_equipamento=ExpressionWrapper(
            F('equipamentos_usados__data_desmobilizacao'),
            output_field=DateField()
        ),
        matricula_equipamento=ExpressionWrapper(
            F('equipamentos_usados__matricula'),
            output_field=CharField()
        ),
        ferramenta_marca=ExpressionWrapper(
            F('ferramentas_usados__catalogo_ferramenta__marca'),
            output_field=CharField()
        ),
        ferramenta_catalogo=ExpressionWrapper(
            F('ferramentas_usados__catalogo_ferramenta__nome'),
            output_field=CharField()
        ),
        ferramenta_empresa=ExpressionWrapper(
            F('ferramentas_usados__empresa__nome'),
            output_field=CharField()
        ),
        tipo_ferramenta=ExpressionWrapper(
            F('ferramentas_usados__tipo'),
            output_field=CharField()
        ),
        ferramenta_id=ExpressionWrapper(
            F('ferramentas_usados__id'),
            output_field=CharField()
        ),
        vida_util_ferramenta=ExpressionWrapper(
            F('ferramentas_usados__catalogo_ferramenta__vida_util_meses'),
            output_field=IntegerField()
        ),
        data_aquisicao_ferramenta=ExpressionWrapper(
            F('ferramentas_usados__data_aquisicao'),
            output_field=DateField()
        ),
        data_desmobilizacao_ferramenta=ExpressionWrapper(
            F('ferramentas_usados__data_desmobilizacao'),
            output_field=DateField()
        ),
        matricula_ferramenta=ExpressionWrapper(
            F('ferramentas_usados__matricula'),
            output_field=CharField()
        ),
        status_servico = ExpressionWrapper(
            F('servico__status'),
            output_field=CharField()
        ),
        material_aplicado =  ExpressionWrapper(
            F('material_usado__material'),
            output_field=CharField()
        ),
        material_categoria=ExpressionWrapper(
            F('material_usado__categoria'),
            output_field=CharField()
        ),
        forma_consumo = ExpressionWrapper(
            F('material_usado__consumo'),
            output_field=CharField()
        ),
        qtd = ExpressionWrapper(
            F('quantidade'),
            output_field=IntegerField(),
        ),
        tipo_material=ExpressionWrapper(
            F('tipo'),
            output_field=CharField(),
        ),
        area_atendida = ExpressionWrapper(
            F('servico__area__nome'),
            output_field=CharField()
        ),
        periodicidade_de_retorno=ExpressionWrapper(
            F('servico__area__periodicidade'),
            output_field=CharField()
        ),
        area_total = ExpressionWrapper(
            F('servico__area__area'),
            output_field=CharField()
        ),
        tipo_vegetacao = ExpressionWrapper(
            F('servico__area__vegetacao'),
            output_field=CharField()
        ),
        tipo_terreno=ExpressionWrapper(
            F('servico__area__terreno'),
            output_field=CharField()
        ),
        localidade=ExpressionWrapper(
            F('servico__area__unidade_jardim__nome'),
            output_field=CharField()
        ),
        tiponegocio=ExpressionWrapper(
            F('servico__area__unidade_jardim__negocio'),
            output_field=CharField()
        ),
        unidade=ExpressionWrapper(
            F('servico__area__unidade_jardim__unidadeoriginial__unidade'),
            output_field=CharField()
        ),
        id_servico=ExpressionWrapper(
            F('id'),
            output_field=IntegerField()
        ),
        tempo_na_area = ExpressionWrapper(
                F('data_hora_retorno_area')-F('data_hora_chegada_na_area'),
                output_field=DurationField()
        ),
        colaborador_envolvido = ExpressionWrapper(
            F('colaborador__nome'),
            output_field=CharField()
        ),
        principalservico=ExpressionWrapper(
            F('servico_aplicado__servico'),
            output_field=CharField()
        ),
        data_hora_chegada = ExpressionWrapper(
            F('data_hora_chegada_na_area'),
            output_field=DateTimeField()
        ),
        data_hora_retorno = ExpressionWrapper(
            F('data_hora_retorno_area'),
            output_field=DateTimeField()
        ),
    ).filter(
        status_servico = "Concluido"
    )

    return dados

def colect_dados_manutencao_equipamentos():
    dados = ManutencaoEquipamentos.objects.annotate(
        id_equipamento=ExpressionWrapper(
            F('id'),
            output_field=IntegerField()
        ),
        data_inicio=ExpressionWrapper(
            F('data_hora_inicio'),
            output_field=DateField()
        ),
        data_fim=ExpressionWrapper(
            F('data_hora_fim'),
            output_field=DateField()
        ),
        equipamento_=ExpressionWrapper(
            F('equipamento__catalogo_equipamento__nome'),
            output_field=CharField()
        ),
        matricula_equipamento=ExpressionWrapper(
            F('equipamento__matricula'),
            output_field=CharField()
        ),
        equipamento_marca=ExpressionWrapper(
            F('equipamento__catalogo_equipamento__marca'),
            output_field=CharField()
        ),
        tipomanutencao=ExpressionWrapper(
            F('tipo_manutencao'),
            output_field=CharField()
        ),
        tempo_em_manutencao=ExpressionWrapper(
            (F('data_hora_fim') - F('data_hora_inicio')),
            output_field=DurationField()
        ),
        tipo_equipameanto=ExpressionWrapper(
            F('equipamento__tipo'),
            output_field=CharField()
        ),
        unidade=ExpressionWrapper(
            F('equipamento__empresa__unidade__unidade'),
            output_field=CharField()
        ),
        empresa=ExpressionWrapper(
            F('equipamento__empresa__nome'),
            output_field=CharField()
        ),
        tipoempresa=ExpressionWrapper(
            F('equipamento__empresa__tipo_empresa'),
            output_field=CharField()
        ),
    )

    return dados

def colect_dados_manutencao_ferramentas():
    dados = ManutencaoFerramentas.objects.annotate(
        id_ferramenta=ExpressionWrapper(
            F('id'),
            output_field=IntegerField()
        ),
        data_inicio=ExpressionWrapper(
            F('data_hora_inicio'),
            output_field=DateField()
        ),
        data_fim=ExpressionWrapper(
            F('data_hora_fim'),
            output_field=DateField()
        ),
        ferramenta_=ExpressionWrapper(
            F('ferramenta__catalogo_ferramenta__nome'),
            output_field=CharField()
        ),
        matricula_ferramenta=ExpressionWrapper(
            F('ferramenta__matricula'),
            output_field=CharField()
        ),
        ferramenta_marca=ExpressionWrapper(
            F('ferramenta__catalogo_ferramenta__marca'),
            output_field=CharField()
        ),
        tipomanutencao=ExpressionWrapper(
            F('tipo_manutencao'),
            output_field=CharField()
        ),
        tempo_em_manutencao=ExpressionWrapper(
            (F('data_hora_fim') - F('data_hora_inicio')),
            output_field=DurationField()
        ),
        tipo_ferramenta=ExpressionWrapper(
            F('ferramenta__tipo'),
            output_field=CharField()
        ),
        unidade=ExpressionWrapper(
            F('ferramenta__empresa__unidade__unidade'),
            output_field=CharField()
        ),
        empresa=ExpressionWrapper(
            F('ferramenta__empresa__nome'),
            output_field=CharField()
        ),
    )

    return dados

def colect_dados_planejamento():
    # Adicione os dados do relatório ao arquivo Excel
    dados = FatoServico.objects.annotate(
        tipodeempresa=ExpressionWrapper(
            F('servico__colaboradores_escalados__gerente__gestor__empresa__tipo_empresa'),
            output_field=CharField()
        ),
        empresaprestadora=ExpressionWrapper(
            F('servico__colaboradores_escalados__gerente__gestor__empresa__nome'),
            output_field=CharField()
        ),
        id_agendamento = ExpressionWrapper(
            F('servico__id'),
            output_field=CharField()
        ),
        tipo_agendamento=ExpressionWrapper(
            F('servico__tipo_servico'),
            output_field=CharField()
        ),
        descricao_do_servico=ExpressionWrapper(
            F('servico__descricao_servico'),
            output_field=CharField()
        ),
        colaboradores_chamados = ExpressionWrapper(
            F('servico__colaboradores_escalados__nome'),
            output_field=CharField()
        ),
        servicos_solicitados=ExpressionWrapper(
            F('servico__servicos_escalados__servico'),
            output_field=CharField()
        ),
        data_de_inicio = ExpressionWrapper(
            F('servico__data_inicio'),
            output_field=CharField()
        ),
        status_servico = ExpressionWrapper(
            F('servico__status'),
            output_field=CharField()
        ),
        area_atendida = ExpressionWrapper(
            F('servico__area__nome'),
            output_field=CharField()
        ),
        periodicidade_de_retorno=ExpressionWrapper(
            F('servico__area__periodicidade'),
            output_field=CharField()
        ),
        area_total = ExpressionWrapper(
            F('servico__area__area'),
            output_field=CharField()
        ),
        tipo_vegetacao = ExpressionWrapper(
            F('servico__area__vegetacao'),
            output_field=CharField()
        ),
        tipo_terreno=ExpressionWrapper(
            F('servico__area__terreno'),
            output_field=CharField()
        ),
        localidade=ExpressionWrapper(
            F('servico__area__unidade_jardim__nome'),
            output_field=CharField()
        ),
        tiponegocio=ExpressionWrapper(
            F('servico__area__unidade_jardim__negocio'),
            output_field=CharField()
        ),
        unidade=ExpressionWrapper(
            F('servico__area__unidade_jardim__unidadeoriginial__unidade'),
            output_field=CharField()
        ),
    ).filter(
        status_servico__in=["Agendado", "Em andamento"]
    )

    return dados
