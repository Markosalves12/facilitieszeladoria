from django.contrib import admin
from unidadee.models import Unidade, Localidade

# Register your models here.
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ("unidade", "link", "status", )
    list_display_links = ("unidade", "link", "status", )
    search_fields = ("unidade", )

admin.site.register(Unidade, UnidadeAdmin)


class LocalidadeAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "unidadeoriginial", "status", "negocio", )
    list_display_links = ("nome", "unidadeoriginial", "status", "negocio", )
    search_fields = ("nome", "unidadeoriginial", "negocio", )

    list_per_page = 20

admin.site.register(Localidade, LocalidadeAdmin)