from django.contrib import admin
from jardins.models import Jardins

# Register your models here.
class JardinsAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "area", "vegetacao", "terreno", "unidade_jardim", )
    list_display_links = ("id", "nome", "area", "vegetacao", "terreno", "unidade_jardim", )
    search_fields = ("vegetacao", "terreno", "unidade_jardim", )
    list_filter = ("vegetacao", "terreno", "unidade_jardim", )

    list_per_page = 20

admin.site.register(Jardins, JardinsAdmin)