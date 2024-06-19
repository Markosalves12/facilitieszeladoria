from django.contrib import admin
from gerente.models import Gerente

# Register your models here.
class GerenteAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "email", "funcao", "senha", "gestor", "status", )
    list_display_links = ("id", "nome", "email", "status", )
    search_fields = ("nome", )
    list_filter = ("nome", )

    list_per_page = 20


admin.site.register(Gerente, GerenteAdmin)