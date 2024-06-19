from django.contrib import admin
from ferramenta.models import CatalogoFerramentas
from ferramenta.models import FerramentaDisponivel
from ferramenta.models import ManutencaoFerramentas

# Register your models here.
class CatalogoFerramentasAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "marca", "vida_util_meses", "empresa",)
    list_display_links = ("id", "nome", "marca",  "empresa", )
    search_fields = ("nome", "marca", "empresa", )
    list_filter = ("nome", "marca", "empresa", )

    list_per_page = 20

class FerramentaDisponivelAdmin(admin.ModelAdmin):
    list_display = ("id", "data_aquisicao", "data_desmobilizacao", "matricula", "catalogo_ferramenta", "empresa", "status", "tipo", )
    list_display_links = ("id", "data_aquisicao", "data_desmobilizacao", "matricula", "catalogo_ferramenta", "empresa", "status", "tipo", )
    search_fields = ("catalogo_ferramenta", "empresa", "tipo", )
    list_filter = ("catalogo_ferramenta", "empresa", "tipo", )

    list_per_page = 20

class ManutencaoFerramentasAdmin(admin.ModelAdmin):
    list_display = ("id", "data_hora_inicio", "data_hora_fim", "descricao_servico", "descricao_motivo", "ferramenta", "tipo_manutencao", )
    list_display_links = ("ferramenta", )
    search_fields = ("ferramenta", "tipo_manutencao", )
    list_filter = ("ferramenta", "tipo_manutencao", )

    list_per_page = 20


admin.site.register(CatalogoFerramentas, CatalogoFerramentasAdmin)
admin.site.register(FerramentaDisponivel, FerramentaDisponivelAdmin)
admin.site.register(ManutencaoFerramentas, ManutencaoFerramentasAdmin)