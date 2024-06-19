from django.contrib import admin
from empresa.models import Empresa

# Register your models here.
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "razao_social", "cnpj", "unidade", "tipo_empresa", )
    list_display_links = ("nome", "razao_social", "tipo_empresa", )
    search_fields = ("nome", "razao_social", "unidade", "tipo_empresa", )

    list_per_page = 20

admin.site.register(Empresa, EmpresaAdmin)
