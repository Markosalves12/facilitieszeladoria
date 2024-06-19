from django.contrib import admin
from catalogoservico.models import CatalogoServicos


# Register your models here.

#controle do banco de dados na administração do django
class CatalogoServicosAdmin(admin.ModelAdmin):
    list_display = ("id", "servico", "empresa", )
    list_display_links = ("id", "servico", "empresa", )
    search_fields = ("id", "servico", "empresa", )
    list_filter = ("id", "servico", "empresa", )

    list_per_page = 20

admin.site.register(CatalogoServicos, CatalogoServicosAdmin)