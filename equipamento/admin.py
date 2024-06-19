from django.contrib import admin
from equipamento.models import CatalogoEquipamentos
from equipamento.models import EquipamentoDisponivel
from equipamento.models import ManutencaoEquipamentos

# Register your models here.
class CatalogoEquipamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "marca", "vida_util_meses", "status",  )
    list_display_links = ("id", "nome", "marca", "status", )
    search_fields = ("nome", "marca", )
    list_filter = ("nome", "marca", )

    list_per_page = 20

class EquipamentoDisponivelAdmin(admin.ModelAdmin):
    list_display = ("id", "data_aquisicao", "data_desmobilizacao", "matricula", "catalogo_equipamento", "empresa", "status", "tipo", )
    list_display_links = ("id", "data_aquisicao", "data_desmobilizacao", "matricula", "catalogo_equipamento", "empresa", "status", "tipo", )
    search_fields = ("catalogo_equipamento", "empresa", "tipo", )
    list_filter = ("catalogo_equipamento", "empresa", "tipo", )

    list_per_page = 20

class ManutencaoEquipamentosAdmin(admin.ModelAdmin):
    list_display = ("id", "data_hora_inicio", "data_hora_fim", "descricao_servico", "descricao_motivo", "equipamento", "tipo_manutencao", )
    list_display_links = ("equipamento", )
    search_fields = ("equipamento", "tipo_manutencao", )
    list_filter = ("equipamento", "tipo_manutencao", )

    list_per_page = 20


admin.site.register(CatalogoEquipamentos, CatalogoEquipamentoAdmin)
admin.site.register(EquipamentoDisponivel, EquipamentoDisponivelAdmin)
admin.site.register(ManutencaoEquipamentos, ManutencaoEquipamentosAdmin)