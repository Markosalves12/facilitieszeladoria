from django.contrib import admin
from manutencao.models import Manutencao

# Register your models here.
class ManutencaoAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo_manutencao", )
    list_display_links = ("id", "tipo_manutencao", )
    search_fields = ("tipo_manutencao", )
    list_filter = ("tipo_manutencao", )

    list_per_page = 20


admin.site.register(Manutencao, ManutencaoAdmin)