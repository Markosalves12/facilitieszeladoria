from django.contrib import admin

from servico.models import Servicos
from servico.models import FatoServico

# Register your models here.

class ServicosAdmin(admin.ModelAdmin):
    # def colaboradores_escalados_list(self, obj):
    #     return ", ".join([colaborador.nome for colaborador in obj.colaboradores_escalados.all()])

    # colaboradores_escalados_list.short_description = "Colaboradores Escalados"
    list_display = ("id", "descricao_servico", "data_inicio", "area",
                    "status", "foto_inicio", "foto", "tipo_servico", )
    list_display_links = ("id",  "descricao_servico", "data_inicio", "area",
                    "status", "foto_inicio", "foto", "tipo_servico", )
    search_fields = ("area", "status", )
    list_filter = ("status", "tipo_servico", )

    list_per_page = 20


class FatoServicoAdmin(admin.ModelAdmin):
    list_display = ("id", "servico", "data_hora_chegada_na_area",
                    "equipamentos_usados", "ferramentas_usados", "data_hora_retorno_area"
                    , "tipo",  )
    list_display_links = ("id", "servico",
                          "data_hora_chegada_na_area", "equipamentos_usados", "ferramentas_usados",
                          "data_hora_retorno_area", "tipo", )
    search_fields = ("id", "servico", "equipamentos_usados", "ferramentas_usados", "tipo", )
    list_filter = ("servico", "equipamentos_usados", "ferramentas_usados", )

    list_per_page = 20

admin.site.register(Servicos, ServicosAdmin)
admin.site.register(FatoServico, FatoServicoAdmin)